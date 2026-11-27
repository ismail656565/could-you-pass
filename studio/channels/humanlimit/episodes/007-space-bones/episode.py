"""HUMAN LIMIT #007 — In space, your bones disappear (X-ray look, painted with numpy + Pillow; helpers as in #006).
Facts: astronauts lose on average about 1–1.5 % of bone mineral density per month in weight-bearing bone, mostly hip
and spine (NASA Human Research Program, 'Risk of Spaceflight-Induced Bone Changes'; Lang et al., J Bone Miner Res
2004; Wikipedia 'Spaceflight osteopenia'); older adults on Earth lose roughly 1–1.5 % per year (NASA Astrobiology
'Space Bones', 2001); ISS crews exercise about 2 hours a day to fight it (NASA); a year after returning from long
missions many astronauts had not fully recovered their bone (Gabel et al., Scientific Reports 2022, TBone study,
University of Calgary / Canadian Space Agency). Science story only, no advice."""
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



def holes(mask, seed, n, rmin, rmax, region=None):
    """punch porous holes into a bone mask (the 'vanishing' look)"""
    rng = np.random.default_rng(seed)
    m = mask.copy(); d = ImageDraw.Draw(m)
    ys, xs = np.nonzero(np.asarray(mask)[::8, ::8])
    for i in rng.choice(len(ys), n, replace=False):
        cx, cy = xs[i] * 8, ys[i] * 8
        if region and not (region[0] * S < cx < region[2] * S and region[1] * S < cy < region[3] * S):
            continue
        r = rng.uniform(rmin, rmax) * S
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=60)
    return m


def stars(arr, x0, seed=2):
    rng = np.random.default_rng(seed)
    for _ in range(260):
        x, y = int(rng.uniform(x0, W) * S), int(rng.uniform(0, H) * S)
        arr[y:y + 3 * S, x:x + 3 * S] = np.maximum(arr[y:y + 3 * S, x:x + 3 * S], 170)
    return arr


def paint(work):
    out = Path(work); (out / 'body').mkdir(parents=True, exist_ok=True); (out / 'hip').mkdir(exist_ok=True)
    m = skeleton()
    xs = np.arange(W * S)[None, :, None]
    earth = tone(m, (225, 246, 255), (50, 160, 255), 1.0)
    thin = holes(m, 4, 900, 6, 16)
    thin = holes(thin, 5, 1400, 8, 20, region=(560, 620, 880, 1500))             # spine + hips worst
    space = tone(thin, (150, 170, 190), (40, 70, 120), 0.5)
    hot = Image.new('L', (W * S, H * S), 0); hd = ImageDraw.Draw(hot)
    hd.rounded_rectangle((680 * S, 640 * S, 760 * S, 1320 * S), 30 * S, fill=255)   # spine glow
    hd.ellipse((560 * S, 1270 * S, 880 * S, 1480 * S), fill=255)                     # pelvis glow
    hg = np.asarray(hot.filter(ImageFilter.GaussianBlur(40 * S)), np.float32)[..., None] / 255
    space = space + hg * np.array([200, 40, 30]) * 0.7
    space = stars(space, 720)
    arr = np.where(xs < 720 * S, earth, space)
    arr[:, 720 * S - 3:720 * S + 3] = (255, 255, 255)
    base = finish(arr)
    label(base, 'ON EARTH', 360, 190, 80, (150, 220, 255))
    label(base, 'IN SPACE', 1080, 190, 80, (255, 140, 120))
    base.save(out / 'body' / '00_split.png')
    d = ImageDraw.Draw(base)
    for y, t in ((900, 'SPINE'), (1380, 'HIPS')):
        d.line([(900, y), (1060, y - 60)], fill=(255, 120, 100), width=8)
        label(base, t, 1170, y - 70, 70, (255, 150, 130))
    base.save(out / 'body' / '01_month.png')

    # ---- plate 2: one hip joint (femur head), Earth year vs space month
    f = Image.new('L', (W * S, H * S), 0); d = ImageDraw.Draw(f)
    rng = np.random.default_rng(9)
    for cx, n, wl in ((380, 560, 7), (1060, 70, 4)):
        d.ellipse(((cx - 230) * S, 700 * S, (cx + 230) * S, 1160 * S), fill=255)          # head
        d.rounded_rectangle(((cx - 120) * S, 1050 * S, (cx + 120) * S, 1900 * S), 50 * S, fill=255)  # neck + shaft
        d.ellipse(((cx - 200) * S, 760 * S, (cx + 200) * S, 1110 * S), fill=40)            # inside: spongy bone
        for _ in range(n):
            t = rng.uniform(0, 2 * math.pi); r = math.sqrt(rng.uniform(0, 1))
            x0, y0 = cx + 180 * r * math.cos(t), 935 + 150 * r * math.sin(t)
            a = rng.uniform(0, math.pi); L = rng.uniform(25, 60)
            d.line([(x0 * S, y0 * S), ((x0 + L * math.cos(a)) * S, (y0 + L * math.sin(a)) * S)], fill=255, width=wl * S)
        d.rounded_rectangle(((cx - 60) * S, 1180 * S, (cx + 60) * S, 1860 * S), 30 * S, fill=70)
    fa = tone(f, (225, 246, 255), (50, 160, 255), 1.0)
    fa[:, 720 * S - 3:720 * S + 3] = (255, 255, 255)
    fb = finish(fa)
    label(fb, 'EARTH', 380, 500, 96, (150, 220, 255)); label(fb, 'SPACE', 1060, 500, 96, (255, 140, 120))
    fb.save(out / 'hip' / '00_hip.png')
    label(fb, '~1% A YEAR', 380, 610, 66, (150, 220, 255)); label(fb, '~1% A MONTH', 1060, 610, 66, (255, 170, 150))
    label(fb, '(older adults)', 380, 2000, 46, (150, 190, 230)); label(fb, '(astronauts)', 1060, 2000, 46, (255, 170, 150))
    fb.save(out / 'hip' / '01_rates.png')
    dd = ImageDraw.Draw(fb)
    dd.rounded_rectangle((160, 110, 1280, 380), 30, fill=(14, 26, 54), outline=(90, 160, 230), width=5)
    label(fb, 'EXERCISE: ~2 HOURS / DAY', 720, 245, 76, (150, 230, 255))
    fb.save(out / 'hip' / '02_gym.png')
    dd = ImageDraw.Draw(fb)
    dd.rounded_rectangle((160, 110, 1280, 380), 30, fill=(40, 16, 20), outline=(240, 120, 100), width=5)
    label(fb, '1 YEAR LATER: NOT ALL BACK', 720, 245, 70, (255, 180, 160))
    fb.save(out / 'hip' / '03_later.png')


