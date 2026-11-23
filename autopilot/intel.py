"""INTEL – Zahlen der eigenen Kanäle + Konkurrenz-Scan für den Kanal-Manager.

  python autopilot/intel.py stats         eigene Videos aller Kanäle (Views, Stayed %, Ø gesehen %, Abos)
                                          -> studio/analytics/<kanal>.json + studio/analytics/stats.md
                                          + Zuschauerbindung der Shorts (wo springen sie ab, bei welchem Satz?)
                                          -> studio/analytics/retention.md + retention-<kanal>.json
  python autopilot/intel.py competitors   Konkurrenz (studio/analytics/competitors.json) -> Ausreißer-Videos
                                          -> studio/analytics/competitors.md (+ Thumbnails/Frames/Transkripte
                                          der Top-Videos in intel_media/, nur als Workflow-Artefakt, nie im Repo)
  python autopilot/intel.py all           beides

Läuft in GitHub Actions (studio-intel.yml) mit den Kanal-Tokens (YT_TOKENS_JSON).
"""
import datetime as dt
import json
import re
import statistics
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import studio as S  # noqa: E402

ROOT = HERE.parent
OUT = ROOT / 'studio' / 'analytics'
MEDIA = ROOT / 'intel_media'
COMP = OUT / 'competitors.json'
TODAY = dt.date.today().isoformat()


def _iso_dur(s):
    m = re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', s or '')
    if not m:
        return 0
    d, h, mi, se = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def _videos(y, ids):
    out = {}
    for i in range(0, len(ids), 50):
        r = y.videos().list(part='snippet,statistics,contentDetails', id=','.join(ids[i:i + 50])).execute()
        for v in r.get('items', []):
            st = v.get('statistics', {})
            out[v['id']] = {
                'id': v['id'], 'title': v['snippet']['title'], 'published': v['snippet']['publishedAt'],
                'seconds': _iso_dur(v['contentDetails'].get('duration')),
                'views': int(st.get('viewCount', 0)), 'likes': int(st.get('likeCount', 0)),
                'comments': int(st.get('commentCount', 0)),
            }
    return out


def _uploads(y, item, n):
    pl = item['contentDetails']['relatedPlaylists']['uploads']
    ids, tok = [], None
    while len(ids) < n:
        r = y.playlistItems().list(part='contentDetails', playlistId=pl, maxResults=50, pageToken=tok).execute()
        ids += [i['contentDetails']['videoId'] for i in r.get('items', [])]
        tok = r.get('nextPageToken')
        if not tok:
            break
    return ids[:n]


def _reader(toks):
    for cid in ['couldyoupass'] + list(toks):
        if cid in toks:
            try:
                return S._build('youtube', 'v3', S.creds(refresh_token=toks[cid]))
            except Exception as ex:
                print(f'(Leser {cid} unbrauchbar: {str(ex)[:80]})')
    raise SystemExit('Kein gültiges Token.')


# ---------------------------------------------------------------- Zuschauerbindung (wo springen sie ab?)
RET_MIN_VIEWS, RET_MAX = 30, 8      # YouTube liefert die Kurve erst ab einigen Views; pro Kanal die neuesten 8 Shorts


def _lines(cid):
    """Studio-Episoden: Satz-Zeiten aus state.json (von produce.py beim Upload gespeichert)"""
    p = ROOT / 'studio' / 'channels' / cid / 'state.json'
    if not p.exists():
        return {}
    up = json.loads(p.read_text(encoding='utf-8')).get('uploads', {})
    return {u['video_id']: u for u in up.values() if u.get('video_id') and u.get('lines')}


def _said(u, sec):
    if not u:
        return ''
    for i, (t0, t1, text) in enumerate(u['lines']):
        nxt = u['lines'][i + 1][0] if i + 1 < len(u['lines']) else 1e9
        if t0 - 0.2 <= sec < nxt:
            w = text.split()
            k = int(len(w) * max(0.0, min(1.0, (sec - t0) / max(0.1, t1 - t0))))
            return f'Satz {i}: „…{" ".join(w[max(0, k - 3):k + 4])}…“'
    return 'nach dem letzten Satz'


