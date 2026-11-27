"""Myth Dug Up #012 (news) — the FCC authorizes SpaceX's "Starmind": up to one million data-center satellites.
Plates: a cut-and-paste collage with a halftone satellite and ransom letters (newscollage), and a data sheet comparing
today's Starlink fleet with the authorized number, the deployment deadlines and who objected (blueprint). No logos,
no likeness.
Facts (FCC order DA-26-1273A1, 25 Nov 2026; Reuters 25 Nov 2026; Via Satellite 25 Nov 2026; Spaceflight Now 26 Nov 2026):
- FCC granted SpaceX authority for up to 1,000,000 optically linked satellites ("Starmind"), orbital data centers for AI
  compute, at 500-1,002 km altitude in 50 km shells. SpaceX filed on 30 Jan 2026.
- Milestones: first satellite by 25 Nov 2033, 10% by 2035, 50% by 2038, full constellation by 25 Nov 2040.
- Petitions to deny from Viasat, Amazon (Leo) and the American Astronomical Society were rejected. The FCC deferred
  SpaceX's request to dispose of satellites in graveyard/heliocentric orbits (affects satellites above 600 km).
- Starlink today: nearly 11,200 spacecraft in orbit (Jonathan McDowell, cited by Spaceflight Now).
- SpaceX says first launch Q3 2027 (Musk); design figures (175 kW average compute) are company claims.
Facts as of 27 Nov 2026."""
from pathlib import Path
from newscollage import NewsCollage, Photo, RED, INK, MUSTARD
from blueprint import Blueprint

W, H = 1440, 2560


def satellite_photo():
    p = Photo(1000, 760, seed=12)
    # solar wings left and right, a box body in the middle
    for x0 in (40, 600):
        p.poly([(x0, 250), (x0 + 360, 210), (x0 + 360, 470), (x0, 510)], height=6, bevel=2, albedo=0.22, metal=0.4, gloss=0.7)
        for k in range(1, 6):
            xx = x0 + k * 60
            p.lines([[(xx, 250 - (xx - x0) * 0.111 + 4), (xx, 510 - (xx - x0) * 0.111 - 4)]], 3, tone=0.6)
        p.lines([[(x0 + 4, 380 - 0), (x0 + 356, 340)]], 3, tone=0.6)
    p.rod((400, 360), (600, 360), 14, z=6, albedo=0.7, metal=1.0)
    p.poly([(420, 230), (580, 230), (580, 500), (420, 500)], z=8, height=24, bevel=5, albedo=0.85, metal=0.6, gloss=0.5)
    p.disc(500, 600, 70, z=10, height=10, bevel=3, albedo=0.9, metal=0.2, gloss=0.6)
    p.rod((500, 500), (500, 540), 10, z=8, albedo=0.7, metal=1.0)
    p.text('AI', 500, 380, 90, font='didone', tone=0.1)
    p.glare(380, 250, 120, 300, 200, 250, strength=0.4)
    return p


def paint_collage(out):
    nc = NewsCollage(W, H, seed=121)
    nc.board()
    for (w, h, x, y, r, sides) in ((980, 1300, 470, 760, -4, 'rb'), (900, 1200, 1010, 1650, 5, 'lt'), (820, 900, 430, 2160, -2, 'rt')):
        s = nc.newsprint(w, h, columns=3); s.tear(sides); nc.paste(s, x, y, rot=r)
    nc.stage('board')
    nc.disc(720, 1230, 520, RED)
    s = nc.print_photo(satellite_photo()); s.cutout(14); nc.paste(s, 720, 1230, rot=-8)
    nc.stage('sat')
    nc.ransom('APPROVED:', 190, 300, 130, rot=2)
    nc.ransom('1,000,000', 170, 560, 120, rot=-2)
    nc.tape(220, 220, 200, rot=-12); nc.tape(1250, 200, 200, rot=10)
    nc.stage('ransom')
    nc.label('DATA CENTERS IN ORBIT', 150, 1880, 62, face='typewriter_bold', rot=3)
    nc.stage('dc')
    nc.label('ALL BY 2040', 220, 2290, 70, face='typewriter_bold', block=MUSTARD, rot=-2)
    nc.tape(230, 2280, 160, rot=70)
    nc.stage('year')
    nc.stamp(1110, 1700, ['FCC', 'APPROVED'], rot=12)
    nc.stage('stamp')
    nc.save(str(out / 'collage.png'), stages_dir=str(out / 'collage'))


