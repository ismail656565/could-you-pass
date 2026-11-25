"""Percept Lab #005 — the spinning dot sphere (Brain Test). ~400 identical dots on latitude rings of a sphere, drawn in
orthographic projection with no size, brightness or occlusion cues, so the 2D motion fits a sphere spinning either way:
the brain picks one direction and can flip it (bistable perception). The 3D shape from 2D motion is the kinetic depth
effect, described by Hans Wallach and D. N. O'Connell in 1953 (Wikipedia 'Kinetic depth effect'; Wallach & O'Connell,
J. Exp. Psychol. 45, 1953). Each ring has a multiple of 8 dots, so 24 stages of 45/24 degrees loop seamlessly;
the stages are cycled as an animation (EPISODE fade=0 = hard cuts)."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

N = 24
ST = ['spin/%02d.png' % i for i in range(N)]
W, H, CX, CY, R = 1440, 2560, 720, 1280, 560
TILT = math.radians(14)


def dots():
    pts = []
    for k in range(1, 16):                                   # 15 latitude rings
        lat = -math.pi / 2 + k * math.pi / 16
        m = max(8, 8 * round(3.4 * math.cos(lat)))
        ph = (k % 2) * math.pi / m
        for j in range(m):
            lon = ph + 2 * math.pi * j / m
            pts.append((math.cos(lat) * math.cos(lon), math.sin(lat), math.cos(lat) * math.sin(lon)))
    return np.array(pts)


def paint(work):
    out = Path(work) / 'spin'; out.mkdir(parents=True, exist_ok=True)
    P = dots()
    S = 2                                                     # supersample
    rng = np.random.default_rng(5)
    stars = rng.random((60, 2)) * [W, H]
    for i in range(N):
        a = (math.pi / 4) * i / N                             # 8-fold symmetry: 45 degrees = one loop
        x = P[:, 0] * math.cos(a) - P[:, 2] * math.sin(a)
        z = P[:, 0] * math.sin(a) + P[:, 2] * math.cos(a)
        y = P[:, 1] * math.cos(TILT) - z * math.sin(TILT)     # tilt the axis a little toward the viewer
        im = Image.new('RGB', (W * S, H * S), (6, 5, 12))
        d = ImageDraw.Draw(im)
        for sx, sy in stars:
            d.ellipse((sx * S - 2, sy * S - 2, sx * S + 2, sy * S + 2), fill=(40, 36, 60))
        glow = Image.new('RGB', (W * S, H * S), (0, 0, 0))
        g = ImageDraw.Draw(glow)
        for px, py in zip(CX + R * x, CY - R * y):
            g.ellipse((px * S - 26, py * S - 26, px * S + 26, py * S + 26), fill=(120, 70, 230))
        glow = glow.filter(ImageFilter.GaussianBlur(14))
        im = Image.fromarray(np.clip(np.asarray(im, np.int16) + np.asarray(glow, np.int16) * 0.8, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im)
        for px, py in zip(CX + R * x, CY - R * y):
            d.ellipse((px * S - 13, py * S - 13, px * S + 13, py * S + 13), fill=(236, 228, 255))
        im.resize((W, H), Image.LANCZOS).save(out / ('%02d.png' % i))


FPS_SPIN = 30
EPISODE = dict(
    chapter='The Spinning Sphere',
    title="Which Way Is It Spinning? Now Flip It With Your Mind 🧠 #shorts",
    description=("Brain Test #2. Which way does the ball of dots spin – left or right? Now try to flip it, only with your "
                 "mind. The animation never changes: every dot is the same size and brightness, so there is no depth "
                 "information, and the motion fits a ball spinning either way. Your brain has to pick one – and it can "
                 "switch. Seeing a 3D shape from flat motion is called the kinetic depth effect, described by the "
                 "psychologists Hans Wallach and D. N. O'Connell in 1953.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['spinning sphere illusion', 'which way is it spinning', 'kinetic depth effect', 'bistable illusion',
          'optical illusion', 'brain test', 'perception'],
    voice='af_nicole',
    lines=["Which way is this ball spinning?",
           "Decide. Now make it spin the other way. Only with your mind.",
           "Blink. Look at the left edge. Try again.",
           "It never changed. The dots have no depth, so your brain picks a side.",
           "It's called the kinetic depth effect, first described in nineteen fifty-three.",
           "So which way is it spinning now?"],
    gaps=[0.15, 0.4, 0.5, 1.0, 0.4, 0.5],
    display=[(4, 'nineteen', '1953.'), (4, 'fifty-three.', '')],
    fade=0, cache=N + 1, bg=(6, 5, 12), tail=1.6,
    plates=[dict(stages=ST, show=[(i / FPS_SPIN, i % N) for i in range(FPS_SPIN * 40)])],
    camera=[(0, 720, 1280, 2480), ('L1', 720, 1280, 2480), ('L1:only', 720, 1280, 2380), ('L3', 720, 1280, 2380),
            ('L3@0.5', 720, 1280, 2480), ('END', 720, 1280, 2480)],
    cards=[dict(at=0, until='L1-0.1', text='LEVEL: EASY', font='AlfaSlabOne-400', size=84, paper=(255, 255, 255),
                ink=(30, 20, 60), x=540, y=250, rot=-2),
           dict(at='L1', until='L3-0.1', text='LEVEL: HARD', font='AlfaSlabOne-400', size=84, paper=(255, 255, 255),
                ink=(170, 30, 40), x=540, y=250, rot=2)],
    stamps=[dict(at='L3', text='YOUR BRAIN CHOSE', size=78, color=(190, 150, 255), x=540, y=260, rot=-4)],
    caption=dict(y=0.82),
    music=dict(sections=[(0, 'L2', ['Am9', 'Esus'], dict(bright=(0.25, 0.4), ticks=True, pulse=True)),
                         ('L2', 'L4', ['Fmaj7', 'Cmaj9'], dict(bright=(0.4, 0.55), pulse=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
