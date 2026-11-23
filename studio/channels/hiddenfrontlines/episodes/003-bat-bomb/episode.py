"""HiddenFrontlines #003 — Weird War Tech #2: the bat bomb (Project X-Ray), blueprint.
Facts (army.mil 'Bats over Tokyo', C. Crane 2008; NPS 'Bat Bombs and Balloons on Fire'; Wikipedia 'Bat bomb'):
idea by dentist Dr. Lytle S. Adams, letter to President Roosevelt, January 1942; Mexican free-tailed bats, each fitted
with a small timed incendiary, released from a casing of hibernating bats over Japanese cities to roost in roofs;
1943: armed bats escaped at the Carlsbad (New Mexico) army airfield's auxiliary base and set much of it on fire;
the Navy (and then the Marines) took over; dropped in 1944."""
from pathlib import Path
from blueprint import Blueprint

ST = ['print/%s.png' % n for n in ('00_bat', '01_callouts', '02_casing', '03_base', '04_block')]


def wing(side):
    pts = [(40, -40), (300, -160), (470, -100), (540, 20), (460, 50), (390, 30), (320, 100), (240, 80), (160, 130), (40, 40)]
    return [(720 + side * x, 820 + y) for x, y in pts]


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    bp = Blueprint(W, H, seed=29)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('INCENDIARY BAT — FRONT VIEW', W / 2, 200, 46, 'ms', pen=2.2, spacing=0.18)
    bp.text('PROJECT X-RAY · 1943', W / 2, 255, 26, 'ms')
    for s in (-1, 1):
        bp.line(wing(s), 'heavy', closed=True)
        bp.hatch([wing(s)], angle=60 * s, spacing=16, pen='fine')
        for x, y in ((300, -160), (470, -100), (540, 20)):          # wing bones
            bp.line([(720 + s * 50, 790), (720 + s * x, 820 + y)], 'thin')
    bp.circle(720, 830, 70, 'heavy', ry=110)
    bp.circle(720, 700, 52, 'heavy')
    for s in (-1, 1):
        bp.line([(720 + s * 18, 660), (720 + s * 50, 590), (720 + s * 50, 668)], 'heavy')
    bp.box(700, 950, 740, 1060, 'heavy')                         # the incendiary capsule
    bp.line([(720, 940), (720, 950)], 'thick')
    bp.dim((180, 1100), (1260, 1100), 40, 'NOT TO SCALE', size=24)
    bp.stage('bat')
    bp.leader([(740, 1010), (980, 1230), (1180, 1230)], 'TIMED INCENDIARY', size=24)
    bp.leader([(500, 900), (380, 1230), (180, 1230)], 'MEXICAN FREE-TAILED BAT', size=22)
    bp.stage('callouts')
    bp.view_title(720, 1380, 'DROP CASING', size=28)
    case = [(420, 1450), (1020, 1450), (1080, 1520), (1020, 1590), (420, 1590), (360, 1520)]
    bp.line(case, 'heavy', closed=True)
    for x in range(470, 1000, 60):
        bp.line([(x, 1460), (x, 1580)], 'thin')
    bp.line([(1080, 1520), (1180, 1450), (1180, 1590), (1080, 1520)], 'medium')
    bp.text('TRAYS OF HIBERNATING BATS', 720, 1660, 24, 'ms', pen=1.6)
    bp.stage('casing')
    bp.view_title(720, 1790, 'AIRFIELD · NEW MEXICO · 1943', size=26)
    bp.ground([(160, 2070), (1280, 2070)])
    for x0, w, h in ((200, 260, 150), (520, 360, 190), (940, 280, 130)):
        bp.line([(x0, 2070), (x0, 2070 - h), (x0 + w / 2, 2070 - h - 60), (x0 + w, 2070 - h), (x0 + w, 2070)], 'heavy')
    bp.box(1170, 1850, 1240, 1930, 'heavy'); bp.line([(1205, 1930), (1205, 2070)], 'thick')
    for x in (300, 650, 760, 1040, 1205):
        b = 2070 - (150 if x < 500 else 190 if x < 900 else 130) - 10
        bp.red([(x - 30, b), (x - 38, b - 50), (x - 12, b - 95), (x, b - 150), (x + 14, b - 85), (x + 36, b - 52), (x + 30, b), (x - 30, b)], width=3.2)
    bp.text('BATS ROOSTED IN THE BUILDINGS', 720, 2140, 24, 'ms', pen=1.6)
    bp.stage('base')
    x0, y0 = 120, 2290
    bp.table(x0, y0, [400, 400, 400], [50, 80], pen='thin', outer='medium')
    for i, (lab, val) in enumerate((('PROJECT', 'X-RAY'), ('IDEA', 'DR. LYTLE S. ADAMS'), ('STATUS', 'DROPPED 1944'))):
        bp.text(lab, x0 + i * 400 + 14, y0 + 24, 16, 'ls')
        bp.text(val, x0 + i * 400 + 200, y0 + 100, 24, 'ms', pen=1.6)
    bp.stage('block')
    bp.fold(xs=(720,), ys=(1280,), wear=0.8)
    bp.stain(260, 1500, 80, 0.6)
    bp.save(str(out / 'print.png'), str(out / 'print'))


