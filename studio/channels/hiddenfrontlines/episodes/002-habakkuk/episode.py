"""HiddenFrontlines #002 — Weird War Tech #1: Project Habakkuk, Britain's aircraft carrier of ice (blueprint).
Facts (Wikipedia 'Project Habakkuk' citing Perutz et al.; Legion Magazine 'A cool idea', 2020): idea by Geoffrey Pyke
(Combined Operations HQ); pykrete = ice + wood pulp (optimum ~14 % pulp), stronger and slower-melting than ice;
planned ship ~600 m (2,000 ft) long; scale model at Patricia Lake, Jasper, Alberta, 18 x 9 m, ~1,000 tonnes,
completed 1943; final board meeting December 1943 shelved it (enormous resources, technical difficulties);
the model slowly melted and sank in the lake."""
from pathlib import Path
from blueprint import Blueprint

ST = ['print/%s.png' % n for n in ('00_ship', '01_callouts', '02_mix', '03_model', '04_block')]


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    bp = Blueprint(W, H, seed=23)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('AIRCRAFT CARRIER — MADE OF ICE', W / 2, 200, 46, 'ms', pen=2.2, spacing=0.18)
    bp.text('PROJECT HABAKKUK · 1943', W / 2, 255, 26, 'ms')
    # side elevation of the 'bergship'
    hull = [(170, 760), (1270, 760), (1270, 900), (1220, 1010), (240, 1010), (170, 930)]
    bp.line(hull, 'heavy', closed=True)
    bp.line([(170, 762), (1270, 762)], 'heavy')
    bp.hatch([[(172, 905), (1268, 905), (1220, 1008), (240, 1008), (172, 930)]], angle=45, spacing=12, pen='thin')
    bp.line([(150, 905), (1290, 905)], 'thin')
    bp.text('WATERLINE', 1180, 895, 16, 'rs')
    bp.box(1030, 660, 1150, 760, 'heavy')
    bp.box(1060, 610, 1110, 660, 'medium')
    for x in (300, 460, 620, 780):                       # aircraft parked on the deck
        bp.line([(x - 50, 745), (x + 50, 745)], 'thick')
        bp.line([(x - 10, 722), (x - 10, 760)], 'thick')
        bp.line([(x + 40, 735), (x + 50, 745)], 'thin')
    bp.dim((170, 1010), (1270, 1010), 80, '600 M', size=30)
    bp.stage('ship')
    bp.leader([(500, 960), (420, 1250), (230, 1250)], 'PYKRETE HULL', size=24)
    bp.leader([(1090, 640), (1200, 480), (1280, 480)], 'BRIDGE', size=22)
    bp.stage('callouts')
    # the material
    bp.view_title(720, 1400, 'PYKRETE — SAMPLE BLOCK', size=28)
    blk = [(470, 1480), (970, 1480), (970, 1700), (470, 1700)]
    bp.line(blk, 'heavy', closed=True)
    bp.hatch([blk], angle=30, spacing=10, pen='fine', kind='cross')
    bp.text('ICE + WOOD PULP', 720, 1770, 30, 'ms', pen=1.8)
    bp.text('STRONGER THAN ICE · MELTS SLOWER', 720, 1815, 20, 'ms')
    bp.stage('mix')
    # the scale model on the lake
    bp.view_title(720, 1920, 'SCALE MODEL · CANADA', size=26)
    bp.line([(460, 1990), (980, 1990), (980, 2060), (940, 2100), (500, 2100), (460, 2060)], 'heavy', closed=True)
    bp.hatch([[(462, 2062), (978, 2062), (940, 2098), (500, 2098)]], angle=45, spacing=10, pen='thin')
    for k in range(4):
        y = 2075 + k * 20
        bp.line([(240 + i * 40, y + (7 if i % 2 else 0)) for i in range(25)], 'thin')
    bp.dim((460, 1990), (980, 1990), -45, '18 M', size=24)
    bp.text('ABOUT 1,000 TONS', 720, 2220, 28, 'ms', pen=1.6)
    bp.stage('model')
    x0, y0 = 120, 2290
    bp.table(x0, y0, [400, 400, 400], [50, 80], pen='thin', outer='medium')
    for i, (lab, val) in enumerate((('PROJECT', 'HABAKKUK'), ('IDEA', 'GEOFFREY PYKE'), ('STATUS', 'SHELVED DEC 1943'))):
        bp.text(lab, x0 + i * 400 + 14, y0 + 24, 16, 'ls')
        bp.text(val, x0 + i * 400 + 200, y0 + 100, 25, 'ms', pen=1.6)
    bp.stage('block')
    bp.fold(xs=(720,), ys=(1280,), wear=0.8)
    bp.stain(1200, 1600, 80, 0.6)
    bp.save(str(out / 'print.png'), str(out / 'print'))


