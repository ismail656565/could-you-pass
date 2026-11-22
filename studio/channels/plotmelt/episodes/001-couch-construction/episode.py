"""PlotMelt #001 — Gary's $50 couch (original fiction). Plates: the living room by day and by night, drawn as a
hand-inked cartoon with a boiling line (claude-drawing-skill: cartoon)."""
from pathlib import Path
import numpy as np
from cartoon import Cartoon, WHITE, RED, YELLOW

E, R, P = Cartoon.ellipse_pts, Cartoon.rrect_pts, Cartoon.place
SOFA, SOFA_D, CUSH = '#4f86c6', '#3a6aa3', '#6aa0dc'
SKIN, SHIRT, SHIRT_D = '#f3c9a0', '#f08a3c', '#c96a26'
FUR, FUR_D, HAT, HAT_D = '#c99060', '#a36d40', '#ffd23c', '#e0a91c'


def couch(c):
    c.shape(R(310, 1180, 1130, 1470, 70), SOFA, shade=(SOFA_D, 14, 14))
    c.shape(R(270, 1430, 1170, 1600, 46), SOFA, shade=(SOFA_D, 10, 14))
    for x0 in (300, 720):
        c.shape(R(x0, 1395, x0 + 420, 1470, 34), CUSH, shade=(SOFA, 8, 10))
    for x0 in (220, 1100):
        c.shape(R(x0, 1310, x0 + 120, 1620, 50), SOFA, shade=(SOFA_D, 12, 12))
    for x in (290, 1150):
        c.shape(R(x - 18, 1600, x + 18, 1680, 8), '#6b4a2e')


def gary(c, mood='happy', y=0, x=560):
    c.shape(E(x, 1290 + y, 120, 150), SHIRT, shade=(SHIRT_D, 12, 12))
    c.shape(E(x, 1080 + y, 105, 100), SKIN, shade=('#dba57a', 10, 10))
    c.shape(E(x, 1000 + y, 100, 50, a0=180, a1=360), '#5a3b26')
    c.face(x, 1095 + y, 120, mood)


def room(c, night):
    wall = '#2a2f55' if night else '#f6e7c8'
    c.fill(np.array([(0, 0), (1440, 0), (1440, 1700), (0, 1700)], np.float32), wall, knock=False)
    c.fill(np.array([(0, 1700), (1440, 1700), (1440, 2560), (0, 2560)], np.float32), '#3d3552' if night else '#d9b48a', knock=False)
    c.line([(0, 1700), (1440, 1700)], 6, taper=(0, 0))
    c.shape(R(860, 380, 1260, 760, 18), '#1b1e3a' if night else '#bfe3f2', width=7)
    c.line([(1060, 380), (1060, 760)], 6, taper=(0, 0)); c.line([(860, 570), (1260, 570)], 6, taper=(0, 0))
    if night:
        c.shape(E(1160, 470, 40, 40), '#f6efc6', width=5)


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    # ---------------- day
    c = Cartoon(W, H, seed=12, boil=2.0)
    c.paper()
    room(c, False)
    c.stage('room')
    couch(c)
    tag = P([(-90, -55), (90, -55), (90, 55), (-90, 55)], 1000, 1240, 1.0, -12)
    c.shape(tag, WHITE)
    c.line([(1000 - 70, 1185), (980, 1120)], 3.5)
    c.letter('$50', 1000, 1268, 82, fill=YELLOW, anchor='m', rot=-12)
    c.stage('couch')
    gary(c, 'happy')
    c.sparkle(840, 1060, 30)
    c.note('GARY', 560, 900, 70, anchor='m')
    c.stage('gary')
    c.save(str(out / 'day.png'), stages_dir=str(out / 'day'))
    # ---------------- night
    n = Cartoon(W, H, seed=13, boil=2.0)
    n.paper()
    room(n, True)
    couch(n)
    n.stage('night')
    n.letter('SKRTCH', 300, 1120, 96, fill=YELLOW, rot=-8)
    n.letter('psst...', 830, 1010, 70, fill='#bfe3f2', depth_colour='#3a6aa3', rot=6)
    n.stage('noises')
    n.shape(R(120, 760, 760, 960, 60), WHITE)
    n.shape(np.array([(560, 950), (640, 1070), (660, 955)], np.float32), WHITE)
    n.note('excuse me.', 440, 890, 80, anchor='m')
    n.letter('3:00 AM', 1060, 300, 70, fill='#f6efc6', depth_colour='#1b1e3a', anchor='m')
    n.stage('voice')
    # the cushion lifted, the hamster in his hard hat
    n.shape(R(720, 1150, 1140, 1230, 34), CUSH, shade=(SOFA, 8, 10))
    n.shape(E(930, 1420, 95, 70), FUR, shade=(FUR_D, 8, 8))
    n.shape(E(930, 1340, 70, 62), FUR, shade=(FUR_D, 8, 8))
    for sx in (-1, 1):
        n.shape(E(930 + sx * 52, 1288, 20, 20), FUR_D)
    n.shape(E(930, 1300, 78, 38, a0=180, a1=360), HAT, shade=(HAT_D, 6, 6))
    n.shape(R(842, 1294, 1018, 1312, 6), HAT)
    n.face(930, 1350, 70, 'wow')
    n.arm((880, 1420), (820, 1360), width=5, hand=14)
    n.shape(R(1020, 1440, 1110, 1460, 4), '#8a8a8a')
    gary(n, 'wow', y=280, x=420)
    n.arm((320, 1560), (250, 1460), width=6, hand=20)
    n.stage('hamster')
    n.shape(R(380, 560, 1380, 830, 60), WHITE)
    n.shape(np.array([(900, 820), (960, 980), (1000, 825)], np.float32), WHITE)
    n.note("you're sitting on", 880, 670, 66, anchor='m')
    n.note('my construction site.', 880, 770, 66, anchor='m')
    n.stage('punchline')
    n.save(str(out / 'night.png'), stages_dir=str(out / 'night'))


