"""PlotMelt #007 — the dog that stared at one wall (original fiction, exploit format: pet + strange repeated behaviour
+ "then he opened it"). Plate 1: living room, a dog staring at one spot near the skirting board, its owner puzzled
behind it; then knock-knock lettering. Plate 2: a hole cut in the plaster reveals a tiny warm mouse bakery (loaves,
string lights, a mouse chef waving), the dog's happy head and the owner's shocked face in front. Ends on plate 1 again
(loop). Hand-inked cartoon (claude-drawing-skill: cartoon). No real brands or known characters."""
from pathlib import Path
import numpy as np
from cartoon import Cartoon, WHITE, RED, YELLOW, ORANGE

E, R = Cartoon.ellipse_pts, Cartoon.rrect_pts
W, PH = 1440, 2560
WALL, WALL_D, FLOOR, FLOOR_D = '#9fc7c2', '#7fa9a4', '#c98f55', '#a8703f'
DOG, DOG_D, EAR = '#e0a35a', '#c07f3b', '#8a5428'
SKIN, SKIN_D, SHIRT, SHIRT_D = '#f2c49a', '#d9a477', '#e86a4f', '#c24f38'
MOUSE, MOUSE_D, BREAD, BREAD_D, HOLE = '#b4b0b8', '#8e8a94', '#e8b064', '#c48a40', '#5a3424'


def room(c):
    c.paper()
    c.fill(np.array([(0, 0), (W, 0), (W, 1900), (0, 1900)], np.float32), WALL, knock=False)
    for x in range(60, W, 160):                                                   # wallpaper stripes
        c.fill(R(x, 0, x + 50, 1880, 4), WALL_D, knock=False)
    c.shape(np.array([(0, 1840), (W, 1840), (W, 1910), (0, 1910)], np.float32), WHITE)   # skirting board
    c.shape(np.array([(0, 1910), (W, 1910), (W, PH), (0, PH)], np.float32), FLOOR, shade=(FLOOR_D, 0, 12))
    for y in (2080, 2280, 2480):
        c.line([(0, y), (W, y)], 4, taper=(0, 0))
    c.shape(R(180, 420, 560, 760, 12), '#f6eed8')                                 # picture frame
    c.shape(np.array([(220, 720), (330, 560), (420, 660), (470, 600), (530, 720)], np.float32), '#7fb069')
    c.shape(E(460, 510, 34, 34), YELLOW)


def dog_side(c, x, y, mood='smile'):
    """sitting dog, facing right; (x, y) = chest"""
    c.shape(np.array([(x - 260, y + 120), (x - 380, y - 60), (x - 330, y - 80), (x - 220, y + 60)], np.float32), DOG)  # tail
    c.shape(E(x - 120, y + 110, 210, 170), DOG, shade=(DOG_D, 10, 10))                     # body
    c.shape(E(x - 190, y + 230, 120, 70), DOG, shade=(DOG_D, 8, 8))                        # back leg
    c.shape(R(x - 20, y + 60, x + 50, y + 300, 30), DOG, shade=(DOG_D, 6, 6))             # front legs
    c.shape(R(x + 60, y + 70, x + 130, y + 300, 30), DOG, shade=(DOG_D, 6, 6))
    c.shape(E(x + 80, y - 150, 150, 130), DOG, shade=(DOG_D, 8, 8))                        # head
    c.shape(E(x + 230, y - 110, 90, 62), DOG)                                              # snout
    c.dot(x + 310, y - 130, 18)                                                            # nose
    c.shape(np.array([(x - 10, y - 250), (x - 90, y - 120), (x - 40, y - 30), (x + 20, y - 170)], np.float32), EAR)
    c.face(x + 130, y - 170, 120, mood, blush=False)


def man(c, x, y, mood='wow'):
    """standing man, (x, y) = head centre"""
    c.shape(R(x - 120, y + 130, x + 120, y + 560, 50), SHIRT, shade=(SHIRT_D, 8, 8))
    c.shape(R(x - 100, y + 540, x - 20, y + 900, 20), '#4a5a80')
    c.shape(R(x + 20, y + 540, x + 100, y + 900, 20), '#4a5a80')
    c.shape(E(x, y, 120, 130), SKIN, shade=(SKIN_D, 8, 8))
    c.shape(np.array([(x - 120, y - 40), (x - 90, y - 140), (x, y - 160), (x + 100, y - 130), (x + 120, y - 40),
                      (x + 60, y - 90), (x - 40, y - 90)], np.float32), '#4b3426')
    c.face(x, y + 20, 160, mood)


