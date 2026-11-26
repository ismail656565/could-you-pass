"""Myth Dug Up #011 (news) — Tidal bans fully AI-generated music and will delete about 29 million tracks.
Plates: a cut-and-paste magazine collage with a halftone vinyl record and ransom letters (newscollage), and a data sheet
with the upload share, daily rejections and how other streamers handle AI music (blueprint). No logos.
Facts (Tidal announcement on X, 24 Nov 2026; TechCrunch 24 Nov 2026; The Next Web, BGR, Engadget/Yahoo Tech, 24-25 Nov 2026):
- Tidal bans songs generated fully with AI; songs made with AI assistance are still accepted. Distributors may not deliver
  100% AI tracks; submissions declaring full AI generation in metadata are rejected.
- Removal starts 9 Dec 2026; more than 29 million songs to be deleted by end of year; ~80,000-85,000 tracks a day to be
  rejected under the new rules.
- Tidal: more than 43% of tracks uploaded in the past 90 days were detected as AI-generated; 96% of fully AI tracks have
  no streams. Tidal began demonetising AI songs in June 2026 (music lead Robert Anderson: demonetisation was not enough).
- Comparison (TechCrunch): Bandcamp banned AI music in Jan 2026; Deezer detects/tags and plans a user filter; Spotify
  and YouTube Music label AI music rather than removing it.
Facts as of 26 Nov 2026."""
from pathlib import Path
from newscollage import NewsCollage, Photo, RED, INK, MUSTARD
from blueprint import Blueprint

W, H = 1440, 2560


def record_photo():
    p = Photo(860, 860, seed=11)
    p.disc(430, 430, 400, height=10, bevel=3, albedo=0.12, metal=0.0, gloss=0.8)
    p.spiral(430, 430, 150, 385, turns=26, width=2.0, z=10, height=1.5, albedo=0.3, metal=0.2, gloss=0.8)
    p.disc(430, 430, 140, z=10, height=3, bevel=1, albedo=0.85, metal=0.0, gloss=0.1)
    p.text('A.I.', 430, 400, 90, font='didone', tone=0.1)
    p.text('NOT ALLOWED', 430, 480, 24, font='didone', tone=0.1)
    p.disc(430, 430, 14, z=14, height=2, albedo=0.05)
    p.glare(330, 300, 160, 380, 200, 250, strength=0.45)
    return p


def paint_collage(out):
    nc = NewsCollage(W, H, seed=111)
    nc.board()
    for (w, h, x, y, r, sides) in ((980, 1300, 470, 760, -4, 'rb'), (900, 1200, 1010, 1650, 5, 'lt'), (820, 900, 430, 2160, -2, 'rt')):
        s = nc.newsprint(w, h, columns=3); s.tear(sides); nc.paste(s, x, y, rot=r)
    nc.stage('board')
    nc.disc(720, 1230, 500, RED)
    s = nc.print_photo(record_photo()); s.cutout(14); nc.paste(s, 720, 1240, rot=-6)
    nc.stage('record')
    nc.ransom('DELETED:', 170, 300, 130, rot=2)
    nc.ransom('29 MILLION', 150, 560, 108, rot=-2)
    nc.tape(220, 220, 200, rot=-12); nc.tape(1250, 200, 200, rot=10)
    nc.stage('ransom')
    nc.label('43% OF NEW UPLOADS: AI', 140, 1880, 60, face='typewriter_bold', rot=3)
    nc.stage('share')
    nc.label('DELETIONS FROM 9 DEC', 190, 2290, 64, face='typewriter_bold', block=MUSTARD, rot=-2)
    nc.tape(210, 2280, 160, rot=70)
    nc.stage('dec')
    nc.stamp(1100, 1690, ['FULLY AI', 'BANNED'], rot=12)
    nc.stage('stamp')
    nc.save(str(out / 'collage.png'), stages_dir=str(out / 'collage'))


def paint_sheet(out):
    bp = Blueprint(W, H, seed=112)
    bp.border(50, 50, W - 50, H - 50, zones=(4, 8), size=18)
    bp.text('AI MUSIC ON TIDAL', W / 2, 190, 58, 'ms', pen=2.2, spacing=0.2)
    bp.text('ANNOUNCED 24 NOV 2026 · COMPANY FIGURES', W / 2, 250, 28, 'ms')
    bp.stage('sheet')
    x0, x1, y0, y1 = 150, 1290, 360, 520
    xs = x0 + (x1 - x0) * 0.43
    bp.box(x0, y0, x1, y1, 'heavy'); bp.line([(xs, y0), (xs, y1)], 'thick')
    bp.hatch([[(x0, y0), (xs, y0), (xs, y1), (x0, y1)]], angle=45, spacing=12)
    bp.text('43% AI', (x0 + xs) / 2, 462, 52, 'ms', pen=2.2)
    bp.text('57% OTHER', (xs + x1) / 2, 462, 44, 'ms', pen=1.8)
    bp.text('NEW UPLOADS, LAST 90 DAYS', W / 2, 590, 30, 'ms')
    bp.stage('split')
    bp.box(150, 680, 1290, 920, 'thick')
    bp.text('80,000+', W / 2, 800, 96, 'ms', pen=2.4)
    bp.text('TRACKS TO BE REJECTED PER DAY', W / 2, 880, 30, 'ms')
    bp.stage('perday')
    bp.box(150, 980, 1290, 1220, 'thick')
    bp.red_text('96%', 620, 1100, 96, rot=-2)
    bp.text('OF FULLY-AI TRACKS: ZERO STREAMS', W / 2, 1180, 30, 'ms')
    bp.stage('zero')
    bx, by, rh = 150, 1420, 150
    rows = (('TIDAL', 'BANS + DELETES'), ('BANDCAMP', 'BANNED (JAN 2026)'), ('DEEZER', 'TAGS, FILTER PLANNED'),
            ('SPOTIFY / YT MUSIC', 'LABELS ONLY'))
    bp.view_title(720, 1350, 'HOW STREAMERS HANDLE FULLY-AI SONGS', size=30)
    bp.table(bx, by, [500, 640], [rh] * 4, pen='thin', outer='heavy')
    for i, (a, v) in enumerate(rows):
        yy = by + i * rh + 92
        bp.text(a, bx + 24, yy, 36 if i < 3 else 30, 'ls', pen=1.8)
        bp.text(v, bx + 524, yy, 38, 'ls', pen=2.0)
        if i in (1, 3):
            bp.stage('rows%d' % i)
    bp.cloud([(bx + 505, by + 3 * rh + 10), (bx + 1135, by + 3 * rh + 10), (bx + 1135, by + 4 * rh - 10), (bx + 505, by + 4 * rh - 10)])
    bp.red_text('AI-ASSISTED SONGS STAY', 720, 2200, 44, rot=2)
    bp.stage('cloud')
    bp.fold(xs=(720,), ys=(1280,), wear=0.7)
    bp.stain(1220, 2420, 70, 0.6)
    bp.save(str(out / 'sheet.png'), str(out / 'sheet'))


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_collage(out)
    paint_sheet(out)


