"""Percept Lab #006 — why you can't tickle yourself (neon on black, numpy + Pillow; animated feather loop).
Facts: Blakemore, Wolpert & Frith, 'Central cancellation of self-produced tickle sensation', Nature Neuroscience 1998
(fMRI: self-produced touch is rated less tickly and evokes less activity in somatosensory cortex; the cerebellum is
thought to predict the sensory consequences of one's own movement); Blakemore, Frith & Wolpert, J. Cogn. Neurosci.
1999: when people tickled themselves through a robot interface, adding a delay (100-300 ms) between their movement and
the touch made it feel more tickly; Blakemore, Wolpert & Frith, 'Why can't you tickle yourself?', NeuroReport 2000."""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, S = 1440, 2560, 2
N = 12
FONT = str(Path(__file__).resolve().parents[4] / 'fonts' / 'Anton-400.woff')
BG = (6, 5, 12)
PINK, CYAN, ORANGE, VIOLET = (255, 80, 170), (70, 230, 255), (255, 150, 40), (170, 120, 255)


def neon(layers, size=(W, H)):
    """layers: list of (draw_fn, colour, width). Returns an RGB image with glow."""
    base = np.zeros((size[1] * S, size[0] * S, 3), np.float32)
    for fn, col, w in layers:
        m = Image.new('L', (size[0] * S, size[1] * S), 0); fn(ImageDraw.Draw(m), w * S)
        g1 = np.asarray(m.filter(ImageFilter.GaussianBlur(14 * S)), np.float32)[..., None] / 255
        g2 = np.asarray(m.filter(ImageFilter.GaussianBlur(4 * S)), np.float32)[..., None] / 255
        a = np.asarray(m, np.float32)[..., None] / 255
        base += g1 * np.array(col) * 1.6 + g2 * np.array(col) * 0.8
        base = base * (1 - a) + a * (np.array(col) * 0.35 + 255 * 0.65)
    base += np.array(BG)
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).resize(size, Image.LANCZOS)


def outline(fill_fn, w):
    """draw a filled silhouette with fill_fn(d) and keep only its rim (w px)"""
    m = Image.new('L', (W * S, H * S), 0); fill_fn(ImageDraw.Draw(m))
    e = m.filter(ImageFilter.MinFilter(int(w) | 1))
    return Image.fromarray(np.clip(np.asarray(m, np.int16) - np.asarray(e, np.int16), 0, 255).astype(np.uint8))


def hand_fill(d):
    k = S
    d.ellipse((500 * k, 1380 * k, 940 * k, 1900 * k), fill=255)                               # palm
    d.rectangle((560 * k, 1800 * k, 880 * k, 2600 * k), fill=255)                             # wrist
    for bx, by, ang, L, r in ((560, 1460, -112, 330, 46), (630, 1420, -100, 400, 48), (720, 1400, -90, 430, 50),
                              (810, 1420, -78, 400, 48), (520, 1700, -160, 300, 52)):       # four fingers + thumb
        a = math.radians(ang); ex, ey = bx + L * math.cos(a), by + L * math.sin(a)
        d.line([(bx * k, by * k), (ex * k, ey * k)], fill=255, width=int(2 * r * k))
        d.ellipse(((ex - r) * k, (ey - r) * k, (ex + r) * k, (ey + r) * k), fill=255)


def hand(d, w):
    o = outline(hand_fill, w)
    d.bitmap((0, 0), o, fill=255)


def feather(t):
    ang = math.radians(-35 + 28 * math.sin(2 * math.pi * t))
    tx, ty = 760 + 70 * math.sin(2 * math.pi * t), 1640

    def fn(d, w):
        k = S
        L = 820
        P = [(tx + s * L * math.cos(ang - math.pi / 2 + 0.25 * s), ty + s * L * math.sin(ang - math.pi / 2 + 0.25 * s))
             for s in np.linspace(0, 1, 30)]
        d.line([(x * k, y * k) for x, y in P], fill=255, width=int(w), joint='curve')
        for j in range(4, 29):
            x, y = P[j]; dx, dy = P[j][0] - P[j - 1][0], P[j][1] - P[j - 1][1]
            n = math.hypot(dx, dy) or 1; nx, ny = -dy / n, dx / n
            v = 110 * math.sin(math.pi * j / 30) + 30
            for side in (-1, 1):
                d.line([(x * k, y * k), ((x + side * nx * v - dx * 2.2) * k, (y + side * ny * v - dy * 2.2) * k)],
                       fill=255, width=int(w * 0.45))
    return fn


def text(im, s, x, y, px, col):
    ImageDraw.Draw(im).text((x, y), s, font=ImageFont.truetype(FONT, px), fill=col, anchor='mm')


