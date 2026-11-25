"""PlotMelt #005 — the old photo (original fiction, time-loop twist). Plates: a flea-market stall (Sam holds a sepia
photo from 1925 that shows his own face, mole and watch; the smiling seller below), then Sam's kitchen table (the back
of the photo in his handwriting, then the watch on his wrist ticking backwards). Hand-inked cartoon
(claude-drawing-skill: cartoon). No real brands or characters."""
from pathlib import Path
import numpy as np
from cartoon import Cartoon, WHITE, RED, YELLOW

E, R, P = Cartoon.ellipse_pts, Cartoon.rrect_pts, Cartoon.place
SKIN, SKIN_D, HAIR = '#f3c9a0', '#dba57a', '#5a3a26'
JACKET, JACKET_D = '#3f8f7a', '#2f6d5c'
SEP, SEP_D, SEP_L = '#b89466', '#8f6d45', '#e3cfa6'
STALL, STALL_D = '#c2563d', '#99402c'
WATCH = '#d9b24a'
PH = 2560
W = 1440


def person(c, x, y, mood, skin=(SKIN, SKIN_D), hair=HAIR, shirt=(JACKET, JACKET_D), s=1.0, hat=None):
    c.shape(E(x, y + 250 * s, 140 * s, 185 * s), shirt[0], shade=(shirt[1], 12, 12))
    c.shape(E(x, y, 116 * s, 110 * s), skin[0], shade=(skin[1], 10, 10))
    c.shape(E(x, y - 66 * s, 120 * s, 62 * s, a0=180, a1=360), hair)
    if hat:
        c.shape(R(x - 150 * s, y - 92 * s, x + 150 * s, y - 66 * s, 10), hat)
        c.shape(R(x - 90 * s, y - 190 * s, x + 90 * s, y - 80 * s, 16), hat)
    c.face(x, y + 15 * s, 132 * s, mood)
    c.dot(x + 62 * s, y + 52 * s, 7 * s)                                   # the mole


def watch(c, x, y, r=34):
    c.shape(R(x - r * 0.55, y - r * 1.7, x + r * 0.55, y + r * 1.7, 8), '#6b4a2e')   # strap
    c.shape(E(x, y, r, r), WATCH)
    c.shape(E(x, y, r * 0.72, r * 0.72), WHITE)
    c.line([(x, y), (x, y - r * 0.55)], 3, taper=(0, 0))
    c.line([(x, y), (x + r * 0.4, y + r * 0.1)], 3, taper=(0, 0))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    # ---------------- plate 1: the flea market
    c = Cartoon(W, PH, seed=51, boil=2.0)
    c.paper()
    c.fill(np.array([(0, 0), (W, 0), (W, PH), (0, PH)], np.float32), '#f1dfb8', knock=False)
    for k in range(6):                                                    # striped awning
        c.shape(R(k * 240, 320, k * 240 + 240, 470, 4), STALL if k % 2 == 0 else WHITE)
    person(c, 380, 1050, 'wow')
    c.arm((480, 1260), (720, 1330), width=6, hand=24)                     # holding the photo
    watch(c, 640, 1312, 26)
    c.shape(R(700, 700, 1340, 1560, 6), WHITE, width=7)                   # the photo, white border
    c.shape(R(740, 740, 1300, 1480, 4), SEP_L)
    person(c, 1020, 1000, 'smile', skin=(SEP, SEP_D), hair=SEP_D, shirt=(SEP_D, '#6e5233'), s=1.0)
    c.arm((1110, 1200), (1200, 1050), width=6, hand=22, glove=SEP_L)
    watch(c, 1180, 1100, 26)
    c.note('1925', 1250, 1450, 54, anchor='r', colour=SEP_D)
    c.shape(R(60, 1900, 1380, 2120, 14), STALL, shade=(STALL_D, 10, 10))  # the stall table
    person(c, 1060, 1760, 'happy', hat='#4a4a5a', shirt=('#7a6aa8', '#5d508a'), s=0.8)
    c.shape(R(60, 1900, 1380, 2120, 14), STALL, shade=(STALL_D, 10, 10))
    c.shape(E(330, 1890, 90, 40), '#9ab0c8')                              # junk on the table
    c.shape(R(470, 1820, 600, 1900, 8), '#7c5a3a')
    c.note('$1', 760, 1880, 80, anchor='m', colour=RED)
    c.stage('market')
    c.line(E(1082, 1052, 38, 38), 6, taper=(0, 0))                     # ring the mole, the watch and his own watch
    c.line(E(1180, 1100, 58, 70), 6, taper=(0, 0))
    c.line(E(640, 1312, 50, 62), 6, taper=(0, 0))
    c.letter('SAME WATCH.', 720, 640, 92, fill=YELLOW, anchor='m', rot=-3)
    c.stage('same')
    c.save(str(out / 'market.png'), stages_dir=str(out / 'market'))
    # ---------------- plate 2: the kitchen table
    k = Cartoon(W, PH, seed=52, boil=2.0)
    k.paper()
    k.fill(np.array([(0, 0), (W, 0), (W, PH), (0, PH)], np.float32), '#a8794f', knock=False)
    for i in range(7):
        k.line([(0, 300 + i * 340), (W, 280 + i * 340)], 3, taper=(0, 0))
    k.shape(P(R(-460, -360, 460, 360, 6), 720, 900, 1.0, -4), '#f3ead6', shade=('#d8ccb0', 12, 12))
    k.note("Don't buy", 720, 860, 104, anchor='m', colour='#2b2b6a', rot=-4)
    k.note('the watch.', 720, 1010, 104, anchor='m', colour='#2b2b6a', rot=-4)
    k.note('- Sam', 1000, 1160, 60, anchor='m', colour='#2b2b6a', rot=-4)
    k.stage('back')
    k.shape(R(560, 1500, 880, 2560, 40), SKIN, shade=(SKIN_D, 12, 12))   # the wrist, from below
    k.shape(R(530, 1820, 910, 2010, 14), '#6b4a2e')
    k.shape(E(720, 1915, 190, 190), WATCH)
    k.shape(E(720, 1915, 150, 150), WHITE)
    for a in range(12):
        ang = np.radians(a * 30)
        k.line([(720 + 120 * np.sin(ang), 1915 - 120 * np.cos(ang)), (720 + 138 * np.sin(ang), 1915 - 138 * np.cos(ang))], 4, taper=(0, 0))
    k.line([(720, 1915), (720, 1815)], 7, taper=(0, 0))
    k.line([(720, 1915), (640, 1940)], 7, taper=(0, 0))
    arc = [(720 + 250 * np.cos(np.radians(t)), 1915 - 250 * np.sin(np.radians(t))) for t in range(20, 160, 6)]
    k.arrow(arc, width=8, head=34)
    k.letter('BACKWARDS?!', 720, 1560, 96, fill=YELLOW, anchor='m', rot=-4)
    k.stage('wrist')
    k.save(str(out / 'table.png'), stages_dir=str(out / 'table'))


