"""HiddenFrontlines #004 — Weird War Tech #3: Project Pigeon (blueprint).
Facts (army.mil 'It's a bird! It's a plane!' 2013; Wikipedia 'Project Pigeon'; Skinner 1960 'Pigeons in a Pelican'):
psychologist B. F. Skinner; OSRD/NDRC contract June 1943; nose cone of the 'Pelican' glide bomb with three lenses and
three pigeons in separate compartments, each pecking at the target's image on a pivoting screen, the pecks moved the
control surfaces; in tests the trained birds kept pecking on target; never used in combat; cancelled October 1944;
revived by the Navy in 1948 as Project ORCON ('organic control'), cancelled 1953 once electronic guidance proved reliable."""
from pathlib import Path
import math
from blueprint import Blueprint

ST = ['print/%s.png' % n for n in ('00_cone', '01_callouts', '02_screen')]


def ell(cx, cy, rx, ry, a0=0, a1=360, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n)))
            for k in range(n + 1)]


def pigeon(bp, x, y, s=1.0):
    bp.line(ell(x, y, 90 * s, 52 * s), 'heavy', closed=True)                    # body
    bp.line([(x + 60 * s, y - 30 * s), (x + 100 * s, y - 80 * s)], 'heavy')     # neck
    bp.circle(x + 112 * s, y - 98 * s, 30 * s, 'heavy')                          # head
    bp.line([(x + 140 * s, y - 100 * s), (x + 175 * s, y - 90 * s), (x + 140 * s, y - 86 * s)], 'heavy')  # beak
    bp.dot(x + 118 * s, y - 104 * s, 4 * s)
    bp.line([(x - 86 * s, y - 8 * s), (x - 150 * s, y - 30 * s), (x - 140 * s, y + 10 * s), (x - 86 * s, y + 14 * s)], 'medium')  # tail
    bp.line(ell(x - 5 * s, y - 5 * s, 60 * s, 28 * s, 180, 360, 20), 'thin')    # wing
    bp.hatch([ell(x - 5 * s, y - 5 * s, 60 * s, 28 * s)], angle=35, spacing=12, pen='fine')
    for dx in (-15, 15):
        bp.line([(x + dx * s, y + 50 * s), (x + dx * s, y + 80 * s)], 'medium')


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    bp = Blueprint(W, H, seed=41)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('GUIDED MISSILE — NOSE SECTION', W / 2, 200, 46, 'ms', pen=2.2, spacing=0.18)
    bp.text('PILOT: PIGEON (x3)', W / 2, 260, 30, 'ms')
    # the nose cone, pointing up: an ogive from y=360 to y=1450
    left = [(720 - 470 * math.sqrt(1 - u / 40), 1450 - 1090 * u / 40) for u in range(41)]
    right = [(1440 - x, y) for x, y in reversed(left)]
    bp.line(left + right[1:], 'heavy')
    bp.line([(250, 1450), (250, 1560), (1190, 1560), (1190, 1450)], 'heavy')
    for x, y in ((520, 650), (720, 560), (920, 650)):                           # three lenses
        bp.circle(x, y, 46, 'heavy'); bp.circle(x, y, 26, 'thin')
    for k, (x, y) in enumerate(((420, 1000), (720, 1250), (980, 1000))):         # three compartments
        bp.box(x - 170, y - 160, x + 190, y + 110, 'thin')
        pigeon(bp, x, y, 0.95)
    bp.stage('cone')
    bp.leader([(520, 650), (300, 520), (120, 520)], '3 LENSES', size=26)
    bp.leader([(1080, 940), (1250, 800), (1330, 800)], 'PILOTS', size=26)
    bp.dim((250, 1620), (1190, 1620), 30, 'NOT TO SCALE', size=24)
    bp.stage('callouts')
    bp.view_title(720, 1760, 'WHAT THE BIRD SEES', size=28)
    bp.box(330, 1820, 1110, 2200, 'heavy')
    ship = [(460, 2060), (980, 2060), (930, 2120), (510, 2120)]
    bp.line(ship, 'heavy', closed=True)
    bp.line([(640, 2060), (640, 2000), (780, 2000), (780, 2060)], 'medium')
    bp.line([(700, 2000), (700, 1940)], 'medium')
    bp.line([(360, 2120), (1080, 2120)], 'thin')
    for dx, dy in ((0, 0), (-18, 10), (14, -8), (6, 16), (-8, -14)):           # peck marks on the target
        bp.red([(705 + dx - 10, 2045 + dy), (705 + dx + 10, 2045 + dy)], width=3.0)
        bp.red([(705 + dx, 2035 + dy), (705 + dx, 2055 + dy)], width=3.0)
    bp.text('PECK ON TARGET = MISSILE STEERS', 720, 2260, 26, 'ms', pen=1.6)
    bp.stage('screen')
    bp.fold(xs=(720,), ys=(1280,), wear=0.8)
    bp.stain(1220, 1400, 70, 0.5)
    bp.save(str(out / 'print.png'), str(out / 'print'))


