"""HiddenFrontlines #001 — the Ghost Army (23rd Headquarters Special Troops, US Army, 1944-45).
Plate: a contact-printed blueprint of an inflatable dummy tank, sonic and radio deception (claude-drawing-skill: blueprint).
Facts (National WWII Museum, Smithsonian, Ghost Army Legacy Project): about 1,100 men, many artists and designers;
inflatable tanks and vehicles, sonic deception (recorded sounds from speaker trucks), fake radio traffic;
missions kept secret for decades — much of the record was declassified in 1996."""
from pathlib import Path
import numpy as np
from blueprint import Blueprint

ST = ['print/%s.png' % n for n in ('00_sheet', '01_tank', '02_seams', '03_sound', '04_radio', '05_block')]


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    bp = Blueprint(W, H, seed=19)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('DUMMY TANK — INFLATABLE', W / 2, 330, 52, 'ms', pen=2.2, spacing=0.2)
    bp.text('23RD HEADQUARTERS SPECIAL TROOPS · 1944', W / 2, 395, 26, 'ms')
    bp.stage('sheet')
    # tank, side elevation
    hull = [(250, 1080), (330, 980), (1080, 980), (1190, 1060), (1190, 1135), (250, 1135)]
    bp.line(hull, 'heavy', closed=True)
    turret = [(560, 980), (600, 860), (860, 860), (905, 980)]
    bp.line(turret, 'heavy', closed=True)
    bp.box(905, 895, 1320, 925, 'heavy')
    bp.line([(230, 1150), (1210, 1150), (1250, 1200), (1210, 1255), (230, 1255), (190, 1200)], 'heavy', closed=True)
    for x in range(320, 1140, 130):
        bp.circle(x, 1202, 46, 'thick'); bp.circle(x, 1202, 12, 'thin')
    bp.ground([(150, 1262), (1290, 1262)])
    bp.dim((230, 1262), (1250, 1262), 70, 'FULL SIZE', size=22)
    bp.stage('tank')
    for x in (420, 600, 780, 960):
        bp.dashed([(x, 985), (x, 1132)], 'fine')
    bp.dashed([(255, 1035), (1150, 1035)], 'fine')
    bp.dot(700, 1100, 6)
    bp.leader([(700, 1100), (560, 760), (360, 760)], 'AIR VALVE', size=24)
    bp.leader([(1000, 1010), (1100, 760), (1240, 760)], 'RUBBER', size=24)
    bp.stage('seams')
    # sonic deception: a half-track with a speaker
    bp.view_title(390, 1500, 'SONIC DECEPTION', size=28)
    bp.line([(170, 1820), (560, 1820), (560, 1700), (450, 1700), (420, 1640), (300, 1640), (300, 1700), (170, 1700)], 'heavy', closed=True)
    for x in (230, 330, 500):
        bp.circle(x, 1840, 32, 'medium')
    bp.line([(440, 1640), (470, 1580), (540, 1560), (540, 1660), (470, 1640)], 'medium', closed=True)
    for k in range(1, 5):
        bp.arc(560, 1610, 40 + k * 34, -55, 55, 'fine', dash=(8, 6))
    bp.text('RECORDED TANK SOUNDS', 390, 1940, 22, 'ms')
    bp.stage('sound')
    # radio deception: a mast and fake traffic
    bp.view_title(1050, 1500, 'RADIO DECEPTION', size=28)
    bp.line([(1050, 1880), (1050, 1600)], 'thick')
    bp.line([(980, 1880), (1050, 1700), (1120, 1880)], 'medium')
    for k in range(1, 5):
        bp.arc(1050, 1600, 30 + k * 32, -150, -30, 'fine', dash=(8, 6))
    bp.text('FAKE RADIO TRAFFIC', 1050, 1940, 22, 'ms')
    bp.stage('radio')
    # title block
    x0, y0 = 120, 2120
    bp.table(x0, y0, [400, 400, 400], [70, 90], pen='thin', outer='medium')
    for i, (lab, val) in enumerate((('UNIT', 'GHOST ARMY'), ('STRENGTH', '≈ 1,100 MEN'), ('STATUS', 'DECLASSIFIED 1996'))):
        bp.text(lab, x0 + i * 400 + 14, y0 + 30, 16, 'ls')
        bp.text(val, x0 + i * 400 + 200, y0 + 125, 26, 'ms', pen=1.6)
    bp.stage('block')
    bp.fold(xs=(720,), ys=(1280,), wear=0.8)
    bp.stain(1180, 1450, 90, 0.7)
    bp.save(str(out / 'print.png'), str(out / 'print'))


EPISODE = dict(
    chapter='The Ghost Army',
    title="The US Army Fought With Rubber Tanks. It Worked. #shorts",
    description=("In 1944 a secret US unit — the 23rd Headquarters Special Troops, the 'Ghost Army' — used inflatable tanks, "
                 "recorded battle sounds and fake radio traffic to fool the enemy. About 1,100 men, many of them artists. "
                 "Their story stayed secret for decades; much of it was declassified in 1996.\n\n"
                 "Illustration painted with code as a blueprint (no photos), narration is synthetic."),
    tags=['ghost army', 'ww2', 'world war 2', 'inflatable tanks', 'military history', 'deception', 'history shorts'],
    voice='am_michael',
    lines=["In nineteen forty-four, the US Army sent a secret unit to Europe, with tanks made of rubber.",
           "They were called the Ghost Army. About eleven hundred soldiers, many of them artists and designers.",
           "Inflatable tanks. Fake radio traffic. Speakers that played the sounds of an entire division.",
           "Their job: make the enemy see an army where there was none.",
           "And their missions stayed classified for decades."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(0, 'nineteen', '1944,'), (0, 'forty-four,', ''), (1, 'eleven', '1,100'), (1, 'hundred', '')],
    plates=[dict(stages=ST, show=[(0, 1), (1.2, 2), ('L2:fake', 4), ('L4', 5)])],
    camera=[(0, 740, 1080, 950), ('L0.end', 740, 1040, 1350), ('L1', 720, 1180, 2300), ('L2', 720, 1080, 1300), ('L2:fake-0.3', 720, 1100, 1350),
            ('L2:fake+0.4', 980, 1720, 1100), ('L2:speakers', 420, 1720, 1100), ('L3', 720, 1250, 2350), ('L4', 720, 1700, 2200),
            ('END', 720, 1270, 2400)],
    cards=[dict(at='L1:ghost', until='L2-0.2', text='THE GHOST ARMY', size=80, x=540, y=560, rot=-3),
           dict(at='L1:eleven', until='L2-0.2', text='≈ 1,100 MEN', font='AlfaSlabOne-400', size=88, ink=(150, 34, 26), x=560, y=1180, rot=3)],
    stamps=[dict(at='L4:classified', text='CLASSIFIED', size=110, color=(170, 30, 24), x=540, y=780, rot=-8),
            dict(at='L4:decades', text='UNTIL 1996', size=70, color=(170, 30, 24), x=600, y=990, rot=-8)],
    music=dict(sections=[(0, 'L2', ['Dm9', 'Am9'], dict(bright=(0.2, 0.35), pulse=True)),
                         ('L2', 'L4', ['Esus', 'Dm9'], dict(bright=(0.35, 0.5), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.4, 0.25), gain=(1, 0.0)))]),
)
