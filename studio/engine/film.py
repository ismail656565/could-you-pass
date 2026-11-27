"""STUDIO film engine — one continuous painted world, a moving camera, paper cut-outs, stamps and captions.

An episode (studio/channels/<cid>/episodes/<slug>/episode.py) defines EPISODE = dict(...) and paint(out_dir):
  paint() draws the plates with the vendored claude-drawing-skill library (each plate 1440x2560, plus draw-on stages).
  EPISODE describes narration, which stage of which plate shows when, camera keyframes, cards, stamps, counter, music.
Plates are stacked vertically into one world: plate k covers world y in [k*2560, (k+1)*2560].

Cues (when something happens) are written relative to the narration:
  2.5            seconds
  'L2'           start of line 2        'L2.end'  its end
  'L2:digging'   start of the first word of line 2 beginning with "digging"   (prefix match, punctuation ignored)
  'L2:digging#2' second such word       'L3@0.5'  halfway through line 3       'END'  end of the film
  any cue + '+0.3' / '-0.2'
"""
import importlib.util, json, math, re, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'vendor' / 'drawing'))
sys.path.insert(0, str(ROOT / 'engine'))
FONTS = ROOT / 'fonts'
PW, PH = 1440, 2560
FPS = 30


def load_episode(path):
    path = Path(path)
    spec = importlib.util.spec_from_file_location('episode_' + path.parent.name.replace('-', '_'), path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    sys.path.insert(0, str(path.parents[2]))           # the channel dir (kit.py)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------ easing
def sm(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eio(x): x = min(1, max(0, x)); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eo(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def back(x, s=1.9): x = min(1, max(0, x)); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def F(name, size): return ImageFont.truetype(str(FONTS / (name + '.woff')), size)


# ------------------------------------------------------------------ paper cut-outs (vox-director style)
def torn(w, h, seed, col=(238, 228, 205), jag=7):
    rng = np.random.default_rng(seed)
    pts = [(x, rng.uniform(0, jag)) for x in np.linspace(0, w, 24)] + \
          [(w - rng.uniform(0, jag), y) for y in np.linspace(0, h, 14)] + \
          [(x, h - rng.uniform(0, jag)) for x in np.linspace(w, 0, 24)] + \
          [(rng.uniform(0, jag), y) for y in np.linspace(h, 0, 14)]
    size = (w + 40, h + 40)
    sh = Image.new('L', size, 0); ImageDraw.Draw(sh).polygon([(x + 26, y + 30) for x, y in pts], fill=120)
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    im = Image.composite(Image.new('RGBA', size, (0, 0, 0, 255)), Image.new('RGBA', size, (0, 0, 0, 0)), sh)
    paper = Image.new('L', size, 0); ImageDraw.Draw(paper).polygon([(x + 20, y + 20) for x, y in pts], fill=255)
    noise = np.random.default_rng(seed + 1).normal(0, 6, (size[1], size[0], 1)).astype(np.float32)
    colarr = np.clip(np.array(col, np.float32)[None, None] + noise, 0, 255).astype(np.uint8)
    im.alpha_composite(Image.fromarray(np.dstack([colarr, np.asarray(paper)]), 'RGBA'))
    return im


def card(text, font='Cinzel-700', size=100, seed=0, paper=(238, 228, 205), ink=(26, 22, 18), pad=(34, 18), tape=True):
    f = F(font, size)
    if '\n' in text:   # multi-line caption card (e.g. meme-style top caption), centred lines
        d0 = ImageDraw.Draw(Image.new('L', (8, 8)))
        bb = [int(round(v)) for v in d0.multiline_textbbox((0, 0), text, font=f, spacing=int(size * 0.22), align='center')]
    else:
        bb = f.getbbox(text)
    w, h = bb[2] - bb[0] + 2 * pad[0], bb[3] - bb[1] + 2 * pad[1]
    im = torn(w, h, seed, paper)
    if '\n' in text:
        ImageDraw.Draw(im).multiline_text((20 + pad[0] - bb[0], 20 + pad[1] - bb[1]), text, font=f, fill=ink,
                                          spacing=int(size * 0.22), align='center')
    else:
        ImageDraw.Draw(im).text((20 + pad[0] - bb[0], 20 + pad[1] - bb[1]), text, font=f, fill=ink)
    if tape:
        tp = Image.new('RGBA', (110, 34), (232, 222, 170, 150)).rotate(-8, expand=True)
        im.alpha_composite(tp, (int(w * 0.5 - 30), 4))
    return im


def stamp(text, size=82, col=(160, 32, 24), seed=0):
    f = F('AlfaSlabOne-400', size)
    bb = f.getbbox(text)
    w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 50
    im = Image.new('L', (w + 20, h + 20), 0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, w + 10, h + 10), 14, outline=255, width=9)
    d.text((40 - bb[0], 35 - bb[1]), text, font=f, fill=255)
    a = np.asarray(im).astype(np.float32) / 255
    rng = np.random.default_rng(seed)
    blot = rng.random((a.shape[0] // 8 + 1, a.shape[1] // 8 + 1)).repeat(8, 0).repeat(8, 1)[:a.shape[0], :a.shape[1]] > 0.8
    a = a * (rng.random(a.shape) > 0.16 + 0.25 * blot) * 0.9
    out = np.zeros(a.shape + (4,), np.uint8); out[..., :3] = col; out[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')


def paste_rot(base, im, x, y, rot, scale=1.0, alpha=1.0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1:
        a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] * max(0, alpha)).astype(np.uint8); im = Image.fromarray(a, 'RGBA')
    base.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))


# ------------------------------------------------------------------ the film
class Film:
    def __init__(self, ep, work, ow=1080, oh=1920):
        self.E, self.work = ep, Path(work)
        self.OW, self.OH = ow, oh
        self.land = ow > oh
        self.pad = 1400 if self.land else 0          # landscape: the plates lie on a dark desk
        self.k = (oh / 1920 * 1.5) if self.land else ow / 1080   # overlay scale
        man = json.loads((self.work / 'vo' / 'manifest.json').read_text())
        gaps = ep.get('gaps') or [0.15] + [0.4] * (len(man) - 1)
        t, self.L = 0.0, []
        for i, m in enumerate(man):
            t += gaps[i]
            self.L.append(dict(file=m['file'], t0=t, t1=t + m['dur'],
                               words=[dict(w=w['w'], t0=t + w['t0'], t1=t + w['t1']) for w in m['words']]))
            t += m['dur']
        self.T = t + ep.get('tail', 1.3)
        self.NF = int(self.T * FPS)
        # plates + stages
        self.plates = []
        for p in ep['plates']:
            ims = [Image.open(self.work / s).convert('RGB') for s in p['stages']]
            show = sorted((self.cue(c), i) for c, i in p.get('show', [(0, len(ims) - 1)]))
            self.plates.append(dict(ims=ims, show=show))
        self._cache = {}
        self.keys = [(self.cue(k[0]),) + tuple(k[1:]) for k in ep['camera']]
        self.keys.sort(key=lambda k: k[0])
        self.cards = [dict(c, t_in=self.cue(c['at']), t_out=self.cue(c.get('until', 'END')),
                           img=card(c['text'], c.get('font', 'Cinzel-700'), c.get('size', 100), seed=i * 7 + 3,
                                    paper=tuple(c.get('paper', (238, 228, 205))), ink=tuple(c.get('ink', (26, 22, 18))),
                                    tape=c.get('tape', True)))
                      for i, c in enumerate(ep.get('cards', []))]
        self.stamps = [dict(s, t=self.cue(s['at']), img=stamp(s['text'], s.get('size', 82), tuple(s.get('color', (160, 32, 24))), i + 5))
                       for i, s in enumerate(ep.get('stamps', []))]
        self.counter = None
        if ep.get('counter'):
            c = dict(ep['counter']); c['t0'], c['t1'], c['tout'] = self.cue(c['start']), self.cue(c['full']), self.cue(c['until'])
            self.counter = c
        self._captions()
        rng = np.random.default_rng(1)
        OW, OH = self.OW, self.OH
        self.grain = [rng.normal(0, 7, (OH // 2, OW // 2)).astype(np.float32).repeat(2, 0).repeat(2, 1)[..., None] for _ in range(6)]
        Y, X = np.mgrid[0:OH, 0:OW].astype(np.float32)
        self.vig = (1 - 0.32 * np.clip((np.hypot((X - OW / 2) / (OW / 2), (Y - OH / 2) / (OH / 2)) - 0.6) / 0.8, 0, 1) ** 1.5)[..., None]

    # ---------------------------------------------------------------- cues
    def cue(self, c):
        if isinstance(c, (int, float)): return float(c)
        m = re.match(r'^\s*([^+\-]+?)\s*(([+\-])\s*([\d.]+))?\s*$', str(c))
        base, off = m.group(1), (float(m.group(4)) * (1 if m.group(3) == '+' else -1) if m.group(2) else 0.0)
        if base == 'END': return self.T + off
        fr = re.match(r'^L(\d+)@([\d.]+)$', base)
        if fr:
            ln = self.L[int(fr.group(1))]
            return ln['t0'] + (ln['t1'] - ln['t0']) * float(fr.group(2)) + off
        mm = re.match(r'^L(\d+)(\.end)?(:([^#]+)(#(\d+))?)?$', base)
        if not mm: return float(base) + off
        ln = self.L[int(mm.group(1))]
        if mm.group(3):
            want, n = mm.group(4).lower(), int(mm.group(6) or 1)
            hits = [w['t0'] for w in ln['words'] if re.sub(r'[^a-z0-9]', '', w['w'].lower()).startswith(re.sub(r'[^a-z0-9]', '', want))]
            if len(hits) < n: raise ValueError(f'cue {c}: word not found in line: {ln["words"]}')
            return hits[n - 1] + off
        return (ln['t1'] if mm.group(2) else ln['t0']) + off

    # ---------------------------------------------------------------- camera
    def cam(self, t):
        K = self.keys
        if t <= K[0][0]: v = list(K[0][1:4])
        elif t >= K[-1][0]: v = list(K[-1][1:4])
        else:
            for a, b in zip(K, K[1:]):
                if a[0] <= t <= b[0]:
                    u = eio((t - a[0]) / max(1e-6, b[0] - a[0]))
                    v = [a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, math.exp(math.log(a[3]) + (math.log(b[3]) - math.log(a[3])) * u)]
                    break
        br = 6 * math.sin(t * 0.9) + 3 * math.sin(t * 2.3 + 1)
        return v[0] + br * 0.6, v[1] + br, v[2] * (1 + 0.004 * math.sin(t * 0.7))

    def state(self, t):
        return tuple(([i for c, i in p['show'] if t >= c] or [p['show'][0][1]])[-1] for p in self.plates)

    def world(self, st):
        if st not in self._cache:
            if len(self._cache) > self.E.get('cache', 5): self._cache.pop(next(iter(self._cache)))
            w = self.desk() if self.pad else Image.new('RGB', (PW, PH * len(self.plates)), tuple(self.E.get('bg', (26, 33, 36))))
            for k, (p, i) in enumerate(zip(self.plates, st)):
                w.paste(p['ims'][i], (self.pad, k * PH))
            a = np.asarray(w).astype(np.float32)
            for k in range(1, len(self.plates)):        # soft seam between stacked plates
                y = k * PH
                band = 160
                shadow = a[y - 4:y].mean(0, keepdims=True) * 0.35
                kk = np.linspace(0, 1, band)[:, None, None]
                xs = slice(self.pad, self.pad + PW)
                a[y - band:y, xs] = a[y - band:y, xs] * (1 - 0.6 * kk) + shadow[:, xs] * 0.6 * kk
                a[y:y + 60, xs] *= np.linspace(0.55, 1, 60)[:, None, None]
            self._cache[st] = Image.fromarray(a.clip(0, 255).astype(np.uint8))
        return self._cache[st]

    def desk(self):
        if not hasattr(self, '_desk'):
            H = PH * len(self.plates); Wd = PW + 2 * self.pad
            rng = np.random.default_rng(3)
            sh = (H // 8, Wd // 8)
            n = rng.normal(0, 1, sh).astype(np.float32)
            from scipy.ndimage import gaussian_filter
            grain = gaussian_filter(n, (0.6, 14)) * 3 + gaussian_filter(n, (6, 40)) * 6
            base = np.array([46, 34, 27], np.float32)[None, None] * (1 + 0.07 * grain[..., None])
            im = Image.fromarray(base.clip(0, 255).astype(np.uint8)).resize((Wd, H), Image.BICUBIC)
            # soft shadow under each plate
            a = np.asarray(im).astype(np.float32)
            m = np.zeros((H // 8, Wd // 8), np.float32); m[:, (self.pad + 30) // 8:(self.pad + PW + 30) // 8] = 1
            sh_ = np.asarray(Image.fromarray((gaussian_filter(m, 5) * 255).astype(np.uint8)).resize((Wd, H), Image.BICUBIC)) / 255.0
            a *= (1 - 0.55 * sh_)[..., None]
            self._desk = Image.fromarray(a.clip(0, 255).astype(np.uint8))
        return self._desk.copy()

    def view(self, img, cx, cy, vh):
        if self.land:
            cx, vh = cx + self.pad, vh * 0.62
        vw = vh * self.OW / self.OH
        s = vh / self.OH
        return img.transform((self.OW, self.OH), Image.AFFINE, (s, 0, cx - vw / 2, 0, s, cy - vh / 2),
                             resample=Image.BICUBIC, fillcolor=tuple(self.E.get('bg', (26, 33, 36))))

    # ---------------------------------------------------------------- captions
    def _captions(self):
        disp = {(li, w.lower()): d for li, w, d in self.E.get('display', [])}
        groups = []
        for li, ln in enumerate(self.L):
            cur = []
            for w in ln['words']:
                d = disp.get((li, w['w'].lower()), w['w'])
                if d == '':
                    if cur: cur[-1]['t1'] = w['t1']
                    continue
                cur.append(dict(w=d.upper(), t0=w['t0'], t1=w['t1']))
                if len(cur) == 3 or d[-1] in '.,:?!':
                    groups.append(cur); cur = []
            if cur: groups.append(cur)
        for g, n in zip(groups, groups[1:] + [None]):
            for w in g: w['gend'] = n[0]['t0'] if n else self.T
        self.groups = groups
        self.cap = self.E.get('caption', {})

    def captions(self, im, t):
        g = next((g for g in self.groups if g[0]['t0'] - 0.04 <= t < min(g[-1]['t1'] + 0.35, g[-1]['gend'])), None)
        if not g: return
        d = ImageDraw.Draw(im)
        parts = [w['w'] for w in g]
        maxw = self.OW * (0.7 if self.land else 0.9)
        for sz in (84, 76, 68, 60, 54):
            cf = F(self.cap.get('font', 'Poppins-800'), int(sz * self.k * (0.8 if self.land else 1)))
            if sum(d.textlength(p + ' ', font=cf) for p in parts) < maxw: break
        widths = [d.textlength(p + ' ', font=cf) for p in parts]
        x = self.OW / 2 - sum(widths) / 2 + d.textlength(' ', font=cf) / 2
        y = (0.84 if self.land else self.cap.get('y', 0.75)) * self.OH + 14 * (1 - eo((t - g[0]['t0']) / 0.12))
        hl = tuple(self.cap.get('hl', (255, 196, 92)))
        for w, wd in zip(g, widths):
            on = w['t0'] - 0.03 <= t
            col = hl if on and t < w['t1'] + 0.12 else ((255, 255, 255) if on else (235, 235, 235))
            d.text((x, y), w['w'], font=cf, fill=col, stroke_width=max(5, int(9 * self.k)), stroke_fill=(16, 12, 10))
            x += wd

    # ---------------------------------------------------------------- frames
    def counter_n(self, t):
        c = self.counter
        if not c or not (c['t0'] <= t < c['tout']): return 0
        return min(c['n'], 1 + int(c['n'] * (t - c['t0']) / max(0.5, c['t1'] - c['t0'])))

    def frame(self, f):
        t = f / FPS
        OW, OH = self.OW, self.OH
        k_ = self.k
        X = (lambda x: x / 1080 * OW) ; Y = (lambda y: y / 1920 * OH)
        cx, cy, vh = self.cam(t)
        st = self.state(t)
        cx2, cy2, vh2 = self.cam(t + 1 / FPS)
        speed = math.hypot(cx2 - cx, cy2 - cy) / vh * OH + abs(vh2 - vh) / vh * OH
        n = 1 if speed < 25 else min(7, int(speed / 18))
        img = self.world(st)
        if n == 1:
            out = np.asarray(self.view(img, cx, cy, vh)).astype(np.float32)
        else:
            out = sum(np.asarray(self.view(img, *self.cam(t + (k / n) / FPS))).astype(np.float32) for k in range(n)) / n
        fd = self.E.get('fade', 0.25)   # stage cross-fade; 0 = hard cuts (e.g. cycling stages as an animation loop)
        pst = self.state(t - fd) if fd > 0 else st
        if pst != st:
            a, b = t - fd, t
            for _ in range(10):
                m_ = (a + b) / 2
                if self.state(m_) == st: b = m_
                else: a = m_
            k = sm((t - b) / fd)
            out = np.asarray(self.view(self.world(pst), cx, cy, vh)).astype(np.float32) * (1 - k) + out * k
        out = out * self.vig + self.grain[f % 6]
        im = Image.fromarray(out.clip(0, 255).astype(np.uint8)).convert('RGBA')
        for c in self.cards:
            a, b = c['t_in'], c['t_out']
            if a <= t < b + 0.3:
                ki = back((t - a) / 0.35); ko = 1 - sm((t - b) / 0.3) if t > b else 1
                paste_rot(im, c['img'], X(c['x']), Y(c['y'] - 60 * (1 - min(1, ki))), c.get('rot', 0) + 6 * (1 - min(1, ki)),
                          (0.7 + 0.3 * ki) * c.get('scale', 1.0) * k_, min(1, ki) * ko)
        n9 = self.counter_n(t)
        if n9:
            c = self.counter
            last = n9 == c['n']
            ci = card(c['fmt'].format(n=n9), c.get('font', 'AlfaSlabOne-400'), c.get('size', 92), 40 + n9,
                      ink=tuple(c.get('last_ink', (150, 34, 26))) if last else (26, 22, 18))
            bump = 0.18 if self.counter_n(t - 0.15) != n9 else 0
            paste_rot(im, ci, X(c.get('x', 300)), Y(c.get('y', 300)), c.get('rot', -4), (1 + bump) * k_)
        for s in self.stamps:
            if t >= s['t'] and ('until' not in s or t < self.cue(s['until'])):
                k = eo((t - s['t']) / 0.16)
                paste_rot(im, s['img'], X(s['x']), Y(s['y']), s.get('rot', 0), (1.9 - 0.9 * k) * k_, min(1, k * 1.4))
        self.captions(im, t)
        return im.convert('RGB')

    # ---------------------------------------------------------------- sound
    def sound(self, out_wav):
        from audio import render_score, mix, loudnorm
        E, T = self.E, self.T
        mu = E.get('music', {})
        secs = [dict(t0=self.cue(s[0]), t1=self.cue(s[1]), chords=s[2], **s[3]) for s in mu.get('sections', [])] or \
               [dict(t0=0, t1=T, chords=['Dm9', 'Am9', 'Fmaj7', 'Esus'], bright=(0.3, 0.5), gain=(1, 0.3), plucks=0.35)]
        ev = [dict(t=0.02, kind='impact', level=0.7)]
        ev += [dict(t=c['t_in'], kind='tick', level=2.2) for c in self.cards]
        ev += [dict(t=s['t'], kind='impact', level=0.6) for s in self.stamps]
        if self.stamps: ev.append(dict(t=self.stamps[-1]['t'] + 0.05, kind='chime', f=440.0))
        if self.counter:
            prev = 0
            for f in range(self.NF):
                n = self.counter_n(f / FPS)
                if n and n != prev: ev.append(dict(t=f / FPS, kind='blip', f=660 + 40 * n, level=0.8))
                prev = n
        # whooshes where the camera moves fast
        sp = []
        for f in range(0, self.NF, 2):
            t = f / FPS
            a, b = self.cam(t), self.cam(t + 1 / FPS)
            sp.append((t, math.hypot(b[0] - a[0], b[1] - a[1]) / a[2] * self.OH + abs(b[2] - a[2]) / a[2] * self.OH))
        last = -9
        for i in range(1, len(sp) - 1):
            t, v = sp[i]
            if v > 40 and v >= sp[i - 1][1] and v >= sp[i + 1][1] and t - last > 1.2:
                ev.append(dict(t=max(0, t - 0.35), kind='whoosh', dur=0.9, level=min(1.8, v / 60))); last = t
        for e in mu.get('events', []):
            ev.append(dict(e[2], t=self.cue(e[0]), kind=e[1]))
        music, fx = render_score(T, secs, ev, seed=E.get('seed', 4))
        tmp = str(out_wav) + '.raw.wav'
        mix([dict(file=l['file'], t0=l['t0']) for l in self.L], T, music, fx, tmp,
            music_db=mu.get('music_db', -6), duck_db=-8, fx_db=-5)
        loudnorm(tmp, str(out_wav))

    def render(self, out_mp4, log=print):
        wav = self.work / f'audio_{self.OW}x{self.OH}.wav'
        self.sound(wav)
        vid = self.work / f'video_{self.OW}x{self.OH}.mp4'
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{self.OW}x{self.OH}',
                              '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                              str(vid)], stdin=subprocess.PIPE)
        for f in range(self.NF):
            p.stdin.write(self.frame(f).tobytes())
            if f % 150 == 0: log(f'  frame {f}/{self.NF}')
        p.stdin.close(); p.wait()
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(vid), '-i', str(wav), '-c:v', 'copy', '-c:a', 'aac',
                        '-b:a', '256k', '-shortest', '-movflags', '+faststart', str(out_mp4)], check=True)
        return out_mp4


def build(episode_py, work, out_mp4, voice=None, stills=None, size=(1080, 1920)):
    """paint (cached) -> narrate (cached) -> render."""
    from voice import narrate
    mod = load_episode(episode_py)
    E = mod.EPISODE
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    if not all((work / s).exists() for p in E['plates'] for s in p['stages']):
        mod.paint(work)
    narrate(E['lines'], work / 'vo', voice or E.get('voice', 'bm_george'), E.get('speed', 1.0), E.get('say'))
    film = Film(E, work, *size)
    if stills:
        for s in stills:
            film.frame(int(float(s) * FPS)).save(work / f'still_{film.OW}_{s}.png')
        return film
    film.render(out_mp4)
    return film


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('episode'); ap.add_argument('--work', required=True); ap.add_argument('--out', default=None)
    ap.add_argument('--stills', default=None); ap.add_argument('--landscape', action='store_true')
    a = ap.parse_args()
    build(a.episode, a.work, a.out or str(Path(a.work) / 'final.mp4'), stills=a.stills.split(',') if a.stills else None,
          size=(1920, 1080) if a.landscape else (1080, 1920))