def paint_sheet(out):
    bp = Blueprint(W, H, seed=122)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('STARMIND AUTHORIZATION', W / 2, 190, 56, 'ms', pen=2.2, spacing=0.2)
    bp.text('FCC ORDER · 25 NOV 2026', W / 2, 250, 28, 'ms')
    bp.stage('sheet')
    # fleet comparison: a 1,000-cell grid = one million; Starlink today fills ~11 cells
    gx0, gy0, cell, cols = 170, 380, 36, 30
    for i in range(cols + 1):
        bp.line([(gx0 + i * cell, gy0), (gx0 + i * cell, gy0 + 20 * cell)], 'fine')
    for j in range(21):
        bp.line([(gx0, gy0 + j * cell), (gx0 + cols * cell, gy0 + j * cell)], 'fine')
    bp.box(gx0, gy0, gx0 + cols * cell, gy0 + 20 * cell, 'heavy')
    bp.text('EACH SQUARE = 1,666 SATELLITES', W / 2, gy0 + 20 * cell + 60, 30, 'ms')
    bp.stage('grid')
    bp.hatch([[(gx0, gy0), (gx0 + 7 * cell, gy0), (gx0 + 7 * cell, gy0 + cell), (gx0, gy0 + cell)]], angle=45, spacing=7, pen='thick')
    bp.red([(gx0 + 3.5 * cell, gy0 + cell + 10), (gx0 + 5 * cell, gy0 + 3 * cell)])
    bp.red_text('STARLINK TODAY: ~11,200', gx0 + 3 * cell, gy0 + 4.5 * cell, 90, rot=-2)
    bp.stage('today')
    bp.text('WHOLE GRID: 1,000,000 APPROVED', W / 2, gy0 + 20 * cell + 120, 38, 'ms', pen=2.2)
    bp.stage('whole')
    bx, by, rh = 150, 1360, 130
    rows = (('FIRST SATELLITE', 'BY 2033'), ('HALF', 'BY 2038'), ('ALL', 'BY 2040'), ('ALTITUDE', '500-1,002 KM'))
    bp.view_title(720, 1300, 'DEADLINES SET BY THE FCC', size=30)
    bp.table(bx, by, [560, 580], [rh] * 4, pen='thin', outer='heavy')
    for i, (a, v) in enumerate(rows):
        yy = by + i * rh + 82
        bp.text(a, bx + 24, yy, 38, 'ls', pen=1.8)
        bp.text(v, bx + 584, yy, 40, 'ls', pen=2.0)
    bp.stage('deadlines')
    bp.view_title(720, 1960, 'OBJECTIONS - REJECTED', size=30)
    bp.text('ASTRONOMERS · AMAZON · VIASAT', W / 2, 2060, 42, 'ms', pen=2.0)
    bp.cloud([(200, 2000), (1240, 2000), (1240, 2100), (200, 2100)])
    bp.red_text('PETITIONS DENIED', 720, 2240, 54, rot=2, anchor='ms')
    bp.stage('objections')
    bp.fold(xs=(720,), ys=(1280,), wear=0.7)
    bp.stain(1220, 2420, 70, 0.6)
    bp.save(str(out / 'sheet.png'), str(out / 'sheet'))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_collage(out)
    paint_sheet(out)


PH = 2560
A = ['collage/%s.png' % n for n in ('00_board', '01_sat', '02_ransom', '03_dc', '04_year', '05_stamp', '06_final')]
B = ['sheet/%s.png' % n for n in ('00_sheet', '01_grid', '02_today', '03_whole', '04_deadlines', '05_objections', '06_final')]

