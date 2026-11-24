"""Percept Lab #004 — the blind spot test (chalk). Close the left eye, stare at the cross with the right eye, move the
phone closer: at roughly 15-25 cm the dot falls on the optic disc (where the optic nerve leaves the eye; no rods or
cones) and vanishes; the brain fills the gap with the surrounding board. Discovered by Edme Mariotte in the 1660s
(Wikipedia 'Blind spot (vision)', 'Edme Mariotte'). Cross and dot sit far apart (~5 cm on a phone) so the test works."""
from pathlib import Path
import numpy as np
from chalk import Chalkboard, WHITE, YELLOW, PINK, BLUE

ST = ['test/00_test.png', 'test/01_eye.png']
CX, DX, Y = 230, 1210, 1280


def disc(W, H, cx, cy, r):
    Yy, X = np.mgrid[0:H, 0:W]
    return ((X - cx) ** 2 + (Yy - cy) ** 2 <= r * r).astype(np.float32)


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    cb = Chalkboard(W, H, seed=44)
    cb.slate(); cb.frame()
    cb.smudge(380, 2250, 260, 70, rot=5, strength=0.4)
    cb.text('CLOSE YOUR LEFT EYE', W / 2, 420, 88, YELLOW, anchor='ms')
    cb.underline(300, 1140, 455, YELLOW)
    cb.text('stare at the cross', W / 2, 560, 60, WHITE, anchor='ms')
    cb.line(CX - 85, Y, CX + 85, Y, WHITE, width=15.0)          # the cross
    cb.line(CX, Y - 85, CX, Y + 85, WHITE, width=15.0)
    cb.shade(disc(W, H, DX, Y, 80), PINK, angle=25, pressure=0.85)
    cb.circle(DX, Y, 80, PINK, 6.0)
    cb.text('move closer, slowly', W / 2, 1560, 60, WHITE, anchor='ms')
    cb.dust()
    cb.stage('test')
    # the explanation: a chalk eye seen from above, optic nerve leaving at the blind spot
    ex, ey, r = 640, 1830, 150
    cb.circle(ex, ey, r, BLUE, 8.0)
    cb.circle(ex, ey - r + 22, 34, WHITE, 6.0)                   # pupil
    cb.loop(ex, ey - r + 30, 70, 26, WHITE, width=4.0)            # lens at the front
    cb.line(ex + 60, ey + r - 20, ex + 110, ey + r + 120, YELLOW, width=9.0)   # optic nerve
    cb.line(ex + 20, ey + r - 10, ex + 70, ey + r + 120, YELLOW, width=9.0)
    cb.arrow([(960, 1960), (860, 1990), (ex + 100, ey + r + 50)], PINK, width=6.0)
    cb.text('no light cells', 1110, 1940, 56, PINK, anchor='ms')
    cb.stage('eye')
    cb.save(str(out / 'test.png'), str(out / 'test'))


EPISODE = dict(
    chapter='The Blind Spot Test',
    title="Close Your Left Eye. This Dot Will Disappear 👁️ #shorts",
    description=("Close your left eye, stare at the white cross with your right eye and slowly bring your phone closer. "
                 "At the right distance (often around 15-25 cm) the pink dot vanishes: it lands on your blind spot, the "
                 "place where the optic nerve leaves the eye and there are no light-sensitive cells. Your brain fills the "
                 "hole with what's around it. The French physicist Edme Mariotte discovered it in the 1660s.\n\n"
                 "Illustrations painted with code on a chalkboard (no photos), narration is synthetic."),
    tags=['blind spot', 'blind spot test', 'optic disc', 'mariotte', 'optical illusion', 'brain test', 'perception'],
    voice='af_nicole',
    lines=["Close your left eye. Stare at the cross.",
           "Now bring your phone closer. Slowly.",
           "Keep staring at the cross. Don't look at the dot.",
           "At the right distance, the dot is gone.",
           "It hit your blind spot, where the optic nerve leaves the eye. Your brain fills the hole.",
           "A French scientist found it over three hundred years ago. Now look again."],
    gaps=[0.15, 0.4, 0.4, 1.2, 0.4, 0.4],
    plates=[dict(stages=ST, show=[(0, 0), ('L4', 1)])],
    camera=[(0, 720, 1280, 2540), ('L1', 720, 1280, 2540), ('L3', 720, 1280, 2540), ('L4', 720, 1340, 2400),
            ('END', 720, 1300, 2480)],
    cards=[dict(at=0, until='L1-0.1', text='WATCH IT VANISH', font='AlfaSlabOne-400', size=84, x=540, y=620, rot=-3)],
    stamps=[dict(at='L4', text='BLIND SPOT', size=96, color=(160, 32, 24), x=540, y=640, rot=-5)],
    caption=dict(y=0.86),
    music=dict(sections=[(0, 'L2', ['Am9', 'Esus'], dict(bright=(0.2, 0.35), ticks=True, plucks=0.3)),
                         ('L2', 'L4', ['Fmaj7', 'Cmaj9'], dict(bright=(0.35, 0.55), pulse=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))],
               events=[('L3:gone', 'chime', dict(f=880.0))]),
)