EPISODE = dict(
    chapter='Project Pigeon',
    title="The US Trained Pigeons to Steer Missiles. They Were Good. #shorts",
    description=("Weird War Tech #3. In June 1943 the psychologist B. F. Skinner got a US government research contract for "
                 "'Project Pigeon': three pigeons in the nose cone of a guided bomb, each looking at the target through a lens "
                 "and pecking at its image on a screen – the pecks moved the controls. In tests the trained birds kept pecking "
                 "on target, but the project was cancelled in October 1944 and never used in combat. The Navy revived it in "
                 "1948 as Project ORCON ('organic control') and cancelled it in 1953, once electronic guidance proved reliable."
                 "\n\nIllustrations painted with code (no photos), narration is synthetic."),
    tags=['project pigeon', 'pigeon guided missile', 'bf skinner', 'project orcon', 'weird war tech', 'ww2', 'military history'],
    voice='am_michael',
    lines=["Inside this missile's nose: three pigeons. Steering.",
           "They pecked at the target, and the missile followed.",
           "Each bird saw the target through a lens. Every peck nudged the controls.",
           "In tests, the trained pigeons kept pecking right on target.",
           "Still, the project was canceled in nineteen forty-four. Never used in combat.",
           "After the war, the navy tried again. Canceled in nineteen fifty-three."],
    gaps=[0.15, 0.35, 0.35, 0.35, 0.4, 0.4],
    display=[(4, 'nineteen', '1944.'), (4, 'forty-four.', ''), (5, 'nineteen', '1953.'), (5, 'fifty-three.', '')],
    plates=[dict(stages=ST, show=[(0, 0), ('L1', 1), ('L2', 2)])],
    camera=[(0, 720, 960, 1820), ('L1', 720, 1000, 1900), ('L1@0.6', 720, 1000, 1900), ('L2', 720, 1700, 1550),
            ('L3', 720, 1780, 1550), ('END', 720, 1760, 1600)],
    cards=[dict(at=0, until='L1-0.2', text='3 PIGEONS. STEERING.', font='AlfaSlabOne-400', size=80, ink=(150, 34, 26), x=540, y=1560, rot=-3)],
    caption=dict(y=0.9),
    stamps=[dict(at='L3:target', text='IT WORKED', size=110, color=(170, 30, 24), x=540, y=470, rot=-7),
            dict(at='L4:canceled', text='CANCELED', size=110, color=(170, 30, 24), x=560, y=660, rot=-8)],
    music=dict(sections=[(0, 'L2', ['Dm9', 'Am9'], dict(bright=(0.2, 0.35), pulse=True)),
                         ('L2', 'L4', ['Esus', 'Dm9'], dict(bright=(0.35, 0.5), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.4, 0.25), gain=(1, 0.0)))]),
)