EPISODE = dict(
    chapter='SpaceX Starmind',
    title="SpaceX Got Approval for 1 Million Satellites. It Has 11,000. #shorts",
    description=("On 25 November the U.S. Federal Communications Commission authorized SpaceX to launch up to one million "
                 "satellites for \"Starmind\", a constellation of solar-powered data centers meant to run AI computing in orbit, "
                 "between 500 and 1,002 km altitude. Starlink has about 11,200 satellites in orbit today. The FCC set deadlines: "
                 "the first satellite by 2033, half by 2038, all by 2040. Petitions from the American Astronomical Society, "
                 "Amazon and Viasat were rejected; the FCC deferred SpaceX's request for graveyard-orbit disposal.\n\n"
                 "Proven: the FCC granted the authorization (official order).\n"
                 "Debated: whether data centers in orbit can work at this scale, and what a million satellites mean for "
                 "astronomy and space debris.\n\n"
                 "Sources: FCC order, Reuters, Via Satellite, Spaceflight Now.\n"
                 "Illustrations painted with code (no photos), narration is synthetic. Facts as of 27 Nov 2026."),
    tags=['spacex', 'starmind', 'starlink', 'fcc', 'satellites', 'orbital data centers', 'space news', 'ai', 'news'],
    voice='bm_george',
    lines=["One million satellites. Just approved.",
           "This week, America's FCC cleared SpaceX to launch up to one million satellites. Starlink has about eleven thousand today.",
           "These aren't for internet. They're flying data centers, built to run AI in orbit, powered by the sun.",
           "Today's fleet is this tiny corner. The first must fly by twenty thirty-three, all by twenty forty. Astronomers, Amazon and Viasat objected. The FCC said no.",
           "Proven: the approval is official. Debated: whether a million data centers in orbit can really work."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(0, 'One', '1'), (1, 'one', '1'), (1, 'eleven', '11,000'), (1, 'thousand', '')],
    plates=[dict(stages=A, show=[(0, 2), ('L1:cleared', 3), ('L2', 4), ('L3', 5), ('L3:astronomers', 6)]),
            dict(stages=B, show=[(0, 1), ('L3-0.3', 2), ('L3:tiny', 3), ('L3:first-0.4', 4), ('L3:astronomers', 5), ('L4', 6)])],
    camera=[(0, 720, 1180, 2300), ('L0.end', 720, 1230, 2350), ('L1+0.2', 720, 1300, 2300), ('L1:starlink', 720, 1250, 2350),
            ('L2', 720, 1450, 2200), ('L2.end', 720, 1500, 2150),
            ('L3-0.1', 720, PH + 1000, 2000), ('L3:tiny', 720, PH + 1000, 1950), ('L3:first-0.4', 720, PH + 1000, 1950), ('L3:first', 720, PH + 1450, 2200), ('L3:astronomers', 720, PH + 1450, 2200), ('L4', 720, PH + 1300, 2450),
            ('END', 720, PH + 1300, 2500)],
    cards=[dict(at=0, until='L1-0.1', text='90X STARLINK', font='AlfaSlabOne-400', size=96, ink=(160, 32, 24), x=540, y=1780, rot=-3),
           dict(at='L1:starlink', until='L2-0.1', text='TODAY: 11,200', font='AlfaSlabOne-400', size=88, x=540, y=1720, rot=2),
           dict(at='L2:flying', until='L2.end', text='AI IN ORBIT', size=80, x=540, y=1720, rot=-2)],
    stamps=[dict(at='L4:proven', text='PROVEN', size=100, color=(30, 70, 52), x=540, y=560, rot=-6),
            dict(at='L4:debated', text='DEBATED', size=100, color=(160, 32, 24), x=560, y=780, rot=5)],
    music=dict(sections=[(0, 'L1', ['Dm9', 'Am9'], dict(bright=(0.3, 0.45), pulse=True)),
                         ('L1', 'L2', ['Esus', 'Dm9'], dict(bright=(0.45, 0.6), pulse=True, ticks=True)),
                         ('L2', 'L4', ['Fmaj7', 'Esus'], dict(bright=(0.5, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
