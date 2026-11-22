"""STUDIO weekly long video — the week's episodes re-filmed in 16:9 (same painted worlds, wider camera on a desk),
joined with chapter cards, a spoken intro and outro, chapters in the description.

  python studio/long.py <channel> [--force] [--dry]

Runs every day from the workflow but only acts on the weekday set in channel.json "long" (and once per week).
"""
import argparse, datetime as dt, json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'studio'))
sys.path.insert(0, str(ROOT / 'studio' / 'engine'))
import produce as P
from film import build, load_episode, card, F
from PIL import Image, ImageDraw
import numpy as np

OW, OH, FPS = 1920, 1080, 30


def desk(seed=3):
    rng = np.random.default_rng(seed)
    from scipy.ndimage import gaussian_filter
    n = rng.normal(0, 1, (OH // 4, OW // 4)).astype(np.float32)
    g = gaussian_filter(n, (0.6, 14)) * 3 + gaussian_filter(n, (6, 40)) * 6
    base = np.array([46, 34, 27], np.float32)[None, None] * (1 + 0.07 * g[..., None])
    im = Image.fromarray(base.clip(0, 255).astype(np.uint8)).resize((OW, OH), Image.BICUBIC)
    Y, X = np.mgrid[0:OH, 0:OW].astype(np.float32)
    vig = 1 - 0.35 * np.clip((np.hypot((X - OW / 2) / (OW / 2), (Y - OH / 2) / (OH / 2)) - 0.5), 0, 1)
    return Image.fromarray((np.asarray(im) * vig[..., None]).clip(0, 255).astype(np.uint8))


def card_clip(out, lines, dur, wav=None):
    """a still desk with torn paper cards (lines = [(text, font, size, ink, y)]) + gentle push-in"""
    base = desk().convert('RGBA')
    for i, (text, font, size, ink, y) in enumerate(lines):
        c = card(text, font, size, seed=90 + i, ink=ink)
        base.alpha_composite(c, (int(OW / 2 - c.width / 2), int(y - c.height / 2)))
    base = base.convert('RGB')
    n = int(dur * FPS)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}', '-r', str(FPS), '-i', '-']
    cmd += (['-i', str(wav)] if wav else ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo'])
    cmd += ['-t', f'{dur:.2f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-ac', '2', '-shortest', str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(n):
        z = 1 + 0.03 * f / max(1, n)
        w, h = OW / z, OH / z
        fr = base.transform((OW, OH), Image.AFFINE, (1 / z, 0, (OW - w) / 2, 0, 1 / z, (OH - h) / 2), resample=Image.BICUBIC)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    return out


def say(text, out_dir, voice):
    from voice import synth
    from audio import loudnorm
    m = synth([text], out_dir, voice)[0]
    wav = Path(out_dir) / 'say.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', m['file'], '-af', 'adelay=400|400,apad=pad_dur=0.8', '-ar', '48000', '-ac', '2',
                    str(wav) + '.tmp.wav'], check=True)
    loudnorm(str(wav) + '.tmp.wav', str(wav))
    return wav, m['dur'] + 1.2


def dur_of(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                                capture_output=True, text=True).stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('channel'); ap.add_argument('--force', action='store_true'); ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    cid = a.channel
    c, st = P.cfg(cid), P.load_state(cid)
    L = c.get('long')
    if not L:
        print(f'{cid}: kein langes Video konfiguriert'); return
    now = dt.datetime.now(P.BERLIN)
    week = now.strftime('%G-W%V')
    st.setdefault('longs', {})
    if not a.force and (now.isoweekday() != L.get('make_on', 6) or week in st['longs']):
        print(f'{cid}: heute kein langes Video (kommt am Wochentag {L.get("make_on", 6)})'); return
    used = {e for lv in st['longs'].values() for e in lv.get('episodes', [])}
    pool = [k for k, u in sorted(st['uploads'].items(), key=lambda kv: kv[1]['publish_at'])
            if u.get('kind') == 'short' and k not in used and dt.datetime.fromisoformat(u['publish_at']) < now + dt.timedelta(days=2)]
    pool = pool[-L.get('max_episodes', 7):]
    if len(pool) < L.get('min_episodes', 5):
        print(f'::warning::{cid}: nur {len(pool)} Episoden für das lange Video – braucht {L.get("min_episodes", 5)}'); return
    work = Path(os.environ.get('STUDIO_WORK', '/tmp/studio')) / cid / f'long-{week}'
    work.mkdir(parents=True, exist_ok=True)
    voice = c.get('voice', 'bm_george')
    n = len(pool)
    title = L['titles'][len(st['longs']) % len(L['titles'])].format(n=n)
    parts, chapters, t = [], [], 0.0
    wav, d = say(L['intro'].format(n=n), work / 'intro', voice)
    parts.append(card_clip(work / 'p00_intro.mp4', [(title.split('(')[0].strip().upper(), 'Cinzel-700', 64, (26, 22, 18), OH * 0.45),
                                                    (c['name'].upper(), 'AlfaSlabOne-400', 44, (150, 34, 26), OH * 0.62)], max(4.0, d), wav))
    chapters.append((0.0, 'Intro')); t += dur_of(parts[-1])
    eps_dir = P.STUDIO / 'channels' / cid / 'episodes'
    for i, slug in enumerate(pool, 1):
        E = load_episode(eps_dir / slug / 'episode.py').EPISODE
        name = E.get('chapter') or slug.split('-', 1)[1].replace('-', ' ').title()
        parts.append(card_clip(work / f'p{i:02d}a.mp4', [(f'{i}', 'AlfaSlabOne-400', 150, (150, 34, 26), OH * 0.40),
                                                        (name.upper(), 'Cinzel-700', 80, (26, 22, 18), OH * 0.62)], 2.2))
        chapters.append((t, f'{i}. {name}')); t += dur_of(parts[-1])
        ew = Path(os.environ.get('STUDIO_WORK', '/tmp/studio')) / cid / slug
        out = work / f'p{i:02d}b.mp4'
        build(eps_dir / slug / 'episode.py', ew, out, voice=voice, size=(OW, OH))
        parts.append(out); t += dur_of(out)
    wav, d = say(L['outro'], work / 'outro', voice)
    parts.append(card_clip(work / 'p99_outro.mp4', [('WHICH ONE SURPRISED YOU?', 'Cinzel-700', 60, (26, 22, 18), OH * 0.45),
                                                   ('SUBSCRIBE FOR MORE', 'AlfaSlabOne-400', 40, (150, 34, 26), OH * 0.62)], max(4.0, d), wav))
    lst = work / 'list.txt'
    lst.write_text(''.join(f"file '{p}'\n" for p in parts))
    final = work / 'long.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c:v', 'libx264', '-preset', 'veryfast',
                    '-crf', '19', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-ac', '2',
                    '-movflags', '+faststart', str(final)], check=True)
    def ts(x): x = int(x); return f'{x // 60}:{x % 60:02d}'
    desc = L['description'].format(n=n) + '\n\n' + '\n'.join(f'{ts(a_)} {b_}' for a_, b_ in chapters)
    if a.dry:
        print('(dry) fertig:', final, '\n', title, '\n', desc); return
    when = P.next_long_slot(L, st) if hasattr(P, 'next_long_slot') else None
    if when is None:
        d0 = now.date() + dt.timedelta(days=(L.get('weekday', 7) - now.isoweekday()) % 7 or 7)
        h, m = map(int, L.get('time', '17:00').split(':'))
        when = dt.datetime(d0.year, d0.month, d0.day, h, m, tzinfo=P.BERLIN)
    E = dict(title=title, description=desc, tags=L.get('tags', []))
    vid = P.upload(cid, final, E, c, when)
    st['longs'][week] = dict(video_id=vid, publish_at=when.isoformat(), title=title, episodes=pool,
                             uploaded=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'))
    P.save_state(cid, st)
    print(f'OK langes Video https://youtu.be/{vid}  (öffentlich ab {when:%d.%m. %H:%M})')


if __name__ == '__main__':
    main()
