"""HUMAN LIMIT #006 — You get a new skeleton about every ten years (X-ray look, painted with numpy + Pillow).
Facts: in adults about 10 % of the skeleton is remodelled each year (Wikipedia 'Bone remodeling', citing Manolagas,
Endocrine Reviews 2000; US Surgeon General, 'Bone Health and Osteoporosis', 2004: the adult skeleton is replaced
roughly every 10 years); osteoclasts resorb old bone, osteoblasts form new bone; trabecular (spongy) bone turns over
much faster than cortical (compact) bone. 'A new skeleton every ten years' is an average – not every bit is renewed
on schedule. Science story only, no advice."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, S = 1440, 2560, 2
FONT = str(Path(__file__).resolve().parents[4] / 'fonts' / 'Anton-400.woff')
NAVY = np.array([8, 14, 32], np.float32)


def font(px):
    return ImageFont.truetype(FONT, px * S)


def bone(d, p0, p1, w, knob=1.6):
    (x0, y0), (x1, y1) = p0, p1
    d.line([(x0 * S, y0 * S), (x1 * S, y1 * S)], fill=255, width=int(w * S))
    for x, y in (p0, p1):
        r = w * knob / 2
        for dx in (-r * 0.45, r * 0.45):
            d.ellipse(((x + dx - r * 0.7) * S, (y - r * 0.7) * S, (x + dx + r * 0.7) * S, (y + r * 0.7) * S), fill=255)


def skeleton():
    m = Image.new('L', (W * S, H * S), 0); d = ImageDraw.Draw(m)
    E = lambda cx, cy, rx, ry, f=255: d.ellipse(((cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S), fill=f)
    E(720, 420, 125, 145); E(720, 575, 82, 52)                                   # skull + jaw
    E(672, 420, 36, 40, 0); E(768, 420, 36, 40, 0); E(720, 482, 14, 22, 0)        # eye sockets, nose
    for k in range(5):
        d.rectangle(((672 + k * 20) * S, 548 * S, (684 + k * 20) * S, 572 * S), fill=0)   # teeth gaps
    for i in range(17):                                                           # spine
        y = 640 + i * 40
        d.rounded_rectangle(((720 - 22 - i * 0.8) * S, y * S, (720 + 22 + i * 0.8) * S, (y + 30) * S), 8 * S, fill=255)
    for i in range(10):                                                           # ribs
        y = 730 + i * 42; rx = 150 + 40 * math.sin(math.pi * (i + 2) / 13)
        for side in (-1, 1):
            pts = [(720 + side * rx * math.sin(t), y + 40 * (1 - math.cos(t)) + t * 22) for t in np.linspace(0.05, 2.4, 30)]
            d.line([(x * S, y_ * S) for x, y_ in pts], fill=255, width=14 * S, joint='curve')
    d.line([(720 * S, 1130 * S), (720 * S, 1140 * S)], fill=255, width=40 * S)
    d.rounded_rectangle((700 * S, 700 * S, 740 * S, 1040 * S), 14 * S, fill=255)   # sternum
    for side in (-1, 1):
        sx = 720 + side * 200
        bone(d, (720 + side * 20, 670), (sx, 655), 20)                            # clavicle
        bone(d, (sx, 670), (720 + side * 250, 1030), 30)                          # humerus
        bone(d, (720 + side * 250, 1040), (720 + side * 275, 1330), 18)           # forearm
        bone(d, (720 + side * 265, 1040), (720 + side * 300, 1325), 14)
        for f in range(4):                                                        # fingers
            bone(d, (720 + side * (268 + f * 14), 1350), (720 + side * (262 + f * 20), 1450), 9, 1.2)
        E(720 + side * 95, 1370, 120, 92)                                         # pelvis
        bone(d, (720 + side * 85, 1450), (720 + side * 105, 1900), 38)            # femur
        E(720 + side * 105, 1925, 30, 26)                                         # kneecap
        bone(d, (720 + side * 100, 1960), (720 + side * 100, 2320), 32)           # tibia
        bone(d, (720 + side * 140, 1970), (720 + side * 138, 2310), 14)           # fibula
        d.polygon([((720 + side * 70) * S, 2340 * S), ((720 + side * 150) * S, 2330 * S),
                   ((720 + side * 175) * S, 2400 * S), ((720 + side * 40) * S, 2410 * S)], fill=255)
    E(720, 1385, 50, 46, 0)
    return m


def tone(mask, bone_rgb, glow_rgb, amount=1.0):
    a = np.asarray(mask, np.float32) / 255
    g = np.asarray(mask.filter(ImageFilter.GaussianBlur(18 * S)), np.float32) / 255
    inner = np.asarray(mask.filter(ImageFilter.GaussianBlur(3 * S)), np.float32) / 255
    edge = np.clip(a - inner * 0.7, 0, 1)                                         # bright rims, like a radiograph
    out = NAVY + g[..., None] * np.array(glow_rgb) * 0.9 * amount
    out = out * (1 - a[..., None]) + a[..., None] * (np.array(bone_rgb) * (0.62 + 0.38 * edge[..., None]))
    return out


def finish(arr):
    rng = np.random.default_rng(3)
    arr = arr + rng.normal(0, 5, arr.shape[:2])[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    return im


def label(im, s, x, y, px, fill, anchor='mm'):
    d = ImageDraw.Draw(im); d.text((x, y), s, font=ImageFont.truetype(FONT, px), fill=fill, anchor=anchor)


def paint(work):
    out = Path(work); (out / 'body').mkdir(parents=True, exist_ok=True); (out / 'femur').mkdir(exist_ok=True)
    m = skeleton()
    xs = np.arange(W * S)[None, :, None]
    old = tone(m, (205, 172, 118), (120, 80, 30), 0.7)
    new = tone(m, (225, 246, 255), (50, 160, 255), 1.0)
    arr = np.where(xs < 720 * S, old, new)
    arr[:, 720 * S - 3:720 * S + 3] = (255, 255, 255)
    base = finish(arr)
    label(base, '10 YEARS AGO', 360, 190, 76, (225, 190, 130))
    label(base, 'NOW', 1080, 190, 76, (150, 220, 255))
    base.save(out / 'body' / '00_split.png')
    rng = np.random.default_rng(8)                                                # ~10 % of the bone lights up
    spots = Image.new('L', (W * S, H * S), 0); sd = ImageDraw.Draw(spots)
    ys, xs_ = np.nonzero(np.asarray(m)[::8, ::8])
    for i in rng.choice(len(ys), 140, replace=False):
        cx, cy = xs_[i] * 8, ys[i] * 8; r = rng.uniform(14, 30) * S
        sd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    spots = Image.fromarray(np.minimum(np.asarray(spots), np.asarray(m)))
    sp = np.asarray(spots.filter(ImageFilter.GaussianBlur(4 * S)), np.float32)[..., None] / 255
    arr2 = arr * (1 - sp) + sp * np.array([255, 150, 40]) + np.asarray(spots.filter(ImageFilter.GaussianBlur(16 * S)),
                                                                        np.float32)[..., None] / 255 * np.array([120, 50, 0])
    im = finish(arr2)
    label(im, '10 YEARS AGO', 360, 190, 76, (225, 190, 130)); label(im, 'NOW', 1080, 190, 76, (150, 220, 255))
    im.save(out / 'body' / '01_ten.png')

    # ---- plate 2: one femur, cut open
    f = Image.new('L', (W * S, H * S), 0); d = ImageDraw.Draw(f)
    E = lambda cx, cy, rx, ry, fill=255: d.ellipse(((cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S), fill=fill)
    d.rounded_rectangle((590 * S, 600 * S, 850 * S, 2050 * S), 40 * S, fill=255)  # shaft
    E(740, 430, 200, 190); E(560, 560, 110, 90)                                    # head + trochanter
    E(650, 2150, 210, 150); E(830, 2150, 190, 150)                                 # knee end
    d.rounded_rectangle((640 * S, 700 * S, 800 * S, 1960 * S), 30 * S, fill=70)     # marrow cavity (hollow)
    spongy = Image.new('L', (W * S, H * S), 0); s2 = ImageDraw.Draw(spongy)
    for cx, cy, rx, ry in ((740, 430, 165, 150), (740, 2140, 330, 110)):
        for _ in range(260):
            t = rng.uniform(0, 2 * math.pi); r = math.sqrt(rng.uniform(0, 1))
            x0, y0 = cx + rx * r * math.cos(t), cy + ry * r * math.sin(t)
            a = rng.uniform(0, math.pi); L = rng.uniform(20, 50)
            s2.line([(x0 * S, y0 * S), ((x0 + L * math.cos(a)) * S, (y0 + L * math.sin(a)) * S)], fill=255, width=5 * S)
    sp = np.asarray(spongy, np.float32)
    fa = np.asarray(f, np.float32)
    inside = np.zeros_like(fa)
    for cx, cy, rx, ry in ((740, 430, 165, 150), (740, 2140, 330, 110)):
        yy, xx = np.ogrid[:H * S, :W * S]
        inside = np.maximum(inside, (((xx - cx * S) / (rx * S)) ** 2 + ((yy - cy * S) / (ry * S)) ** 2 < 1).astype(np.float32))
    fa = np.where(inside > 0, np.maximum(40, sp * 0.95), fa)
    fm = Image.fromarray(fa.astype(np.uint8))
    farr = tone(fm, (225, 246, 255), (50, 160, 255), 1.0)
    fb = finish(farr)
    fb.save(out / 'femur' / '00_femur.png')
    dd = ImageDraw.Draw(fb)
    for k in range(3):                                                             # osteoclasts in a pit (left wall)
        cy = 1150 + k * 70
        dd.ellipse((560, cy - 40, 650, cy + 40), fill=(170, 80, 220), outline=(240, 200, 255), width=4)
        for n in range(3):
            dd.ellipse((575 + n * 22, cy - 10, 591 + n * 22, cy + 6), fill=(70, 20, 110))
    label(fb, 'OSTEOCLASTS', 380, 1180, 64, (220, 160, 255)); label(fb, 'dissolve old bone', 380, 1250, 44, (220, 200, 240))
    for k in range(6):                                                             # osteoblasts in a row (right wall)
        cy = 1450 + k * 44
        dd.rounded_rectangle((850, cy, 900, cy + 38), 10, fill=(70, 200, 120), outline=(200, 255, 220), width=3)
        dd.ellipse((866, cy + 12, 882, cy + 26), fill=(20, 90, 50))
    label(fb, 'OSTEOBLASTS', 1080, 1540, 64, (130, 240, 170)); label(fb, 'build new bone', 1080, 1610, 44, (200, 240, 215))
    fb.save(out / 'femur' / '01_cells.png')
    glow = Image.fromarray((np.clip(inside * sp / 255, 0, 1) * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    g = np.asarray(glow, np.float32)[..., None] / 255
    fc = np.asarray(fb, np.float32) * (1 - g * 0.8) + g * 0.8 * np.array([255, 160, 50])
    fc = Image.fromarray(np.clip(fc, 0, 255).astype(np.uint8))
    label(fc, 'SPONGY BONE: FAST', 1080, 250, 52, (255, 180, 80))
    label(fc, 'HARD SHELL: SLOWER', 1090, 900, 48, (170, 220, 255))
    fc.save(out / 'femur' / '02_spongy.png')
    dd = ImageDraw.Draw(fc)
    for k in range(10):
        x0 = 170 + k * 112
        dd.rounded_rectangle((x0, 2400, x0 + 100, 2470), 10, fill=(80, 190, 255) if k < 10 else None)
    label(fc, '10 YEARS', 720, 2350, 64, (220, 245, 255))
    fc.save(out / 'femur' / '03_years.png')


A = ['body/00_split.png', 'body/01_ten.png']
B = ['femur/00_femur.png', 'femur/01_cells.png', 'femur/02_spongy.png', 'femur/03_years.png']
PH = 2560

EPISODE = dict(
    chapter='A New Skeleton Every Ten Years',
    title="You Get a New Skeleton About Every 10 Years 🦴 #shorts",
    description=("Your bones are alive. In adults, about 10 % of the skeleton is broken down and rebuilt every year: "
                 "cells called osteoclasts dissolve old bone, osteoblasts lay down new bone. Spongy bone inside the "
                 "bone ends renews much faster than the hard outer shell. On average that adds up to roughly a whole "
                 "skeleton's worth about every ten years (US Surgeon General's report 'Bone Health and Osteoporosis', "
                 "2004; Manolagas, Endocrine Reviews, 2000). It's an average – not every piece is renewed on schedule.\n\n"
                 "Science story, not a challenge. Illustrations painted with code (no photos), narration is synthetic."),
    tags=['bone remodeling', 'skeleton', 'human body', 'osteoclasts', 'osteoblasts', 'body facts', 'science shorts'],
    voice='af_heart',
    lines=["Your skeleton isn't the one you had ten years ago.",
           "Every year, about ten percent of it is broken down, and rebuilt.",
           "Cells called osteoclasts dissolve old bone. Osteoblasts lay down new bone.",
           "The spongy bone inside renews fastest. The hard outer shell, more slowly.",
           "On average, that adds up to a new skeleton about every ten years.",
           "So right now, your body is quietly rebuilding you."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.4, 0.5],
    display=[(0, 'ten', '10'), (1, 'ten', '10'), (1, 'percent', '%'), (4, 'ten', '10')],
    plates=[dict(stages=A, show=[(0, 0), ('L1', 1)]),
            dict(stages=B, show=[(0, 0), ('L2', 1), ('L3', 2), ('L4', 3)])],
    camera=[(0, 720, 1300, 2440), ('L1', 720, 1300, 2440), ('L1.end', 720, 1290, 2400),
            ('L2', 720, PH + 1300, 2100), ('L3', 720, PH + 1100, 2100), ('L4', 720, PH + 1280, 2460),
            ('END', 720, PH + 1280, 2460)],
    cards=[dict(at=0, until='L1-0.2', text='NEW BONES.', font='AlfaSlabOne-400', size=100, ink=(150, 34, 26), x=540,
                y=1330, rot=-3)],
    caption=dict(y=0.86),
    stamps=[dict(at='L4:skeleton', text='EVERY ~10 YEARS', size=80, color=(200, 50, 30), x=540, y=1430, rot=-6)],
    music=dict(sections=[(0, 'L2', ['Esus', 'Am9'], dict(bright=(0.2, 0.35), ticks=True)),
                         ('L2', 'L4', ['Dm9', 'Esus'], dict(bright=(0.35, 0.55), pulse=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
