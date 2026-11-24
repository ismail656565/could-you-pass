"""Thumbnails for long videos (1280x720): strongest frame + 2–4 huge words.

  python studio/thumb.py <video.mp4|segment-dir> --text "TROY WAS REAL" [--hl REAL] [--out thumb.jpg]

meta.json of a long can set:
  "thumb": {"text": "TROY WAS REAL", "hl": "REAL", "shot": 7, "color": "#FFD400"}
  text = max ~4 words, a promise or shock (not the title), hl = word in accent color,
  shot = story.json shot index for the background (else: auto-pick the most striking frame).
"""
import argparse
import os
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageStat

FONT = Path(__file__).resolve().parent / 'assets' / 'fonts' / 'Anton-Regular.ttf'
W, H = 1280, 720


def _dur(mp4):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(mp4)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def frames(mp4, fracs):
    out, d = [], _dur(mp4)
    tmp = Path(tempfile.mkdtemp())
    for k, f in enumerate(fracs):
        p = tmp / f'f{k}.jpg'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(0, d * f):.2f}', '-i', str(mp4), '-frames:v', '1', str(p)])
        if p.exists():
            out.append(Image.open(p).convert('RGB'))
    return out


def score(im):
    """Striking = contrast + colour + detail, but not mostly empty paper."""
    sm = im.resize((320, 180))
    g = sm.convert('L')
    contrast = ImageStat.Stat(g).stddev[0]
    sat = ImageStat.Stat(sm.convert('HSV')).mean[1]
    edges = ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).mean[0]
    ink = sum(1 for v in g.tobytes() if v < 170) / (320 * 180)   # share of drawn (non-paper) pixels
    return contrast * 1.0 + sat * 0.6 + edges * 2.0 + min(ink, 0.45) * 120


def best_frame(src):
    src = Path(src)
    cands = []
    if src.is_dir():                                   # kit segment dir: end of each shot = fully drawn
        for seg in sorted(src.glob('*.mp4')):
            cands += frames(seg, [0.75, 0.95])
    else:
        cands = frames(src, [0.08 + i * 0.84 / 23 for i in range(24)])
    if not cands:
        raise SystemExit(f'keine Frames aus {src}')
    return max(cands, key=score)


def _fit(draw, lines, font_path, max_w, max_h):
    for size in range(230, 60, -6):
        f = ImageFont.truetype(str(font_path), size)
        ws = [draw.textlength(l, font=f) for l in lines]
        h = len(lines) * size * 1.02
        if max(ws) <= max_w and h <= max_h:
            return f, size
    return ImageFont.truetype(str(font_path), 60), 60


def _lines(text):
    w = text.upper().split()
    if len(w) <= 2:
        return [' '.join(w)] if len(' '.join(w)) <= 9 else w
    cut = (len(w) + 1) // 2
    return [' '.join(w[:cut]), ' '.join(w[cut:])]


def compose(bg, text, hl='', color='#FFD400', side='left'):
    bg = bg.convert('RGB')
    # cover-crop to 16:9 with a slight zoom so the drawing feels close and bold
    r = max(W / bg.width, H / bg.height) * 1.12
    bg = bg.resize((int(bg.width * r), int(bg.height * r)), Image.LANCZOS)
    x0 = (bg.width - W) // 2 + (int(W * 0.06) if side == 'left' else -int(W * 0.06))
    x0 = max(0, min(bg.width - W, x0))
    bg = bg.crop((x0, (bg.height - H) // 2, x0 + W, (bg.height - H) // 2 + H))
    bg = ImageEnhance.Contrast(ImageEnhance.Color(bg).enhance(1.35)).enhance(1.2)
    # dark gradient behind the text side
    grad = Image.new('L', (W, H))
    gd = ImageDraw.Draw(grad)
    for x in range(W):
        t = x / W if side == 'right' else 1 - x / W
        gd.line([(x, 0), (x, H)], fill=int(215 * max(0, min(1, (t - 0.32) / 0.4))))
    bg = Image.composite(Image.new('RGB', (W, H), (10, 10, 14)), bg, grad)
    d = ImageDraw.Draw(bg)
    lines = _lines(text)
    f, size = _fit(d, lines, FONT, W * 0.56, H * 0.82)
    y = (H - len(lines) * size * 1.02) / 2 - size * 0.08
    hlw = {w.upper() for w in hl.split()}
    for ln in lines:
        lw = d.textlength(ln, font=f)
        x = 54 if side == 'left' else W - 54 - lw
        for word in ln.split(' '):
            fill = color if word.strip('!?.,') in hlw else '#FFFFFF'
            d.text((x, y), word, font=f, fill=fill, stroke_width=max(6, size // 18), stroke_fill='#000000')
            x += d.textlength(word + ' ', font=f)
        y += size * 1.02
    d.rectangle([0, 0, W - 1, H - 1], outline=color, width=10)
    return bg


def make(src, text, out, hl='', color='#FFD400', side='left'):
    im = compose(best_frame(src), text, hl, color, side)
    im.save(out, 'JPEG', quality=90, optimize=True)
    if os.path.getsize(out) > 1_900_000:
        im.save(out, 'JPEG', quality=78, optimize=True)
    return out


def default_text(title):
    w = [x for x in title.replace(':', ' ').split() if x[0].isalnum()]
    return ' '.join(w[:3])


def set_thumbnail(cid, vid, path):
    """Upload as custom thumbnail. Needs a phone-verified channel; failures only warn."""
    import studio as S
    from googleapiclient.http import MediaFileUpload
    try:
        S.yt(cid).thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(path), mimetype='image/jpeg')).execute()
        print(f'  Thumbnail gesetzt: {vid}')
        return True
    except Exception as ex:
        print(f'::warning::Thumbnail für {vid} nicht gesetzt ({str(ex)[:200]}) – Kanal per Telefon verifizieren: youtube.com/verify')
        return False


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('--text', required=True); ap.add_argument('--hl', default='')
    ap.add_argument('--color', default='#FFD400'); ap.add_argument('--side', default='left')
    ap.add_argument('--out', default='thumb.jpg')
    a = ap.parse_args()
    print(make(a.src, a.text, a.out, a.hl, a.color, a.side))
