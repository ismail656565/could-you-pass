"""PlotMelt #004 — the 3 AM pizza (original fiction, time-loop twist). Plates: the doorway at night (Theo meets a
delivery guy with his own face), then the couch and the doorstep (Theo in the red cap, ringing the bell); hand-inked
cartoon with a boiling line (claude-drawing-skill: cartoon). No real brands: the box only says PIZZA."""
from pathlib import Path
import numpy as np
from cartoon import Cartoon, WHITE, RED, YELLOW

E, R, P = Cartoon.ellipse_pts, Cartoon.rrect_pts, Cartoon.place
SKIN, HAIR = '#f3c9a0', '#3b2a22'
TEE, TEE_D = '#4f8fd6', '#3a6fae'
CAP, CAP_D = '#e2463a', '#b8342b'
BOX, BOX_D = '#e9c58f', '#c9a26a'
NIGHT, WALL, DOOR = '#1f2a4a', '#efe3c8', '#8a5a3a'
PH = 2560


def theo(c, x, y, mood, cap=False, shirt=(TEE, TEE_D), scar=True):
    c.shape(E(x, y + 250, 140, 185), shirt[0], shade=(shirt[1], 12, 12))
    c.shape(E(x, y, 116, 110), SKIN, shade=('#dba57a', 10, 10))
    if cap:
        c.shape(E(x, y - 62, 120, 66, a0=180, a1=360), CAP, shade=(CAP_D, 6, 6))
        c.shape(R(x - 10, y - 74, x + 170, y - 50, 12), CAP_D)
    else:
        c.shape(E(x, y - 66, 120, 62, a0=180, a1=360), HAIR)
    c.face(x, y + 15, 132, mood)
    if scar:
        c.line([(x + 58, y - 22), (x + 82, y + 22)], 5, taper=(2, 2))
        c.line([(x + 62, y - 6), (x + 80, y - 10)], 3, taper=(1, 1))


def pizza_box(c, x, y, s=1.0):
    c.shape(R(x - 150 * s, y - 34 * s, x + 150 * s, y + 34 * s, 8), BOX, shade=(BOX_D, 6, 6))
    c.note('PIZZA', x, y + 14 * s, int(40 * s), anchor='m')


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    # ---------------- plate 1: the doorway at 3 AM
    c = Cartoon(W, H, seed=41, boil=2.0)
    c.paper()
    c.fill(np.array([(0, 0), (W, 0), (W, H), (0, H)], np.float32), WALL, knock=False)
    c.shape(R(690, 520, 1360, 2150, 10), NIGHT, width=8)                  # the open door, night outside
    c.shape(R(1290, 520, 1440, 2150, 6), DOOR)
    for k in range(5):
        c.sparkle(780 + k * 120, 620 + (k % 2) * 90, 12, colour=YELLOW)
    c.fill(np.array([(0, 2150), (W, 2150), (W, H), (0, H)], np.float32), '#b78a5e', knock=False)
    c.line([(0, 2150), (W, 2150)], 6, taper=(0, 0))
    theo(c, 400, 1250, 'wow')                                             # Theo, inside
    theo(c, 1030, 1250, 'happy', cap=True, shirt=(CAP, CAP_D))            # the delivery guy, outside
    pizza_box(c, 1030, 1640, 1.0)
    c.arm((930, 1450), (900, 1620), width=6, hand=22)
    c.arm((1130, 1450), (1160, 1620), width=6, hand=22)
    c.note('3:00 AM', 260, 720, 110, anchor='l', colour=RED)
    c.stage('door')
    c.letter('SAME SCAR.', 720, 1980, 96, fill=YELLOW, anchor='m', rot=-4)
    c.stage('scar')
    c.shape(P(R(-100, -140, 100, 140, 6), 1190, 1830, 1.0, 8), WHITE)          # the receipt
    for k in range(4):
        c.line([(1120, 1740 + k * 34), (1250, 1752 + k * 34)], 3, taper=(0, 0))
    c.note('Theo', 1185, 1925, 52, anchor='m', colour=RED, rot=8)
    c.stage('receipt')
    c.save(str(out / 'door.png'), stages_dir=str(out / 'door'))
    # ---------------- plate 2a: the couch
    n = Cartoon(W, H, seed=42, boil=2.0)
    n.paper()
    n.fill(np.array([(0, 0), (W, 0), (W, H), (0, H)], np.float32), '#d8cde9', knock=False)
    n.fill(np.array([(0, 1900), (W, 1900), (W, H), (0, H)], np.float32), '#b78a5e', knock=False)
    n.shape(R(160, 1180, 1280, 1800, 60), '#6b8f5a', shade=('#557347', 14, 14))   # couch
    n.shape(R(220, 1500, 1220, 1700, 40), '#7fa66b')
    theo(n, 560, 1330, 'sleepy', scar=True)
    pizza_box(n, 1000, 1980, 1.2)
    n.letter('Z', 760, 1080, 80, fill=WHITE, rot=8)
    n.letter('Z', 850, 960, 110, fill=WHITE, rot=-6)
    n.note('3:00 AM?', 260, 720, 100, anchor='l', colour=RED)
    n.stage('couch')
    n.save(str(out / 'couch.png'), stages_dir=str(out / 'couch'))
    # ---------------- plate 2b: the doorstep, outside — Theo is now the delivery guy
    s = Cartoon(W, H, seed=43, boil=2.0)
    s.paper()
    s.fill(np.array([(0, 0), (W, 0), (W, H), (0, H)], np.float32), NIGHT, knock=False)
    for k in range(7):
        s.sparkle(120 + k * 200, 300 + (k % 3) * 110, 14, colour=YELLOW)
    s.shape(R(100, 600, 640, 2150, 10), DOOR, width=8)                    # the closed door
    s.shape(E(560, 1400, 26, 26), YELLOW)
    s.fill(np.array([(0, 2150), (W, 2150), (W, H), (0, H)], np.float32), '#6d6f7a', knock=False)
    s.line([(0, 2150), (W, 2150)], 6, taper=(0, 0))
    theo(s, 1000, 1250, 'wow', cap=True, shirt=(CAP, CAP_D))
    pizza_box(s, 1000, 1640, 1.0)
    s.arm((1100, 1450), (1130, 1620), width=6, hand=22)
    s.stage('step')
    s.shape(R(690, 1150, 760, 1220, 10), '#d9d9d9')                       # the bell
    s.arm((900, 1440), (760, 1190), width=6, hand=22)
    s.letter('DING', 720, 1000, 90, fill=YELLOW, anchor='m', rot=-6)
    s.stage('bell')
    s.save(str(out / 'step.png'), stages_dir=str(out / 'step'))


