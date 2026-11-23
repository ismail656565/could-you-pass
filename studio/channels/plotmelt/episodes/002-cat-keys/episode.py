"""PlotMelt #002 — the cat that left keys (original fiction). Plates: Leo's doorstep by day, his living room by
evening, hand-inked cartoon with a boiling line (claude-drawing-skill: cartoon)."""
from pathlib import Path
import numpy as np
from cartoon import Cartoon, WHITE, RED, YELLOW

E, R, P = Cartoon.ellipse_pts, Cartoon.rrect_pts, Cartoon.place
SKIN, SHIRT, SHIRT_D, HAIR = '#f3c9a0', '#4bb37a', '#358a5b', '#3b2a20'
CAT, CAT_D = '#f29a3c', '#c9742a'
KEY, KEY_D = '#ffd23c', '#d9a51c'
PH = 2560


def leo(c, x, y, mood):
    c.shape(E(x, y + 230, 130, 170), SHIRT, shade=(SHIRT_D, 12, 12))
    c.shape(E(x, y, 112, 106), SKIN, shade=('#dba57a', 10, 10))
    c.shape(E(x, y - 80, 108, 52, a0=180, a1=360), HAIR)
    c.face(x, y + 15, 130, mood)


def cat(c, x, y, s=1.0, mood='happy'):
    c.line([(x + 80 * s, y + 90 * s), (x + 170 * s, y + 40 * s), (x + 160 * s, y - 60 * s)], 16 * s, taper=(4, 10))
    c.shape(E(x, y + 60 * s, 95 * s, 85 * s), CAT, shade=(CAT_D, 8, 8))
    for sx in (-1, 1):
        c.shape(np.array([(x + sx * 30 * s, y - 95 * s), (x + sx * 75 * s, y - 165 * s), (x + sx * 82 * s, y - 70 * s)], np.float32), CAT)
    c.shape(E(x, y - 60 * s, 85 * s, 72 * s), CAT, shade=(CAT_D, 8, 8))
    c.face(x, y - 52 * s, 90 * s, mood)
    for sx in (-1, 1):
        for dy in (-8, 8):
            c.line([(x + sx * 50 * s, y - 35 * s + dy), (x + sx * 115 * s, y - 40 * s + dy * 2)], 3, taper=(2, 4))


