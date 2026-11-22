"""Myth Dug Up #003 — Vinland. Plates: a two-block linocut of a Norse ship under the moon (linocut), and a coastal chart
of Newfoundland's northern tip with the find (codex field notebook). Facts: the Saga of the Greenlanders and Erik the
Red's Saga tell of Leif Erikson reaching 'Vinland'; Helge Ingstad and Anne Stine Ingstad identified L'Anse aux Meadows
in 1960 (excavated 1961-68): Norse-style turf buildings, iron rivets, a soapstone spindle whorl. Kuitems et al.,
Nature 2021: wood cut with metal tools dated to AD 1021 (cosmic-ray event of 993). Where 'Vinland' itself was is debated."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from linocut import Linocut
from core import spline
import kit

LINO = ['ship/%s.png' % n for n in ('00_inked', '01_sky', '02_sea', '03_ship', '04_colour')] + ['ship.png']


def paint_ship(out):
    W, H = 1440, 2560
    BX0, BY0, BX1, BY1 = 90, 120, 1350, 2300
    L = Linocut(W, H, block=(BX0, BY0, BX1, BY1), seed=7)
    red = L.colour_block('#b8432f', offset=(4, -3))
    KEY = [L.key]
    L.stage('inked', blocks=KEY)
    HZ = 1520
    MX, MY, MR = 1010, 560, 92
    sky = [(BX0 - 10, BY0 - 10), (BX1 + 10, BY0 - 10), (BX1 + 10, HZ), (BX0 - 10, HZ)]
    L.clear(L.disc(MX, MY, MR), chatter=0.2, angle=-30)
    md = lambda x, y: np.hypot(x - MX, y - MY)
    L.flow(sky, lambda x, y: 178 + 4 * np.sin(x / 260 + y / 110), n=260, length=(40, 300), width=(1.6, 4.6), step=3.0,
           density=lambda x, y: float(np.clip((md(x, y) - 200) / 80, 0, 1)) * (0.35 + 0.65 * float(y < 1100)))
    L.moon(MX, MY, MR, rings=(1.42, 1.72, 2.05, 2.42))
    L.stage('sky', blocks=KEY)
    sea = [(BX0 - 10, HZ), (BX1 + 10, HZ), (BX1 + 10, BY1 + 10), (BX0 - 10, BY1 + 10)]
    L.flow(sea, lambda x, y: 4 * np.sin(x / 70 + y / 40) + 2 * np.sin(x / 23), n=520, length=(30, 180), width=(2.0, 6.0), step=3.0,
           density=lambda x, y: float(np.clip(0.25 + 0.75 * np.exp(-((x - MX) / 160) ** 2), 0, 1)) * float(np.clip((y - HZ) / 60, 0, 1)))
    refl = L.poly(spline([(170, HZ + 60), (720, HZ + 10), (1270, HZ + 60), (1100, HZ + 300), (720, HZ + 360), (340, HZ + 300), (170, HZ + 60)], 8))
    L.clear(refl, chatter=0.5, angle=0)
    L.hatch(refl, angle=0, spacing=10, width=3.0, dash=(30, 180), gap=(10, 50), cut=False,
            density=lambda x, y: float(np.clip(0.2 + ((x - 720) / 560) ** 2 * 0.8 + ((y - HZ - 150) / 220) ** 2 * 0.5, 0, 0.92)))
    L.stage('sea', blocks=KEY)
    # the ship: hull, stems, dragon head, mast, sail, shields
    hull = [(300, 1470), (360, 1540), (500, 1590), (720, 1610), (940, 1590), (1080, 1540), (1150, 1470), (1180, 1380),
            (1205, 1300), (1232, 1262), (1262, 1258), (1272, 1282), (1246, 1296), (1222, 1340), (1196, 1452), (1150, 1520),
            (1000, 1505), (720, 1500), (440, 1505), (320, 1520), (270, 1440), (250, 1340), (262, 1300), (280, 1330), (282, 1420)]
    sail = [(470, 880), (970, 880), (1000, 1380), (440, 1380)]
    L.clear(L.poly(sail), chatter=0.2, angle=90)
    for k in range(6):
        if k % 2 == 0:
            x0 = 440 + k * 93.3; x1 = x0 + 93.3
            L.leave(L.poly([(x0 + 5 + 30 * (1 - (k / 6)), 880), (x1 + 5 + 30 * (1 - ((k + 1) / 6)) - 25, 880), (x1, 1380), (x0, 1380)]), on=red)
    L.outline(L.poly(sail), 4.0)
    L.leave(L.poly([(712, 760), (728, 760), (730, 1520), (710, 1520)]))
    L.leave(L.poly([(430, 872), (1010, 872), (1010, 888), (430, 888)]))
    hm = L.poly(spline(hull + [hull[0]], 4))
    L.outline(hm, 7.0)
    L.leave(hm)
    for k in range(9):
        cx = 400 + k * 80
        L.clear(L.disc(cx, 1490, 26), chatter=0.1)
        L.leave(L.disc(cx, 1490, 9))
        if k % 2: L.leave(L.disc(cx, 1490, 24), on=red)
    L.stage('ship', blocks=KEY)
    L.stage('colour')
    L.sign(edition='1/30', title='Vinland', name='')
    L.save(str(Path(out) / 'ship.png'), stages_dir=str(Path(out) / 'ship'))


CHART = None


def paint(work):
    global CHART
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_ship(out)
    CHART = kit.chart(out, 'chart', 'VINLAND?', 'northern tip of Newfoundland · 1960', seed=43, land='right', coast_x=700, amp=150,
                      places=[('St. Anthony', 980, 1900), ('NEWFOUNDLAND', 860, 1500)],
                      find=(820, 640, "L'Anse aux Meadows"), islands=[(430, 700, 50), (360, 1050, 34)])


PH = 2560
CH = ['chart/%s.png' % n for n in ('00_sheet', '01_title', '02_coast', '03_land', '04_sea', '05_places', '06_find')] + ['chart.png']

EPISODE = dict(
    chapter='Vinland',
    title="The Vikings Reached America First — and We Can Prove It #shorts",
    description=("For centuries, Vinland was just a saga: Leif Erikson sailing west from Greenland. In 1960 Helge Ingstad and "
                 "Anne Stine Ingstad found Norse buildings at L'Anse aux Meadows in Newfoundland. In 2021, scientists dated "
                 "wood cut with metal tools there to exactly AD 1021.\n\n"
                 "Proven: Norse people were in North America around AD 1021.\n"
                 "Debated: where the 'Vinland' of the sagas really was.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['vikings', 'vinland', "l'anse aux meadows", 'leif erikson', 'norse', 'newfoundland', 'archaeology', 'history shorts'],
    lines=["Almost five hundred years before Columbus, Vikings sailed to America. At least, that's what the sagas said.",
           "Two Icelandic sagas tell of Leif Erikson finding a land far to the west. They called it Vinland. For centuries, it sounded like a legend.",
           "Then, in nineteen sixty, Helge and Anne Stine Ingstad found a site on the northern tip of Newfoundland. Lahnss oh Meadows.",
           "Under the grass: Norse buildings. Iron rivets. A spindle whorl. A real Viking camp.",
           "And in twenty twenty-one, scientists dated the wood cuts to one year: ten twenty-one. Proven: Vikings were here. Debated: where Vinland really was."],
    gaps=[0.15, 0.35, 0.45, 0.40, 0.45],
    display=[(0, 'five', '500'), (0, 'hundred', ''), (2, 'nineteen', '1960,'), (2, 'sixty,', ''), (2, 'lahnss', "L'ANSE"),
             (2, 'oh', 'AUX'), (4, 'twenty', '2021,'), (4, 'twenty-one,', ''), (4, 'ten', '1021.'), (4, 'twenty-one.', '')],
    plates=[dict(stages=LINO, show=[(0, 3), (0.8, 4), (1.6, 5)]),
            dict(stages=CH, show=[(0, 0), ('L2-0.2', 1), ('L2+0.5', 2), ('L2@0.3', 3), ('L2@0.5', 4), ('L2@0.7', 5), ('L2.end-0.6', 6), ('L4', 7)])],
    camera=[(0, 720, 1180, 1150), ('L0.end', 740, 1250, 1500), ('L1', 720, 1300, 2450), ('L2-0.3', 720, 1280, 2350),
            ('L2+0.5', 530, PH + 520, 1450), ('L2.end-0.4', 760, PH + 760, 1500), ('L3', 800, PH + 700, 1100),
            ('L3.end', 790, PH + 720, 1000), ('L4+0.3', 720, PH + 1250, 2450), ('END', 720, PH + 1240, 2400)],
    cards=[dict(at='L1:leif', until='L2-0.2', text='LEIF ERIKSON', size=86, x=540, y=300, rot=-3),
           dict(at='L1:vinland', until='L2-0.2', text='VINLAND', font='AlfaSlabOne-400', size=110, ink=(150, 34, 26), x=600, y=1080, rot=3),
           dict(at='L2:nineteen', until='L3-0.2', text='1960', font='AlfaSlabOne-400', size=120, x=840, y=250, rot=-3),
           dict(at='L3:norse', until='L3.end', text='TURF HOUSES', size=64, x=330, y=1120, rot=-4),
           dict(at='L3:iron', until='L3.end', text='IRON RIVETS', size=64, x=740, y=1210, rot=3),
           dict(at='L3:spindle', until='L3.end', text='SPINDLE WHORL', size=64, x=420, y=1300, rot=-2),
           dict(at='L4:ten-0.1', until='L4:proven-0.1', text='AD 1021', font='AlfaSlabOne-400', size=130, ink=(150, 34, 26), x=540, y=760, rot=-3)],
    stamps=[dict(at='L4:proven', text='VIKINGS: PROVEN', size=74, color=(30, 70, 52), x=540, y=640, rot=-6),
            dict(at='L4:debated', text='VINLAND: DEBATED', size=70, color=(160, 32, 24), x=540, y=860, rot=5)],
    music=dict(sections=[(0, 'L2-0.3', ['Dm9', 'Fmaj7'], dict(bright=(0.2, 0.35), plucks=0.4)),
                         ('L2-0.3', 'L3', ['Am9', 'Esus'], dict(bright=(0.35, 0.5), pulse=True, plucks=0.3)),
                         ('L3', 'L4', ['Dm9', 'Esus'], dict(bright=(0.45, 0.6), pulse=True, ticks=True)),
                         ('L4', 'END', ['Fmaj7', 'Am9'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
