"""Original generative score + sound design + mix (numpy only, no samples, no licences).
Every cue is placed from the narration timeline, so music and SFX hit the edit exactly."""
import json, subprocess, math
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve, resample_poly

SR = 48000
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def tt(n): return np.arange(n) / SR

def lp(x, fc, order=2):
    sos = butter(order, fc / (SR / 2), "low", output="sos"); return sosfilt(sos, x, axis=0)
def hp(x, fc, order=2):
    sos = butter(order, fc / (SR / 2), "high", output="sos"); return sosfilt(sos, x, axis=0)
def bp(x, f0, f1, order=2):
    sos = butter(order, [f0 / (SR / 2), f1 / (SR / 2)], "band", output="sos"); return sosfilt(sos, x, axis=0)

def env_ar(n, a, r):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na) ** 1.5
    if nr: e[-nr:] *= np.linspace(1, 0, nr) ** 1.6
    return e

def reverb_ir(sec=2.4, seed=3, damp=3500):
    rng = np.random.default_rng(seed)
    n = int(sec * SR); t = tt(n)
    ir = rng.standard_normal((n, 2)) * np.exp(-t * 6.9 / sec)[:, None]
    ir = lp(ir, damp); ir[:int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))[:, None]
    return ir / np.sqrt((ir ** 2).sum(0))

IR = reverb_ir()
def reverb(x, wet=0.3):
    if x.ndim == 1: x = np.stack([x, x], 1)
    y = np.stack([fftconvolve(x[:, c], IR[:, c])[:len(x)] for c in range(2)], 1)
    return x * (1 - wet) + y * wet * 1.6

def pan(x, p):  # p in [-1,1]
    l, r = math.cos((p + 1) * math.pi / 4), math.sin((p + 1) * math.pi / 4)
    return np.stack([x * l, x * r], 1)

def add(buf, x, t0):
    i = int(t0 * SR)
    if i >= len(buf): return
    if x.ndim == 1: x = np.stack([x, x], 1)
    j = min(len(buf), i + len(x)); buf[i:j] += x[:j - i]

# ---------------------------------------------------------------- instruments
def pad_note(f, dur, bright=False, seed=0):
    n = int(dur * SR); t = tt(n); rng = np.random.default_rng(seed)
    out = np.zeros(n)
    for det in (-0.07, 0.0, 0.07):            # three detuned voices (cents-ish ratio)
        ff = f * 2 ** (det / 12); ph = rng.uniform(0, 2 * np.pi)
        for k in range(1, 9):
            out += np.sin(2 * np.pi * k * ff * t + ph * k) / k ** (1.15 if bright else 1.5)
    out += 0.6 * np.sin(2 * np.pi * f / 2 * t)  # sub
    lfo = 1 + 0.08 * np.sin(2 * np.pi * 0.17 * t + seed)
    return out * lfo / 6

def pluck(f, dur=0.9, tone=0.5):
    n = int(dur * SR); t = tt(n)
    x = np.sin(2 * np.pi * f * t) + 0.35 * tone * np.sin(2 * np.pi * 2 * f * t) + 0.12 * tone * np.sin(2 * np.pi * 3.01 * f * t)
    return x * np.exp(-t * 6.5) * (1 - np.exp(-t * 900))

def bass_pulse(f, dur=0.32):
    n = int(dur * SR); t = tt(n)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return np.tanh(1.6 * x) * np.exp(-t * 9) * (1 - np.exp(-t * 400))

def tick(level=1.0, seed=0):
    rng = np.random.default_rng(seed); n = int(0.035 * SR)
    x = hp(rng.standard_normal(n), 6000) * np.exp(-tt(n) * 220)
    return x * level

def riser(dur, f0=300, f1=5000, seed=1):
    n = int(dur * SR); t = tt(n); rng = np.random.default_rng(seed)
    noise = rng.standard_normal(n)
    out = np.zeros(n); seg = int(0.02 * SR)
    for i in range(0, n, seg):
        u = i / n; fc = f0 * (f1 / f0) ** u
        out[i:i + seg] = bp(noise[max(0, i - 2000):i + seg], fc * 0.7, min(fc * 1.4, 22000))[-min(seg, n - i):]
    tone = np.sin(2 * np.pi * np.cumsum(220 * (1 + 2 * (t / dur) ** 2)) / SR) * 0.15
    e = (t / dur) ** 2.2
    return (out * 0.8 + tone) * e

