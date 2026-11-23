"""HUMAN LIMIT #003 — Anna Bågenholm, 13.7 °C (thermal camera look, claude-drawing-skill: thermal; anonymous silhouette,
no likeness). Facts (Wikipedia 'Anna Bågenholm' citing Gilbert et al., Lancet 2000; ScienceAlert 2016): May 1999, skiing
in the mountains near Narvik, Norway; fell through ice, found an air pocket; circulatory arrest after ~40 minutes in the
water, 80 minutes trapped; core temperature 13.7 °C; rewarmed on heart-lung bypass at the University Hospital of North
Norway in Tromsø; no heartbeat for about 2 h 35 min; recovered and returned to work (later as a radiologist there).
Science story only, no advice."""
from pathlib import Path
from thermal import Thermal

ST = ['cam/%s.png' % n for n in ('00_cold', '01_warming', '02_alive')]


def body(t):
    parts = [t.ellipse(720, 1010, 82, 102), t.blob(720, 1390, 185, 300, rough=0.06, seed=3),
             t.line([(560, 1180), (450, 1520), (430, 1700)], 64), t.line([(880, 1180), (990, 1520), (1010, 1700)], 64),
             t.line([(650, 1640), (610, 2120)], 92), t.line([(790, 1640), (830, 2120)], 92), t.line([(720, 1080), (720, 1150)], 70)]
    m = parts[0]
    for p in parts[1:]:
        m = m + p - m * p
    return m


def paint(work):
    out = Path(work); out.mkdir(parents=True, exist_ok=True)
    W, H = 1440, 2560
    t = Thermal(W, H, sensor=(540, 960), seed=5, ambient=-6)
    t.camera(palette='iron', span=(-8, 38), agc=0.15, netd=0.05)
    t.room(top=-8, bottom=-4, y_top=0, y_bottom=700)
    t.surface(t.rect(0, 700, W, 830), -2.5, grain=0.4)                    # ice sheet
    t.surface(t.rect(0, 830, W, H), t.ramp((0, 830), 3.0, (0, H), 1.5), grain=0.3)   # icy water
    t.surface(t.ellipse(720, 860, 210, 60), 0.5, soft=6)                  # the air pocket under the ice
    m = body(t)
    t.surface(m, 13.7, limb=2.0, soft=2)
    t.stage('cold')
    t.surface(m, t.radial(720, 1350, 260, 520, 27, 22), limb=2.0, soft=2)
    t.stage('warming')
    t.surface(m, t.radial(720, 1350, 260, 520, 36.5, 33), limb=2.0, soft=2)
    t.warm(t.ellipse(745, 1290, 60, 70), 1.2)
    t.stage('alive')
    t.save(str(out / 'cam.png'), str(out / 'cam'))


EPISODE = dict(
    chapter='13.7 °C',
    title="Her Body Cooled to 13.7 °C. She Survived. 🧊 #shorts",
    description=("In May 1999 Anna Bågenholm, a young Swedish doctor, fell through ice while skiing near Narvik, Norway. She found an "
                 "air pocket, but after about 40 minutes in the icy water her circulation stopped. When she was rescued her core "
                 "temperature was 13.7 °C (56.7 °F). At the University Hospital of North Norway in Tromsø, doctors rewarmed her "
                 "blood with a heart-lung machine; her heart had not beaten for about two and a half hours. She recovered and "
                 "went back to work as a doctor.\n\nScience story, not a challenge. Thermal-camera look painted with code "
                 "(no photos, anonymous silhouette), narration is synthetic."),
    tags=['anna bagenholm', 'hypothermia', 'human body', 'survival story', 'science shorts', 'medical history'],
    voice='af_heart',
    lines=["Her heart stopped for hours. And she survived.",
           "In nineteen ninety-nine, a young doctor, Anna Bågenholm, fell through ice while skiing in Norway.",
           "She found an air pocket. But after forty minutes in icy water, her heart stopped.",
           "When rescuers finally pulled her out, her body temperature was just thirteen point seven degrees Celsius.",
           "In Tromsø, a machine slowly warmed her blood. Hours later, her heart beat again.",
           "She recovered, and went back to work as a doctor."],
    gaps=[0.15, 0.4, 0.4, 0.4, 0.45, 0.45],
    display=[(1, 'nineteen', '1999,'), (1, 'ninety-nine,', ''), (2, 'forty', '40'),
             (3, 'thirteen', '13.7'), (3, 'point', ''), (3, 'seven', ''), (3, 'degrees', '°C.'), (3, 'celsius.', '')],
    plates=[dict(stages=ST, show=[(0, 0), ('L4:machine', 1), ('L4:heart', 2)])],
    camera=[(0, 720, 1360, 2400), ('L1', 720, 1300, 2300), ('L2', 720, 1000, 1500), ('L3', 720, 1700, 1700),
            ('L4', 720, 1360, 2350), ('END', 720, 1360, 2400)],
    cards=[dict(at=0, until='L1-0.2', text='13.7 °C', font='AlfaSlabOne-400', size=120, ink=(150, 34, 26), x=540, y=300, rot=-3),
           dict(at='L3:thirteen', until='L4', text='13.7 °C', font='AlfaSlabOne-400', size=120, ink=(150, 34, 26), x=540, y=330, rot=-3),
           dict(at='L1:anna', until='L2-0.2', text='ANNA BÅGENHOLM · 1999', size=64, x=540, y=330, rot=2)],
    stamps=[dict(at='L5:recovered', text='SURVIVED', size=100, color=(230, 230, 230), x=540, y=380, rot=-6)],
    caption=dict(y=0.76),
    music=dict(sections=[(0, 'L3', ['Am9', 'Esus'], dict(bright=(0.15, 0.3), ticks=True)),
                         ('L3', 'L4', ['Dm9', 'Esus'], dict(bright=(0.3, 0.45), pulse=True)),
                         ('L4', 'END', ['Fmaj7', 'Cmaj9'], dict(bright=(0.5, 0.35), gain=(1, 0.0), plucks=0.4))],
               events=[('L4:heart', 'chime', dict(f=880.0))]),
)
