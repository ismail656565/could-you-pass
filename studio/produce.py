"""STUDIO producer — renders the next episodes of a channel and schedules them on YouTube.

  python studio/produce.py <channel> [--shorts N] [--dry]      render + upload the next N Shorts (default from channel.json)
  python studio/produce.py <channel> --list                    show queue / what is already scheduled

Every channel lives in studio/channels/<id>/:
  channel.json      voice, publish slots (Berlin time), tags, description footer
  episodes/<NNN-slug>/episode.py   one Short each (see studio/engine/film.py)
  state.json        what was uploaded when (written by this script, committed by the workflow)
"""
import argparse, datetime as dt, json, os, sys, time, traceback
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STUDIO = ROOT / 'studio'
sys.path.insert(0, str(STUDIO / 'engine'))
sys.path.insert(0, str(ROOT / 'autopilot'))
BERLIN = ZoneInfo('Europe/Berlin')


def cfg(cid): return json.loads((STUDIO / 'channels' / cid / 'channel.json').read_text())


def state_path(cid): return STUDIO / 'channels' / cid / 'state.json'


def load_state(cid):
    p = state_path(cid)
    return json.loads(p.read_text()) if p.exists() else {'uploads': {}}


def save_state(cid, st):
    state_path(cid).write_text(json.dumps(st, indent=1, ensure_ascii=False) + '\n')


def episodes(cid):
    d = STUDIO / 'channels' / cid / 'episodes'
    return sorted(p for p in d.iterdir() if (p / 'episode.py').exists())


def next_slots(c, st, n, now=None):
    """the next n publish slots (Berlin wall-clock times from channel.json), after everything already scheduled
    and at least 90 minutes from now"""
    now = now or dt.datetime.now(BERLIN)
    taken = [dt.datetime.fromisoformat(u['publish_at']) for u in st['uploads'].values()]
    after = max(taken + [now + dt.timedelta(minutes=90)])
    out, day = [], now.date()
    while len(out) < n:
        for hm in c['slots']:
            h, m = map(int, hm.split(':'))
            t = dt.datetime(day.year, day.month, day.day, h, m, tzinfo=BERLIN)
            if t > after and len(out) < n:
                out.append(t)
        day += dt.timedelta(days=1)
    return out


def already_uploaded(y, title):
    ch = y.channels().list(part='contentDetails', mine=True).execute()['items'][0]
    pl = ch['contentDetails']['relatedPlaylists']['uploads']
    items = y.playlistItems().list(part='snippet', playlistId=pl, maxResults=50).execute().get('items', [])
    for it in items:
        if it['snippet']['title'].strip().lower() == title.strip().lower():
            return it['snippet']['resourceId']['videoId']
    return None


def upload(cid, mp4, E, c, when):
    import studio as S
    from googleapiclient.http import MediaFileUpload
    y = S.yt(cid)                                     # channel guard: aborts on the wrong channel
    vid = already_uploaded(y, E['title'])
    if vid:
        print(f'  schon hochgeladen: {vid}')
        return vid
    desc = E['description'].rstrip() + '\n\n' + c.get('footer', '')
    body = dict(
        snippet=dict(title=E['title'][:100], description=desc[:4900], tags=list(dict.fromkeys(E.get('tags', []) + c.get('tags', [])))[:30],
                     categoryId=str(c.get('category', 27)), defaultLanguage='en', defaultAudioLanguage='en'),
        status=dict(privacyStatus='private', publishAt=when.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    selfDeclaredMadeForKids=False, embeddable=True))
    for attempt in range(4):
        try:
            req = y.videos().insert(part='snippet,status', body=body, media_body=MediaFileUpload(str(mp4), chunksize=-1, resumable=True))
            resp = None
            while resp is None:
                _, resp = req.next_chunk()
            return resp['id']
        except Exception as e:
            print('  Upload-Fehler:', e)
            if attempt == 3: raise
            time.sleep(20 * (attempt + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('channel'); ap.add_argument('--shorts', type=int, default=None)
    ap.add_argument('--dry', action='store_true'); ap.add_argument('--list', action='store_true')
    ap.add_argument('--force', action='store_true', help='auch wenn heute schon hochgeladen wurde')
    a = ap.parse_args()
    cid = a.channel
    c, st = cfg(cid), load_state(cid)
    eps = [e for e in episodes(cid) if e.name not in st['uploads']]
    if a.list:
        for k, u in st['uploads'].items(): print('  hochgeladen', k, u)
        for e in eps: print('  wartet     ', e.name)
        return
    if not c.get('enabled', True):
        print(f'{cid}: deaktiviert'); return
    n = a.shorts if a.shorts is not None else c.get('shorts_per_day', 2)
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    if not a.force and any(u.get('uploaded', '').startswith(today) for u in st['uploads'].values()):
        print(f'{cid}: heute schon hochgeladen'); return
    if n == 0:
        print(f'{cid}: 0 Shorts angefordert'); return
    if len(eps) < c.get('warn_below', 6):
        print(f'::warning::{cid}: nur noch {len(eps)} Episoden im Vorrat')
    todo = eps[:n]
    if not todo:
        print(f'::error::{cid}: keine Episoden mehr im Vorrat'); sys.exit(1)
    slots = next_slots(c, st, len(todo))
    from film import build, load_episode
    failed = 0
    for ep, when in zip(todo, slots):
        print(f'== {cid}/{ep.name}  ->  {when:%a %d.%m. %H:%M} Berlin', flush=True)
        try:
            work = Path(os.environ.get('STUDIO_WORK', '/tmp/studio')) / cid / ep.name
            mp4 = work / 'final.mp4'
            build(ep / 'episode.py', work, mp4, voice=c.get('voice'))
            if a.dry:
                print('  (dry) fertig:', mp4); continue
            E = load_episode(ep / 'episode.py').EPISODE
            vid = upload(cid, mp4, E, c, when)
            st['uploads'][ep.name] = dict(video_id=vid, publish_at=when.isoformat(), kind='short', title=E['title'],
                                          uploaded=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'))
            save_state(cid, st)
            print(f'  OK https://youtu.be/{vid}  (öffentlich ab {when:%d.%m. %H:%M})', flush=True)
        except Exception:
            failed += 1
            traceback.print_exc()
            print(f'::error::{cid}/{ep.name} fehlgeschlagen')
    if failed == len(todo): sys.exit(1)


if __name__ == '__main__':
    main()