def impact(dur=1.6):
    n = int(dur * SR); t = tt(n)
    f = 58 * np.exp(-t * 1.2) + 30
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.6)
    noise = lp(np.random.default_rng(5).standard_normal(n), 900) * np.exp(-t * 18) * 0.6
    return np.tanh(1.4 * (x + noise))

def whoosh(dur=0.9, reverse=False, seed=2):
    n = int(dur * SR); t = tt(n); rng = np.random.default_rng(seed)
    x = rng.standard_normal(n); out = np.zeros(n); seg = int(0.015 * SR)
    for i in range(0, n, seg):
        u = i / n; fc = 400 + 3500 * math.sin(math.pi * u)
        out[i:i + seg] = bp(x[max(0, i - 2000):i + seg], fc * 0.6, min(fc * 1.6, 20000))[-min(seg, n - i):]
    e = np.sin(np.pi * t / dur) ** 1.5
    y = out * e
    return y[::-1] if reverse else y

def tape_rewind(dur=0.95):
    n = int(dur * SR); t = tt(n)
    f = 900 * (1 + 0.6 * np.sin(2 * np.pi * 7 * t)) * (0.4 + 0.6 * t / dur)
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    x = lp(saw, 2500) * 0.25 + whoosh(dur, seed=9) * 0.9
    return x * np.sin(np.pi * t / dur) ** 0.7

def blip(f=988, dur=0.25):
    n = int(dur * SR); t = tt(n)
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 1.5 * f * t)) * np.exp(-t * 26)

def chime(f=659.25, dur=2.6):
    n = int(dur * SR); t = tt(n)
    x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for r, a, d in
            [(1, 1, 1.6), (2.0, 0.35, 2.4), (2.76, 0.22, 3.5), (5.4, 0.08, 6)])
    return x * (1 - np.exp(-t * 600))

# ---------------------------------------------------------------- score
CHORDS = {
    "Am9": [45, 57, 60, 64, 67, 71], "Fmaj7": [41, 53, 57, 60, 64], "Cmaj9": [48, 55, 59, 62, 64],
    "G6": [43, 55, 59, 62, 64], "Dm9": [38, 53, 57, 60, 64], "Esus": [40, 52, 57, 59, 64],
}

