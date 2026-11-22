"""HUMAN LIMIT #001 — Randy Gardner's 264 hours awake (San Diego, Dec 1963 – Jan 1964, age 17, a high-school science
fair project; observed by Stanford sleep researcher William Dement). Plate: a lab notebook page with a pencil chart
(claude-drawing-skill: notebook). Science story only, no advice."""
from pathlib import Path
import numpy as np
from notebook import Notebook, INK, SOFT, LEAD, RED, MINT

ST = ['page/%s.png' % n for n in ('00_notebook', '01_header', '02_axes', '03_curve', '04_notes', '05_record')]


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    nb = Notebook(W, H, seed=31)
    nb.desk()
    nb.notebook(80, 150, 1360, 2430)
    nb.stain(1180, 2240, 70, strength=0.25)
    nb.stage('notebook')
    nb.text('EXPERIMENT · 1963', 200, 420, 34, SOFT, 'typewriter', medium='typed')
    nb.text('HOW LONG CAN', 200, 560, 96, INK)
    nb.text('A HUMAN STAY', 200, 670, 96, INK)
    nb.text('AWAKE?', 200, 780, 96, INK)
    nb.highlight(196, 640, 755, 70, tilt=-2, alpha=0.7)
    nb.label_tape('SAN DIEGO · AGE 17', 200, 880, 28)
    nb.stage('header')
    to_px = nb.axes(260, 1080, 1220, 1880, (0, 12), (0, 300), list(range(0, 12, 2)) + [11], [0, 100, 200, 264],
                    xlabels=['0', '2', '4', '6', '8', '10', '11'], ylabels=['0', '100', '200', '264'], size=26)
    nb.text('DAYS', 1230, 1960, 26, SOFT, 'typewriter', 'ms', medium='typed')
    nb.text('HOURS AWAKE', 260, 1040, 26, SOFT, 'typewriter', 'ls', medium='typed')
    nb.stage('axes')
    days = np.linspace(0, 11, 60)
    nb.pencil([to_px(d, 24 * d) for d in days], 4.2, 0.85, 1.2)
    nb.stage('curve')
    for d, t in ((2.2, 'mood swings'), (4.5, 'memory slips'), (6.5, 'seeing things')):
        x, y = to_px(d, 24 * d)
        nb.pencil([(x, y), (x + 70, y + 110)], 2.2, 0.7)
        nb.text(t, x + 78, y + 150, 34, INK, 'hand' if False else 'sans_bold', medium='ink')
    nb.stage('notes')
    x, y = to_px(11, 264)
    nb.pen_loop(x, y, 52, 46, width=5.0)
    nb.pen_arrow([(x - 260, y - 140), (x - 120, y - 120), (x - 62, y - 40)], 4.4, 20)
    nb.text('264 h', x - 420, y - 130, 64, RED)
    nb.sticker(1090, 900, 300, 150, rot=-6, colour=RED, lines=[('11 DAYS', 150, 100, 64, 'sans_bold', '#ffffff', 'ms')])
    nb.stage('record')
    nb.save(str(out / 'page.png'), stages_dir=str(out / 'page'))


EPISODE = dict(
    chapter='264 Hours Awake',
    title="A 17-Year-Old Stayed Awake for 11 Days. Here's What Happened #shorts",
    description=("In 1963 Randy Gardner, a 17-year-old student in San Diego, stayed awake for 264 hours as a science fair project — "
                 "one of the most famous cases in sleep research. A science story, not a challenge: don't try this.\n\n"
                 "Illustration painted with code as a lab notebook (no photos), narration is synthetic."),
    tags=['randy gardner', 'sleep deprivation', 'sleep science', 'human body', 'science shorts', 'record'],
    voice='af_heart',
    lines=["In nineteen sixty-three, a seventeen-year-old student in San Diego decided to stay awake. For as long as he could.",
           "His name was Randy Gardner, and it started as a school science project.",
           "As the days went on, his mood swung, his memory slipped, and he started seeing things that weren't there.",
           "He made it to two hundred and sixty-four hours. Eleven days, awake.",
           "His record became one of the most famous cases in sleep science."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(0, 'nineteen', '1963,'), (0, 'sixty-three,', ''), (0, 'seventeen-year-old', '17-YEAR-OLD'),
             (3, 'two', '264'), (3, 'hundred', ''), (3, 'and', ''), (3, 'sixty-four', 'HOURS.'), (3, 'hours.', ''), (3, 'eleven', '11')],
    plates=[dict(stages=ST, show=[(0, 1), ('L1', 2), ('L1.end-0.5', 3), ('L2:mood', 4), ('L3', 5)])],
    camera=[(0, 560, 640, 1300), ('L0.end', 640, 700, 1450), ('L1', 720, 1250, 2400), ('L2', 720, 1500, 1500),
            ('L2.end', 760, 1450, 1350), ('L3', 980, 1250, 1200), ('L3.end', 900, 1700, 1700), ('L4', 720, 1290, 2450),
            ('END', 720, 1290, 2400)],
    cards=[dict(at='L1:randy', until='L2-0.2', text='RANDY GARDNER', size=84, x=540, y=380, rot=-3)],
    stamps=[dict(at='L4:famous', text='RECORD', size=110, color=(160, 32, 24), x=380, y=1250, rot=-7)],
    caption=dict(y=0.80),
    music=dict(sections=[(0, 'L2', ['Esus', 'Am9'], dict(bright=(0.2, 0.35), ticks=True)),
                         ('L2', 'L3', ['Dm9', 'Esus'], dict(bright=(0.35, 0.55), pulse=True, ticks=True)),
                         ('L3', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))],
               events=[('L3', 'chime', dict(f=880.0))]),
)