A = ['body/00_split.png', 'body/01_month.png']
B = ['hip/00_hip.png', 'hip/01_rates.png', 'hip/02_gym.png', 'hip/03_later.png']
PH = 2560

EPISODE = dict(
    chapter='Bones in Space',
    title="In Space, Your Bones Disappear. 1% Every Month. 🚀 #shorts",
    description=("Without gravity, your skeleton stops carrying weight – and starts to shrink. Astronauts lose on average "
                 "about 1–1.5 % of bone mineral density per month in the hips and spine (NASA Human Research Program; "
                 "Lang et al., Journal of Bone and Mineral Research, 2004). Older adults on Earth lose roughly that much "
                 "in a whole year (NASA, 'Space Bones', 2001). That's why crews on the International Space Station "
                 "exercise about two hours a day. And a year after long missions, many astronauts still hadn't fully "
                 "recovered their bone (TBone study, Gabel et al., Scientific Reports, 2022).\n\n"
                 "Science story, not a challenge – no medical advice. Illustrations painted with code (no photos), "
                 "narration is synthetic."),
    tags=['space bone loss', 'astronaut', 'spaceflight osteopenia', 'human body', 'body in space', 'nasa',
          'science shorts'],
    voice='af_heart',
    lines=["Go to space, and your bones start to vanish.",
           "About one percent every month, mostly in your hips and spine.",
           "On Earth, older adults lose roughly that much in a whole year.",
           "That's why astronauts exercise about two hours, every single day.",
           "And a year after landing, many still haven't won it all back."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(1, 'one', '1'), (1, 'percent', '%'), (3, 'two', '2')],
    plates=[dict(stages=A, show=[(0, 0), ('L1', 1)]),
            dict(stages=B, show=[(0, 0), ('L2', 1), ('L3', 2), ('L4', 3)])],
    camera=[(0, 720, 1280, 2300), ('L1', 720, 1280, 2380), ('L1@0.6', 720, 1280, 2440), ('L1.end', 720, 1280, 2440),
            ('L2', 720, PH + 1300, 2300), ('L3', 720, PH + 1320, 2440), ('END', 720, PH + 1320, 2440)],
    cards=[dict(at=0, until='L1-0.2', text='VANISHING', font='AlfaSlabOne-400', size=104, ink=(150, 34, 26), x=540,
                y=1560, rot=-3)],
    caption=dict(y=0.86),
    stamps=[dict(at='L1:month', text='-1% / MONTH', size=84, color=(200, 50, 30), x=540, y=1500, rot=-6, until='L2')],
    music=dict(sections=[(0, 'L2', ['Esus', 'Am9'], dict(bright=(0.2, 0.35), ticks=True)),
                         ('L2', 'L4', ['Dm9', 'Esus'], dict(bright=(0.35, 0.55), pulse=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