def render_score(T, sections, events, seed=0):
    """sections: list of dict(t0,t1,chords:[names], bright:(b0,b1), gain:(g0,g1), pulse:bool, plucks:density, ticks:bool)
       events: list of dict(t, kind, ...)"""
    n = int((T + 3) * SR)
    pad_d = np.zeros((n, 2)); pad_b = np.zeros((n, 2)); mel = np.zeros((n, 2)); rhythm = np.zeros((n, 2)); fx = np.zeros((n, 2))
    bright_curve = np.zeros(n); gain_curve = np.zeros(n)
    beat = 60 / 84
    rng = np.random.default_rng(seed)
    for si, s in enumerate(sections):
        t0, t1 = s["t0"], s["t1"]; chords = s["chords"]
        seglen = (t1 - t0) / len(chords)
        for ci, ch in enumerate(chords):
            c0 = t0 + ci * seglen; dur = seglen + 1.4
            for k, m in enumerate(CHORDS[ch]):
                f = mtof(m)
                e = env_ar(int(dur * SR), 0.9 if ci or si else 0.4, 1.4)
                v = 0.11 if m < 50 else 0.07
                for buf, br in ((pad_d, False), (pad_b, True)):
                    x = pad_note(f, dur, br, seed=k + 10 * ci) * e * v
                    add(buf, pan(x, -0.5 + k / max(1, len(CHORDS[ch]) - 1)), c0)
        i0, i1 = int(t0 * SR), int(t1 * SR)
        b0, b1 = s.get("bright", (0.2, 0.2)); g0, g1 = s.get("gain", (1, 1))
        bright_curve[i0:i1] = np.linspace(b0, b1, i1 - i0)
        gain_curve[i0:i1] = np.linspace(g0, g1, i1 - i0)
        # rhythm layers
        tcur = t0; step = 0
        while tcur < t1 - 0.05:
            ch = chords[min(len(chords) - 1, int((tcur - t0) / seglen))]
            notes = CHORDS[ch]
            if s.get("pulse") and step % 2 == 0:
                add(rhythm, pan(bass_pulse(mtof(notes[0] + (12 if notes[0] < 40 else 0))) * 0.22, 0), tcur)
            if s.get("plucks", 0) > 0 and rng.random() < s["plucks"]:
                m = notes[1 + (step * 3) % (len(notes) - 1)] + 12
                add(mel, pan(pluck(mtof(m), tone=0.6) * 0.06, 0.45 * (1 if step % 2 else -1)), tcur)
            if s.get("ticks"):
                add(rhythm, pan(tick(0.05 if step % 2 else 0.09, seed=step), 0.3), tcur)
                add(rhythm, pan(tick(0.035, seed=step + 99), -0.3), tcur + beat / 4)
            tcur += beat / 2; step += 1
    b = np.clip(bright_curve, 0, 1)[:, None]
    pads = lp(pad_d, 900) * (1 - b) + lp(pad_b, 3200) * b
    music = reverb(pads, 0.35) + reverb(mel, 0.45) + rhythm
    music *= np.clip(gain_curve, 0, 2)[:, None]
    # events (SFX + musical accents)
    for e in events:
        k = e["kind"]; lvl = e.get("level", 1.0)
        if k == "impact": add(fx, reverb(impact() * 0.55 * lvl, 0.25), e["t"])
        elif k == "riser":
            r = riser(e["dur"]) * 0.22 * lvl; add(fx, reverb(r, 0.2), e["t"] - e["dur"])
        elif k == "whoosh": add(fx, pan(whoosh(e.get("dur", 0.8), e.get("reverse", False)) * 0.16 * lvl, e.get("pan", 0)), e["t"])
        elif k == "rewind": add(fx, reverb(tape_rewind(e["dur"]) * 0.42 * lvl, 0.15), e["t"])
        elif k == "blip": add(fx, reverb(pan(blip(e.get("f", 988)) * 0.12 * lvl, e.get("pan", 0)), 0.3), e["t"])
        elif k == "chime": add(fx, reverb(chime(e.get("f", 659.25)) * 0.13 * lvl, 0.45), e["t"])
        elif k == "tick": add(fx, pan(tick(0.12 * lvl, seed=int(e["t"] * 100)), e.get("pan", 0)), e["t"])
        elif k == "mute":  # duck the music bed (e.g. during a rewind)
            i0, i1 = int(e["t"] * SR), int((e["t"] + e["dur"]) * SR)
            ramp = np.ones(i1 - i0); m = int(0.08 * SR)
            ramp[:] = e.get("to", 0.15); ramp[:m] = np.linspace(1, e.get("to", 0.15), m); ramp[-m:] = np.linspace(e.get("to", 0.15), 1, m)
            music[i0:i1] *= ramp[:, None]
    return music[:int(T * SR)], fx[:int(T * SR)]

# ---------------------------------------------------------------- mix
def load_mono(path):
    import os
    path = os.path.abspath(path)
    x, sr = sf.read(path, dtype="float64")
    if x.ndim > 1: x = x.mean(1)
    if sr != SR: x = resample_poly(x, SR, sr)
    return x

def mix(lines, T, music, fx, out_wav, vo_gain_db=0.0, duck_db=-9.0, music_db=-17.0, fx_db=-6.0):
    n = int(T * SR)
    vo = np.zeros(n)
    for ln in lines:
        x = load_mono(ln["file"])
        # gentle presence EQ + de-ess-ish shelf
        x = x + 0.25 * bp(x, 2500, 5000) - 0.15 * hp(x, 7500)
        i = int(ln["t0"] * SR); j = min(n, i + len(x)); vo[i:j] += x[:j - i]
    vo *= 10 ** (vo_gain_db / 20)
    # sidechain ducking from VO envelope
    envv = np.abs(vo); win = int(0.12 * SR)
    envv = np.convolve(envv, np.ones(win) / win, mode="same")
    act = np.clip(envv / (np.percentile(envv[envv > 1e-4], 60) + 1e-9), 0, 1)
    act = np.convolve(act, np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    duck = 10 ** ((duck_db * act) / 20)
    m = music * 10 ** (music_db / 20) * duck[:, None]
    f = fx * 10 ** (fx_db / 20)
    mixd = np.stack([vo, vo], 1) + m + f
    peak = np.abs(mixd).max()
    if peak > 0.98: mixd *= 0.98 / peak
    sf.write(out_wav, mixd.astype(np.float32), SR)

def loudnorm(in_wav, out_wav, I=-14.0, TP=-1.0):
    """two-pass EBU R128 to YouTube's reference loudness."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", in_wav, "-af", f"loudnorm=I={I}:TP={TP}:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    af = (f"loudnorm=I={I}:TP={TP}:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", in_wav, "-af", af, "-ar", "48000", out_wav], check=True)
    return js