PH = 2560
D = ['day/%s.png' % s for s in ('00_room', '01_couch', '02_gary')] + ['day.png']
N = ['night/%s.png' % s for s in ('00_night', '01_noises', '02_voice', '03_hamster', '04_punchline')] + ['night.png']

EPISODE = dict(
    chapter="Gary's $50 Couch",
    title="He Bought a $50 Couch. Something Was Living In It. #shorts",
    description="Gary found a bargain. The couch had other plans.\n\nAn original animated story, drawn with code. Narration is synthetic.",
    tags=['animated story', 'funny story', 'plot twist', 'cartoon', 'shorts'],
    voice='am_puck',
    lines=["Gary bought a couch for fifty dollars.",
           "That night, it started making noises.",
           "Scratching. Whispering. Then, at three a.m., a tiny voice said: excuse me.",
           "Gary lifted the cushion, ready for anything.",
           "Inside was a hamster, wearing a tiny hard hat. Sir, it said. You're sitting on my construction site."],
    gaps=[0.15, 0.35, 0.35, 0.4, 0.45],
    display=[(0, 'fifty', '$50.'), (0, 'dollars.', ''), (2, 'three', '3'), (2, 'a.m.,', 'AM,')],
    plates=[dict(stages=D, show=[(0, 1), (0.5, 2), (1.2, 3)]),
            dict(stages=N, show=[(0, 0), ('L2', 1), ('L2:tiny', 2), ('L4', 3), ('L4:sir', 4), ('L4.end', 5)])],
    camera=[(0, 760, 1230, 1300), ('L0.end', 720, 1250, 1650), ('L1-0.2', 720, 1300, 1700),
            ('L1+0.6', 720, PH + 1250, 1900), ('L2:tiny', 600, PH + 1000, 1500), ('L3', 900, PH + 1300, 1300),
            ('L4', 700, PH + 1450, 1300), ('L4:sir', 760, PH + 1050, 1650), ('END', 720, PH + 1080, 1750)],
    caption=dict(y=0.82),
    stamps=[dict(at='L4:construction', text='PLOT MELTED', size=80, color=(200, 40, 30), x=540, y=1800, rot=-6)],
    music=dict(sections=[(0, 'L1', ['Cmaj9', 'G6'], dict(bright=(0.5, 0.6), plucks=0.8, pulse=True)),
                         ('L1', 'L4', ['Am9', 'Esus'], dict(bright=(0.2, 0.3), ticks=True, plucks=0.3)),
                         ('L4', 'END', ['Fmaj7', 'Cmaj9'], dict(bright=(0.6, 0.5), gain=(1, 0.0), plucks=0.8))],
               events=[('L4', 'impact', dict(level=0.5))]),
)