EPISODE = dict(
    chapter='The Bat Bomb',
    title="The US Strapped Firebombs to Bats. They Burned Their Own Base. #shorts",
    description=("Weird War Tech #2. In 1942 a Pennsylvania dentist, Dr. Lytle S. Adams, wrote to President Roosevelt with a plan: "
                 "release hibernating Mexican free-tailed bats over Japanese cities, each carrying a tiny timed incendiary, so they "
                 "would roost in roofs and start fires. In 1943 armed bats escaped at an army airfield near Carlsbad, New Mexico, "
                 "and set much of it on fire. The Navy and the Marines kept testing as 'Project X-Ray', but the project was "
                 "dropped in 1944.\n\nIllustrations painted with code (no photos), narration is synthetic."),
    tags=['bat bomb', 'project x-ray', 'ww2', 'weird war tech', 'military history', 'carlsbad', 'history shorts'],
    voice='am_michael',
    lines=["America armed bats with fire bombs.",
           "The idea came from a dentist, Little Adams, who wrote to President Roosevelt in nineteen forty-two.",
           "Sleeping bats would be dropped over Japanese cities, and roost in the roofs. Each one with a tiny timed firebomb.",
           "Then, in nineteen forty-three, armed bats escaped at an airfield in New Mexico.",
           "They roosted in the buildings, and burned much of the base.",
           "The Navy and the Marines kept testing. In nineteen forty-four, the project was dropped."],
    gaps=[0.15, 0.35, 0.35, 0.4, 0.3, 0.45],
    display=[(1, 'little', 'Lytle'), (1, 'nineteen', '1942.'), (1, 'forty-two.', ''), (3, 'nineteen', '1943,'), (3, 'forty-three,', ''),
             (5, 'nineteen', '1944,'), (5, 'forty-four,', '')],
    plates=[dict(stages=ST, show=[(0, 0), ('L1', 1), ('L2', 2), ('L3', 3), ('L5:dropped', 4)])],
    camera=[(0, 720, 1000, 1900), ('L1', 720, 1050, 2000), ('L2', 720, 1450, 1500), ('L2:each', 720, 1000, 1500),
            ('L3', 720, 1910, 1300), ('L4', 720, 1960, 1200), ('L5', 720, 1900, 1300), ('END', 720, 1900, 1300)],
    cards=[dict(at=0, until='L1-0.2', text='ARMED BATS.', font='AlfaSlabOne-400', size=100, ink=(150, 34, 26), x=540, y=1200, rot=-3)],
    stamps=[dict(at='L4:burned', text='OOPS', size=120, color=(170, 30, 24), x=760, y=500, rot=-8),
            dict(at='L5:dropped', text='CANCELLED', size=110, color=(170, 30, 24), x=540, y=1700, rot=-8)],
    music=dict(sections=[(0, 'L2', ['Dm9', 'Am9'], dict(bright=(0.2, 0.35), pulse=True)),
                         ('L2', 'L4', ['Esus', 'Dm9'], dict(bright=(0.35, 0.5), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.4, 0.25), gain=(1, 0.0)))]),
)