def bakery(c):
    c.paper()
    c.fill(np.array([(0, 0), (W, 0), (W, PH), (0, PH)], np.float32), WALL, knock=False)
    for x in range(60, W, 160):
        c.fill(R(x, 0, x + 50, PH, 4), WALL_D, knock=False)
    hole = np.array([(170, 1750), (160, 1000), (260, 640), (520, 470), (900, 470), (1170, 640), (1280, 1000),
                     (1270, 1750)], np.float32)
    rim = np.array([(120, 1790), (100, 1300), (130, 980), (200, 700), (330, 520), (470, 450), (600, 400), (720, 430),
                    (860, 390), (1000, 450), (1150, 540), (1260, 720), (1330, 1000), (1310, 1350), (1330, 1790)], np.float32)
    c.shape(rim, '#f4efe2', width=6)                                                       # broken plaster edge
    c.shape(hole, HOLE, width=8)
    c.fill(E(720, 760, 380, 200), '#7a4a2c', knock=False)                                  # warm glow
    for k, sy in enumerate((900, 1200)):                                                   # shelves + loaves
        c.shape(R(260, sy, 1180, sy + 36, 8), '#a8743f')
        for j in range(6):
            bx = 340 + j * 150
            c.shape(E(bx, sy - 44, 60, 42), BREAD, shade=(BREAD_D, 5, 5))
            c.line([(bx - 24, sy - 60), (bx - 8, sy - 30)], 4, taper=(0, 0))
            c.line([(bx + 6, sy - 62), (bx + 22, sy - 32)], 4, taper=(0, 0))
    for j in range(9):                                                                     # string lights
        lx, ly = 300 + j * 105, 640 + 50 * np.sin(j * 0.75)
        c.shape(E(lx, ly, 18, 24), YELLOW, width=4)
    c.line([(300 + j * 105, 620 + 50 * np.sin(j * 0.75)) for j in range(9)], 4, taper=(0, 0))
    c.shape(R(380, 1500, 1060, 1750, 14), '#c98f55', shade=('#a8703f', 6, 6))              # counter
    mx, my = 760, 1400                                                                     # mouse chef
    c.shape(E(mx, my + 20, 70, 90), MOUSE, shade=(MOUSE_D, 5, 5))
    for dx in (-60, 60):
        c.shape(E(mx + dx, my - 110, 38, 38), MOUSE, shade=(MOUSE_D, 4, 4))
    c.shape(E(mx, my - 70, 60, 54), MOUSE)
    c.face(mx, my - 62, 70, 'happy', blush=True)
    c.shape(R(mx - 50, my - 190, mx + 50, my - 120, 20), WHITE)                             # chef hat
    c.shape(E(mx, my - 200, 62, 40), WHITE)
    c.arm((mx + 50, my), (mx + 150, my - 120), width=4, hand=16, glove=MOUSE)
    c.shape(E(560, 1460, 50, 32), BREAD, shade=(BREAD_D, 4, 4))
    c.shape(R(170, 1750, 1270, 1790, 6), WHITE)
    # dog's happy head bottom-left, owner bottom-right
    dx, dy = 400, 2180
    c.shape(np.array([(dx - 160, dy - 200), (dx - 300, dy + 20), (dx - 220, dy + 160), (dx - 120, dy - 40)], np.float32), EAR)
    c.shape(np.array([(dx + 160, dy - 200), (dx + 300, dy + 20), (dx + 220, dy + 160), (dx + 120, dy - 40)], np.float32), EAR)
    c.shape(E(dx, dy, 220, 200), DOG, shade=(DOG_D, 8, 8))
    c.shape(E(dx, dy + 110, 110, 80), '#f2d3a0')
    c.dot(dx, dy + 70, 26)
    c.face(dx, dy - 40, 190, 'happy', blush=False)
    man(c, 1080, 2080, 'wow')


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    c = Cartoon(W, PH, seed=71, boil=2.0)
    room(c)
    c.shape(E(1110, 1790, 26, 16), '#6f5a4a')                                             # the spot
    c.line([(1090, 1770), (1120, 1740), (1112, 1710)], 4, taper=(0, 0))
    man(c, 400, 1100, 'wow')
    dog_side(c, 700, 1820, 'smile')
    c.line([(1010, 1700), (1060, 1730)], 5, taper=(0, 0)); c.line([(1000, 1760), (1060, 1770)], 5, taper=(0, 0))
    c.stage('stare')
    c.note('KNOCK KNOCK', 980, 1480, 84, anchor='m', colour=RED, rot=-4)
    c.pop_lines(1110, 1790, 70, 140, [200, 240, 290, 330])
    c.note('knock', 1150, 1620, 52, anchor='m', colour='#4a3a30', rot=6)
    c.stage('knock')
    c.save(str(out / 'room.png'), stages_dir=str(out / 'room'))

    k = Cartoon(W, PH, seed=72, boil=2.0)
    bakery(k)
    k.stage('bakery')
    for sx in (400, 700, 1000):
        k.steam(sx, 780, 110)
    k.shape(R(560, 300, 880, 420, 14), WHITE)
    k.note('OPEN', 720, 362, 80, anchor='m', colour=RED)
    k.sparkle(300, 480, 30); k.sparkle(1160, 520, 26)
    k.stage('open')
    k.save(str(out / 'bakery.png'), stages_dir=str(out / 'bakery'))


