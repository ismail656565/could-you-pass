"""Myth Dug Up #004 — Thonis-Heracleion. Plates: an Egyptian tomb-style wall painting of the legendary port (a colossal
king before Amun's temple pylon, a ship with a couple arriving on the Nile) (tomb), and a field-notebook section through
the seabed of Aboukir Bay (codex).
Facts (checked): Herodotus (5th c. BC) wrote that Heracles first set foot in Egypt at Heracleion and that Paris and Helen
came there before the Trojan War (franckgoddio.org). The city was found in 2000 by Franck Goddio's team (IEASM, with
Egypt's Supreme Council of Antiquities) in Aboukir Bay, about 6.5 km off today's coast and about 10 m deep
(franckgoddio.org; JSTOR Daily). A stele of Nectanebo I (c. 380 BC) names "Thonis-Heracleion", proving the Egyptian
Thonis and the Greek Heracleion were one city. Finds: colossi of a king, a queen (4.9 m) and the Nile god Hapy (5.4 m)
in red granite, the temple of Amun-Gereb, more than 700 ancient anchors, dozens of wrecks (IEASM now counts about 125).
It sank in stages (collapse of the soft delta sediment, floods, earthquakes) and was underwater by the 8th c. AD.
Left out (uncertain): exact year of the stele find, exact cause/date of the final sinking.
Sources: https://www.franckgoddio.org/projects/sunken-civilizations/heracleion ; https://daily.jstor.org/the-lost-city-of-heracleion"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tomb import TombPainting
from core import spline
import kit

W, H = 1440, 2560


def paint_wall(out):
    tp = TombPainting(W, H, seed=12)
    tp.wall()
    tp.stage('wall')
    tp.grid((150, 330, 1290, 2180), cell=22, base=1330)
    tp.stage('grid')
    # frame
    B = 40
    tp.block_border(60, 60, W - 60, 60 + B, block=34)
    tp.block_border(60, H - 60 - B, W - 60, H - 60, block=34)
    tp.block_border(60, 60 + B, 60 + B, H - 60 - B, block=34)
    tp.block_border(W - 60 - B, 60 + B, W - 60, H - 60 - B, block=34)
    tp.kheker(100, W - 100, 100, 250, w=34)
    # --- upper register: temple pylon + colossus
    BASE1 = 1330
    tp.guide((110, BASE1), (W - 110, BASE1))
    # pylon towers (trapezoids) and gate
    for x0, x1 in ((640, 900), (1040, 1300)):
        tp.part([(x0, BASE1), (x1, BASE1), (x1 - 34, 520), (x0 + 34, 520)], 'white', width=2.6)
        tp.part([(x0 + 30, 560), (x1 - 30, 560), (x1 - 34, 520), (x0 + 34, 520)], 'blue', width=2)
        for k in range(3):
            y = 640 + k * 230
            tp.part([(x0 + 60, y), (x1 - 60, y), (x1 - 60, y + 150), (x0 + 60, y + 150)], 'yellow', width=2)
    tp.part([(900, BASE1), (1040, BASE1), (1040, 760), (900, 760)], 'red', width=2.6)          # gate
    tp.part([(890, 760), (1050, 760), (1050, 712), (890, 712)], 'blue', width=2)
    tp.part([(930, BASE1), (1010, BASE1), (1010, 860), (930, 860)], 'black', width=2)            # door
    for fx in (670, 1270):                                                                         # flagpoles
        tp.rod((fx, BASE1), (fx, 380), 10, 'ochre')
        tp.part([(fx, 390), (fx + (40 if fx < 900 else -40), 410), (fx, 440)], 'red', width=1.6)
    # the colossal king before the pylon (red granite)
    king = tp.figure(400, BASE1, 900, 'stand', facing=1, skin='red', wig='cap', dress='kilt')
    # hieroglyph column on the left
    tp.column(150, 330, 230, 1290, n=30, seed=4)
    tp.column(560, 330, 620, 900, n=14, seed=9)
    # --- middle band
    tp.band(100, W - 100, BASE1 + 10, [('red', 18), ('yellow', 14), ('blue', 18)])
    # --- lower register: the ship on the river
    RY0 = 1900
    tp.river(100, 1960, W - 100, 2290, fish=4, lotus=6, seed=3)
    tp.kheker(100, W - 100, 2300, H - 100, w=34)
    hull = spline([(180, 1700), (250, 1860), (430, 1930), (720, 1950), (1010, 1930), (1190, 1860), (1270, 1690),
                   (1240, 1700), (1150, 1830), (980, 1870), (720, 1880), (460, 1870), (290, 1830), (210, 1710)], 6)
    tp.part(hull, 'ochre', width=3.0)
    tp.part([(250, 1855), (1190, 1855), (1150, 1880), (290, 1880)], 'red', width=1.6, z=tp._z)
    tp.rod((720, 1880), (720, 1420), 16, 'brown')
    tp.part([(500, 1450), (940, 1450), (930, 1720), (510, 1720)], 'linen', width=2.4)            # sail
    tp.rod((480, 1450), (960, 1450), 10, 'brown'); tp.rod((490, 1720), (950, 1720), 10, 'brown')
    man = tp.figure(390, 1868, 300, 'stand', facing=1, wig='short', dress='kilt')
    wom = tp.figure(300, 1868, 290, 'stand', facing=1, sex='f', skin='skin_f', wig='woman', dress='dress')
    rower = tp.figure(1100, 1868, 260, 'hold', facing=-1, wig='cap', dress='kilt')
    tp.rod((1050, 1700), (1250, 2000), 9, 'brown')
    tp.stage('declared')
    tp.sketch(); tp.stage('sketch')
    tp.ground('#d8bd84'); tp.stage('ground')
    tp.colour(); tp.stage('colour')
    tp.ink(); tp.colour(layer='text'); tp.ink(layer='text'); tp.stage('ink')
    tp.age(losses=[(1230, 2350, 70, 50)], cracks=7); tp.stage('aged')
    tp.save(str(Path(out) / 'wall.png'), stages_dir=str(Path(out) / 'wall'))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_wall(out)
    kit.section(out, 'seabed', 'ABOUKIR BAY', 'section through the seabed · 2000', LAYERS, seed=24, hump=0,
                note=('colossi · temple · anchors', 2), highlight=(2,), extra=finds)


def finds(c, bounds, xs):
    from codex import Codex
    y0 = float(bounds[0].mean())
    for k in range(3):                                   # waves on the surface
        xx = np.linspace(130, 1110, 90)
        c.quill(np.stack([xx, y0 - 26 - 22 * k + 9 * np.sin(xx / 38 + k)], 1), width=1.6, ink=0.75)
    # a boat at the surface and the divers' line down to the city
    c.contour([(560, y0 - 90), (800, y0 - 90), (760, y0 - 50), (600, y0 - 50)], width=2.4, closed=True)
    c.quill([(680, y0 - 90), (680, y0 - 200)], width=2.0)
    c.dotted([(680, y0 - 50), (690, 900), (670, 1300), (680, 1560)], width=1.6)
    c.write(["Goddio's divers", '2000'], 720, 760, size=30, mirror=False, ink=0.95)
    top, bot = float(bounds[2].mean()), float(bounds[3].mean())
    yb = bot - 40
    # the colossus, toppled on the seabed of the old city
    hx, hy, L = 230, yb - 60, 420
    c.contour([(hx, hy - 40), (hx + L, hy - 50), (hx + L, hy + 30), (hx, hy + 40)], width=3.0, closed=True)
    c.contour(Codex.arc(hx - 40, hy, 52, 0, 360), width=3.0, closed=True)
    c.quill([(hx + 150, hy - 45), (hx + 150, hy + 36)], width=1.8)
    c.quill([(hx + 260, hy - 47), (hx + 260, hy + 33)], width=1.8)
    c.hatch(c.poly_mask([(hx, hy - 40), (hx + L, hy - 50), (hx + L, hy + 30), (hx, hy + 40)]), shade=0.7, angle=20, spacing=5)
    c.write(['colossus, 5 m'], hx + 30, hy - 80, size=28, mirror=False, ink=1.0)
    # temple columns standing in the mud
    for cx in (820, 930, 1040):
        c.contour([(cx - 24, yb), (cx - 24, top + 70), (cx + 24, top + 70), (cx + 24, yb)], width=2.6)
    c.contour([(780, top + 70), (1080, top + 70), (1080, top + 40), (780, top + 40)], width=2.6, closed=True)
    c.write(['temple of Amun'], 800, top + 22, size=26, mirror=False, ink=0.95)
    # stone anchors
    for ax in (620, 690):
        ay = yb - 20
        c.contour([(ax - 22, ay + 30), (ax + 22, ay + 30), (ax + 14, ay - 34), (ax - 14, ay - 34)], width=2.2, closed=True)
        c.quill(Codex.arc(ax, ay - 16, 6, 0, 360), width=1.6)
    c.write(['anchors'], 595, yb - 80, size=24, mirror=False, ink=0.9)
    c.sanguines([Codex.arc(hx + 160, hy, 300, 0, 350, ry=120)], width=3.0)


LAYERS = [('THE SEA', 'about 10 m of water'), ('SAND & SILT', 'since the 8th c. AD'),
          ('THE CITY', 'Thonis-Heracleion'), ('DELTA MUD', 'soft Nile sediment')]
PH = 2560
WALL = ['wall/%s.png' % n for n in ('03_sketch', '04_ground', '05_colour', '06_ink', '07_aged')] + ['wall.png']
SEC = ['seabed/%s.png' % n for n in ['00_sheet', '01_title', '02_surface'] +
       ['%02d_layer_%02d' % (3 + i, i) for i in range(len(LAYERS))] + ['%02d_notes' % (3 + len(LAYERS))]] + ['seabed.png']

EPISODE = dict(
    chapter='Thonis-Heracleion',
    title="Egypt's Legendary Port Sank Into the Sea. Divers Found It. #shorts",
    description=("Herodotus wrote of a great port at the mouth of the Nile, where Heracles first set foot in Egypt and where "
                 "Paris and Helen of Troy came ashore. Then it vanished. In 2000, Franck Goddio's team found it in Aboukir Bay, "
                 "about 6.5 km (4 miles) off the coast and about 10 m (30 ft) down: colossal granite statues, a temple of Amun, more than 700 "
                 "anchors and dozens of shipwrecks.\n\n"
                 "Proven: Thonis-Heracleion was a real port city, now under the sea.\n"
                 "Debated: whether Helen of Troy (or Heracles) has anything to do with it — that part is legend.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['thonis-heracleion', 'heracleion', 'sunken city', 'franck goddio', 'ancient egypt', 'herodotus', 'underwater archaeology',
          'archaeology', 'lost city', 'history shorts'],
    lines=["This city sank beneath the sea.",
           "The Greek historian Herodotus wrote of a great port at the mouth of the Nile, where Heracles first set foot in Egypt, "
           "and where Paris and Helen of Troy came ashore. Then it vanished.",
           "In two thousand, divers led by Frank Goddio found the city, four miles offshore, about thirty feet down.",
           "Granite statues over five metres tall. A temple of Amun. More than seven hundred anchors, and dozens of shipwrecks.",
           "Proven: the sunken port was real. Debated: whether Helen of Troy was ever here."],
    gaps=[0.15, 0.35, 0.45, 0.40, 0.45],
    display=[(2, 'two', '2000,'), (2, 'thousand,', ''), (2, 'frank', 'FRANCK'), (2, 'four', '4'), (2, 'thirty', '30'),
             (3, 'five', '5'), (3, 'seven', '700'), (3, 'hundred', '')],
    plates=[dict(stages=WALL, show=[(0, 2), (0.6, 3), (1.3, 4), (2.0, 5)]),
            dict(stages=SEC, show=[(0, 0), ('L2-0.2', 1), ('L2+0.4', 2)] +
                 [('L2@%.2f' % (0.4 + 0.12 * i), 3 + i) for i in range(len(LAYERS))] + [('L3-0.1', 7), ('L4', 8)])],
    camera=[(0, 720, 1080, 1900), ('L0.end', 720, 1150, 2100), ('L1+0.4', 720, 1290, 2450), ('L1:paris-0.6', 720, 1290, 2380),
            ('L1:paris+0.4', 560, 1700, 1250), ('L1:vanished-0.3', 600, 1720, 1350), ('L1.end+0.2', 720, 1300, 2450),
            ('L2-0.1', 740, PH + 900, 2150), ('L2:four-0.2', 740, PH + 1000, 2250), ('L2.end', 740, PH + 1400, 2350),
            ('L3+0.2', 700, PH + 1650, 1700), ('L3.end-0.3', 720, PH + 1640, 1800), ('L4+0.2', 720, PH + 1290, 2450),
            ('END', 720, PH + 1270, 2400)],
    cards=[dict(at='L1:herodotus', until='L1:heracles-0.2', text='HERODOTUS', size=96, x=540, y=290, rot=-3),
           dict(at='L1:heracles', until='L1:paris-0.3', text='HERACLEION', font='AlfaSlabOne-400', size=100, ink=(150, 34, 26), x=560, y=300, rot=3),
           dict(at='L1:helen', until='L1:then', text='HELEN OF TROY?', size=70, x=560, y=1180, rot=-2),
           dict(at='L2:two', until='L3-0.2', text='2000', font='AlfaSlabOne-400', size=120, x=830, y=260, rot=-3),
           dict(at='L2:frank', until='L2:four-0.1', text='FRANCK GODDIO', size=76, x=500, y=1120, rot=2),
           dict(at='L2:four', until='L3-0.2', text='4 MILES OFFSHORE', size=66, x=470, y=1120, rot=-2),
           dict(at='L3:granite', until='L3.end', text='COLOSSI 5 M+', size=64, x=330, y=330, rot=-4),
           dict(at='L3:temple', until='L3.end', text='TEMPLE OF AMUN', size=64, x=700, y=440, rot=3),
           dict(at='L3:more', until='L3.end', text='700+ ANCHORS', size=64, x=380, y=1140, rot=-2),
           dict(at='L3:dozens', until='L3.end', text='SHIPWRECKS', size=64, x=740, y=1240, rot=2)],
    stamps=[dict(at='L4:proven', text='PORT: PROVEN', color=(30, 70, 52), x=540, y=660, rot=-6),
            dict(at='L4:debated', text='HELEN: DEBATED', size=76, color=(160, 32, 24), x=540, y=880, rot=5)],
    music=dict(sections=[(0, 'L2-0.3', ['Am9', 'Fmaj7'], dict(bright=(0.2, 0.35), plucks=0.4)),
                         ('L2-0.3', 'L3', ['Dm9', 'Esus'], dict(bright=(0.35, 0.5), pulse=True, plucks=0.3)),
                         ('L3', 'L4', ['Am9', 'Esus'], dict(bright=(0.45, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Fmaj7', 'Am9'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
