"""Myth Dug Up #002 — Pompeii. Plates: the CAVE CANEM guard-dog floor mosaic (mosaic), and an excavator's plan of
Pompeii's street blocks (codex field notebook). Facts: Vesuvius buried Pompeii in AD 79; its location was forgotten;
systematic excavation began in 1748; Giuseppe Fiorelli made the first plaster casts of victims' voids in 1863;
the traditional date 24 August comes from copies of Pliny the Younger's letter, but a charcoal inscription found in
2018 dated to mid-October suggests an autumn eruption — the exact date is debated."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from mosaic import Mosaic
from core import spline, blob_pts
import kit

DOG = [(0, 212), (36, 192), (92, 172), (148, 124), (172, 88), (196, 132), (236, 150), (300, 186), (420, 200), (560, 194),
       (680, 184), (760, 188), (792, 176), (846, 108), (878, 58), (898, 70), (866, 132), (818, 204), (806, 250),
       (846, 318), (904, 398), (916, 424), (866, 426), (800, 344), (756, 304), (650, 292), (540, 300), (470, 308),
       (400, 318), (352, 340), (300, 404), (244, 436), (204, 434), (218, 410), (276, 378), (300, 334), (262, 300),
       (214, 282), (160, 262), (96, 252), (32, 242), (58, 226)]


def paint_mosaic(out):
    W, H = 1440, 2560
    m = Mosaic(W, H, seed=5, tile=14)
    m.paint(np.ones((H, W), np.float32), 'white')
    U = lambda *ms: np.clip(sum(ms), 0, 1)
    DX = 170
    body = U(m.ellipse(820, 1160, 300, 92, rot=-0.06), m.ellipse(600, 1150, 135, 112))
    neck = m.band([(570, 1120), (470, 1030)], 92)
    head = U(m.ellipse(425, 1005, 86, 64), m.poly_mask([(410, 960), (282, 1012), (270, 1046), (406, 1062)]))
    ear = m.poly_mask([(402, 958), (432, 872), (470, 952)])
    legs = U(m.band([(590, 1200), (500, 1300), (415, 1352)], 44, 34), m.band([(640, 1215), (580, 1320), (500, 1392)], 42, 32),
             m.band([(1030, 1180), (1075, 1285), (1155, 1360)], 50, 34), m.band([(970, 1200), (990, 1310), (1040, 1392)], 46, 32))
    paws = U(*[m.ellipse(x, y, 30, 15) for x, y in ((406, 1356), (490, 1396), (1165, 1364), (1050, 1396))])
    tail = m.band([(1100, 1125), (1170, 1045), (1220, 950)], 30, 10)
    dog = U(body, neck, head, ear, legs, paws, tail)
    collar = m.band([(488, 990), (542, 1112)], 36) * dog
    eye = m.ellipse(398, 992, 11, 9)
    mouth = m.band([(278, 1032), (370, 1040)], 8) * dog
    chain = [(520, 1050), (550, 940), (590, 820), (640, 690), (690, 560)]
    m.paint(dog, 'black'); m.paint(collar, 'red'); m.paint(eye, 'white'); m.paint(mouth, 'red')
    m.sinopia(dog, width=3.2)
    m.sinopia(pts=[(220, 1640), (1220, 1640)], width=2.6, strength=0.5)
    m.stage('sinopia')
    m.frame(40, 40, W - 40, H - 40, 110, size=12, stones=['black'])
    m.frame(150, 150, W - 150, H - 150, 34, size=11, stones=['red', 'brick'])
    m.outline(dog, 'black', 1, 7)
    m.fill(dog * (1 - collar) * (1 - eye) * (1 - mouth), 7, colour='black')
    m.fill(collar, 6, stones=['red', 'brick'])
    m.fill(mouth, 5, stones=['red'])
    m.fill(eye, 5, colour='white')
    m.line(chain, 'black', 8)
    m.stage('dog')
    m.letters('CAVE CANEM', W / 2, 1640, 100, 'black')
    m.stage('letters')
    inner = m.rect(184, 184, W - 184, H - 184)
    m.halo(inner, rows=2, size=12, stones=['white', 'bone'])
    m.rows(inner * (1 - m.everything()), size=13, wobble=5, stones=['white', 'bone', 'cream'])
    m.rows(np.clip(1 - m.everything(), 0, 1), size=12, stones=['white', 'bone'])
    m.stage('ground')
    m.lacuna(m.poly_mask(blob_pts(1150, 2240, 100, 64, rough=0.3, seed=4)))
    m.lacuna(m.poly_mask(blob_pts(300, 420, 60, 90, rough=0.3, seed=8)))
    m.crack([(1440, 760), (1300, 820), (1240, 900), (1180, 930), (1100, 1010)])
    m.crack([(0, 2000), (160, 1960), (250, 1990), (380, 1930)])
    m.patina(1.0)
    m.save(str(Path(out) / 'mosaic.png'), stages_dir=str(Path(out) / 'mosaic'))
    return MOS


def blocks():
    """Pompeii-like insulae: a skewed grid of blocks cut by streets, each block split into houses"""
    rng = np.random.default_rng(3)
    rooms = []
    xs = [160, 420, 690, 960, 1270]
    ys = [440, 760, 1120, 1480, 1840, 2230]
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            x0, x1, y0, y1 = xs[i] + 22, xs[i + 1] - 22, ys[j] + 22, ys[j + 1] - 22
            if (i, j) == (1, 1):                       # the forum: an open square
                rooms.append((x0, y0, x1 + 270 - 22, y1)); continue
            if (i, j) == (2, 1): continue
            cut = rng.uniform(0.38, 0.62)
            xm = x0 + (x1 - x0) * cut
            ym = y0 + (y1 - y0) * rng.uniform(0.35, 0.65)
            rooms += [(x0, y0, xm, ym), (xm, y0, x1, ym), (x0, ym, x1, y1)]
    return rooms


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    global MOSAIC, PLAN
    paint_mosaic(out)
    kit.plan(out, 'plan', 'POMPEII', 'excavated street blocks · after 1748', blocks(),
             labels=[('FORUM', 500, 940, 46), ("Via dell'Abbondanza", 180, 1160, 30), ('Vesuvius  ↑  9 km', 980, 380, 30)],
             red=(9,), hatch_rooms=(3, 7, 13, 20), scale_text='0        50       100 m')


PH = 2560
MOS = ['mosaic/%s.png' % n for n in ('00_sinopia', '01_dog', '02_letters', '03_ground')] + ['mosaic.png']
PLAN = ['plan/00_sheet.png', 'plan/01_title.png', 'plan/02_grid.png'] + ['plan/%02d_rooms_%02d.png' % (3 + k, i) for k, i in enumerate([12, 25, 38, 51])] + ['plan/07_notes.png', 'plan.png']

EPISODE = dict(
    chapter='Pompeii',
    title="This Dog Has Guarded a Door for 2,000 Years #shorts",
    description=("CAVE CANEM — 'beware of the dog'. Pompeii was buried by Vesuvius in AD 79 and then forgotten. "
                 "Excavations began in 1748, and in 1863 Giuseppe Fiorelli filled the empty spaces left in the ash with plaster.\n\n"
                 "Proven: Vesuvius buried Pompeii in AD 79.\n"
                 "Debated: the exact day — a charcoal inscription found in 2018 points to October rather than 24 August.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['pompeii', 'vesuvius', 'cave canem', 'roman mosaic', 'ancient rome', 'archaeology', 'fiorelli', 'history shorts'],
    lines=["This dog has been guarding a door for almost two thousand years.",
           "Pompeii. A Roman city buried by Vesuvius in seventy-nine A.D. For centuries, people knew the name, but not where it was.",
           "Then, in seventeen forty-eight, excavators broke through. Streets. Shops. Bakeries. A whole city, sealed in ash.",
           "The people were gone, but their shapes weren't. In eighteen sixty-three, Giuseppe Fiorelli filled the hollows in the ash with plaster.",
           "Proven: Vesuvius buried Pompeii in seventy-nine A.D. Debated: the exact day. An inscription found in twenty eighteen points to October, not August."],
    gaps=[0.15, 0.30, 0.45, 0.40, 0.45],
    display=[(0, 'two', '2,000'), (0, 'thousand', ''), (1, 'seventy-nine', '79'), (1, 'a.d.', 'AD.'), (2, 'seventeen', '1748,'), (2, 'forty-eight,', ''),
             (3, 'eighteen', '1863,'), (3, 'sixty-three,', ''), (4, 'seventy-nine', '79'), (4, 'a.d.', 'AD.'),
             (4, 'twenty', '2018'), (4, 'eighteen', '')],
    plates=[dict(stages=MOS, show=[(0, 1), (0.9, 2), ('L1', 3), ('L1+1.2', 4)]),
            dict(stages=PLAN, show=[(0, 0), ('L2-0.2', 1), ('L2+0.4', 2), ('L2@0.3', 3), ('L2@0.5', 4), ('L2@0.7', 5), ('L2@0.9', 6),
                                     ('L3@0.5', 7), ('L4', 8)])],
    camera=[(0, 560, 1110, 950), ('L0.end', 680, 1180, 1250), ('L1+0.8', 720, 1330, 2450), ('L2-0.3', 720, 1300, 2350),
            ('L2+0.5', 560, PH + 560, 1500), ('L2@0.8', 720, PH + 1250, 2300), ('L3', 620, PH + 1200, 1400),
            ('L3.end', 560, PH + 1050, 1250), ('L4+0.3', 720, PH + 1300, 2450), ('END', 720, PH + 1290, 2400)],
    cards=[dict(at='L1:seventy', until='L2-0.2', text='AD 79', font='AlfaSlabOne-400', size=120, ink=(150, 34, 26), x=820, y=250, rot=4),
           dict(at='L2:seventeen', until='L3-0.2', text='1748', font='AlfaSlabOne-400', size=120, ink=(26, 22, 18), x=840, y=260, rot=-3),
           dict(at='L3:giuseppe-0.05', until='L4-0.2', text='GIUSEPPE FIORELLI · 1863', size=58, x=540, y=1080, rot=-2)],
    stamps=[dict(at='L4:proven', text='ERUPTION: PROVEN', size=74, color=(30, 70, 52), x=540, y=640, rot=-6),
            dict(at='L4:debated', text='DATE: DEBATED', size=74, color=(160, 32, 24), x=540, y=860, rot=5)],
    music=dict(sections=[(0, 'L2-0.3', ['Am9', 'Fmaj7'], dict(bright=(0.2, 0.35), plucks=0.4)),
                         ('L2-0.3', 'L3', ['Dm9', 'Esus'], dict(bright=(0.35, 0.5), pulse=True, plucks=0.3)),
                         ('L3', 'L4', ['Am9', 'Dm9'], dict(bright=(0.3, 0.4), plucks=0.2)),
                         ('L4', 'END', ['Fmaj7', 'Esus'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