A = ['room/00_stare.png', 'room/01_knock.png']
B = ['bakery/00_bakery.png', 'bakery/01_open.png']

EPISODE = dict(
    chapter='The Wall',
    title="His Dog Stared at One Wall for a Week. Then He Opened It. #shorts",
    description="Seven days. One spot on the wall. The dog never barked – it just sniffed and wagged. Then something "
                "knocked back…\n\nAn original animated story, drawn with code. Narration is synthetic.",
    tags=['animated story', 'funny story', 'dog', 'plot twist', 'cartoon', 'short story', 'shorts'],
    voice='am_puck',
    lines=["For seven days, his dog stared at the same spot on the wall.",
           "It didn't bark. It just sniffed, and wagged.",
           "So he knocked. Something knocked back. Very softly.",
           "He cut a little hole. Behind the plaster was a tiny bakery, run by mice.",
           "Warm little lights, fresh bread, and a tiny chef who waved hello.",
           "The dog had smelled the bread all week."],
    gaps=[0.15, 0.35, 0.4, 0.5, 0.4, 0.5],
    plates=[dict(stages=A, show=[(0, 0), ('L2', 1), ('L5', 0)]),
            dict(stages=B, show=[(0, 0), ('L4', 1)])],
    camera=[(0, 760, 1500, 2000), ('L1', 760, 1520, 2100), ('L1.end', 760, 1380, 2440), ('L2', 760, 1380, 2440),
            ('L2.end', 900, 1580, 2100), ('L3', 720, PH + 1260, 2440), ('L4', 720, PH + 1260, 2440),
            ('L4.end', 720, PH + 1200, 2300), ('L5', 760, 1400, 2440), ('END', 760, 1440, 2300)],
    cards=[dict(at=0, until='L1-0.1', text='7 DAYS. ONE SPOT.', font='AlfaSlabOne-400', size=86, paper=(255, 255, 255),
                ink=(20, 20, 20), x=540, y=250, rot=-2)],
    caption=dict(y=0.86),
    stamps=[dict(at='L3:tiny', text='MOUSE BAKERY', size=70, color=(200, 40, 30), x=540, y=1270, rot=-5, until='L5')],
    music=dict(sections=[(0, 'L2', ['Dm9', 'Am9'], dict(bright=(0.25, 0.35), plucks=0.4)),
                         ('L2', 'L3', ['Esus', 'Am9'], dict(bright=(0.3, 0.4), pulse=True, ticks=True)),
                         ('L3', 'END', ['Fmaj7', 'Cmaj9'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.6))],
               events=[('L2:knocked#2', 'impact', dict(level=0.35))]),
)
