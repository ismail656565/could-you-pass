"""HUMAN LIMIT #005 — Space makes your heart rounder (lab notebook, claude-drawing-skill: notebook).
Facts (American College of Cardiology press release, 29 March 2014, 'Study Finds Astronauts' Hearts Become More
Spherical in Space'; ScienceDaily 2014): in a study of 12 astronauts, who imaged their own hearts with ultrasound
machines on the International Space Station, the heart became more spherical by 9.4 percent in microgravity; the shape
appears to be temporary and returns to its normal elongated shape shortly after return to Earth. Lead author
Chris May, M.D.; senior author James Thomas, M.D. (NASA). Science story only, no advice."""
from pathlib import Path
import math
import numpy as np
from notebook import Notebook, INK, SOFT, LEAD, RED, MINT

ST = ['page/%s.png' % n for n in ('00_hearts', '01_rounder', '02_scan', '03_earth')]
W, H = 1440, 2560


def heart(cx, cy, sx, sy, n=90):
    pts = []
    for k in range(n + 1):
        t = 2 * math.pi * k / n
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * sx, cy - y * sy))
    return pts


def mask(pts):
    from PIL import Image, ImageDraw
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon(pts, fill=255)
    return np.asarray(m, np.float32) / 255


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    nb = Notebook(W, H, seed=52)
    nb.desk()
    nb.notebook(80, 150, 1360, 2430)
    nb.text('YOUR HEART IN SPACE', 200, 400, 84, INK)
    nb.highlight(196, 1050, 375, 60, tilt=-1.5, alpha=0.6)
    earth = heart(450, 1050, 12.5, 19.0)                  # long, egg-like
    space = heart(1010, 1060, 15.5, 15.0)                 # rounder
    nb.hatch(mask(earth), angle=40, spacing=10, colour=LEAD, pressure=0.45)
    nb.pencil(earth, 4.2, 0.9)
    nb.hatch(mask(space), angle=40, spacing=7, colour=RED, pressure=0.7, width=2.2)
    nb.pen(space, 5.0, RED)
    nb.label_tape('ON EARTH', 450, 1520, 30, anchor='m')
    nb.label_tape('IN SPACE', 1010, 1520, 30, anchor='m')
    nb.text('(drawing exaggerated)', 1240, 470, 26, SOFT, 'typewriter', 'rs', medium='typed')
    nb.stage('hearts')
    nb.pen_loop(1010, 1080, 300, 330, width=5.0)
    nb.text('+9.4 %', 1250, 700, 70, RED, anchor='rs')
    nb.text('rounder', 1250, 760, 44, RED, anchor='rs')
    nb.stage('rounder')
    nb.sticky(450, 1950, 560, 300, rot=-3, colour='#efe596')
    nb.text('12 ASTRONAUTS', 210, 1880, 46, INK)
    nb.text('scanned their own', 210, 1945, 38, INK)
    nb.text('hearts on the ISS', 210, 1995, 38, INK)
    nb.text('(ultrasound)', 210, 2045, 34, SOFT)
    nb.stage('scan')
    nb.sticky(1030, 1960, 520, 280, rot=3, colour=MINT)
    nb.text('BACK ON EARTH:', 810, 1905, 42, INK)
    nb.text('normal, longer', 810, 1965, 38, INK)
    nb.text('shape again', 810, 2015, 38, INK)
    nb.pen_arrow([(830, 1830), (690, 1690), (520, 1440)], 4.0, 18)
    nb.stage('earth')
    nb.save(str(out / 'page.png'), stages_dir=str(out / 'page'))


EPISODE = dict(
    chapter='Space Makes Your Heart Round',
    title="Space Makes Your Heart Round. Then It Changes Back. 🚀 #shorts",
    description=("In a study of 12 astronauts who scanned their own hearts with ultrasound on the International Space "
                 "Station, the heart became about 9.4 % more spherical in microgravity. The change appears to be "
                 "temporary: shortly after the return to Earth, the heart goes back to its normal, more elongated shape "
                 "(American College of Cardiology, 2014; lead author Chris May, senior author James Thomas, NASA).\n\n"
                 "Science story, not a challenge. Illustrations painted with code (no photos), narration is synthetic."),
    tags=['astronaut heart', 'heart in space', 'space body', 'microgravity', 'human body', 'science shorts', 'nasa'],
    voice='af_heart',
    lines=["Go to space, and your heart changes shape.",
           "It turns rounder. About nine percent more like a ball.",
           "Twelve astronauts scanned their own hearts with ultrasound on the space station.",
           "The good news: back on Earth, it soon returns to its normal, longer shape.",
           "Take gravity away, and even your heart's shape changes."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.5],
    display=[(1, 'nine', '9'), (1, 'percent', '%'), (2, 'twelve', '12')],
    plates=[dict(stages=ST, show=[(0, 0), ('L1', 1), ('L2', 2), ('L3', 3)])],
    camera=[(0, 720, 1060, 1950), ('L1', 720, 1020, 1950), ('L1@0.5', 1000, 960, 1300), ('L2', 600, 1700, 1600),
            ('L3', 820, 1750, 1650), ('L4', 720, 1280, 2450), ('END', 720, 1280, 2450)],
    cards=[dict(at=0, until='L1-0.2', text='ROUNDER.', font='AlfaSlabOne-400', size=100, ink=(150, 34, 26), x=540,
                y=520, rot=-3)],
    caption=dict(y=0.82),
    music=dict(sections=[(0, 'L2', ['Esus', 'Am9'], dict(bright=(0.2, 0.35), ticks=True)),
                         ('L2', 'L4', ['Dm9', 'Esus'], dict(bright=(0.35, 0.55), pulse=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
