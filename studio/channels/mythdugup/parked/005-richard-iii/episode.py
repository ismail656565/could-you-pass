"""Myth Dug Up #005 — Richard III. Plates: a late-medieval illuminated manuscript leaf with a miniature of the king and
his white-boar badge, Latin text telling the legends (illuminated), and an excavator's plan of the grave in trench 1 under
the Leicester car park (codex field notebook).
Facts (checked): Richard III was killed at Bosworth on 22 Aug 1485 and buried in the Greyfriars (Franciscan friary)
church in Leicester; the site was lost; one story said his bones were thrown into the River Soar (National Geographic).
Shakespeare made him a hunchbacked villain. The 'Looking for Richard' project was initiated by Philippa Langley
(Richard III Society); University of Leicester Archaeological Services (lead archaeologist Richard Buckley) began
digging a council car park on 25 Aug 2012 and found the skeleton within days, in the choir of the friary church, near a
bay painted 'R' (for 'reserved'). Announced 4 Feb 2013. The skeleton had severe adolescent-onset idiopathic scoliosis
(not kyphosis) and 11 wounds, 9 to the skull (Appleby et al., The Lancet 2014). mtDNA matched two living relatives in
the female line, Michael Ibsen and Wendy Duldig; probability 99.999% (King et al., Nature Communications 2014).
Reburied in Leicester Cathedral, March 2015. Debated: how villainous he really was (e.g. the Princes in the Tower).
Sources: https://www.nature.com/articles/ncomms6631 ; https://www.cam.ac.uk/research/news/richard-iii-case-closed-after-529-years ;
https://www.nationalgeographic.com/history/article/how-did-englands-lost-king-end-up-beneath-a-parking-lot ;
https://theconversation.com/nine-blows-to-the-head-and-then-he-was-dead-modern-forensics-suggest-how-richard-iii-died-31751"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from illuminated import Illuminated, AZURE, AZURE_DARK, RED, RED_DARK, ROSE, GREEN, GREEN_DARK, WHITE, SILVER, OCHRE
from core import spline
import kit

W, H = 1440, 2560


def paint_leaf(path, stages):
    il = Illuminated(W, H, seed=8)
    il.desk()
    il.codex(-1290, 70, 1370, 2490)            # only the right-hand leaf is in the picture; gutter at the left edge
    X0, X1 = 230, 1250                          # text block
    il.rule(X0, X1, [1650 + 64 * i for i in range(11)], prick_x=1320, top=150, bottom=2380)
    il.stage('vellum')
    # ---- the miniature panel
    P = (X0, 250, X1, 1500)
    px0, py0, px1, py1 = P
    panel = il.mask([[(px0, py0), (px1, py0), (px1, py1), (px0, py1)]])
    inner = il.mask([[(px0 + 26, py0 + 26), (px1 - 26, py0 + 26), (px1 - 26, py1 - 26), (px0 + 26, py1 - 26)]])
    frame = np.clip(panel - inner, 0, 1)
    ground = il.mask([spline([(px0 + 26, 1330), (500, 1300), (800, 1320), (1100, 1290), (px1 - 26, 1310)], 8).tolist() +
                      [(px1 - 26, py1 - 26), (px0 + 26, py1 - 26)]]) * inner
    cx = 640
    cloak = il.mask([[(cx - 120, 640), (cx + 110, 630), (cx + 250, 1360), (cx + 120, 1380), (cx - 130, 1385), (cx - 270, 1360)]])
    robe = il.mask([[(cx - 105, 650), (cx + 95, 638), (cx + 175, 1395), (cx - 190, 1400)]])
    sleeveL = il.mask([[(cx - 105, 650), (cx - 160, 900), (cx - 120, 960), (cx - 60, 760)]])
    sleeveR = il.mask([[(cx + 95, 638), (cx + 150, 880), (cx + 100, 930), (cx + 40, 760)]])
    ermine = il.mask([spline([(cx - 140, 668), (cx - 60, 700), (cx + 40, 690), (cx + 130, 650)], 8).tolist() +
                      spline([(cx + 130, 612), (cx + 40, 648), (cx - 60, 652), (cx - 140, 626)], 8).tolist()])
    belt = il.mask([[(cx - 125, 900), (cx + 120, 895), (cx + 122, 925), (cx - 127, 930)]])
    neck = il.mask([[(cx - 22, 580), (cx + 22, 580), (cx + 24, 640), (cx - 24, 640)]])
    head = il.ellipse(cx - 4, 535, 56, 68)
    hair = np.clip(il.ellipse(cx - 4, 525, 72, 80) - il.mask([[(cx - 50, 480), (cx + 48, 480), (cx + 50, 640), (cx - 52, 640)]]), 0, 1)
    hair = np.clip(hair + il.mask([[(cx - 70, 520), (cx - 50, 520), (cx - 48, 600), (cx - 78, 590)],
                                   [(cx + 46, 520), (cx + 66, 520), (cx + 72, 590), (cx + 44, 600)]]), 0, 1)
    crown = il.mask([[(cx - 70, 478), (cx + 66, 478), (cx + 70, 420), (cx + 40, 452), (cx + 20, 400), (cx, 448), (cx - 22, 398),
                      (cx - 42, 450), (cx - 72, 418)]])
    hands = np.clip(il.circle(cx - 16, 960, 24) + il.circle(cx + 18, 948, 24), 0, 1)
    blade = il.mask([[(cx - 9, 1000), (cx + 9, 1000), (cx + 9, 1330), (cx, 1360), (cx - 9, 1330)]])
    hilt = np.clip(il.mask([[(cx - 70, 985), (cx + 70, 985), (cx + 70, 1003), (cx - 70, 1003)],
                             [(cx - 8, 900), (cx + 8, 900), (cx + 8, 985), (cx - 8, 985)]]) + il.circle(cx, 892, 15), 0, 1)
    # the white boar (his badge)
    bx, by = 1000, 1220
    boar = np.clip(il.ellipse(bx, by, 150, 78) + il.mask([[(bx - 120, by - 50), (bx - 250, by + 10), (bx - 255, by + 40), (bx - 120, by + 50)]])
                   + il.mask([[(bx - 140, by - 50), (bx - 120, by - 110), (bx - 100, by - 50)]])
                   + il.mask([[(x - 18, by + 40), (x + 18, by + 40), (x + 14, by + 130), (x - 12, by + 130)] for x in (bx - 90, bx - 40, bx + 60, bx + 110)]), 0, 1)
    tusk = il.mask([[(bx - 225, by + 22), (bx - 250, by - 20), (bx - 210, by + 14)]])
    eye = il.circle(bx - 170, by - 8, 7)
    boar = np.clip(boar + il.mask(lines=[(spline([(bx + 145, by - 10), (bx + 185, by - 30), (bx + 175, by - 60)], 6), 7)]), 0, 1)
    figure = np.clip(cloak + robe + sleeveL + sleeveR + neck + head + hair + crown + hands + blade + hilt + boar, 0, 1)
    gold_bg = np.clip(inner - ground - figure, 0, 1)
    # ---- workshop order: drawing
    lines = []
    il.outline(np.clip(figure + ground, 0, 1), 1.2, 'diagram', 0.6)
    il.outline(panel, 1.4, 'diagram', 0.6)
    il.write('Ricardus tercius rex anglie', X0 + 10, 1590, 30, kind='red')
    il.stage('drawing')
    il.gild(gold_bg, cushion=4.0)
    il.gild(crown, cushion=2.5)
    il.gild(hilt, cushion=2.0)
    il.gild(belt * robe, cushion=1.5)
    il.punch([(x, y) for x in np.arange(px0 + 60, px1 - 40, 46) for y in np.arange(py0 + 60, 1300, 46)
              if gold_bg[int(y), int(x)] > 0.95], 1.6, 1.8)
    il.stage('gold')
    il.paint(frame, AZURE, mix=(ROSE, il.mask([[(px0, py0), (px1, py0), (px0, py1)]])), granular=0.8)
    il.paint(ground, GREEN, mix=(GREEN_DARK, np.clip((il.YY - 1300) / 200, 0, 1)))
    il.paint(cloak, RED, mix=(RED_DARK, np.clip((il.XX - cx + 200) / 500, 0, 1)))
    il.paint(np.clip(robe + sleeveL + sleeveR - belt, 0, 1), AZURE, mix=(AZURE_DARK, np.clip((il.XX - cx + 150) / 330, 0, 1)), granular=1.0)
    il.paint(ermine, WHITE)
    il.paint(np.clip(head + neck + hands, 0, 1), '#e9c6a4', mix=('#c99c78', np.clip((il.XX - cx + 40) / 120, 0, 1)))
    il.paint(hair, '#5a3a22')
    il.paint(blade, SILVER)
    il.paint(np.clip(boar - tusk, 0, 1), WHITE, mix=('#cfc6b4', np.clip((il.YY - by + 40) / 160, 0, 1)))
    il.paint(tusk, '#f7f1df'); il.paint(eye, '#2a1a10')
    il.stage('colour')
    il.outline(np.clip(cloak + robe, 0, 1), 1.6); il.outline(sleeveL, 1.2); il.outline(sleeveR, 1.2)
    il.outline(ermine, 1.0); il.outline(head, 1.3); il.outline(hair, 1.0); il.outline(crown, 1.4); il.outline(hands, 1.0)
    il.outline(blade, 1.2); il.outline(hilt, 1.2); il.outline(boar, 1.6); il.outline(tusk, 1.0); il.outline(belt * robe, 1.0)
    il.outline(frame, 1.8); il.outline(ground, 1.2)
    # ermine tails, face, folds, flowers in the grass
    il.pen([np.array([(x, y), (x, y + 10)], np.float32) for x, y in ((cx - 100, 660), (cx - 50, 674), (cx, 672), (cx + 50, 664), (cx + 100, 646))], 3.0, 'iron')
    il.pen([np.array([(cx - 30, 528), (cx - 14, 526)]), np.array([(cx + 8, 526), (cx + 24, 528)]), np.array([(cx - 4, 536), (cx - 10, 562), (cx + 2, 564)]),
            np.array([(cx - 18, 582), (cx + 10, 582)])], 1.4, 'iron')
    il.pen([spline([(cx - 60 + k * 40, 940), (cx - 70 + k * 46, 1150), (cx - 80 + k * 52, 1390)], 6) for k in range(4)], 1.0, 'iron', 0.6)
    il.pen([spline([(px0 + 70 + k * 85, 1360 + (k % 3) * 30), (px0 + 74 + k * 85, 1330 + (k % 3) * 30)], 4) for k in range(12)], 1.2, 'iron', 0.8)
    for k in range(12):
        x, y = px0 + 74 + k * 85, 1326 + (k % 3) * 30
        if abs(x - cx) > 220 and not (bx - 270 < x < bx + 170):
            il.paint(il.circle(x, y, 8), WHITE if k % 2 else ROSE)
    il.pen([spline([(px0 + 40 + 60 * k, 270), (px0 + 70 + 60 * k, 240)], 4) for k in range(0)], 1.0)
    # text below the miniature
    blk = il.column('*Ricardus tercius* rex anglie ^occisus est in bello anno domini mcccclxxxv '
                    '^et corpus eius sepultum est apud fratres minores leycestrie. ¶ ^Post multa secula locus sepulture '
                    'oblitus est et nemo sciebat ubi iaceret rex. ¶ ^Alii dicunt corpus eius in flumen sore proiectum esse. '
                    '¶ ^Et dicunt eum gibbosum fuisse, monstrum horribile, ut fabulae narrant. |',
                    X0, X1, 1714, 30, 64)
    il.scribe(blk); il.rubricate(blk)
    bd = il.border(np.array([(175, 250), (175, 2330)], np.float32), width=12, seed=3, bounds=(110, 150, 215, 2400))
    bd.gild(); bd.paint(); bd.pen()
    il.write('anno mcccclxxxv', X0 + 150, 2200, 56, kind='red')
    il.stage('text')
    il.age(foxing=30)
    il.stage('aged')
    il.save(path, stages_dir=stages)




def skeleton(c):
    """the grave in trench 1: the skeleton with its curved spine, the painted 'R' of the car park bay"""
    from codex import Codex
    c.dotted([(300, 980), (1150, 980), (1180, 1300), (300, 1310), (300, 980)], width=1.6)          # grave cut
    hx, hy = 400, 1130
    c.contour(Codex.arc(hx, hy, 52, 0, 360, ry=60), width=2.8, closed=True)                        # skull
    c.contour(Codex.arc(hx - 10, hy - 6, 13, 0, 360), width=1.6, closed=True)
    c.contour(Codex.arc(hx + 14, hy - 8, 13, 0, 360), width=1.6, closed=True)
    xs = np.linspace(hx + 58, 770, 50)                                                              # the S-curved spine
    ys = hy + 4 + 55 * np.sin((xs - hx - 58) / (770 - hx - 58) * 2 * np.pi)
    c.contour(np.stack([xs, ys], 1), width=4.0, searching=1)
    for x in np.linspace(hx + 66, 765, 22):                                                         # vertebrae
        y = float(np.interp(x, xs, ys))
        c.quill([(x, y - 11), (x, y + 11)], width=2.4)
    for x in np.linspace(500, 660, 7):                                                              # ribs, both sides
        y = float(np.interp(x, xs, ys))
        for sgn in (-1, 1):
            c.quill(spline([(x, y + sgn * 8), (x + 6, y + sgn * 50), (x - 12, y + sgn * 85), (x - 36, y + sgn * 100)], 6), width=1.9)
    c.contour([(470, 1050), (520, 1040)], width=2.4)                                                # collarbones
    c.contour([(470, 1215), (520, 1225)], width=2.4)
    for sgn, y0 in ((-1, 1045), (1, 1220)):                                                         # arms, hands on the pelvis
        c.contour([(520, y0), (650, y0 + sgn * 22), (655, y0 + sgn * 22)], width=2.6)
        c.contour(Codex.arc(658, y0 + sgn * 22, 12, 0, 360), width=1.8, closed=True)
        c.contour([(665, y0 + sgn * 18), (790, 1135 + sgn * 38)], width=2.4)
    c.contour(Codex.arc(830, 1135, 55, 0, 360, ry=85), width=2.8, closed=True)                      # pelvis
    c.contour(Codex.arc(830, 1135, 22, 0, 360, ry=30), width=1.6, closed=True)
    for sgn in (-1, 1):                                                                             # legs (the feet were lost)
        k = 1135 + sgn * 45
        c.contour([(870, k), (1020, k + sgn * 6)], width=3.0)
        c.contour(Codex.arc(1030, k + sgn * 6, 14, 0, 360), width=1.8, closed=True)
        c.contour([(1044, k + sgn * 6), (1160, k + sgn * 4)], width=2.6)
        c.contour([(1044, k + sgn * 6 + 12), (1160, k + sgn * 4 + 12)], width=1.6)
    c.sanguines([Codex.arc(hx, hy, 85, 0, 350, ry=92)], width=3.0)                                 # the head wounds
    c.write(['9 of 11 wounds', 'on the skull'], hx - 120, 1360, size=28, mirror=False, ink=1.0)
    c.write(['curved spine'], 600, 920, size=30, mirror=False, ink=1.0)
    c.arrow([(660, 935), (640, 990), (615, 1060)], width=1.8)
    # the car park: bay lines and the painted R
    for x in (330, 560, 790, 1020):
        c.dotted([(x, 1520), (x + 60, 1900)], width=2.0, dash=12, gap=8)
    c.write(['R'], 640, 1790, size=150, mirror=False, ink=0.85)
    c.write(['bay marked R', '(reserved)'], 900, 1980, size=28, mirror=False, ink=0.9)


ROOMS = [(230, 860, 1230, 1400)]      # trench 1, in the choir of the friary church


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    paint_leaf(str(out / 'leaf.png'), str(out / 'leaf'))
    kit.plan(out, 'grave', 'GREYFRIARS', 'Leicester · trench 1 · 2012', ROOMS, seed=35,
             labels=[('TRENCH 1 · in the choir of the friary church', 250, 830, 30)],
             scale_text='0                                   1 m', box=(150, 420, 1290, 2100), extra=skeleton)


PH = 2560
LEAF = ['leaf/%s.png' % n for n in ('01_drawing', '02_gold', '03_colour', '04_text', '05_aged')] + ['leaf.png']
GRAVE = ['grave/%s.png' % n for n in ('00_sheet', '01_title', '02_grid', '03_rooms_00', '04_notes')] + ['grave.png']

EPISODE = dict(
    chapter='Richard III',
    title="England Lost a King for 500 Years. He Was Under a Car Park. #shorts",
    description=("Richard III died at Bosworth in 1485. Shakespeare made him a hunchbacked villain, and one story said his "
                 "bones were thrown into a river. In 2012, Philippa Langley's search and a University of Leicester team dug "
                 "up a council car park where the Greyfriars church once stood. Within days they found a skeleton with a "
                 "curved spine and 11 wounds, 9 to the skull. DNA from two living relatives matched.\n\n"
                 "Proven: the skeleton is Richard III, and he had scoliosis (not a hunchback).\n"
                 "Debated: whether he really was the villain Shakespeare made him.\n\n"
                 "Illustrations painted with code (no photos), narration is synthetic."),
    tags=['richard iii', 'king under the car park', 'leicester', 'philippa langley', 'bosworth', 'shakespeare', 'scoliosis',
          'archaeology', 'dna', 'history shorts'],
    lines=["This king was lost for five hundred years.",
           "Richard the Third died at the Battle of Bosworth in fourteen eighty-five. Shakespeare made him a hunchbacked villain, "
           "and one story said his bones were thrown into a river.",
           "In twenty twelve, Philippa Langley and a University of Leicester team dug up a car park, where an old friary church once stood.",
           "Within days, they found a skeleton with a curved spine and eleven wounds, nine of them to the skull. DNA from two living relatives matched.",
           "Proven: it was Richard, with scoliosis, not a hunched back. Debated: whether he really was Shakespeare's villain."],
    gaps=[0.15, 0.35, 0.45, 0.40, 0.45],
    display=[(0, 'five', '500'), (0, 'hundred', ''), (1, 'third', 'III'), (1, 'fourteen', '1485.'), (1, 'eighty-five.', ''),
             (2, 'twenty', '2012,'), (2, 'twelve,', ''), (3, 'eleven', '11'), (3, 'nine', '9')],
    plates=[dict(stages=LEAF, show=[(0, 3), (0.6, 4), (1.3, 5)]),
            dict(stages=GRAVE, show=[(0, 0), ('L2-0.2', 1), ('L2+0.5', 2), ('L2@0.5', 3), ('L3-0.2', 4), ('L3:dna', 5)])],
    camera=[(0, 690, 830, 1450), ('L0.end', 700, 880, 1650), ('L1+0.3', 720, 1290, 2450), ('L1:shakespeare-0.3', 710, 1260, 2300),
            ('L1:shakespeare+0.5', 680, 900, 1500), ('L1:bones-0.2', 700, 1050, 1800), ('L1.end-0.2', 730, 1880, 1300),
            ('L2-0.1', 720, PH + 760, 1700), ('L2:car-0.3', 720, PH + 1250, 2100), ('L2.end', 720, PH + 1350, 2200),
            ('L3+0.2', 680, PH + 1130, 1300), ('L3:nine-0.2', 560, PH + 1150, 1050), ('L3:dna-0.2', 700, PH + 1250, 1900),
            ('L4+0.2', 720, PH + 1290, 2450), ('END', 720, PH + 1270, 2400)],
    cards=[dict(at='L1:richard', until='L1:shakespeare-0.3', text='RICHARD III', font='AlfaSlabOne-400', size=110, ink=(150, 34, 26), x=540, y=280, rot=-3),
           dict(at='L1:fourteen', until='L1:shakespeare-0.3', text='BOSWORTH 1485', size=70, x=560, y=1150, rot=2),
           dict(at='L1:thrown', until='L2-0.15', text='IN A RIVER?', size=80, x=560, y=320, rot=-3),
           dict(at='L2:twenty', until='L3-0.2', text='2012', font='AlfaSlabOne-400', size=120, x=840, y=250, rot=-3),
           dict(at='L2:philippa', until='L2:car-0.2', text='PHILIPPA LANGLEY', size=72, x=520, y=1100, rot=-2),
           dict(at='L2:university', until='L2:car-0.2', text='UNIVERSITY OF LEICESTER', size=54, x=560, y=1220, rot=2),
           dict(at='L2:car', until='L3-0.2', text='A CAR PARK', size=80, x=540, y=380, rot=-2),
           dict(at='L3:dna', until='L4-0.1', text='DNA MATCH', font='AlfaSlabOne-400', size=100, ink=(30, 70, 52), x=560, y=330, rot=-3)],
    stamps=[dict(at='L4:proven', text='KING: PROVEN', color=(30, 70, 52), x=540, y=640, rot=-6),
            dict(at='L4:debated', text='VILLAIN: DEBATED', size=70, color=(160, 32, 24), x=540, y=860, rot=5)],
    music=dict(sections=[(0, 'L2-0.3', ['Dm9', 'Am9'], dict(bright=(0.2, 0.35), plucks=0.4)),
                         ('L2-0.3', 'L3', ['Fmaj7', 'Esus'], dict(bright=(0.35, 0.5), pulse=True, plucks=0.3)),
                         ('L3', 'L4', ['Dm9', 'Esus'], dict(bright=(0.45, 0.65), gain=(1, 1.1), pulse=True, ticks=True)),
                         ('L4', 'END', ['Am9', 'Fmaj7'], dict(bright=(0.5, 0.3), gain=(1, 0.0), plucks=0.4))]),
)
