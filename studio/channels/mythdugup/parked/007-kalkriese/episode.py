"""Myth Dug Up #007 — Kalkriese (the Varus battle). Plates: a Roman floor mosaic of a legion's eagle with LEG XIX and
Augustus' cry VARE, LEGIONES REDDE (mosaic), and a field-notebook sketch plan of the pass at Kalkriese between the hill
and the great bog, with the turf wall, trenches and finds (codex).
Facts (checked): AD 9, three legions (XVII, XVIII, XIX) under Publius Quinctilius Varus were destroyed by Germanic
warriors led by Arminius (Tacitus, Cassius Dio, Velleius); Suetonius reports Augustus crying "Quintili Vare, legiones
redde". The site was lost for centuries. 1987: British army officer Major Tony Clunn, with a metal detector near Kalkriese
(Osnabrueck), found Roman silver coins (denarii); then three lead sling shots (1988). Excavation from 1989 (Wolfgang
Schlueter): an iron cavalry face mask (once silver-coated), a turf wall at least 700 m long, bone pits. Museum opened
2002. A 2022 metal-fingerprint study linked finds to Legio XIX. Debated: whether Kalkriese is the Varus battle itself or
a later fight (Germanicus' campaigns AD 15-16), and whether the wall is Germanic or part of a Roman camp.
Sources: https://www.livius.org/articles/battle/teutoburg-forest-9-ce/teutoburg-forest-4 ;
https://www.smithsonianmag.com/history-archaeology/ambush.html ; https://www.spektrum.de/news/fand-die-varusschlacht-in-kalkriese-statt/1676512 ;
https://www.kalkriese-varusschlacht.de/en/museum-park.html"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from mosaic import Mosaic
from core import spline, blob_pts, fbm1d
import kit

W, H = 1440, 2560


def paint_mosaic(path, stages):
    m = Mosaic(W, H, seed=9, tile=14)
    m.paint(np.ones((H, W), np.float32), 'white')
    U = lambda *ms: np.clip(sum(ms), 0, 1)
    cx = 720
    # the eagle of a legion (aquila): wings raised, head turned left, standing on a thunderbolt bar
    body = m.ellipse(cx, 900, 120, 200)
    head = m.ellipse(cx - 20, 650, 74, 70)
    beak = m.poly_mask([(cx - 78, 622), (cx - 150, 630), (cx - 176, 672), (cx - 150, 662), (cx - 86, 692)])
    wl = [(cx - 80, 780), (cx - 190, 640), (cx - 300, 470), (cx - 420, 380), (cx - 400, 520), (cx - 470, 560), (cx - 420, 650),
          (cx - 480, 700), (cx - 400, 770), (cx - 440, 830), (cx - 300, 860), (cx - 100, 980)]
    wing_l = m.poly_mask(wl)
    wing_r = m.poly_mask([(2 * cx - x, y) for x, y in wl])
    tail = m.poly_mask([(cx - 70, 1060), (cx + 70, 1060), (cx + 130, 1200), (cx - 130, 1200)])
    legs = U(m.band([(cx - 50, 1060), (cx - 60, 1190)], 30), m.band([(cx + 50, 1060), (cx + 60, 1190)], 30))
    eagle = U(body, head, beak, wing_l, wing_r, tail, legs)
    eye = m.ellipse(cx - 40, 640, 10, 10)
    bolt = m.poly_mask([(cx - 230, 1190), (cx + 230, 1190), (cx + 200, 1240), (cx - 200, 1240)])
    wreath = U(m.ellipse(cx, 1340, 150, 58)) - m.ellipse(cx, 1340, 112, 30)
    wreath = np.clip(wreath, 0, 1)
    pole = m.band([(cx, 1240), (cx, 1560)], 30)
    m.shade(eagle, 'yellow', 'ochre', (cx, 450), (cx, 1200))
    m.paint(beak, 'gold'); m.paint(eye, 'black'); m.paint(bolt, 'scarlet'); m.paint(wreath, 'green'); m.paint(pole, 'brown')
    m.sinopia(eagle, width=3.2); m.sinopia(bolt, width=2.6); m.sinopia(pole, width=2.4)
    m.stage('sinopia')
    m.frame(40, 40, W - 40, H - 40, 110, size=12, stones=['black'])
    m.frame(150, 150, W - 150, H - 150, 34, size=11, stones=['red', 'brick'])
    m.outline(eagle, 'umber', 1, 7)
    for side in (-1, 1):                                    # feather rows
        for k in range(4):
            y0 = 560 + 80 * k
            pts = [(cx + side * (150 + 30 * k), y0 + 230), (cx + side * (230 + 30 * k), y0 + 110), (cx + side * (300 + 15 * k), y0 + 40 + 10 * k)]
            wing = wing_l if side < 0 else wing_r
            pts = [p for p in pts if wing[int(p[1]), int(p[0])] > 0.5]
            if len(pts) >= 2:
                m.line(pts, 'brown', 6)
    m.fill(eagle * (1 - eye), 7)
    m.fill(eye, 5, colour='black')
    m.outline(bolt, 'black', 1, 7); m.fill(bolt, 7, stones=['scarlet', 'red'])
    m.outline(wreath, 'black', 1, 6); m.fill(wreath, 6, stones=['green'])
    m.fill(pole * (1 - m.everything()), 7, stones=['brown', 'umber'])
    m.stage('eagle')
    m.tabula(cx - 260, 1600, cx + 260, 1740, [('LEG · XIX', 80, 'black')], ear=70)
    m.letters('VARE,', W / 2, 1860, 110, 'red')
    m.letters('LEGIONES', W / 2, 2010, 110, 'black')
    m.letters('REDDE!', W / 2, 2160, 110, 'black')
    m.stage('letters')
    inner = m.rect(184, 184, W - 184, H - 184)
    m.halo(inner, rows=2, size=12, stones=['white', 'bone'])
    m.rows(inner * (1 - m.everything()), size=13, wobble=5, stones=['white', 'bone', 'cream'])
    m.rows(np.clip(1 - m.everything(), 0, 1), size=12, stones=['white', 'bone'])
    m.stage('ground')
    m.lacuna(m.poly_mask(blob_pts(1120, 300, 90, 60, rough=0.3, seed=5)))
    m.lacuna(m.poly_mask(blob_pts(260, 1900, 50, 80, rough=0.3, seed=7)))
    m.crack([(1440, 1500), (1300, 1560), (1240, 1640), (1160, 1660)])
    m.patina(1.0)
    m.save(path, stages_dir=stages)



def landscape(c):
    """the pass: great bog to the north, Kalkriese hill to the south, the turf wall at the foot of the hill"""
    from codex import Codex
    rng = np.random.default_rng(4)
    for k in range(70):                                                         # marsh tufts in the bog
        x, y = rng.uniform(200, 1240), rng.uniform(480, 940)
        for a in (-0.5, 0, 0.5):
            c.quill([(x, y), (x + 14 * a, y - 18)], width=1.2, ink=0.7)
        c.quill([(x - 14, y + 2), (x + 14, y + 2)], width=1.0, ink=0.6)
    for k in range(4):
        xs = np.linspace(200, 1240, 80)
        c.dotted(np.stack([xs, 980 + 14 * k + 10 * fbm1d(80, 12, 2, k)], 1), width=1.0, dash=5, gap=7)
    c.write(['THE GREAT BOG'], 470, 720, size=44, mirror=False, ink=1.0)
    for k in range(6):                                                          # the hill: contour lines
        xs = np.linspace(170, 1270, 90)
        y = 1620 + 95 * k + 40 * np.sin(xs / 210 + k * 0.4) + 12 * fbm1d(90, 20, 3, 10 + k)
        c.contour(np.stack([xs, y], 1), width=1.8, searching=1)
    c.write(['KALKRIESE HILL'], 470, 2000, size=44, mirror=False, ink=1.0)
    xs = np.linspace(230, 1150, 90)                                             # turf wall, red chalk
    wall = np.stack([xs, 1520 + 30 * np.sin(xs / 140) + 8 * fbm1d(90, 10, 2, 3)], 1)
    c.sanguines([wall, wall + [0, 10]], width=5.0)
    c.write(['turf wall'], 230, 1590, size=30, mirror=False, ink=1.0)
    c.dotted([(200, 1260), (700, 1230), (1240, 1270)], width=2.0)               # the narrow pass
    c.write(['the narrow pass'], 860, 1200, size=30, mirror=False, ink=0.9)
    for x, y, t in ((1060, 1340, 'silver coins, 1987'), (720, 1440, 'face mask')):
        c.quill([(x - 20, y - 20), (x + 20, y + 20)], width=3.5); c.quill([(x + 20, y - 20), (x - 20, y + 20)], width=3.5)
        c.write([t], x + 30, y - 24, size=28, mirror=False, ink=1.0)


ROOMS = [(380, 1470, 520, 1560), (640, 1460, 780, 1550)]


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_mosaic(str(out / 'mosaic.png'), str(out / 'mosaic'))
    kit.plan(out, 'pass', 'KALKRIESE', 'near Osnabrueck · the Oberesch · 1987-', ROOMS, seed=37,
             labels=[('trenches', 540, 1640, 28)], scale_text='sketch · not to scale', extra=landscape)


PH = 2560
MOS = ['mosaic/%s.png' % n for n in ('01_eagle', '02_letters', '03_ground')] + ['mosaic.png']
PASS = ['pass/%s.png' % n for n in ('00_sheet', '01_title', '02_grid', '03_rooms_00', '04_rooms_01', '05_notes')] + ['pass.png']

EPISODE = dict(
    chapter='Kalkriese',
    title="Rome Lost 3 Legions. A Metal Detector Found Where. #shorts",
    description=("In AD 9, Germanic warriors led by Arminius destroyed three Roman legions under Varus. Augustus reportedly "
                 "cried: 'Varus, give me back my legions!' Then the battlefield was lost for centuries. In 1987 British army "
                 "officer Major Tony Clunn searched near Kalkriese with a metal detector and found Roman silver coins, then lead "
                 "sling shots. Excavations found a long turf wall, human bones and the iron face mask of a Roman cavalryman.\n\n"
                 "Proven: a Roman army fought and died at Kalkriese.\n"
                 "Debated: whether it is the Varus battle itself or a later fight (Germanicus, AD 15-16).\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['varus', 'teutoburg forest', 'kalkriese', 'arminius', 'roman legions', 'tony clunn', 'metal detecting', 'roman empire',
          'archaeology', 'history shorts'],
    lines=["Three Roman legions simply vanished.",
           "In the year nine, Arminius ambushed the Roman general Varus. Emperor Augustus reportedly cried: Varus, give me back my legions! "
           "Then the battlefield was forgotten.",
           "In nineteen eighty-seven, a British army officer, Tony Clunn, searched near Kalk-reeza with a metal detector and found Roman silver coins.",
           "Then lead sling shots. Then archaeologists found a long turf wall, human bones, and the iron face mask of a Roman cavalryman.",
           "Proven: Romans fought and died here. Debated: is it Varus's battlefield, or a later one?"],
    gaps=[0.15, 0.35, 0.45, 0.40, 0.45],
    display=[(1, 'nine,', 'AD 9,'), (2, 'nineteen', '1987,'), (2, 'eighty-seven,', ''), (2, 'kalk-reeza', 'KALKRIESE')],
    plates=[dict(stages=MOS, show=[(0, 0), (0.6, 1), (1.2, 2), (1.8, 3)]),
            dict(stages=PASS, show=[(0, 0), ('L2-0.2', 1), ('L2+0.4', 2), ('L2@0.45', 3), ('L2@0.6', 4), ('L2:found', 5), ('L4', 6)])],
    camera=[(0, 720, 800, 1250), ('L0.end', 720, 1000, 1700), ('L1+0.3', 720, 1290, 2450), ('L1:augustus-0.3', 720, 1350, 2300),
            ('L1:augustus+0.5', 720, 2000, 1550), ('L1:then-0.3', 720, 1950, 1650), ('L1:then+0.4', 720, 950, 1650), ('L1.end+0.1', 720, 1000, 1800),
            ('L2-0.1', 720, PH + 800, 1900), ('L2:found-0.4', 760, PH + 1150, 2100), ('L2.end', 820, PH + 1320, 1550),
            ('L3:turf-0.3', 700, PH + 1500, 1500), ('L3:mask-0.3', 640, PH + 1460, 1200), ('L3.end', 680, PH + 1450, 1400),
            ('L4+0.2', 720, PH + 1290, 2450), ('END', 720, PH + 1270, 2400)],
    cards=[dict(at='L1:arminius', until='L1:varus-0.1', text='ARMINIUS', size=100, x=540, y=290, rot=-3),
           dict(at='L1:varus', until='L1:emperor-0.1', text='VARUS', font='AlfaSlabOne-400', size=120, ink=(150, 34, 26), x=560, y=300, rot=3),
           dict(at='L1:emperor', until='L1:then-0.2', text='AUGUSTUS', size=90, x=540, y=290, rot=-2),
           dict(at='L2:nineteen', until='L3-0.2', text='1987', font='AlfaSlabOne-400', size=120, x=840, y=250, rot=-3),
           dict(at='L2:tony', until='L2:found-0.2', text='MAJOR TONY CLUNN', size=70, x=520, y=1130, rot=-2),
           dict(at='L2:found', until='L3-0.2', text='SILVER COINS', size=76, x=520, y=1130, rot=2),
           dict(at='L3:lead', until='L3:archaeologists-0.1', text='SLING SHOTS', size=76, x=540, y=330, rot=-3),
           dict(at='L3:turf', until='L3:iron-0.1', text='TURF WALL', size=76, x=540, y=330, rot=3),
           dict(at='L3:iron', until='L4-0.1', text='CAVALRY FACE MASK', size=66, x=540, y=330, rot=-2)],
    stamps=[dict(at='L4:proven', text='BATTLE: PROVEN', size=76, color=(30, 70, 52), x=540, y=640, rot=-6),
            dict(at='L4:debated', text='VARUS: DEBATED', size=76, color=(160, 32, 24), x=540, y=860, rot=5)],
    music=dict(sections=[(0, 'L2-0.3', ['Dm9', 'Esus'], dict(bright=(0.2, 0.35), plucks=0.4)),
                         ('L2-0.3', 'L3', ['Fmaj7', 'Am9'], dict(bright=(0.35, 0.5), pulse=True, plucks=0.3)),
                         ('L3', 'L4', ['Dm9', 'Esus'], dict(bright=(0.45, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
