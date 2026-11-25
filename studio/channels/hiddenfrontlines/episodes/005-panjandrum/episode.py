"""HiddenFrontlines #005 — Weird War Tech #4: the Great Panjandrum (blueprint).
Facts (The Past, 'Back to the drawing board: The Great Panjandrum', 2024; Amusing Planet 2024, quoting Brian Johnson's
account in the BBC documentary 'The Secret War', 1977; Wikipedia 'Panjandrum'): British Admiralty (DMWD) project to
breach the concrete defences of the Atlantic Wall, launched from a landing craft; two wheels about 10 ft (3 m) across
with cordite rockets on the rims and a central drum built for over a ton of explosives (production design 4,000 lb);
trials on the beach at Westward Ho!, Devon, 1943-44: rockets flew off, it veered off course; at the January 1944
demonstration for officials a clamp gave, rockets broke free, it turned back toward the shore and crashed on the sand;
Johnson's account: the cameraman (Klemantaski) kept filming and had to run. The project was scrapped, never used in
combat. No chase by a dog is claimed."""
from pathlib import Path
import math
from blueprint import Blueprint

ST = ['print/%s.png' % n for n in ('00_wheel', '01_callouts', '02_trial')]
WX, WY, WR = 720, 1000, 420


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    bp = Blueprint(W, H, seed=45)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('ROCKET-PROPELLED DEMOLITION WHEEL', W / 2, 200, 40, 'ms', pen=2.2, spacing=0.16)
    bp.text('SIDE ELEVATION', W / 2, 256, 28, 'ms')
    bp.circle(WX, WY, WR, 'heavy'); bp.circle(WX, WY, WR - 34, 'medium')
    bp.circle(WX, WY, 180, 'heavy'); bp.circle(WX, WY, 150, 'thin')           # the explosive drum
    bp.hatch([[(WX + 150 * math.cos(math.radians(a)), WY + 150 * math.sin(math.radians(a))) for a in range(0, 361, 10)]],
             angle=45, spacing=14, pen='fine')
    for k in range(12):                                                         # spokes
        a = math.radians(k * 30)
        bp.line([(WX + 180 * math.cos(a), WY + 180 * math.sin(a)), (WX + (WR - 34) * math.cos(a), WY + (WR - 34) * math.sin(a))], 'medium')
    for k in range(18):                                                         # rockets on the rim, tangential
        a = math.radians(k * 20 + 10)
        cx, cy = WX + (WR + 40) * math.cos(a), WY + (WR + 40) * math.sin(a)
        tx, ty = -math.sin(a), math.cos(a)
        nx, ny = math.cos(a), math.sin(a)
        L, w = 60, 15
        pts = [(cx - tx * L - nx * w, cy - ty * L - ny * w), (cx + tx * L - nx * w, cy + ty * L - ny * w),
               (cx + tx * (L + 22), cy + ty * (L + 22)),
               (cx + tx * L + nx * w, cy + ty * L + ny * w), (cx - tx * L + nx * w, cy - ty * L + ny * w)]
        bp.line(pts, 'heavy', closed=True)
        bp.line([(cx - tx * L, cy - ty * L), (cx - tx * (L + 40), cy - ty * (L + 40))], 'thin')   # exhaust
    bp.ground([(120, WY + WR + 10), (1320, WY + WR + 10)])
    bp.stage('wheel')
    bp.dim((WX - WR, WY + WR + 110), (WX + WR, WY + WR + 110), 0, '10 FT', size=30)
    bp.leader([(WX + 60, WY - 60), (WX + 80, WY - 600), (WX + 110, WY - 600)], '1 TON+ EXPLOSIVES', size=26)
    bp.leader([(WX - WR - 60, WY - 160), (300, WY - 600), (330, WY - 600)], 'ROCKETS', size=26)
    bp.stage('callouts')
    bp.view_title(720, 1800, 'BEACH TRIAL — DEVON', 'NOT TO SCALE', size=28)
    bp.box(150, 1860, 1290, 2380, 'heavy')
    shore = [(150, 2150), (400, 2130), (700, 2160), (1000, 2135), (1290, 2155)]
    bp.line(shore, 'medium')
    bp.hatch([shore + [(1290, 2380), (150, 2380)]], angle=0, spacing=18, pen='fine')
    bp.text('SEA', 1180, 2330, 24, 'ms')
    bp.text('SAND', 1180, 1920, 24, 'ms')
    path = [(420, 2340), (430, 2200), (470, 2060), (560, 1960), (690, 1930), (800, 1980), (830, 2080), (760, 2150)]
    bp.dashed(path, 'medium')
    bp.arrowhead(path[-1], (path[-1][0] - path[-2][0], path[-1][1] - path[-2][1]), size=20)
    bp.red([(735, 2130), (785, 2180)], width=5.0); bp.red([(785, 2130), (735, 2180)], width=5.0)
    bp.red_text('CRASH', 860, 2200, 40, rot=-4)
    bp.stage('trial')
    bp.fold(xs=(720,), ys=(1280,), wear=0.8)
    bp.stain(1220, 1500, 70, 0.5)
    bp.save(str(out / 'print.png'), str(out / 'print'))