def paint(work):
    out = Path(work); (out / 'tickle').mkdir(parents=True, exist_ok=True); (out / 'brain').mkdir(exist_ok=True)
    for i in range(N):
        im = neon([(hand, PINK, 9), (feather(i / N), CYAN, 8)])
        im.save(out / 'tickle' / ('%02d.png' % i))

    def brain_fill(d):
        k = S
        d.ellipse((250 * k, 720 * k, 1190 * k, 1300 * k), fill=255)

    def brain(d, w):
        k = S
        d.bitmap((0, 0), outline(brain_fill, w), fill=255)
        for j in range(6):                                                            # folds
            cx = 420 + j * 120; cy = 960 + 50 * math.sin(j * 1.7)
            d.arc(((cx - 60) * k, (cy - 90) * k, (cx + 60) * k, (cy + 90) * k), 200, 340, fill=255, width=int(w * 0.6))
            d.arc(((cx - 50) * k, (cy + 40) * k, (cx + 50) * k, (cy + 170) * k), 20, 160, fill=255, width=int(w * 0.6))
        d.line([(880 * k, 1290 * k), (920 * k, 1560 * k)], fill=255, width=int(w * 2.2))   # stem

    def cereb(d, w):
        k = S
        d.ellipse((900 * k, 1260 * k, 1210 * k, 1470 * k), outline=255, width=int(w))
        for j in range(4):
            d.arc(((930 + j * 8) * k, (1290 + j * 30) * k, (1180 - j * 8) * k, (1440 - j * 10) * k), 190, 350, fill=255, width=int(w * 0.6))

    b = neon([(brain, VIOLET, 8), (cereb, ORANGE, 10)])
    text(b, 'CEREBELLUM', 1060, 1640, 92, ORANGE)
    b.save(out / 'brain' / '00_brain.png')
    text(b, 'PREDICTS YOUR OWN TOUCH', 720, 1790, 70, (255, 220, 180))
    text(b, '- AND TURNS IT DOWN', 720, 1880, 70, (255, 220, 180))
    b.save(out / 'brain' / '01_predict.png')

    def robot(d, w):
        k = S
        pts = [(260, 2560), (260, 2200), (520, 2080), (640, 2300)]
        d.line([(x * k, y * k) for x, y in pts], fill=255, width=int(w * 2))
        for x, y in pts[1:]:
            d.ellipse(((x - 26) * k, (y - 26) * k, (x + 26) * k, (y + 26) * k), outline=255, width=int(w))
    r = neon([(robot, CYAN, 7)])
    rb = np.maximum(np.asarray(b), np.asarray(r))
    rb = Image.fromarray(rb)
    text(rb, '+ TINY DELAY', 1010, 2010, 90, CYAN)
    text(rb, '= TICKLES AGAIN', 1010, 2120, 90, CYAN)
    rb.save(out / 'brain' / '02_robot.png')


T = ['tickle/%02d.png' % i for i in range(N)]
B = ['brain/00_brain.png', 'brain/01_predict.png', 'brain/02_robot.png']
FPS = 12
PH = 2560

EPISODE = dict(
    chapter="Why You Can't Tickle Yourself",
    title="Why Can't You Tickle Yourself? Try It 🧠 #shorts",
    description=("Brain Test. Try to tickle yourself – it barely works. Your brain predicts the touch from your own "
                 "movement and turns the feeling down. In 1998, Sarah-Jayne Blakemore, Daniel Wolpert and Chris Frith "
                 "showed with brain scans that self-made touch causes less activity in the touch areas of the brain, and "
                 "pointed to the cerebellum as the part that makes the prediction. In a 1999 follow-up, people tickled "
                 "themselves through a robot: adding a delay of a fraction of a second made it feel more ticklish "
                 "again.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['tickle yourself', 'why cant you tickle yourself', 'cerebellum', 'brain test', 'perception', 'brain facts',
          'science shorts'],
    voice='af_nicole',
    lines=["Try to tickle yourself. Right now.",
           "Harder. Nothing? Now imagine someone else's fingers.",
           "Your brain predicts your own touch, and turns it down.",
           "In nineteen ninety-eight, brain scans pointed to the cerebellum.",
           "Add a tiny delay with a robot arm, and it tickles again.",
           "Your brain can't surprise itself. Try again."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.4, 0.5],
    display=[(3, 'nineteen', '1998,'), (3, 'ninety-eight,', '')],
    fade=0, cache=N + 4, bg=BG, tail=1.4,
    plates=[dict(stages=T, show=[(i / FPS, i % N) for i in range(FPS * 40)]),
            dict(stages=B, show=[(0, 0), ('L2+0.8', 1), ('L4', 2)])],
    camera=[(0, 720, 1500, 2100), ('L1', 720, 1500, 2100), ('L1@0.6', 720, 1620, 1700), ('L2', 720, 1620, 1700),
            ('L2+0.5', 720, PH + 1300, 2440), ('END', 720, PH + 1300, 2440)],
    cards=[dict(at=0, until='L1-0.1', text='TRY IT NOW', font='AlfaSlabOne-400', size=90, paper=(255, 255, 255),
                ink=(30, 20, 60), x=540, y=250, rot=-2),
           dict(at='L1:now', until='L2', text='SOMEONE ELSE?', font='AlfaSlabOne-400', size=84,
                paper=(255, 255, 255), ink=(170, 30, 40), x=540, y=250, rot=2)],
    stamps=[dict(at='L5:surprise', text='BRAIN: 1  YOU: 0', size=78, color=(255, 120, 180), x=540, y=300, rot=-4)],
    caption=dict(y=0.9),
    music=dict(sections=[(0, 'L2', ['Am9', 'Esus'], dict(bright=(0.25, 0.4), ticks=True, pulse=True)),
                         ('L2', 'L4', ['Fmaj7', 'Cmaj9'], dict(bright=(0.4, 0.55), pulse=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
