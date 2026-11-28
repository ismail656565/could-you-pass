"""Myth Dug Up #014 (news) — Chile's competition prosecutor asks a court to fine Apple about $80 million and open up iOS.
Plates: a cut-and-paste collage with a halftone locked smartphone and ransom letters (newscollage), and a case file with
the four alleged practices and the four demanded changes (blueprint). No logos (no apple shape), no likeness.
Facts (Reuters 27 Nov 2026; 9to5Mac 27 Nov 2026; Diario Financiero / Meganoticias 27 Nov 2026):
- Chile's Fiscalia Nacional Economica (FNE) filed a complaint (requerimiento) against Apple at the competition tribunal
  (TDLC): alleged abuse of a dominant position on iOS in Chile, from at least 2019 to now.
- Markets: app distribution on iOS and sales of paid digital goods inside apps.
- Alleged: no installing apps from the web (sideloading), no third-party app stores, developers must use Apple's
  in-app purchase system, anti-steering (developers may not tell users about cheaper prices or outside payment).
- FNE seeks a fine of about US$80 million (30% of sales of the related lines over the period) and orders to allow
  sideloading, other app stores, other in-app billing, and friction-free links to outside payment and other prices.
- Apple has defended the sideloading ban on security and privacy grounds; FNE calls that unnecessary and disproportionate.
  No new Apple statement. The tribunal has not ruled; these are allegations.
Facts as of 28 Nov 2026."""
from pathlib import Path
from newscollage import NewsCollage, Photo, RED, INK, MUSTARD
from blueprint import Blueprint

W, H = 1440, 2560


def phone_photo():
    p = Photo(640, 1120, seed=14)
    p.poly([(70, 40), (570, 40), (600, 80), (600, 1040), (570, 1080), (70, 1080), (40, 1040), (40, 80)],
           height=10, bevel=5, albedo=0.12, metal=0.5, gloss=0.7)
    p.poly([(70, 90), (570, 90), (570, 1030), (70, 1030)], z=10, height=2, bevel=1, albedo=0.55, metal=0.1, gloss=0.8)
    for r in range(4):                 # app icon grid
        for c in range(4):
            x, y = 110 + c * 115, 150 + r * 125
            p.poly([(x, y), (x + 80, y), (x + 80, y + 80), (x, y + 80)], z=12, height=3, bevel=2,
                   albedo=0.25 + 0.15 * ((r + c) % 3), metal=0.1, gloss=0.5)
    # padlock over the lower screen
    p.ring(320, 760, 95, 125, z=14, height=8, albedo=0.75, metal=1.0, gloss=0.6)
    p.poly([(190, 760), (450, 760), (450, 960), (190, 960)], z=16, height=12, bevel=4, albedo=0.7, metal=1.0, gloss=0.6)
    p.disc(320, 840, 22, z=28, height=3, albedo=0.1)
    p.poly([(310, 845), (330, 845), (336, 905), (304, 905)], z=28, height=3, albedo=0.1)
    p.glare(220, 300, 80, 300, 200, 250, strength=0.45)
    return p


def coin_photo():
    p = Photo(420, 420, seed=15)
    p.disc(210, 210, 190, height=12, bevel=5, albedo=0.7, metal=1.0, gloss=0.6)
    p.ring(210, 210, 150, 165, z=12, albedo=0.7, metal=1.0)
    p.text('$', 210, 220, 190, font='didone', tone=0.15)
    p.glare(160, 140, 60, 160, 200, 250, strength=0.5)
    return p