EPISODE = dict(
    chapter='The Great Panjandrum',
    title="Britain Built a Rocket Wheel Bomb. It Went Out of Control. #shorts",
    description=("Weird War Tech #4. In 1943 the British Admiralty built the 'Great Panjandrum': two wheels about ten feet "
                 "(3 m) across, rockets on the rims and a drum in the middle built to hold over a ton of explosives. It was "
                 "meant to roll off a landing craft and blast holes in the concrete defences of the Atlantic Wall. In trials "
                 "on a beach in Devon, rockets flew off and it veered off course; at a demonstration in January 1944 it turned "
                 "back toward the shore and crashed on the sand – by one witness's account the cameraman had to run. "
                 "The project was scrapped and never used in combat.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['great panjandrum', 'panjandrum', 'weird war tech', 'ww2 weapons', 'failed weapons', 'd-day', 'military history'],
    voice='am_michael',
    lines=["Britain built a giant wheel. With rockets on it.",
           "On the beach test, the rockets tore loose, and it turned back toward the shore.",
           "The plan: roll off a landing ship and blast through the concrete Atlantic Wall.",
           "Each wheel was ten feet tall. The drum in the middle was built for over a ton of explosives.",
           "In nineteen forty-four, it crashed on the sand. A witness said the cameraman had to run.",
           "The Great Panjandrum was scrapped. It never went to war."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.4, 0.4],
    display=[(3, 'ten', '10'), (4, 'nineteen', '1944,'), (4, 'forty-four,', '')],
    plates=[dict(stages=ST, show=[(0, 0), ('L1@0.3', 2)])],
    camera=[(0, 720, 1040, 2000), ('L1', 720, 1040, 1950), ('L1@0.35', 760, 1905, 1300), ('L2', 720, 1100, 1900),
            ('L3', 720, 1050, 2000), ('L4', 760, 1905, 1300), ('L5', 720, 1280, 2480), ('END', 720, 1280, 2480)],
    cards=[dict(at=0, until='L1-0.2', text='ROCKET WHEEL BOMB', font='AlfaSlabOne-400', size=80, ink=(150, 34, 26),
                x=540, y=1600, rot=-3)],
    caption=dict(y=0.9),
    stamps=[dict(at='L1:loose', text='OOPS', size=110, color=(170, 30, 24), x=820, y=1480, rot=-7),
            dict(at='L5:scrapped', text='CANCELLED', size=110, color=(170, 30, 24), x=540, y=1180, rot=-8)],
    music=dict(sections=[(0, 'L2', ['Dm9', 'Am9'], dict(bright=(0.2, 0.35), pulse=True)),
                         ('L2', 'L4', ['Esus', 'Dm9'], dict(bright=(0.35, 0.5), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.4, 0.25), gain=(1, 0.0)))]),
)
