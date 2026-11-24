"""Myth Dug Up #006 — Sanxingdui. Plates: a Chinese ink-wash hanging scroll of the mountains of Shu with the legendary
first king Cancong, his eyes standing out of his head (inkpaint), and a field-notebook section through sacrificial
pit 2 at Sanxingdui with a bronze mask in the fill (codex).
Facts (checked): the Chronicles of Huayang (Huayang Guozhi, by Chang Qu, 4th c. AD) describe Cancong, first king of
Shu, with protruding eyes (Archaeology Magazine 2024; Sanxingdui Museum via Google Arts & Culture). In 1986 brick-factory
workers hit two sacrificial pits at Sanxingdui, Sichuan; Sichuan archaeologists excavated them (Smithsonian). Finds:
bronze masks with protruding cylindrical eyes, the largest 138 cm wide; a bronze standing figure about 2.6 m tall; a
bronze tree about 3.96 m tall; jade, gold, elephant tusks. Objects were smashed, burned and then buried. Six more pits
were found from 2019. Radiocarbon dating of the pits: roughly 1200-1000 BC (2022 study c. 1100-1050 BC; 2025 results
1201-1012 BC). No deciphered writing; whether the masks show Cancong is an interpretation (debated).
Left out (uncertain): the exact first-find year (1927 or 1929), the exact eye length, total artefact counts.
Sources: https://archaeology.org/issues/november-december-2024/features/the-many-faces-of-the-kingdom-of-shu/ ;
https://www.smithsonianmag.com/smart-news/trove-of-13000-artifacts-sheds-light-on-enigmatic-chinese-civilization-180980254/ ;
https://artsandculture.google.com/asset/mask-with-protruding-eyes/5AFJRU7_hxc1yA"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from inkpaint import Painting
from core import spline, curve, blur
import kit

W, H = 1440, 2560


def polymask(pts, soft=2.0):
    im = Image.new('L', (W, H), 0)
    ImageDraw.Draw(im).polygon([tuple(map(float, p)) for p in pts], fill=255)
    return blur(np.asarray(im, np.float32) / 255, soft)


def paint_scroll(path, stages):
    p = Painting(W, H, seed=21)
    p.paper()
    p.stage('paper')
    # far peaks of Shu, mist between them
    far = p.ridge(900, peaks=[(300, 380, 200), (760, 300, 170), (1180, 420, 190)], rough=22)
    p.wash(far, dens=0.16, decay=200, mist_y=1050, mist_h=110)
    mid = p.ridge(1320, peaks=[(160, 360, 230), (620, 250, 220), (1300, 330, 200)], rough=26)
    p.wash(mid, dens=0.3, decay=170, mist_y=1450, mist_h=90)
    p.cun(mid, 0, W, n=110, shadow_x=520, max_y=1500)
    p.mist(1500, 120, 0.85)
    p.sun(1110, 470, 70)
    p.birds([(420, 620, 1.6), (500, 590, 1.2), (560, 640, 1.0)])
    p.stage('mountains')
    # near cliff the king stands on, a pine leaning out
    near = p.ridge(2280, peaks=[(1000, 140, 420), (180, 60, 200)], rough=18)
    p.rock(near, dens=0.62, texture=60)
    p.moss(near, 40, 1400, n=90)
    p.stage('cliff')
    # ---- the legendary first king of Shu: profile facing left, his eye standing out like a tube
    fx, foot = 960, near[960] + 8
    top = foot - 900
    hx, hy = fx - 10, top + 230                       # head centre
    def shape(pts, dens, w=5, ink=0.9, dry=0.3, smooth=True):
        p.over(p.D, polymask(pts) * dens * (0.8 + 0.2 * p.noise2d(40, 3, 5)))
        ring = list(pts) + [pts[0]]
        p.stroke(spline(ring, 6) if smooth else np.array(ring, np.float32), w, ink, dry=dry)
    # robe, belt, folds
    robe = [(fx - 70, top + 320), (fx + 80, top + 320), (fx + 140, foot - 10), (fx - 150, foot - 10)]
    shape(robe, 0.40, 7, 0.85, 0.45, smooth=False)
    p.stroke([(fx - 160, foot - 14), (fx + 150, foot - 14)], 9, 0.9, dry=0.3)
    p.over(p.D, polymask([(fx - 86, top + 520), (fx + 96, top + 520), (fx + 100, top + 556), (fx - 90, top + 556)]) * 0.5)
    for k in range(5):
        x = fx - 80 + 40 * k
        p.stroke(spline([(x, top + 580), (x - 6 - 4 * k, top + 700), (x - 14 - 8 * k, foot - 40)], 8), 2.2, 0.5, dry=0.6)
    # a wide sleeve held forward, hands closed round a ring
    sleeve = [(fx - 60, top + 330), (fx + 30, top + 340), (fx - 40, top + 520), (fx - 190, top + 600), (fx - 230, top + 520)]
    shape(sleeve, 0.55, 6, 0.9, 0.35)
    p.stroke(spline([(fx - 100, top + 420), (fx - 150, top + 500)], 6), 2.2, 0.6, dry=0.5)
    p.stroke(spline([(fx - 252, top + 470), (fx - 280, top + 540), (fx - 252, top + 610)], 8), 13, 0.9, dry=0.2)
    p.stroke(spline([(fx - 210, top + 470), (fx - 236, top + 540), (fx - 210, top + 610)], 8), 13, 0.9, dry=0.2)
    p.dot(fx - 240, top + 540, 16, 0.55)
    # neck, head in profile, a great ear
    p.over(p.D, polymask([(hx - 20, hy + 70), (hx + 40, hy + 60), (hx + 48, top + 330), (hx - 30, top + 330)]) * 0.25)
    ear = [(hx + 28, hy - 50), (hx + 115, hy - 85), (hx + 128, hy + 5), (hx + 70, hy + 62), (hx + 40, hy + 30)]
    shape(ear, 0.3, 6, 0.9)
    p.stroke(spline([(hx + 60, hy - 40), (hx + 100, hy - 55), (hx + 100, hy)], 6), 2.4, 0.7, dry=0.3)
    face = [(hx - 58, hy - 78), (hx - 70, hy - 50), (hx - 82, hy - 36), (hx - 76, hy - 14), (hx - 100, hy + 14), (hx - 74, hy + 22),
            (hx - 80, hy + 40), (hx - 72, hy + 52), (hx - 66, hy + 76), (hx + 10, hy + 88), (hx + 48, hy + 40), (hx + 50, hy - 78)]
    shape(face, 0.10, 5, 0.9, 0.25)
    p.stroke([(hx - 78, hy + 46), (hx - 40, hy + 48)], 3.0, 0.85, dry=0.2)                        # mouth
    # the eye: a tube standing far out of the face
    ey = hy - 26
    tube = [(hx - 40, ey - 22), (hx - 190, ey - 26), (hx - 190, ey + 20), (hx - 40, ey + 22)]
    shape(tube, 0.5, 4.5, 0.95, 0.15, smooth=False)
    p.stroke(spline([(hx - 190, ey - 26), (hx - 204, ey - 3), (hx - 190, ey + 20), (hx - 178, ey - 3), (hx - 190, ey - 26)], 6), 3.5, 0.95, dry=0.1)
    p.stroke([(hx - 150, ey - 24), (hx - 150, ey + 21)], 2.2, 0.6, dry=0.4)
    p.stroke([(hx - 110, ey - 23), (hx - 110, ey + 21)], 2.2, 0.6, dry=0.4)
    # tall crown flaring upward
    crown = [(hx - 58, hy - 78), (hx + 50, hy - 80), (hx + 78, hy - 250), (hx - 92, hy - 246)]
    shape(crown, 0.5, 6, 0.9, 0.3, smooth=False)
    for k in range(3):
        p.stroke([(hx - 64 - 8 * k, hy - 120 - 40 * k), (hx + 56 + 7 * k, hy - 124 - 40 * k)], 2.2, 0.45, dry=0.5)
    p.stage('king')
    # a seal in vermilion (a plain carved square, no characters)
    sx, sy, s = 1250, 2380, 90
    p.over(p.R, polymask([(sx, sy), (sx + s, sy), (sx + s, sy + s), (sx, sy + s)], 1.2) * 0.85)
    for a, b in (((sx + 18, sy + 22), (sx + 72, sy + 22)), ((sx + 45, sy + 22), (sx + 45, sy + 70)), ((sx + 18, sy + 70), (sx + 72, sy + 70))):
        p.R *= 1 - 0.9 * polymask([(a[0] - 4, a[1] - 4), (b[0] + 4, a[1] - 4), (b[0] + 4, b[1] + 4), (a[0] - 4, b[1] + 4)], 0.8)
    p.stage('seal')
    p.save(path, stages_dir=stages)



def mask_in_pit(c, bounds, xs):
    """the bronze mask lying in the pit fill: wide face, eyes as tubes seen end-on, huge ears; tusks beside it"""
    from codex import Codex
    a, b = float(np.interp(645, xs, bounds[2])), float(np.interp(645, xs, bounds[3]))
    cx, cy = 645, (a + b) / 2 + 70
    k = 0.72
    S = lambda pts: [(cx + k * (x - cx), cy + k * (y - cy)) for x, y in pts]
    face = S([(cx - 150, cy - 70), (cx + 150, cy - 70), (cx + 135, cy + 60), (cx + 60, cy + 95), (cx - 60, cy + 95), (cx - 135, cy + 60)])
    c.contour(face, width=3.0, closed=True)
    for sx in (-1, 1):
        ex = cx + sx * 68 * k
        c.contour(Codex.arc(ex, cy - 20 * k, 30 * k, 0, 360), width=2.6, closed=True)            # tube rims, end-on
        c.contour(Codex.arc(ex, cy - 20 * k, 16 * k, 0, 360), width=1.8, closed=True)
        ear = S([(cx + sx * 150, cy - 60), (cx + sx * 240, cy - 110), (cx + sx * 255, cy - 20), (cx + sx * 160, cy + 40)])
        c.contour(ear, width=2.6, closed=True)
    c.contour(S([(cx - 10, cy - 55), (cx, cy + 25), (cx + 12, cy + 25)]), width=2.0)               # nose
    c.contour(S([(cx - 70, cy + 55), (cx + 70, cy + 55)]), width=2.4)                               # mouth
    c.hatch(c.poly_mask(face), shade=0.35, angle=30, spacing=6)
    for kk in range(2):                                                                             # elephant tusks
        y = cy - 150 + 30 * kk
        c.contour(Codex.arc(cx - 20 + 20 * kk, y + 120, 160, 240, 300, ry=110), width=2.4)
    c.write(['bronze mask', 'eyes stand out'], cx + 210, cy - 40, size=28, mirror=False, ink=1.0)
    c.arrow([(cx + 205, cy - 30), (cx + 120, cy - 20), (cx + 70, cy - 15)], width=1.8)
    c.write(['tusks'], cx - 300, cy - 120, size=26, mirror=False, ink=0.9)


LAYERS = [('FIELDS', 'topsoil today'), ('LATER SOIL', 'after c. 1000 BC'), ('PIT LEVEL', 'c. 1200-1000 BC'),
          ('SUBSOIL', 'natural clay')]


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_scroll(str(out / 'scroll.png'), str(out / 'scroll'))
    kit.section(out, 'pit', 'SANXINGDUI', 'section through sacrificial pit 2 · 1986', LAYERS, seed=26, hump=110,
                trench=(440, 850, 2, 'pit 2: brick workers', 'hit it in 1986'), note=('smashed, burnt', 2),
                highlight=(2,), extra=mask_in_pit)


PH = 2560
SCROLL = ['scroll/%s.png' % n for n in ('01_mountains', '02_cliff', '03_king', '04_seal')] + ['scroll.png']
PIT = ['pit/%s.png' % n for n in ['00_sheet', '01_title', '02_surface', '03_trench'] +
       ['%02d_layer_%02d' % (4 + i, i) for i in range(len(LAYERS))] + ['%02d_notes' % (4 + len(LAYERS))]] + ['pit.png']

EPISODE = dict(
    chapter='Sanxingdui',
    title="A Legend Said This King's Eyes Stuck Out. Then They Dug. #shorts",
    description=("An old Chinese chronicle (the Chronicles of Huayang) says Cancong, the first king of Shu, had protruding "
                 "eyes. In 1986 brick-factory workers at Sanxingdui in Sichuan hit two sacrificial pits: bronze masks with "
                 "eyes sticking out like tubes (the biggest 1.38 m wide), a bronze tree almost 4 m tall, gold, jade and "
                 "elephant tusks, about 3,000 years old, smashed and burned before burial.\n\n"
                 "Proven: a lost Bronze Age culture in Sichuan made faces with protruding eyes, just like the legend.\n"
                 "Debated: whether the masks show Cancong himself — the culture left no writing we can read.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['sanxingdui', 'bronze masks', 'cancong', 'shu kingdom', 'sichuan', 'ancient china', 'bronze age', 'archaeology',
          'chinese history', 'history shorts'],
    lines=["This king's eyes stuck out of his head.",
           "An old Chinese chronicle says the first king of Shu, Tsahn-tsong, had protruding eyes. For centuries, it sounded like pure myth.",
           "Then, in nineteen eighty-six, brick factory workers in western China hit two pits packed with buried treasure at Sahn-shing-dway.",
           "Inside: bronze masks with eyes sticking out like tubes, the biggest over a meter wide. A bronze tree almost four meters tall. "
           "All about three thousand years old, smashed and burned before burial.",
           "Proven: a lost Bronze Age kingdom with eyes like the legend. Debated: whether the masks show Tsahn-tsong himself."],
    gaps=[0.15, 0.35, 0.45, 0.40, 0.45],
    display=[(1, 'tsahn-tsong,', 'CANCONG,'), (2, 'nineteen', '1986,'), (2, 'eighty-six,', ''), (2, 'sahn-shing-dway.', 'SANXINGDUI.'),
             (3, 'four', '4'), (3, 'three', '3,000'), (3, 'thousand', ''), (4, 'tsahn-tsong', 'CANCONG')],
    plates=[dict(stages=SCROLL, show=[(0, 2), (0.8, 3), (1.4, 4)]),
            dict(stages=PIT, show=[(0, 0), ('L2-0.2', 1), ('L2+0.4', 2), ('L2:workers', 3)] +
                 [('L2@%.2f' % (0.55 + 0.1 * i), 4 + i) for i in range(len(LAYERS))] + [('L3-0.1', 8), ('L4', 9)])],
    camera=[(0, 830, 1500, 1350), ('L0.end', 800, 1560, 1750), ('L1+0.3', 720, 1290, 2450), ('L1:protruding-0.4', 740, 1350, 2100),
            ('L1:protruding+0.4', 820, 1470, 1150), ('L1:sounded', 800, 1450, 1350), ('L1.end+0.1', 720, 1290, 2450),
            ('L2-0.1', 720, PH + 720, 1800), ('L2:hit-0.3', 720, PH + 1150, 2250), ('L2.end', 720, PH + 1300, 2300),
            ('L3+0.2', 700, PH + 1640, 1450), ('L3:a#2', 700, PH + 1620, 1550), ('L3:all-0.2', 720, PH + 1450, 2100),
            ('L4+0.2', 720, PH + 1290, 2450), ('END', 720, PH + 1270, 2400)],
    cards=[dict(at='L1:chronicle', until='L1:tsahn-0.2', text='CHRONICLES OF HUAYANG', size=56, x=540, y=300, rot=-2),
           dict(at='L1:tsahn', until='L2-0.15', text='CANCONG', font='AlfaSlabOne-400', size=110, ink=(150, 34, 26), x=560, y=290, rot=3),
           dict(at='L2:nineteen', until='L3-0.2', text='1986', font='AlfaSlabOne-400', size=120, x=840, y=250, rot=-3),
           dict(at='L2:western', until='L3-0.2', text='SICHUAN, CHINA', size=66, x=470, y=1150, rot=-2),
           dict(at='L3:biggest', until='L3:a#1-0.1', text='MASK 1.38 M WIDE', size=66, x=540, y=300, rot=-3),
           dict(at='L3:a#2', until='L3:all-0.1', text='BRONZE TREE ~4 M', size=66, x=540, y=300, rot=3),
           dict(at='L3:all', until='L4-0.1', text='c. 1200-1000 BC', font='AlfaSlabOne-400', size=84, ink=(150, 34, 26), x=560, y=300, rot=-2)],
    stamps=[dict(at='L4:proven', text='KINGDOM: PROVEN', size=72, color=(30, 70, 52), x=540, y=640, rot=-6),
            dict(at='L4:debated', text='CANCONG: DEBATED', size=70, color=(160, 32, 24), x=540, y=860, rot=5)],
    music=dict(sections=[(0, 'L2-0.3', ['Am9', 'Dm9'], dict(bright=(0.2, 0.35), plucks=0.45)),
                         ('L2-0.3', 'L3', ['Fmaj7', 'Esus'], dict(bright=(0.35, 0.5), pulse=True, plucks=0.3)),
                         ('L3', 'L4', ['Am9', 'Esus'], dict(bright=(0.45, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Dm9', 'Am9'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