A = ['door/%s.png' % x for x in ('00_door', '01_scar', '02_receipt')]
B = ['couch/00_couch.png', 'step/00_step.png', 'step/01_bell.png']

EPISODE = dict(
    chapter='The 3 AM Pizza',
    title="He Ordered Pizza at 3 AM. He Delivered It. #shorts",
    description="The pizza guy at the door had his face. Same scar. Same shirt. Same voice.\n\n"
                "An original animated story, drawn with code. Narration is synthetic.",
    tags=['animated story', 'funny story', 'plot twist', 'time loop', 'pizza', 'cartoon', 'shorts'],
    voice='am_puck',
    lines=["The pizza guy at the door had Theo's face.",
           "Same scar. Same shirt. Same voice.",
           "Large pepperoni, the stranger said. You'll understand soon. Then he walked off into the dark.",
           "The receipt was signed in Theo's own handwriting.",
           "Shaking, he ate a slice and fell asleep on the couch.",
           "He woke up on a doorstep, in a red cap, holding a large pepperoni.",
           "It was three in the morning. He rang the bell."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.4, 0.4, 0.45],
    plates=[dict(stages=A, show=[(0, 0), ('L1:scar', 1), ('L3', 2)]),
            dict(stages=B, show=[(0, 0), ('L5', 1), ('L6:rang', 2)])],
    camera=[(0, 720, 1300, 1800), ('L1', 720, 1300, 2000), ('L1@0.6', 720, 1450, 1700), ('L2', 720, 1300, 2200), ('L2@0.6', 720, 1300, 2200),
            ('L3', 1000, 1550, 1500), ('L3.end', 1000, 1550, 1500), ('L4', 720, PH + 1350, 2000), ('L5', 760, PH + 1300, 2100), ('L6', 760, PH + 1300, 2100),
            ('END', 720, PH + 1300, 2250)],
    cards=[dict(at=0, until='L1-0.2', text='SAME FACE.', font='AlfaSlabOne-400', size=100, ink=(150, 34, 26), x=540, y=1500, rot=-3)],
    caption=dict(y=0.84),
    stamps=[dict(at='L6:rang', text='PLOT MELTED', size=80, color=(200, 40, 30), x=540, y=300, rot=-6)],
    music=dict(sections=[(0, 'L2', ['Am9', 'Esus'], dict(bright=(0.2, 0.3), ticks=True, plucks=0.3)),
                         ('L2', 'L5', ['Dm9', 'Am9'], dict(bright=(0.3, 0.4), pulse=True)),
                         ('L5', 'END', ['Fmaj7', 'Esus'], dict(bright=(0.4, 0.3), gain=(1, 0.0), plucks=0.6))],
               events=[('L6:rang', 'impact', dict(level=0.5))]),
)
