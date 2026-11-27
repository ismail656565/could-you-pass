"""PlotMelt #008 — my printer prints one page every night (original fiction, exploit format, first person).
Plate 1: dark study at 3:12, an unplugged printer pushing out a page, me in pyjamas in the doorway; then the pages on
the floor ("Hi.", "Buy milk.", a drawing of me asleep). Plate 2: the hallway — the printer with a final page
"FINE. THEN I'LL WALK.", then it grows tiny paper feet and scoots toward the bedroom. Comic, not scary.
Hand-inked cartoon (claude-drawing-skill: cartoon). No real brands or known characters."""
from pathlib import Path
import numpy as np
from cartoon import Cartoon, WHITE, RED, YELLOW

E, R = Cartoon.ellipse_pts, Cartoon.rrect_pts
W, PH = 1440, 2560
NIGHT, NIGHT_D, FLOOR, FLOOR_D = '#2c3a5c', '#24304d', '#5b4a63', '#4a3c52'
PRN, PRN_D, SKIN, SKIN_D, PJ, PJ_D = '#e9e6df', '#bdb8ae', '#f2c49a', '#d9a477', '#7fb3e0', '#5d92c2'
DESK, DESK_D = '#a8743f', '#7d5429'


def night_room(c, floor_y=1900):
    c.paper()
    c.fill(np.array([(0, 0), (W, 0), (W, floor_y), (0, floor_y)], np.float32), NIGHT, knock=False)
    c.shape(np.array([(0, floor_y), (W, floor_y), (W, PH), (0, PH)], np.float32), FLOOR, shade=(FLOOR_D, 0, 12))


def printer(c, x, y, s=1.0, mood='wow'):
    """(x, y) = centre of the printer body"""
    c.shape(R(x - 300 * s, y - 120 * s, x + 300 * s, y + 160 * s, 30), PRN, shade=(PRN_D, 10, 10))
    c.shape(R(x - 230 * s, y - 200 * s, x + 230 * s, y - 110 * s, 16), PRN_D)            # paper tray
    c.shape(R(x - 200 * s, y + 40 * s, x + 200 * s, y + 80 * s, 10), '#3a3a44')          # output slot
    c.dot(x + 240 * s, y - 60 * s, 14 * s, kind='flat')
    c.shape(E(x + 240 * s, y - 60 * s, 16 * s, 16 * s), '#7ee07a', width=4)
    c.face(x - 40 * s, y - 30 * s, 150 * s, mood, blush=False)


def page(c, x, y, w, h, text=None, size=60, rot=0.0):
    pts = Cartoon.place(R(-w / 2, -h / 2, w / 2, h / 2, 6), x, y, 1.0, rot)
    c.shape(pts, WHITE, width=5)
    if text:
        c.note(text, x, y, size, anchor='m', colour='#2a2a40', rot=-np.degrees(rot) if rot else 0)


