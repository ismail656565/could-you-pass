"""HUMAN LIMIT #002 — Space makes you taller (lab notebook, claude-drawing-skill: notebook).
Facts: astronauts can grow up to ~3 % taller in microgravity, about 5 cm / 2 in for a 1.8 m person (NASA ISS ultrasound
study, Space.com 2013); 'more than half of U.S. astronauts report back pain during their mission' (Chang et al., UC San
Diego, Spine 2016, via Live Science); the extra height goes back within a few months on Earth (Space.com).
Science story only, no advice."""
from pathlib import Path
from notebook import Notebook, INK, SOFT, LEAD, RED, MINT

ST = ['page/%s.png' % n for n in ('00_figures', '01_labels', '02_height', '03_pain', '04_earth')]
FEET = 1720


def figure(nb, cx, H, colour, gap):
    top = FEET - H
    Y = lambda f: top + f * H
    nb.pencil([(cx + H * 0.07 * __import__('math').cos(a / 20 * 6.2832), Y(0.075) + H * 0.075 * __import__('math').sin(a / 20 * 6.2832))
               for a in range(21)], 4.0, 0.85)
    side = [(-0.03, 0.15), (-0.13, 0.19), (-0.17, 0.50), (-0.135, 0.51), (-0.11, 0.28), (-0.10, 0.53), (-0.09, 1.0),
            (-0.025, 1.0), (0, 0.58)]
    pts = [(cx + x * H, Y(y)) for x, y in side] + [(cx - x * H, Y(y)) for x, y in reversed(side[:-1])]
    nb.pencil(pts, 4.0, 0.85)
    n = 15
    seg = (0.55 - 0.16) / n
    for i in range(n):                                   # the spine: vertebrae, with gaps between them
        y0 = Y(0.16 + i * seg + gap * 0.5); y1 = Y(0.16 + (i + 1) * seg - gap * 0.5)
        w = H * (0.018 + 0.012 * i / n)
        if colour == RED:
            nb.pen([(cx - w, y0), (cx + w, y0), (cx + w, y1), (cx - w, y1), (cx - w, y0)], 3.2, RED)
        else:
            nb.pencil([(cx - w, y0), (cx + w, y0), (cx + w, y1), (cx - w, y1), (cx - w, y0)], 2.6, 0.8)


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    nb = Notebook(W, H, seed=41)
    nb.desk()
    nb.notebook(80, 150, 1360, 2430)
    nb.text('YOUR SPINE IN SPACE', 200, 400, 84, INK)
    nb.highlight(196, 1000, 375, 60, tilt=-1.5, alpha=0.6)
    figure(nb, 470, 1060, LEAD, 0.006)
    figure(nb, 1000, 1150, RED, 0.016)
    nb.rule(240, FEET + 6, 1240, FEET + 6, 3.0)
    nb.stage('figures')
    nb.label_tape('ON EARTH', 470, FEET + 90, 30, anchor='m')
    nb.label_tape('IN SPACE', 1000, FEET + 90, 30, anchor='m')
    nb.stage('labels')
    for y in (FEET - 1060, FEET - 1150):
        nb.pen([(380, y), (1150, y)], 3.0, RED)
    nb.pen_arrow([(1220, FEET - 1060), (1220, FEET - 1150)], 4.0, 16)
    nb.text('+3 %', 1180, FEET - 1180, 58, RED, anchor='rs')
    nb.text('(drawing exaggerated)', 760, 2000, 30, SOFT, 'typewriter', 'ms', medium='typed')
    nb.stage('height')
    nb.pen_loop(1000, FEET - 1150 * 0.52, 90, 120, width=5.0)
    nb.sticky(1010, 2160, 540, 230, rot=-3, colour='#efe596')
    nb.text('BACK PAIN:', 780, 2120, 46, INK)
    nb.text('more than half of', 780, 2180, 38, INK)
    nb.text('US astronauts', 780, 2230, 38, INK)
    nb.stage('pain')
    nb.sticky(430, 2160, 480, 210, rot=3, colour=MINT)
    nb.text('BACK ON EARTH:', 230, 2125, 40, INK)
    nb.text('height returns', 230, 2185, 36, INK)
    nb.text('in a few months', 230, 2230, 36, INK)
    nb.stage('earth')
    nb.save(str(out / 'page.png'), stages_dir=str(out / 'page'))


EPISODE = dict(
    chapter='Space Makes You Taller',
    title="Space Makes You Taller. Then It Hurts. 🚀 #shorts",
    description=("In microgravity, astronauts can grow up to about 3 % taller — around 5 cm (2 in) for a 1.8 m person — because "
                 "nothing presses their spine together (NASA ISS study). But more than half of U.S. astronauts report back pain "
                 "during their missions (UC San Diego study, Spine, 2016), and back on Earth the extra height disappears within "
                 "a few months.\n\nScience story, not a challenge. Illustrations painted with code (no photos), narration is synthetic."),
    tags=['astronauts taller in space', 'space spine', 'human body', 'microgravity', 'science shorts', 'nasa'],
    voice='af_heart',
    lines=["Go to space, and you come back taller.",
           "Without gravity pressing down, an astronaut's spine stretches out.",
           "On long missions, they can grow up to three percent taller. That's about two inches.",
           "But it hurts. More than half of US astronauts report back pain during their missions.",
           "And back on Earth, gravity wins. Within a few months, the extra height is gone."],
    gaps=[0.15, 0.4, 0.4, 0.4, 0.45],
    display=[(2, 'three', '3'), (2, 'percent', '%'), (2, 'two', '2')],
    plates=[dict(stages=ST, show=[(0, 0), ('L1', 1), ('L2', 2), ('L3:back', 3), ('L4:within', 4)])],
    camera=[(0, 720, 1200, 2100), ('L1', 720, 1150, 1700), ('L1:spine', 1000, 1100, 1300), ('L2', 820, 900, 1500),
            ('L3', 820, 1600, 1700), ('L4', 720, 1290, 2450), ('END', 720, 1290, 2450)],
    cards=[dict(at=0, until='L1-0.2', text='TALLER IN SPACE.', font='AlfaSlabOne-400', size=80, ink=(150, 34, 26), x=540, y=1240, rot=-3)],
    counter=dict(start='L2:up', full='L2:taller', until='L3', n=3, fmt='+{n} %', x=540, y=330, rot=-4, size=100),
    stamps=[dict(at='L3:back', text='OUCH', size=90, color=(160, 32, 24), x=900, y=820, rot=8)],
    caption=dict(y=0.78),
    music=dict(sections=[(0, 'L2', ['Esus', 'Am9'], dict(bright=(0.2, 0.35), ticks=True)),
                         ('L2', 'L4', ['Dm9', 'Esus'], dict(bright=(0.35, 0.55), pulse=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