def retention(a, cid, vids):
    """Kurve audienceWatchRatio über elapsedVideoTimeRatio (100 Punkte) für die neuesten Shorts.
    Werte >100 % sind bei Shorts normal (Wiederholungen/Loop)."""
    timed = _lines(cid)
    shorts = [v for v in vids.values() if v['seconds'] <= 180 and v['views'] >= RET_MIN_VIEWS]
    out = []
    for v in sorted(shorts, key=lambda v: v['published'], reverse=True)[:RET_MAX]:
        try:
            rep = a.reports().query(ids='channel==MINE', startDate='2020-01-01', endDate=TODAY, metrics='audienceWatchRatio',
                                    dimensions='elapsedVideoTimeRatio', filters=f"video=={v['id']}").execute()
        except Exception as ex:
            print(f"{cid}: Retention-Fehler {v['id']} {str(ex)[:100]}")
            continue
        pts = sorted((r[0], r[1]) for r in rep.get('rows', []))
        if len(pts) < 10:
            continue
        dur = timed.get(v['id'], {}).get('duration') or v['seconds']
        sec = [r * dur for r, _ in pts]
        w = [100 * x for _, x in pts]
        i3 = min(range(len(sec)), key=lambda i: abs(sec[i] - 3))
        drops = []                                      # the 2 steepest drops, at least 3 s apart
        for d, i in sorted(((w[i - 1] - w[i], i) for i in range(max(1, i3), len(w) - 1)), reverse=True):
            if all(abs(sec[i] - sec[j]) >= 3 for _, j in drops):
                drops.append((d, i))
            if len(drops) == 2:
                break
        u = timed.get(v['id'])
        out.append(dict(id=v['id'], title=v['title'], views=v['views'], start=round(w[0]), at3s=round(w[i3]),
                        mid=round(w[len(w) // 2]), end=round(w[-1]),
                        cliffs=[dict(sec=round(sec[i], 1), drop=round(d, 1), said=_said(u, sec[i])) for d, i in drops if d > 0],
                        curve=[[round(s, 1), round(x)] for s, x in zip(sec[::5], w[::5])]))
    return out


def _retention_md(name, rows):
    md = [f'## {name}', '']
    if not rows:
        return md + [f'(noch keine Kurven – Shorts brauchen ≥ {RET_MIN_VIEWS} Views und 1–2 Tage)', '']
    md += ['| Short | Views | Start % | nach 3 s % | Mitte % | Ende % | Größter Abbruch (Sekunde, gesprochen) |',
           '|---|---:|---:|---:|---:|---:|---|']
    for r in rows:
        c = '; '.join(f"{x['sec']} s (−{x['drop']}) {x['said']}" for x in r['cliffs']) or '–'
        md.append(f"| {r['title'][:50]} | {r['views']} | {r['start']} | {r['at3s']} | {r['mid']} | {r['end']} | {c} |")
    return md + ['']


# ---------------------------------------------------------------- eigene Kanäle
def stats():
    OUT.mkdir(parents=True, exist_ok=True)
    toks = S.tokens()
    md = [f'# Eigene Kanäle – Zahlen', '', f'Stand: {dt.datetime.utcnow():%Y-%m-%d %H:%M} UTC. '
          'Stayed = engagedViews/views (≈ „Stayed to watch“). Analytics-Zahlen hängen 1–2 Tage hinterher, '
          'Views (live) kommen direkt aus der Data-API.', '']
    ret_md = ['# Zuschauerbindung der Shorts', '', f'Stand: {dt.datetime.utcnow():%Y-%m-%d %H:%M} UTC. '
              'Werte = Anteil der Zuschauer, der an dieser Stelle noch zuschaut (YouTube audienceWatchRatio; über 100 % '
              '= Wiederholungen/Loop). „nach 3 s“ niedrig = Hook-Problem; „Größter Abbruch“ = Sekunde mit dem steilsten '
              'Verlust und der Satz, der dort gesprochen wurde (nur Studio-Episoden mit gespeicherten Satz-Zeiten).', '']
    for ch in S.registry():
        cid = ch['id']
        if cid not in toks:
            continue
        try:
            c = S.creds(refresh_token=toks[cid])
            y = S._build('youtube', 'v3', c)
            item = y.channels().list(part='snippet,statistics,contentDetails', mine=True).execute()['items'][0]
            if not S.matches(ch, item['snippet']['title']):
                print(f'{cid}: falscher Kanal – übersprungen')
                continue
            vids = _videos(y, _uploads(y, item, 60))
            a = S._build('youtubeAnalytics', 'v2', c)
            try:
                rep = a.reports().query(ids='channel==MINE', startDate='2020-01-01', endDate=TODAY,
                                        metrics='views,engagedViews,averageViewPercentage,averageViewDuration,subscribersGained',
                                        dimensions='video', sort='-views', maxResults=200).execute()
                cols = [h['name'] for h in rep['columnHeaders']]
                for row in rep.get('rows', []):
                    d = dict(zip(cols, row))
                    v = vids.get(d['video'])
                    if v:
                        v.update(a_views=d['views'], engaged=d['engagedViews'], avgPct=round(d['averageViewPercentage'], 1),
                                 avgSec=d['averageViewDuration'], subs=d['subscribersGained'],
                                 stayed=round(100 * d['engagedViews'] / max(1, d['views']), 1))
            except Exception as ex:
                print(f'{cid}: Analytics-Fehler {str(ex)[:120]}')
            ret = retention(a, cid, vids)
            (OUT / f'retention-{cid}.json').write_text(json.dumps(ret, ensure_ascii=False, indent=1), encoding='utf-8')
            ret_md += _retention_md(ch['name'], ret)
            st = item['statistics']
            data = {'id': cid, 'name': ch['name'], 'checked': TODAY, 'subs': int(st.get('subscriberCount', 0)),
                    'views': int(st.get('viewCount', 0)), 'videos': sorted(vids.values(), key=lambda v: v['published'], reverse=True)}
            (OUT / f'{cid}.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
            md += [f"## {ch['name']} – {data['subs']} Abos, {data['views']} Views", '',
                   '| Datum | Typ | Titel | Views | Stayed % | Ø gesehen % | Abos | Likes |', '|---|---|---|---:|---:|---:|---:|---:|']
            for v in data['videos'][:15]:
                typ = 'Short' if v['seconds'] <= 180 else f"Long {v['seconds'] // 60}m"
                md.append(f"| {v['published'][:10]} | {typ} | {v['title'][:60]} | {v['views']} | {v.get('stayed', '–')} | "
                          f"{v.get('avgPct', '–')} | {v.get('subs', '–')} | {v['likes']} |")
            md.append('')
            print(f"{cid}: {len(vids)} Videos")
        except Exception as ex:
            print(f'{cid}: Fehler {str(ex)[:160]}')
    (OUT / 'stats.md').write_text('\n'.join(md), encoding='utf-8')
    (OUT / 'retention.md').write_text('\n'.join(ret_md), encoding='utf-8')


# ---------------------------------------------------------------- Konkurrenz
def _grab_media(v, cid):
    """Thumbnail + (wenn möglich) 12 Frames als Kontaktbogen + Auto-Untertitel – nur fürs Artefakt."""
    d = MEDIA / cid / v['id']
    d.mkdir(parents=True, exist_ok=True)
    for q in ('maxresdefault', 'hqdefault'):
        try:
            urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{v['id']}/{q}.jpg", d / 'thumb.jpg')
            break
        except Exception:
            pass
    url = f"https://www.youtube.com/watch?v={v['id']}"
    try:
        subprocess.run(['yt-dlp', '-q', '--no-warnings', '-f', 'worst[height>=240]/worst', '-o', str(d / 'v.%(ext)s'),
                        '--write-auto-subs', '--sub-langs', 'en.*', '--sub-format', 'vtt', url],
                       timeout=180, check=False, capture_output=True)
        vid = next((p for p in d.glob('v.*') if p.suffix not in ('.vtt',)), None)
        if vid:
            n = 12
            dur = max(1, v['seconds'])
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(vid), '-vf',
                            f"fps={n / dur},scale=240:-1,tile=6x2", '-frames:v', '1', str(d / 'frames.jpg')],
                           timeout=180, check=False)
            vid.unlink()
        vtt = next(d.glob('*.vtt'), None)
        if vtt:
            lines, last = [], ''
            for ln in vtt.read_text(encoding='utf-8', errors='ignore').splitlines():
                ln = re.sub(r'<[^>]+>', '', ln).strip()
                if not ln or '-->' in ln or ln.startswith(('WEBVTT', 'Kind:', 'Language:')) or ln == last:
                    continue
                lines.append(ln)
                last = ln
            (d / 'transcript.txt').write_text(' '.join(lines)[:6000], encoding='utf-8')
            vtt.unlink()
    except Exception as ex:
        print(f"  Medien {v['id']}: {str(ex)[:80]}")


def competitors():
    OUT.mkdir(parents=True, exist_ok=True)
    if not COMP.exists():
        COMP.write_text(json.dumps({'_info': 'Pro Kanal Konkurrenz-Handles (@name) oder Kanal-IDs (UC…). Pflegt der Manager.',
                                    'channels': {}}, indent=1), encoding='utf-8')
    conf = json.loads(COMP.read_text(encoding='utf-8')).get('channels', {})
    y = _reader(S.tokens())
    since = (dt.datetime.utcnow() - dt.timedelta(days=30)).isoformat()
    md = ['# Konkurrenz – Ausreißer der letzten 30 Tage', '',
          f'Stand: {TODAY}. Faktor = Views ÷ Median der letzten Videos desselben Konkurrenz-Kanals. '
          'Thumbnails, Frame-Kontaktbögen und Transkripte der Top-Videos liegen im Artefakt „intel-media“ des Workflow-Laufs '
          '(`gh run download <id> -n intel-media`).', '']
    for cid, handles in conf.items():
        rows = []
        for h in handles:
            try:
                kw = {'id': h} if h.startswith('UC') else {'forHandle': h}
                it = y.channels().list(part='snippet,statistics,contentDetails', **kw).execute().get('items', [])
                if not it:
                    print(f'{cid}: {h} nicht gefunden')
                    continue
                it = it[0]
                vids = list(_videos(y, _uploads(y, it, 30)).values())
                med = statistics.median([v['views'] for v in vids]) if vids else 0
                for v in vids:
                    if v['published'] >= since:
                        v.update(channel=it['snippet']['title'], handle=h, subs=int(it['statistics'].get('subscriberCount', 0)),
                                 factor=round(v['views'] / max(1, med), 1))
                        rows.append(v)
            except Exception as ex:
                print(f'{cid}: {h} Fehler {str(ex)[:100]}')
        rows.sort(key=lambda v: (v['factor'], v['views']), reverse=True)
        (OUT / f'competitors-{cid}.json').write_text(json.dumps(rows[:40], ensure_ascii=False, indent=1), encoding='utf-8')
        md += [f'## {cid}', '', '| Faktor | Views | Typ | Kanal | Titel | ID |', '|---:|---:|---|---|---|---|']
        for v in rows[:12]:
            typ = 'Short' if v['seconds'] <= 180 else f"Long {v['seconds'] // 60}m"
            md.append(f"| {v['factor']}× | {v['views']} | {typ} | {v['channel'][:24]} | {v['title'][:70]} | {v['id']} |")
        md.append('')
        for v in rows[:4]:
            _grab_media(v, cid)
        print(f'{cid}: {len(rows)} Konkurrenz-Videos')
    (OUT / 'competitors.md').write_text('\n'.join(md), encoding='utf-8')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if cmd in ('stats', 'all'):
        stats()
    if cmd in ('competitors', 'all'):
        competitors()
    if cmd not in ('stats', 'competitors', 'all'):
        print(__doc__)