def paint_collage(out):
    nc = NewsCollage(W, H, seed=141)
    nc.board()
    for (w, h, x, y, r, sides) in ((980, 1300, 470, 760, -4, 'rb'), (900, 1200, 1010, 1650, 5, 'lt'), (820, 900, 430, 2160, -2, 'rt')):
        s = nc.newsprint(w, h, columns=3); s.tear(sides); nc.paste(s, x, y, rot=r)
    nc.stage('board')
    nc.disc(720, 1250, 560, RED)
    s = nc.print_photo(phone_photo()); s.cutout(14); nc.paste(s, 720, 1250, rot=-6)
    nc.stage('phone')
    nc.ransom('CHILE vs', 260, 400, 92, rot=2)
    nc.ransom('THE iPHONE', 170, 620, 88, rot=-2)
    nc.tape(240, 320, 200, rot=-12); nc.tape(1250, 300, 200, rot=10)
    nc.stage('ransom')
    s = nc.print_photo(coin_photo()); s.cutout(10); nc.paste(s, 1170, 1720, rot=12)
    nc.label('FINE SOUGHT: $80,000,000', 130, 1980, 60, face='typewriter_bold', rot=3)
    nc.stage('fine')
    nc.label('ONE STORE. ONE CHECKOUT.', 130, 2290, 62, face='typewriter_bold', block=MUSTARD, rot=-2)
    nc.tape(150, 2280, 160, rot=70)
    nc.stage('store')
    nc.stamp(1080, 2120, ['NOT', 'YET RULED'], rot=-10)
    nc.stage('stamp')
    nc.save(str(out / 'collage.png'), stages_dir=str(out / 'collage'))


def paint_sheet(out):
    bp = Blueprint(W, H, seed=142)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('CASE FILE: FNE v. APPLE', W / 2, 190, 50, 'ms', pen=2.2, spacing=0.2)
    bp.text('CHILE COMPETITION TRIBUNAL · SINCE 2019', W / 2, 250, 28, 'ms')
    bp.stage('sheet')
    bp.view_title(720, 380, 'WHAT IS ALLEGED', size=34)
    rows = (('1', 'NO APPS FROM THE WEB'), ('2', 'NO OTHER APP STORES'), ('3', "APPLE'S PAYMENT ONLY"),
            ('4', 'NO "CHEAPER ELSEWHERE"'))
    bx, by, rh = 150, 440, 150
    bp.table(bx, by, [160, 980], [rh] * 4, pen='thin', outer='heavy')
    for i, (a, v) in enumerate(rows):
        yy = by + i * rh + 98
        bp.text(a, bx + 55, yy, 56, 'ls', pen=2.2)
        bp.text(v, bx + 200, yy, 44, 'ls', pen=2.0)
        if i == 1:
            bp.stage('rows')
    bp.stage('rows2')
    bp.view_title(720, 1180, 'WHAT CHILE DEMANDS', size=34)
    dem = (('OTHER APP STORES', 1300), ('OTHER PAYMENT BUTTONS', 1420), ('LINKS TO CHEAPER PRICES', 1540))
    for t, y in dem:
        bp.box(190, y - 50, 250, y + 10, 'heavy')
        bp.red([(198, y - 20), (215, y), (245, y - 48)], width=6)
        bp.text(t, 290, y, 46, 'ls', pen=2.0)
    bp.stage('demands')
    bp.red_text('~$80 MILLION FINE', 720, 1820, 110, rot=-3, anchor='ms')
    bp.text('30% OF RELATED SALES', W / 2, 1910, 32, 'ms')
    bp.stage('fine')
    bp.cloud([(200, 2040), (1240, 2040), (1240, 2300), (200, 2300)])
    bp.text('APPLE: RULES PROTECT', W / 2, 2140, 48, 'ms', pen=2.2)
    bp.text('SECURITY & PRIVACY', W / 2, 2230, 48, 'ms', pen=2.2)
    bp.stage('apple')
    bp.fold(xs=(720,), ys=(1280,), wear=0.7)
    bp.stain(1220, 2420, 70, 0.6)
    bp.save(str(out / 'sheet.png'), str(out / 'sheet'))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_collage(out)
    paint_sheet(out)


PH = 2560
A = ['collage/%s.png' % n for n in ('00_board', '01_phone', '02_ransom', '03_fine', '04_store', '05_stamp', '06_final')]
B = ['sheet/%s.png' % n for n in ('00_sheet', '01_rows', '02_rows2', '03_demands', '04_fine', '05_apple', '06_final')]

