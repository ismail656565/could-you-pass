"""Percept Lab #002 — the negative afterimage. A flag printed in its opposite colours (green/black stripes, yellow
canton, black stars) as a Bauhaus screen print (claude-drawing-skill: bauhaus). Stare at the dot for ~20 s, then look
at the blank sheet: the cone cells that adapted to each colour respond less, so you see the opposite colours —
red, white and blue."""
from pathlib import Path
import math
import numpy as np
from bauhaus import Bauhaus, YELLOW, BLACK

GREEN = '#169c5c'
ST = ['flag/00_flag.png', 'white/00_white.png', 'white/01_name.png']
FX0, FY0, SH = 76, 900, 52            # flag left, top, stripe height (13 stripes -> 676 px, ratio 1.9)
FX1, FY1 = FX0 + 1287, FY0 + 13 * SH
CX, CY = 720, FY0 + 6.5 * SH          # the white dot: centre of the flag


def star(b, cx, cy, r):
    pts = [(cx + (r if k % 2 == 0 else r * 0.4) * math.sin(k * math.pi / 5),
            cy - (r if k % 2 == 0 else r * 0.4) * math.cos(k * math.pi / 5)) for k in range(10)]
    return b.poly(pts)


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    b = Bauhaus(W, H, seed=12, misreg=1.2)
    b.paper()
    dot = b.circle(CX, CY, 15)
    b.text('STARE AT THE DOT', W / 2, 700, 96, anchor='ms')
    green = sum(b.rect(FX0, FY0 + i * SH, FX1, FY0 + (i + 1) * SH) for i in range(0, 13, 2))
    b.pull(green, GREEN, knock=dot, opacity=0.95)
    blk = sum(b.rect(FX0, FY0 + i * SH, FX1, FY0 + (i + 1) * SH) for i in range(1, 13, 2))
    cw, ch = 514, 7 * SH
    b.pull(np.clip(blk - b.rect(FX0, FY0, FX0 + cw, FY0 + ch), 0, 1), BLACK, knock=dot)
    b.pull(b.rect(FX0, FY0, FX0 + cw, FY0 + ch), YELLOW, opacity=0.97, edge=0.3)
    stars = 0
    for row in range(9):
        n = 6 if row % 2 == 0 else 5
        for k in range(n):
            x = FX0 + cw * ((2 * k + 1 + (row % 2)) / 12)
            y = FY0 + ch * ((row + 1) / 10)
            stars = stars + star(b, x, y, 15)
    b.pull(np.clip(stars, 0, 1), BLACK, edge=0.3)
    b.text("DON'T BLINK.", W / 2, 1760, 64, anchor='ms')
    b.stage('flag')
    b.save(str(out / 'flag.png'), str(out / 'flag'))
    w = Bauhaus(W, H, seed=13, misreg=1.0)
    w.paper(colour='#fbf9f3', warm='#f4efe4')
    w.text('LOOK AT THE DOT', W / 2, 700, 96, anchor='ms')
    w.pull(w.circle(CX, CY, 15), BLACK)
    w.stage('white')
    w.text('NEGATIVE AFTERIMAGE', W / 2, 1960, 72, anchor='ms')
    w.pull(w.rect(300, 1995, 1140, 2009), BLACK)
    w.stage('name')
    w.save(str(out / 'white.png'), str(out / 'white'))


EPISODE = dict(
    chapter='The Negative Afterimage',
    title="Stare at This Flag for 20 Seconds, Then Look at the White 👁️ #shorts",
    description=("Stare at the dot on a flag printed in the 'wrong' colours, then look at a blank page: you see red, white and "
                 "blue. It's a negative afterimage — the cone cells in your eyes adapt to each colour while you stare, so "
                 "afterwards they briefly show you the opposite colours.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['afterimage', 'optical illusion', 'brain test', 'flag illusion', 'stare at the dot', 'perception', 'illusions'],
    voice='af_nicole',
    lines=["Stare at the white dot. Don't blink.",
           "Keep your eyes on the dot for twenty seconds. Don't look away.",
           "These colours look wrong. Your eyes are getting tired of them.",
           "Almost there. Keep staring.",
           "Now look at the white. Red, white and blue! It's a negative afterimage: tired cells in your eyes show you the opposite colours. Now look again."],
    gaps=[0.15, 1.2, 2.0, 2.4, 1.4],
    display=[(1, 'twenty', '20')],
    plates=[dict(stages=ST, show=[(0, 0), ('L4:white', 1), ('L4:negative', 2)])],
    camera=[(0, 720, 1240, 2440), ('L4:white', 720, 1240, 2440), ('END', 720, 1260, 2400)],
    cards=[],
    counter=dict(start=0.3, full='L4-0.3', until='L4:white', n=20, fmt='{n}s', x=540, y=300, rot=-3, size=110),
    stamps=[dict(at='L4:negative', text='YOUR BRAIN: FOOLED', size=66, color=(160, 32, 24), x=540, y=1240, rot=-5)],
    caption=dict(y=0.73),
    music=dict(sections=[(0, 'L4', ['Am9', 'Esus'], dict(bright=(0.15, 0.3), ticks=True)),
                         ('L4', 'END', ['Fmaj7', 'Cmaj9'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))],
               events=[('L4:white', 'chime', dict(f=880.0))]),
)
