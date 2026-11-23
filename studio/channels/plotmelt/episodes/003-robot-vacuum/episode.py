"""PlotMelt #003 — my robot vacuum avoids one spot (original fiction, first-person title experiment). Plates: the living
room with the rug, then the rug lifted; hand-inked cartoon with a boiling line (claude-drawing-skill: cartoon)."""
from pathlib import Path
import numpy as np
from cartoon import Cartoon, WHITE, RED, YELLOW

E, R, P = Cartoon.ellipse_pts, Cartoon.rrect_pts, Cartoon.place
SKIN, SHIRT, SHIRT_D, HAIR = '#f3c9a0', '#9b6dd6', '#7a51b0', '#c0582a'
VAC, VAC_D = '#7d8794', '#5b636e'
RUG, RUG_D = '#e94e77', '#c03a5e'
FUR, FUR_D = '#e8b27a', '#c48a55'
PH = 2560


def me(c, x, y, mood):
    c.shape(E(x, y + 230, 130, 170), SHIRT, shade=(SHIRT_D, 12, 12))
    c.shape(E(x, y, 112, 106), SKIN, shade=('#dba57a', 10, 10))
    c.shape(E(x, y - 70, 118, 62, a0=180, a1=360), HAIR)
    c.face(x, y + 15, 130, mood)


def vacuum(c, x, y, s=1.0, mood='happy'):
    c.shape(E(x, y + 18 * s, 170 * s, 58 * s), VAC_D)
    c.shape(E(x, y, 170 * s, 58 * s), VAC, shade=(VAC_D, 6, 6))
    c.shape(E(x, y - 6 * s, 70 * s, 22 * s), '#aeb6c0')
    c.face(x, y + 22 * s, 70 * s, mood, blush=False)


def room(c):
    c.fill(np.array([(0, 0), (1440, 0), (1440, 1500), (0, 1500)], np.float32), '#cde7d6', knock=False)
    c.fill(np.array([(0, 1500), (1440, 1500), (1440, 2560), (0, 2560)], np.float32), '#c99b6b', knock=False)
    c.line([(0, 1500), (1440, 1500)], 6, taper=(0, 0))
    for y in range(1640, 2560, 180):
        c.line([(0, y), (1440, y)], 3, taper=(0, 0))
    c.shape(R(920, 380, 1300, 760, 18), '#bfe3f2', width=7)
    c.line([(1110, 380), (1110, 760)], 6, taper=(0, 0))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    c = Cartoon(W, H, seed=31, boil=2.0)
    c.paper(); room(c)
    c.shape(P(R(-330, -170, 330, 170, 24), 1080, 1830, 1.0, 3), RUG, shade=(RUG_D, 10, 10))
    for k in range(3):
        c.line([(810, 1740 + k * 90), (1350, 1755 + k * 90)], 4, taper=(0, 0))
    vacuum(c, 400, 1900, 1.3, 'wow')
    c.speed_lines((560, 1820), (640, 1960), angle=180, n=4)
    c.letter('BEEP!', 280, 1680, 100, fill=YELLOW, rot=-8)
    me(c, 520, 1060, 'wow')
    c.arm((610, 1240), (760, 1450), width=6, hand=22)
    c.stage('corner')
    c.letter('RESET?', 900, 1150, 90, fill=YELLOW, anchor='m', rot=6)
    c.letter('BEEP!', 260, 2160, 90, fill=YELLOW, rot=6)
    c.stage('tries')
    c.save(str(out / 'room.png'), stages_dir=str(out / 'room'))
    # ---------------- the rug lifted
    n = Cartoon(W, H, seed=32, boil=2.0)
    n.paper(); room(n)
    n.shape(P(R(-120, -330, 120, 330, 24), 800, 1500, 1.0, -18), RUG, shade=(RUG_D, 10, 10))   # the rug, lifted up
    me(n, 400, 1000, 'wow')
    n.arm((470, 1180), (700, 1200), width=6, hand=22)
    n.stage('lift')
    for x, y, r in ((1000, 1800, 85), (1150, 1780, 100), (1290, 1810, 85), (1080, 1660, 75), (1220, 1650, 75), (1150, 1550, 65)):
        n.puff(x, y, r, colour='#d6d6dc', shadow='#b5b5c0')
    n.shape(R(1100, 1760, 1200, 1870, 40), '#3a3040')                  # the door of the dust house
    n.shape(E(1150, 2010, 85, 58), FUR, shade=(FUR_D, 6, 6))
    n.shape(E(1150, 1945, 64, 54), FUR, shade=(FUR_D, 6, 6))
    for sx in (-1, 1):
        n.shape(E(1150 + sx * 45, 1900, 17, 17), FUR_D)
    n.face(1150, 1950, 64, 'happy')
    n.note('NIBBLES', 1150, 2160, 60, anchor='m')
    n.stage('hamster')
    vacuum(n, 560, 2100, 1.2, 'happy')
    n.crumbs(560, 2030, n=7, spread=(90, 20))
    n.crumbs(960, 2040, n=8, spread=(80, 30))
    n.sparkle(760, 1980, 26)
    n.stage('crumbs')
    n.save(str(out / 'rug.png'), stages_dir=str(out / 'rug'))