def key(c, x, y, rot=0.0, s=1.0):
    c.shape(P(E(0, 0, 34, 34), x, y, s, rot), KEY, shade=(KEY_D, 4, 4))
    c.shape(P(R(28, -9, 120, 9, 4), x, y, s, rot), KEY)
    c.shape(P(R(88, 6, 102, 30, 3), x, y, s, rot), KEY)
    c.shape(P(R(106, 6, 118, 22, 3), x, y, s, rot), KEY)


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    # ---------------- the doorstep
    c = Cartoon(W, H, seed=21, boil=2.0)
    c.paper()
    c.fill(np.array([(0, 0), (1440, 0), (1440, 1750), (0, 1750)], np.float32), '#cfe6f2', knock=False)
    c.fill(np.array([(0, 1750), (1440, 1750), (1440, 2560), (0, 2560)], np.float32), '#b8a58c', knock=False)
    c.line([(0, 1750), (1440, 1750)], 6, taper=(0, 0))
    c.shape(R(140, 520, 640, 1750, 16), '#9b5a33', shade=('#7a4424', 12, 12))
    c.shape(R(200, 600, 580, 1000, 10), '#b06a3f'); c.shape(R(200, 1100, 580, 1650, 10), '#b06a3f')
    c.shape(E(560, 1200, 22, 22), KEY)
    c.shape(R(110, 1760, 900, 1900, 30), '#7d8f4e', shade=('#5f6e3a', 8, 8))
    for i, (kx, ky, rot) in enumerate(((240, 1810, 10), (380, 1840, -25), (520, 1805, 40), (650, 1850, -5), (760, 1815, 70))):
        key(c, kx, ky, rot, 0.8)
    cat(c, 470, 1590, 1.05, 'happy')
    leo(c, 1080, 1250, 'wow')
    c.arm((990, 1440), (880, 1150), width=6, hand=22)
    key(c, 860, 1080, -30, 1.0)
    c.letter('?!', 1240, 1060, 110, fill=YELLOW, rot=10)
    c.stage('doorstep')
    c.note('MON', 480, 2010, 60, anchor='m'); c.note('TUE', 720, 2010, 60, anchor='m'); c.note('...FRI', 960, 2010, 60, anchor='m')
    c.letter('5 KEYS', 720, 2200, 120, fill=YELLOW, anchor='m', rot=-6)
    c.stage('count')
    c.save(str(out / 'day.png'), stages_dir=str(out / 'day'))
    # ---------------- the living room
    n = Cartoon(W, H, seed=22, boil=2.0)
    n.paper()
    n.fill(np.array([(0, 0), (1440, 0), (1440, 1900), (0, 1900)], np.float32), '#f1dcb4', knock=False)
    n.fill(np.array([(0, 1900), (1440, 1900), (1440, 2560), (0, 2560)], np.float32), '#a77b55', knock=False)
    n.shape(R(0, 1860, 1440, 1905, 4), '#e6c79a')
    n.line([(0, 1905), (1440, 1905)], 6, taper=(0, 0))
    n.shape(R(780, 1520, 1400, 1900, 60), '#d0584a', shade=('#a8433a', 12, 12))
    n.shape(R(740, 1700, 1440, 1960, 40), '#d0584a', shade=('#a8433a', 10, 12))
    n.speed_lines((700, 1600), (700, 1900), angle=0, n=4)
    leo(n, 1050, 1050, 'wow')
    n.stage('room')
    n.shape(R(240, 1560, 560, 1900, 120), '#7a4a2a', shade=('#5c361d', 8, 8))
    n.shape(E(500, 1740, 14, 14), KEY)
    n.stage('door')
    n.shape(R(240, 1560, 560, 1900, 120), '#2a1d2e')                   # the door swings open
    n.shape(np.array([(560, 1600), (640, 1560), (640, 1900), (560, 1900)], np.float32), '#7a4a2a')
    for i, col in enumerate(('#e94e77', '#4f86c6', '#ffd23c', '#4bb37a', '#ffffff', '#f08a3c', '#9b6dd6', '#e94e77', '#4f86c6')):
        x = 290 + (i % 5) * 55; y = 1860 - (i // 5) * 40
        n.shape(E(x, y, 42, 24, rot=(i * 37) % 60 - 30), col)
    n.letter('CLICK', 160, 1440, 110, fill=YELLOW, rot=-8)
    n.stage('open')
    cat(n, 400, 1700, 0.75, 'sleepy')
    key(n, 470, 1790, 15, 0.6)
    n.shape(R(120, 1040, 700, 1290, 60), WHITE)
    n.shape(np.array([(380, 1280), (420, 1440), (470, 1285)], np.float32), WHITE)
    n.note('rent.', 410, 1200, 110, anchor='m')
    n.stage('rent')
    n.save(str(out / 'eve.png'), stages_dir=str(out / 'eve'))


D = ['day/%s.png' % s for s in ('00_doorstep', '01_count')]
N = ['eve/%s.png' % s for s in ('00_room', '01_door', '02_open', '03_rent')]

EPISODE = dict(
    chapter='The Cat Who Left Keys',
    title="A Cat Kept Leaving Him Keys. Then He Found the Door. #shorts",
    description="Every morning, a key on the doormat. Leo finally found the lock.\n\nAn original animated story, drawn with code. Narration is synthetic.",
    tags=['animated story', 'funny story', 'plot twist', 'cat story', 'cartoon', 'shorts'],
    voice='am_puck',
    lines=["Every morning, the cat left a key on Leo's doormat.",
           "Monday, one key. Tuesday, another. By Friday, he had five.",
           "None of them opened anything. Then he moved the sofa, and found a tiny door in the wall.",
           "The smallest key fit. Click.",
           "Inside: every sock he had ever lost, piled into a bed. The cat strolled in, dropped one more key, and purred: rent."],
    gaps=[0.15, 0.35, 0.4, 0.35, 0.45],
    display=[(1, 'five.', '5.')],
    plates=[dict(stages=D, show=[(0, 0), ('L1:friday', 1)]),
            dict(stages=N, show=[(0, 0), ('L2:tiny', 1), ('L3:click', 2), ('L4:strolled', 3)])],
    camera=[(0, 720, 1400, 2100), ('L1', 720, 1500, 2050), ('L1:friday', 720, 1700, 1700), ('L1.end', 720, 1700, 1700),
            ('L2', 720, PH + 1350, 1900), ('L2:tiny', 560, PH + 1600, 1500), ('L3', 450, PH + 1650, 1150),
            ('L4', 500, PH + 1700, 1200), ('L4:strolled', 560, PH + 1450, 1500), ('END', 720, PH + 1400, 2000)],
    cards=[dict(at=0, until='L1-0.2', text='ANOTHER KEY.', font='AlfaSlabOne-400', size=96, ink=(150, 34, 26), x=540, y=330, rot=-3)],
    caption=dict(y=0.82),
    stamps=[dict(at='L4:rent', text='PLOT MELTED', size=80, color=(200, 40, 30), x=540, y=1760, rot=-6)],
    music=dict(sections=[(0, 'L2', ['Cmaj9', 'G6'], dict(bright=(0.5, 0.6), plucks=0.8, pulse=True)),
                         ('L2', 'L4', ['Am9', 'Esus'], dict(bright=(0.2, 0.3), ticks=True, plucks=0.3)),
                         ('L4', 'END', ['Fmaj7', 'Cmaj9'], dict(bright=(0.6, 0.5), gain=(1, 0.0), plucks=0.8))],
               events=[('L3:click', 'impact', dict(level=0.5))]),
)