EPISODE = dict(
    chapter='Chile vs Apple',
    title="Chile Just Came for Apple's App Store… #shorts",
    description=("Chile's competition prosecutor (FNE) has asked the country's competition tribunal to fine Apple about "
                 "$80 million for allegedly abusing its dominance on iOS since at least 2019. The complaint says iPhone users "
                 "in Chile cannot install apps from the web or use other app stores, developers must use Apple's in-app "
                 "payment system, and apps may not tell users about cheaper prices elsewhere. The FNE wants the tribunal to "
                 "order other app stores, other payment systems and friction-free links to outside payment. Apple has "
                 "defended its rules on security and privacy grounds. The tribunal has not ruled.\n\n"
                 "Proven: the complaint has been filed with Chile's competition tribunal.\n"
                 "Debated: whether Apple broke Chilean competition law - these are allegations, not a ruling.\n\n"
                 "Sources: Reuters, 9to5Mac, Diario Financiero, FNE complaint.\n"
                 "Illustrations painted with code (no photos), narration is synthetic. Facts as of 28 Nov 2026."),
    tags=['apple', 'app store', 'iphone', 'chile', 'antitrust', 'sideloading', 'fne', 'tech news', 'news'],
    voice='bm_george',
    lines=["Chile wants to crack open the iPhone.",
           "Its competition prosecutor is asking a court to fine Apple about eighty million dollars, for allegedly abusing its App Store power since twenty nineteen.",
           "The charge: no app stores but Apple's, no apps from the web, and developers forced to use Apple's payment system.",
           "But the fine isn't the point. Chile wants other app stores, other payment buttons, and links to cheaper prices. Apple says its rules protect security and privacy.",
           "Proven: the complaint was filed. Debated: whether Apple broke the law."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(1, 'eighty', '$80'), (1, 'million', 'MILLION'), (1, 'dollars,', ''),
             (1, 'twenty', '2019'), (1, 'nineteen.', '')],
    plates=[dict(stages=A, show=[(0, 2), ('L1:fine', 3), ('L2', 4), ('L2:developers', 5)]),
            dict(stages=B, show=[(0, 1), ('L2:no#2', 2), ('L3', 3), ('L3:apple', 4), ('L4', 6)])],
    camera=[(0, 720, 1150, 2300), ('L0.end', 720, 1200, 2350), ('L1+0.2', 720, 1450, 2300), ('L1:fine', 720, 1600, 2250),
            ('L1.end', 720, 1550, 2300),
            ('L2-0.1', 720, PH + 1050, 2100), ('L2.end', 720, PH + 1100, 2150),
            ('L3-0.1', 720, PH + 1500, 2100), ('L3:apple', 720, PH + 1530, 2000), ('L4', 720, PH + 1300, 2450),
            ('END', 720, PH + 1300, 2500)],
    cards=[dict(at=0, until='L1-0.1', text='BREAKING', font='AlfaSlabOne-400', size=78, paper=(178, 30, 24), ink=(250, 246, 238),
                tape=False, x=540, y=95, rot=0),
           dict(at=0, until='L1-0.1', text='$80M vs APPLE', font='AlfaSlabOne-400', size=92, paper=(252, 250, 246), x=540, y=1700, rot=-2),
           dict(at='L2', until='L3-0.1', text='ONE STORE ONLY?', font='AlfaSlabOne-400', size=84, x=540, y=1720, rot=2),
           dict(at='L3', until='L4-0.1', text='OPEN IT UP', size=84, x=540, y=1720, rot=-2)],
    stamps=[dict(at='L4:proven', text='PROVEN', size=100, color=(30, 70, 52), x=540, y=560, rot=-6),
            dict(at='L4:debated', text='DEBATED', size=100, color=(160, 32, 24), x=560, y=780, rot=5)],
    music=dict(sections=[(0, 'L1', ['Dm9', 'Am9'], dict(bright=(0.3, 0.45), pulse=True)),
                         ('L1', 'L2', ['Esus', 'Dm9'], dict(bright=(0.45, 0.6), pulse=True, ticks=True)),
                         ('L2', 'L4', ['Fmaj7', 'Esus'], dict(bright=(0.5, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