D = ['room/%s.png' % s for s in ('00_corner', '01_tries')]
N = ['rug/%s.png' % s for s in ('00_lift', '01_hamster', '02_crumbs')]

EPISODE = dict(
    chapter='My Robot Vacuum Avoids One Spot',
    title="My Robot Vacuum Avoids One Spot. I Finally Checked. #shorts",
    description="It cleaned everything except one corner. So I lifted the rug.\n\nAn original animated story, drawn with code. Narration is synthetic.",
    tags=['animated story', 'funny story', 'plot twist', 'robot vacuum', 'hamster', 'cartoon', 'shorts'],
    voice='am_puck',
    lines=["My robot vacuum refuses to touch one corner.",
           "Every day it cleans the whole room, stops at the rug, and turns around.",
           "I reset it. I moved the furniture. It still beeps and backs away.",
           "So last night, I lifted the rug.",
           "Under it: Nibbles, my hamster who escaped in March, living in a tiny house made of dust. And my vacuum? It's been bringing him crumbs."],
    gaps=[0.15, 0.35, 0.35, 0.4, 0.45],
    plates=[dict(stages=D, show=[(0, 0), ('L2', 1)]),
            dict(stages=N, show=[(0, 0), ('L4:nibbles', 1), ('L4:and', 2)])],
    camera=[(0, 720, 1400, 2100), ('L1', 760, 1600, 1800), ('L2', 720, 1700, 1700), ('L2.end', 720, 1700, 1700),
            ('L3', 720, PH + 1300, 2000), ('L4:nibbles', 1000, PH + 1800, 1300), ('L4:and', 720, PH + 1700, 1700),
            ('END', 720, PH + 1600, 1900)],
    cards=[dict(at=0, until='L1-0.2', text='NOT THAT CORNER.', font='AlfaSlabOne-400', size=90, ink=(150, 34, 26), x=540, y=300, rot=-3)],
    caption=dict(y=0.82),
    stamps=[dict(at='L4:crumbs', text='PLOT MELTED', size=80, color=(200, 40, 30), x=540, y=1720, rot=-6)],
    music=dict(sections=[(0, 'L2', ['Cmaj9', 'G6'], dict(bright=(0.5, 0.6), plucks=0.8, pulse=True)),
                         ('L2', 'L4', ['Am9', 'Esus'], dict(bright=(0.2, 0.3), ticks=True, plucks=0.3)),
                         ('L4', 'END', ['Fmaj7', 'Cmaj9'], dict(bright=(0.6, 0.5), gain=(1, 0.0), plucks=0.8))],
               events=[('L3:lifted', 'impact', dict(level=0.5))]),
)