PH = 2560
A = ['collage/%s.png' % n for n in ('00_board', '01_record', '02_ransom', '03_share', '04_dec', '05_stamp', '06_final')]
B = ['sheet/%s.png' % n for n in ('00_sheet', '01_split', '02_perday', '03_zero', '04_rows1', '05_rows3', '06_cloud', '07_final')]

EPISODE = dict(
    chapter='Tidal vs AI music',
    title="Tidal Is Deleting 29 Million AI Songs. Spotify Isn't. #shorts",
    description=("Music streamer Tidal announced on 24 November that it is banning songs generated fully with AI. Removal starts on "
                 "9 December, and more than 29 million tracks are set to be deleted by the end of the year. Tidal says more than "
                 "43% of tracks uploaded in the last 90 days were detected as AI-generated, and that 96% of fully AI tracks never "
                 "got a single stream. Songs made with AI assistance are still allowed. Spotify and YouTube Music label AI music "
                 "instead of removing it; Bandcamp banned it in January.\n\n"
                 "Proven: Tidal announced the ban and the 9 December start (company statement).\n"
                 "Debated: whether detection can reliably tell fully AI songs from human or AI-assisted ones.\n\n"
                 "Sources: Tidal announcement, TechCrunch, The Next Web, BGR, Yahoo Tech.\n"
                 "Illustrations painted with code (no photos), narration is synthetic. Facts as of 26 Nov 2026."),
    tags=['tidal', 'ai music', 'ai generated music', 'spotify', 'suno', 'music streaming', 'tech news', 'music news', 'news'],
    voice='bm_george',
    lines=["Twenty-nine million songs are about to vanish.",
           "Streaming service Tidal says forty-three percent of its recent uploads were flagged as made by AI. Now it is banning songs made fully by AI.",
           "Deletions start next month. The company says almost all of those tracks never got a single stream.",
           "Songs made with AI help can stay. Spotify and YouTube Music only label AI music. They don't remove it.",
           "Proven: Tidal announced the ban. Debated: whether its detection can really tell AI from human."],
    gaps=[0.15, 0.35, 0.4, 0.4, 0.45],
    display=[(0, 'Twenty-nine', '29'), (1, 'forty-three', '43%'), (1, 'percent', '')],
    plates=[dict(stages=A, show=[(0, 2), ('L1:forty', 3), ('L1:now', 4), ('L1:banning', 6)]),
            dict(stages=B, show=[(0, 1), ('L2', 2), ('L2:almost', 3), ('L3', 4), ('L3:spotify', 5), ('L3:label', 6),
                                 ('L4', 7)])],
    camera=[(0, 720, 1180, 2300), ('L0.end', 720, 1230, 2350), ('L1+0.2', 720, 1450, 2250), ('L1:forty', 720, 1500, 2100),
            ('L1.end', 720, 1480, 2140), ('L2-0.1', 720, PH + 1090, 2150), ('L2.end', 720, PH + 1110, 2180),
            ('L3-0.1', 720, PH + 1500, 2120), ('L4', 720, PH + 1490, 2140), ('END', 720, PH + 1300, 2450)],
    cards=[dict(at=0, until='L1-0.1', text='AI SONGS BANNED', font='AlfaSlabOne-400', size=96, ink=(160, 32, 24), x=540, y=1780, rot=-3),
           dict(at='L2', until='L2:almost', text='FROM DEC 9', font='AlfaSlabOne-400', size=88, x=540, y=1720, rot=2),
           dict(at='L3:spotify', until='L4-0.1', text='ONLY LABELED', size=72, x=540, y=1720, rot=-2)],
    stamps=[dict(at='L4:proven', text='PROVEN', size=100, color=(30, 70, 52), x=540, y=560, rot=-6),
            dict(at='L4:debated', text='DEBATED', size=100, color=(160, 32, 24), x=560, y=780, rot=5)],
    music=dict(sections=[(0, 'L1', ['Dm9', 'Am9'], dict(bright=(0.3, 0.45), pulse=True)),
                         ('L1', 'L2', ['Esus', 'Dm9'], dict(bright=(0.45, 0.6), pulse=True, ticks=True)),
                         ('L2', 'L4', ['Fmaj7', 'Esus'], dict(bright=(0.5, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
