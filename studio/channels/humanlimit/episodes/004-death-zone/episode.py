"""HUMAN LIMIT #004 — Above 8,000 m: the 'death zone' (lab notebook, claude-drawing-skill: notebook).
Facts (Wikipedia 'Death zone' / 'Effects of high altitude on humans'; ScienceAlert/Business Insider 2019 'What happens to
your body in Everest's death zone'; Britannica 'Mount Everest'): above about 8,000 m the air pressure – and so the oxygen
in each breath – is roughly a third of sea level at Everest's summit; the body cannot acclimatise there and deteriorates;
risks include high-altitude pulmonary oedema (fluid in the lungs) and cerebral oedema (brain swelling); most climbers use
bottled (supplemental) oxygen. Science story only, no advice, no challenge."""
from pathlib import Path
import math
import numpy as np
from notebook import Notebook, INK, SOFT, LEAD, RED, MINT

ST = ['page/%s.png' % n for n in ('00_figures', '01_oxygen', '02_lungs', '03_bottle')]
FEET, HGT = 1760, 1080


def ell(cx, cy, rx, ry, n=36):
    return [(cx + rx * math.cos(a / n * 6.2832), cy + ry * math.sin(a / n * 6.2832)) for a in range(n + 1)]


def emask(W, H, cx, cy, rx, ry):
    Y, X = np.mgrid[0:H, 0:W]
    return ((((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2) <= 1).astype(np.float32)


def figure(nb, cx, danger, W, H):
    top = FEET - HGT
    Y = lambda f: top + f * HGT
    nb.pencil(ell(cx, Y(0.075), HGT * 0.075, HGT * 0.08), 4.0, 0.85)
    side = [(-0.03, 0.155), (-0.15, 0.19), (-0.18, 0.52), (-0.145, 0.53), (-0.12, 0.29), (-0.11, 0.55), (-0.10, 1.0),
            (-0.025, 1.0), (0, 0.6)]
    pts = [(cx + x * HGT, Y(y)) for x, y in side] + [(cx - x * HGT, Y(y)) for x, y in reversed(side[:-1])]
    nb.pencil(pts, 4.0, 0.85)
    for s in (-1, 1):                                                       # lungs
        lx, ly = cx + s * 0.05 * HGT, Y(0.31)
        if danger:
            nb.hatch(emask(W, H, lx, ly, 0.04 * HGT, 0.095 * HGT), angle=45 * s, spacing=9, colour=RED, pressure=0.7)
            nb.pen(ell(lx, ly, 0.04 * HGT, 0.095 * HGT), 3.4, RED)
        else:
            nb.pencil(ell(lx, ly, 0.04 * HGT, 0.095 * HGT), 2.8, 0.8)
    if danger:                                                              # brain
        nb.hatch(emask(W, H, cx, Y(0.065), 0.055 * HGT, 0.045 * HGT), angle=-30, spacing=9, colour=RED, pressure=0.7)
        nb.pen(ell(cx, Y(0.065), 0.055 * HGT, 0.045 * HGT), 3.4, RED)


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    nb = Notebook(W, H, seed=57)
    nb.desk()
    nb.notebook(80, 150, 1360, 2430)
    nb.text('YOUR BODY ABOVE 8,000 M', 190, 400, 60, INK)
    nb.highlight(186, 1210, 380, 50, tilt=-1.2, alpha=0.6)
    figure(nb, 440, False, W, H)
    figure(nb, 1000, True, W, H)
    nb.rule(220, FEET + 6, 1260, FEET + 6, 3.0)
    nb.label_tape('SEA LEVEL', 440, FEET + 90, 32, anchor='m')
    nb.label_tape('ABOVE 8,000 M', 1000, FEET + 90, 32, anchor='m')
    nb.stage('figures')
    for k in range(9):                                                      # oxygen per breath: 9 vs 3 dots
        x, y = 300 + (k % 3) * 52, 560 + (k // 3) * 52
        nb.pen(ell(x, y, 18, 18, 18), 3.4, '#2f6fb0')
    for k in range(3):
        nb.pen(ell(1040 + (k % 3) * 52, 560, 18, 18, 18), 3.4, '#2f6fb0')
    nb.text('O2 per breath', 352, 520, 34, SOFT, 'typewriter', 'ms', medium='typed')
    nb.text('about 1/3', 1092, 520, 34, RED, 'typewriter', 'ms', medium='typed')
    nb.stage('oxygen')
    nb.sticky(1010, 2030, 520, 200, rot=-3, colour='#efe596')
    nb.text('LUNGS: fluid', 790, 2005, 44, INK)
    nb.text('BRAIN: can swell', 790, 2070, 40, INK)
    nb.stage('lungs')
    nb.sticky(430, 2030, 480, 200, rot=3, colour=MINT)
    nb.text('MOST CLIMBERS:', 230, 2000, 38, INK)
    nb.text('bottled oxygen', 230, 2065, 38, INK)
    nb.stage('bottle')
    nb.save(str(out / 'page.png'), stages_dir=str(out / 'page'))


EPISODE = dict(
    chapter='The Death Zone',
    title="Above 8,000 m, Your Body Starts Dying 🏔️ #shorts",
    description=("Mountaineers call the altitudes above about 8,000 m (26,000 ft) the 'death zone'. Near the top of Everest, "
                 "every breath brings only about a third of the oxygen you get at sea level, and the body cannot adapt – it "
                 "slowly gets weaker, and the heart beats faster even at rest. Fluid can leak into the lungs (high-altitude pulmonary oedema) and the brain can swell "
                 "(cerebral oedema). That's why most Everest climbers breathe bottled oxygen.\n\n"
                 "Science story, not a challenge. Illustrations painted with code (no photos), narration is synthetic."),
    tags=['death zone', 'mount everest', 'high altitude', 'human body', 'hypoxia', 'science shorts', 'mountaineering'],
    voice='af_heart',
    lines=["Climb above eight thousand meters, and your body starts to die.",
           "Each breath brings about a third of the oxygen you get at sea level.",
           "Up here, your body can't adapt. It just keeps getting weaker.",
           "Your heart races, even while you rest.",
           "Fluid can leak into your lungs. Your brain can swell.",
           "That's why most climbers on Everest breathe bottled oxygen.",
           "Climbers have a name for it. The death zone."],
    gaps=[0.15, 0.4, 0.4, 0.4, 0.4, 0.4, 0.45],
    display=[(0, 'eight', '8,000'), (0, 'thousand', ''), (0, 'meters,', 'm,')],
    plates=[dict(stages=ST, show=[(0, 0), ('L1', 1), ('L4', 2), ('L5', 3)])],
    camera=[(0, 720, 1150, 2100), ('L1', 720, 1100, 1900), ('L2', 720, 1150, 2050), ('L4', 720, 1400, 2100),
            ('L6', 720, 1290, 2450), ('END', 720, 1290, 2450)],
    cards=[dict(at=0, until='L1-0.2', text='DEATH ZONE.', font='AlfaSlabOne-400', size=96, ink=(150, 34, 26), x=540, y=1380, rot=-3),
           dict(at='L1:third', until='L2', text='1/3 OXYGEN', font='AlfaSlabOne-400', size=90, ink=(150, 34, 26), x=540, y=1250, rot=3)],
    stamps=[dict(at='L6:death', text='DEATH ZONE', size=100, color=(160, 32, 24), x=540, y=1150, rot=-5)],
    caption=dict(y=0.88),
    music=dict(sections=[(0, 'L2', ['Am9', 'Esus'], dict(bright=(0.15, 0.3), ticks=True)),
                         ('L2', 'L5', ['Dm9', 'Esus'], dict(bright=(0.3, 0.45), pulse=True)),
                         ('L5', 'END', ['Fmaj7', 'Am9'], dict(bright=(0.4, 0.25), gain=(1, 0.0), plucks=0.3))]),
)