A = ['market/00_market.png', 'market/01_same.png']
B = ['table/00_back.png', 'table/01_wrist.png']

EPISODE = dict(
    chapter='The Old Photo',
    title="He Found His Face in a 100-Year-Old Photo. #shorts",
    description="Same face. Same mole. Same watch – the one on his wrist right now. And the photo was from 1925.\n\n"
                "An original animated story, drawn with code. Narration is synthetic.",
    tags=['animated story', 'funny story', 'plot twist', 'time travel', 'old photo', 'cartoon', 'shorts'],
    voice='am_puck',
    lines=["Sam found his own face in a hundred-year-old photo.",
           "Same mole. Same watch. The one on his wrist right now.",
           "The seller took one dollar, smiled and said: Took you long enough.",
           "At home, Sam turned the photo over.",
           "On the back, in his own handwriting: Don't buy the watch.",
           "He looked at his wrist. The watch was ticking backwards."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.35, 0.45],
    display=[(0, 'hundred-year-old', '100-year-old')],
    plates=[dict(stages=A, show=[(0, 0), ('L1:watch', 1)]),
            dict(stages=B, show=[(0, 0), ('L5', 1)])],
    camera=[(0, 735, 1180, 2150), ('L1', 735, 1180, 2100), ('L1:watch', 820, 1150, 1750), ('L2', 720, 1700, 1700),
            ('L3', 720, PH + 960, 1500), ('L4', 720, PH + 960, 1400), ('L5', 720, PH + 1850, 1350), ('END', 720, PH + 1850, 1350)],
    cards=[dict(at=0, until='L1-0.2', text='HIS FACE. 1925.', font='AlfaSlabOne-400', size=90, ink=(150, 34, 26),
                x=540, y=250, rot=-3)],
    caption=dict(y=0.84),
    stamps=[dict(at='L5:backwards', text='PLOT MELTED', size=80, color=(200, 40, 30), x=540, y=330, rot=-6)],
    music=dict(sections=[(0, 'L2', ['Am9', 'Esus'], dict(bright=(0.2, 0.3), ticks=True, plucks=0.3)),
                         ('L2', 'L4', ['Dm9', 'Am9'], dict(bright=(0.3, 0.4), pulse=True)),
                         ('L4', 'END', ['Fmaj7', 'Esus'], dict(bright=(0.4, 0.3), gain=(1, 0.0), plucks=0.6))],
               events=[('L5:backwards', 'impact', dict(level=0.5))]),
)