def me(c, x, y, mood='wow'):
    c.shape(R(x - 110, y + 120, x + 110, y + 700, 50), PJ, shade=(PJ_D, 8, 8))
    for k in range(4):
        c.dot(x, y + 220 + k * 110, 9)
    c.shape(E(x, y, 115, 125), SKIN, shade=(SKIN_D, 8, 8))
    c.shape(np.array([(x - 115, y - 30), (x - 70, y - 150), (x + 20, y - 170), (x + 110, y - 110), (x + 120, y - 30),
                      (x + 40, y - 100), (x - 50, y - 80)], np.float32), '#4b3426')
    c.face(x, y + 20, 150, mood)


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    c = Cartoon(W, PH, seed=81, boil=2.0)
    night_room(c)
    c.shape(R(880, 520, 1300, 940, 16), '#3f5582')                                       # window + moon
    c.shape(E(1160, 660, 70, 70), '#f6e7a8')
    c.line([(1060, 520), (1060, 940)], 6, taper=(0, 0)); c.line([(820, 730), (1300, 730)], 6, taper=(0, 0))
    c.shape(R(250, 600, 780, 860, 30), '#1b2236', width=6)                                # glowing clock
    c.note('3:12', 515, 732, 190, anchor='m', colour='#ff5a4a')
    c.shape(R(200, 1420, 1240, 1500, 12), DESK, shade=(DESK_D, 6, 6))                    # desk
    c.shape(R(250, 1500, 310, 1960, 10), DESK_D); c.shape(R(1130, 1500, 1190, 1960, 10), DESK_D)
    printer(c, 720, 1230, 1.0, 'wow')
    page(c, 720, 1340, 360, 230)
    c.line([(980, 1360), (1080, 1600), (1010, 1880), (1120, 2020)], 7, taper=(0, 0))      # unplugged cable
    c.shape(R(1100, 2000, 1180, 2060, 10), '#3a3a44')
    for px in (1125, 1155):
        c.line([(px, 2060), (px, 2100)], 6, taper=(0, 0))
    c.stage('print')
    page(c, 330, 2080, 300, 200, 'Hello.', 70, 0.12)
    page(c, 700, 2240, 330, 210, 'Buy milk.', 58, -0.08)
    pts = Cartoon.place(R(-200, -150, 200, 150, 6), 360, 1700, 1.0, -0.05)               # drawing of me asleep
    c.shape(pts, WHITE, width=5)
    c.shape(E(340, 1730, 120, 40), '#dfe6f2', width=4)
    c.shape(E(330, 1690, 56, 50), SKIN, width=4)
    c.face(330, 1695, 70, 'sleepy', blush=False)
    c.note('z z', 450, 1620, 46, anchor='m', colour='#2a2a40')
    c.stage('pages')
    c.save(str(out / 'study.png'), stages_dir=str(out / 'study'))

    k = Cartoon(W, PH, seed=82, boil=2.0)
    night_room(k, 1820)
    k.shape(R(980, 500, 1380, 1830, 10), '#3a2f4a')                                        # bedroom door, open
    k.shape(R(1020, 560, 1340, 1830, 6), '#f3d38a')                                        # warm light
    me(k, 1180, 1000, 'wow')
    printer(k, 560, 1500, 0.95, 'smile')
    page(k, 560, 1050, 640, 300)
    k.note('FINE.', 560, 990, 96, anchor='m', colour='#2a2a40')
    k.note("THEN I'LL WALK.", 560, 1100, 70, anchor='m', colour='#2a2a40')
    k.stage('note')
    for fx in (380, 520, 640, 760):                                                       # tiny paper feet
        k.shape(R(fx - 22, 1650, fx + 22, 1760, 8), WHITE, width=4)
        k.shape(E(fx + 18, 1770, 46, 22), WHITE, width=4)
    k.speed_lines((80, 1300), (80, 1700), angle=0, n=5)
    k.note('tap tap tap', 560, 1950, 66, anchor='m', colour=YELLOW, rot=-3)
    k.stage('walk')
    k.save(str(out / 'hall.png'), stages_dir=str(out / 'hall'))


A = ['study/00_print.png', 'study/01_pages.png']
B = ['hall/00_note.png', 'hall/01_walk.png']

EPISODE = dict(
    chapter='The Printer',
    title="My Printer Prints One Page Every Night. I Read It. #shorts",
    description="Every night at 3:12 the printer wakes up and prints exactly one page. It isn't connected. It isn't even "
                "plugged in. So I started reading them…\n\nAn original animated story, drawn with code. Narration is synthetic.",
    tags=['animated story', 'funny story', 'printer', 'plot twist', 'cartoon', 'short story', 'shorts'],
    voice='am_puck',
    lines=["Every night at three twelve, my printer prints one page.",
           "Nobody's connected. It's not even plugged in.",
           "The first page read: hello. Another one read: buy milk.",
           "Page thirty was a perfect drawing of me, asleep.",
           "So I unplugged the whole wall. It printed one more page.",
           "It said: Fine. Then I'll walk."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45, 0.5],
    display=[(0, 'three', '3:12,'), (0, 'twelve,', '')],
    plates=[dict(stages=A, show=[(0, 0), ('L2', 1)]),
            dict(stages=B, show=[(0, 0), ('L5', 1)])],
    camera=[(0, 720, 1200, 1900), ('L1', 720, 1260, 2100), ('L1.end', 720, 1280, 2440), ('L2', 720, 1500, 2300),
            ('L3', 720, 1520, 2000), ('L3.end', 720, 1520, 2000), ('L4', 720, PH + 1240, 2440),
            ('L5', 760, PH + 1300, 2300), ('END', 760, PH + 1300, 2200)],
    cards=[dict(at=0, until='L1-0.1', text="IT'S NOT PLUGGED IN.", font='AlfaSlabOne-400', size=74,
                paper=(255, 255, 255), ink=(20, 20, 20), x=540, y=230, rot=-2)],
    caption=dict(y=0.88),
    stamps=[dict(at='L3:perfect', text='PAGE 30', size=64, color=(200, 40, 30), x=820, y=1130, rot=-6, until='L4')],
    music=dict(sections=[(0, 'L2', ['Am9', 'Esus'], dict(bright=(0.2, 0.3), ticks=True)),
                         ('L2', 'L4', ['Dm9', 'Am9'], dict(bright=(0.3, 0.45), pulse=True, ticks=True)),
                         ('L4', 'END', ['Fmaj7', 'Cmaj9'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.6))],
               events=[('L5:Fine', 'impact', dict(level=0.4))]),
)
