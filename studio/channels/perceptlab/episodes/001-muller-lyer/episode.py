"""Percept Lab #001 — the Müller-Lyer illusion (Franz Carl Müller-Lyer, 1889), drawn on a classroom chalkboard
(claude-drawing-skill: chalk). Stages let the fins vanish and the guide lines appear."""
from pathlib import Path
from chalk import Chalkboard, WHITE, YELLOW, PINK, BLUE

ST = ['board/%s.png' % n for n in ('00_title', '01_lines', '02_fins', '03_guides', '04_name')]


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    cb = Chalkboard(W, H, seed=7)
    cb.slate()
    cb.frame()
    cb.smudge(380, 2050, 300, 90, rot=8, strength=0.5)
    cb.dust()
    cb.text('WHICH LINE IS LONGER?', W / 2, 640, 74, YELLOW, anchor='ms')
    cb.underline(300, 1140, 668, YELLOW)
    cb.stage('title')
    X0, X1, YA, YB = 420, 1020, 1020, 1420
    cb.text('A', 300, YA + 22, 64, PINK, anchor='ms')
    cb.text('B', 300, YB + 22, 64, BLUE, anchor='ms')
    cb.line(X0, YA, X1, YA, WHITE, 7.0, 0.95, overshoot=0)
    cb.line(X0, YB, X1, YB, WHITE, 7.0, 0.95, overshoot=0)
    cb.stage('lines')
    F = 95
    for x, s in ((X0, -1), (X1, 1)):                       # A: fins pointing out  >—<
        for dy in (-1, 1):
            cb.line(x, YA, x + s * F * 0.75, YA + dy * F * 0.75, WHITE, 7.0, 0.95, overshoot=0)
    for x, s in ((X0, 1), (X1, -1)):                       # B: arrowheads  <—>
        for dy in (-1, 1):
            cb.line(x, YB, x + s * F * 0.75, YB + dy * F * 0.75, WHITE, 7.0, 0.95, overshoot=0)
    cb.stage('fins')
    for x in (X0, X1):
        cb.dashed([(x, YA - 200), (x, YB + 200)], YELLOW, width=4.0)
    cb.text('SAME LENGTH', W / 2, 1830, 84, YELLOW, anchor='ms')
    cb.underline(360, 1080, 1856, YELLOW, double=True)
    cb.stage('guides')
    cb.text('Müller-Lyer illusion · 1889', W / 2, 2010, 46, WHITE, anchor='ms')
    cb.chalk_stick(980, 2120, 90, YELLOW, rot=-4)
    cb.eraser(420, 2124)
    cb.stage('name')
    cb.save(str(out / 'board.png'), stages_dir=str(out / 'board'))


EPISODE = dict(
    chapter='The Müller-Lyer Illusion',
    title="Which Line Is Longer? Your Brain Gets This Wrong #shorts",
    description=("Two lines, one question. The Müller-Lyer illusion (Franz Carl Müller-Lyer, 1889) still fools your brain even "
                 "after you know the answer.\n\nDrawn with code on a chalkboard, narration is synthetic."),
    tags=['optical illusion', 'muller-lyer illusion', 'brain test', 'perception', 'illusions'],
    voice='af_nicole',
    lines=["Which line is longer? The top one, or the bottom one?",
           "Take a second. Trust your eyes.",
           "Now watch what happens when the arrows disappear.",
           "They're exactly the same length.",
           "It's called the Müller-Lyer illusion, from eighteen eighty-nine. And even when you know the trick, your brain still falls for it."],
    gaps=[0.15, 0.25, 0.6, 0.35, 0.45],
    display=[(4, 'eighteen', '1889,'), (4, 'eighty-nine.', '')],
    plates=[dict(stages=ST, show=[(0, 2), ('L2:disappear', 1), ('L3-0.1', 3), ('L4', 4)])],
    camera=[(0, 720, 1120, 1950), ('L1', 720, 1140, 1880), ('L2', 720, 1160, 2000), ('L3', 720, 1250, 2150),
            ('L4', 720, 1330, 2400), ('END', 720, 1320, 2350)],
    cards=[dict(at='L1', until='L2', text='A or B?', font='AlfaSlabOne-400', size=96, x=760, y=1290, rot=4)],
    stamps=[dict(at='L4:brain', text='YOUR BRAIN: FOOLED', size=66, color=(160, 32, 24), x=540, y=520, rot=-5)],
    caption=dict(y=0.80),
    music=dict(sections=[(0, 'L2', ['Am9', 'Esus'], dict(bright=(0.2, 0.35), ticks=True, plucks=0.3)),
                         ('L2', 'L4', ['Fmaj7', 'Cmaj9'], dict(bright=(0.4, 0.6), pulse=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))],
               events=[('L3-0.1', 'chime', dict(f=880.0))]),
)
