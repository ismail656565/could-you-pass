"""Percept Lab #003 — Brain Test #1: the Ebbinghaus illusion (after Hermann Ebbinghaus; popularised in English by
Edward B. Titchener's 1901 lab manual, hence 'Titchener circles'). Chalkboard (claude-drawing-skill: chalk).
Two boards share the same seed, so the orange circles are identical; on the second the surrounding circles are gone."""
from pathlib import Path
import math
import numpy as np
from chalk import Chalkboard, WHITE, YELLOW, PINK, BLUE

ORANGE = '#f29a3a'
ST = ['quiz/00_quiz.png', 'reveal/00_bare.png', 'reveal/01_guides.png']
R, AY, BY = 95, 950, 1650


def disc(W, H, cx, cy, r):
    Y, X = np.mgrid[0:H, 0:W]
    return ((X - cx) ** 2 + (Y - cy) ** 2 <= r * r).astype(np.float32)


def base(W, H):
    cb = Chalkboard(W, H, seed=31)
    cb.slate(); cb.frame()
    cb.smudge(1100, 2250, 280, 80, rot=-6, strength=0.45)
    cb.text('WHICH IS BIGGER?', W / 2, 380, 92, YELLOW, anchor='ms')
    cb.underline(330, 1110, 412, YELLOW)
    cb.text('A', 120, AY + 26, 80, PINK, anchor='ms')
    cb.text('B', 120, BY + 26, 80, BLUE, anchor='ms')
    for cy in (AY, BY):
        cb.shade(disc(W, H, 720, cy, R), ORANGE, angle=20, pressure=0.6)
        cb.circle(720, cy, R, ORANGE, 5.0)
    return cb


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    cb = base(W, H)
    for k in range(6):                                   # A: big neighbours
        a = k * math.pi / 3 + math.pi / 6
        x, y = 720 + 300 * math.cos(a), AY + 300 * math.sin(a)
        cb.shade(disc(W, H, x, y, 150), WHITE, angle=-30, pressure=0.32)
        cb.circle(x, y, 150, WHITE, 4.0)
    for k in range(8):                                   # B: small neighbours
        a = k * math.pi / 4
        x, y = 720 + 150 * math.cos(a), BY + 150 * math.sin(a)
        cb.shade(disc(W, H, x, y, 38), WHITE, angle=-30, pressure=0.32)
        cb.circle(x, y, 38, WHITE, 3.6)
    cb.dust()
    cb.stage('quiz')
    cb.save(str(out / 'quiz.png'), str(out / 'quiz'))
    rv = base(W, H)
    rv.dust()
    rv.stage('bare')
    for x in (720 - R, 720 + R):
        rv.dashed([(x, AY - 200), (x, BY + 200)], YELLOW, width=4.0)
    rv.text('Ebbinghaus illusion', W / 2, 2180, 56, WHITE, anchor='ms')
    rv.chalk_stick(1040, 2300, 90, YELLOW, rot=-4)
    rv.stage('guides')
    rv.save(str(out / 'reveal.png'), str(out / 'reveal'))


EPISODE = dict(
    chapter='Brain Test #1: The Ebbinghaus Illusion',
    title="Which Orange Circle Is Bigger? Brain Test #1 🧠 #shorts",
    description=("Brain Test #1: which orange circle is bigger, A or B? This is the Ebbinghaus illusion, named after the German "
                 "psychologist Hermann Ebbinghaus and made popular in English by Edward B. Titchener in 1901 (that's why "
                 "it's also called 'Titchener circles'). Your brain judges size by comparing it with what's around it.\n\n"
                 "Illustrations painted with code on a chalkboard (no photos), narration is synthetic."),
    tags=['ebbinghaus illusion', 'titchener circles', 'optical illusion', 'brain test', 'perception', 'illusions'],
    voice='af_nicole',
    lines=["Which orange circle is bigger? A or B?",
           "Decide now. Trust your eyes.",
           "Now let's take the other circles away.",
           "They're exactly the same size.",
           "It's called the Ebbinghaus illusion. Your brain judges size by what's around it. Now look again."],
    gaps=[0.15, 0.4, 0.8, 0.4, 0.45],
    plates=[dict(stages=ST, show=[(0, 0), ('L2:away', 1), ('L3-0.1', 2)])],
    camera=[(0, 720, 1240, 2400), ('L1', 720, 1260, 2330), ('L2', 720, 1300, 2300), ('L3', 720, 1300, 2400),
            ('END', 720, 1260, 2440)],
    cards=[dict(at=0, until='L2', text='A or B?', font='AlfaSlabOne-400', size=96, x=820, y=1770, rot=4)],
    stamps=[dict(at='L3:same', text='SAME SIZE', size=90, color=(160, 32, 24), x=540, y=1000, rot=-5)],
    caption=dict(y=0.80),
    music=dict(sections=[(0, 'L2', ['Am9', 'Esus'], dict(bright=(0.2, 0.35), ticks=True, plucks=0.3)),
                         ('L2', 'L4', ['Fmaj7', 'Cmaj9'], dict(bright=(0.4, 0.6), pulse=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))],
               events=[('L2:away', 'chime', dict(f=880.0))]),
)
