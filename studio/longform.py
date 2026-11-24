"""STUDIO long videos — 16:9 animated long-form (ReachMora 2D long-form kit, encrypted in studio/kits).

  python studio/longform.py <channel> [--dry] [--res 1080]

A long video project lives in studio/channels/<channel>/longs/NNN-slug/:
  script.txt   the narration, one paragraph per line; chapter cards as lines starting with "# "
  story.json   the storyboard for the kit (see the kit's references/story-format.md)
  meta.json    {"title": ..., "description": ..., "tags": [...]}  (+ optional "voice")
The oldest project that is not yet in state.json "longs_done" is voiced (Kokoro), aligned, rendered and
uploaded as a scheduled video (channel.json "long_time", default 17:00 Berlin, today if ≥ 2 h ahead, else tomorrow).
"""
import argparse, datetime as dt, json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'studio'))
sys.path.insert(0, str(ROOT / 'studio' / 'engine'))
import produce as P

KIT = ROOT / 'studio' / 'kits' / '_unpacked' / 'reachmora-2d-longform'


def voice_wav(script, out, voice):
    import numpy as np, soundfile as sf
    from voice import models
    from kokoro_onnx import Kokoro
    k = Kokoro(*models())
    paras = [l.strip() for l in script.read_text().splitlines() if l.strip() and not l.strip().startswith('#')]
    parts, sr = [], 24000
    for p in paras:
        a, sr = k.create(p, voice=voice, speed=1.0, lang='en-us')
        parts += [a, np.zeros(int(sr * 0.45), np.float32)]
    sf.write(out, np.concatenate(parts), sr)


def run(*args):
    print('$', ' '.join(map(str, args)), flush=True)
    subprocess.run([sys.executable, '-m', 'engine', *map(str, args)], cwd=KIT, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('channel'); ap.add_argument('--dry', action='store_true'); ap.add_argument('--res', default='1080')
    ap.add_argument('--project', default=None, help='a project folder to render instead of the queue (tests)')
    a = ap.parse_args()
    cid = a.channel
    c, st = P.cfg(cid), P.load_state(cid)
    st.setdefault('longs_done', {})
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    if not a.project and not a.dry and any(u.get('uploaded', '').startswith(today) for u in st['longs_done'].values()):
        print(f'{cid}: heute schon ein langes Video hochgeladen'); return
    if a.project:
        projects = [Path(a.project)]
    else:
        d = P.STUDIO / 'channels' / cid / 'longs'
        projects = sorted(p for p in d.iterdir() if (p / 'story.json').exists() and (p / 'script.txt').exists()) if d.exists() else []
        projects = [p for p in projects if p.name not in st['longs_done']]
        if not a.dry:  # meta.json "hold": true = nur Probelauf, kein Upload bis zur Freigabe
            projects = [p for p in projects if not ((p / 'meta.json').exists() and json.loads((p / 'meta.json').read_text()).get('hold'))]
    if not projects:
        print(f'{cid}: kein langes Video in der Warteschlange'); return
    if not KIT.exists():
        print('::error::Kit nicht entpackt (studio/kits/unpack.sh, Secret STUDIO_KIT_KEY)'); sys.exit(1)
    src = projects[0]
    meta = json.loads((src / 'meta.json').read_text()) if (src / 'meta.json').exists() else {}
    work = Path(os.environ.get('STUDIO_WORK', '/tmp/studio')) / cid / f'long-{src.name}'
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    for f in ('script.txt', 'story.json'):
        shutil.copy(src / f, work / f)
    print(f'== {cid}: langes Video {src.name}', flush=True)
    voice_wav(work / 'script.txt', work / 'voice.wav', meta.get('voice') or c.get('voice', 'bm_george'))
    run('align', work)
    run('plan', work)
    run('all', work, '--res', a.res)
    mp4 = sorted((work / 'out').glob('*.mp4'))[-1]
    print('fertig:', mp4, flush=True)
    if a.dry:
        return
    now = dt.datetime.now(P.BERLIN)
    h, m = map(int, c.get('long_time', '17:00').split(':'))
    when = now.replace(hour=h, minute=m, second=0, microsecond=0)
    if when < now + dt.timedelta(hours=2):
        when += dt.timedelta(days=1)
    E = dict(title=meta.get('title') or json.loads((work / 'story.json').read_text()).get('title', src.name),
             description=meta.get('description', ''), tags=meta.get('tags', []))
    vid = P.upload(cid, mp4, E, c, when)
    st['longs_done'][src.name] = dict(video_id=vid, publish_at=when.isoformat(), title=E['title'],
                                      uploaded=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'))
    P.save_state(cid, st)
    print(f'OK langes Video https://youtu.be/{vid}  (öffentlich ab {when:%d.%m. %H:%M})')


if __name__ == '__main__':
    main()