EPISODE = dict(
    chapter='Project Habakkuk',
    title="Britain Tried to Build an Aircraft Carrier Out of Ice #shorts",
    description=("Weird War Tech #1. During WWII, Geoffrey Pyke of Britain's Combined Operations HQ proposed an aircraft carrier "
                 "made of 'pykrete' — frozen water mixed with wood pulp, stronger and slower-melting than plain ice. The planned "
                 "ship was about 600 m long. In 1943 a 1,000-tonne scale model was built on Patricia Lake in Jasper, Canada. "
                 "The project was shelved in December 1943 because of the enormous resources it needed; the model slowly "
                 "melted and sank.\n\nIllustrations painted with code (no photos), narration is synthetic."),
    tags=['project habakkuk', 'pykrete', 'ice aircraft carrier', 'ww2', 'weird war tech', 'military history', 'history shorts'],
    voice='am_michael',
    lines=["Britain once tried to build a warship out of ice.",
           "The idea came from Jeffrey Pike: freeze water with wood pulp. They called it pie-kreet.",
           "It was stronger than ice, and melted far more slowly. The ship was planned at six hundred meters long.",
           "On a lake in Canada, they built a scale model. It still weighed a thousand tons.",
           "But the real ship needed enormous resources. By the end of nineteen forty-three, it was shelved.",
           "The model slowly melted, and sank to the bottom of the lake."],
    gaps=[0.15, 0.35, 0.35, 0.4, 0.4, 0.45],
    display=[(1, 'jeffrey', 'Geoffrey'), (1, 'pike:', 'Pyke:'), (1, 'pie-kreet.', 'PYKRETE.'), (2, 'six', '600'), (2, 'hundred', ''),
             (3, 'thousand', '1,000'), (4, 'nineteen', '1943,'), (4, 'forty-three,', '')],
    plates=[dict(stages=ST, show=[(0, 0), ('L1', 1), ('L1:pie', 2), ('L3', 3), ('L4:shelved', 4)])],
    camera=[(0, 720, 1020, 2000), ('L1', 720, 1060, 2050), ('L1:pie-0.3', 720, 1200, 1900), ('L2', 720, 1600, 1300),
            ('L2:ship', 720, 980, 1900), ('L3', 720, 1910, 1300), ('L4', 720, 1290, 2500), ('L5', 720, 1290, 2500),
            ('END', 720, 1290, 2500)],
    cards=[dict(at=0, until='L1-0.2', text='MADE OF ICE.', font='AlfaSlabOne-400', size=100, ink=(150, 34, 26), x=540, y=420, rot=-3),
           dict(at='L1:pie', until='L2:ship', text='PYKRETE', size=90, x=540, y=380, rot=3)],
    stamps=[dict(at='L4:shelved', text='CANCELLED', size=110, color=(170, 30, 24), x=540, y=1150, rot=-8)],
    music=dict(sections=[(0, 'L2', ['Dm9', 'Am9'], dict(bright=(0.2, 0.35), pulse=True)),
                         ('L2', 'L4', ['Esus', 'Dm9'], dict(bright=(0.35, 0.5), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.4, 0.25), gain=(1, 0.0)))]),
)
