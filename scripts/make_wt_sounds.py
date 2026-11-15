"""Erzeugt die eigenen (lizenzfreien) Sounds für Wildly True – komplett synthetisch, keine fremden Samples.
  public/sfx/wt-pulse.wav  Musikbett, 120 BPM, 16 s nahtlose Schleife (Beat 1 bei 0,0 s) – Schnitte rasten darauf ein
  public/sfx/wt-boom.wav   Impact (Hook + Schlüsselfakt)
  public/sfx/wt-swish.wav  leiser Whoosh für Schnitte
Aufruf: python scripts/make_wt_sounds.py"""
from pathlib import Path
import numpy as np
import soundfile as sf

SR = 44100
OUT = Path(__file__).resolve().parent.parent / 'public' / 'sfx'
rng = np.random.default_rng(7)


def env_exp(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def kick(amp=1.0):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 42 + 95 * np.exp(-t / 0.045)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return amp * np.sin(ph) * env_exp(n, 0.11)


def hat(amp=0.25):
    n = int(0.045 * SR)
    x = rng.standard_normal(n)
    x = np.diff(x, prepend=0)  # Hochpass
    return amp * x * env_exp(n, 0.012)


def lowpass(x, a):
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc)
        y[i] = acc
    return y


def pulse_bed():
    bpm, bars_beats = 120, 32
    beat = 60 / bpm
    n = int(round(bars_beats * beat * SR))  # 16 s
    t = np.arange(n) / SR
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.125 * t)  # 2 volle Zyklen pro Schleife
    drone = 0.16 * np.sin(2 * np.pi * 55 * t) + 0.09 * np.sin(2 * np.pi * 82.5 * t) + 0.04 * np.sin(2 * np.pi * 110 * t + 0.3)
    drone *= lfo
    # leise dunkle Fläche aus gefiltertem Rauschen (atmet mit dem LFO)
    air = lowpass(rng.standard_normal(n) * 0.05, 0.02) * (1.2 - lfo)
    mix = drone + air
    # Herzschlag-Puls: Kick auf jedem Schlag, Akzent auf 1, Hi-Hat auf den Offbeats ab Takt 3
    for k in range(bars_beats):
        s = int(round(k * beat * SR))
        kk = kick(0.55 if k % 4 == 0 else 0.32)
        e = min(n, s + len(kk))
        mix[s:e] += kk[:e - s]
        if k >= 8:
            h = hat(0.07)
            s2 = int(round((k + 0.5) * beat * SR))
            e2 = min(n, s2 + len(h))
            mix[s2:e2] += h[:e2 - s2]
    # nahtlos: Drone/LFO haben ganze Zyklen in 16 s, die letzte Kick (0,35 s) klingt vor dem Schleifenende aus
    mix /= np.max(np.abs(mix)) / 0.8
    return mix.astype(np.float32)


def boom():
    n = int(1.4 * SR)
    t = np.arange(n) / SR
    f = 34 + 120 * np.exp(-t / 0.08)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.38)
    click = rng.standard_normal(n) * env_exp(n, 0.006) * 0.5
    rumble = lowpass(rng.standard_normal(n), 0.01) * env_exp(n, 0.5) * 3
    x = body + click + rumble
    return (x / np.max(np.abs(x)) * 0.9).astype(np.float32)


def swish():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    # Filter öffnet und schließt sich (Glocke), Lautstärke-Hüllkurve mit Gipfel bei 0,12 s
    shape = np.exp(-((t - 0.12) / 0.07) ** 2)
    y = np.empty(n)
    acc = 0.0
    for i in range(n):
        a = 0.02 + 0.25 * shape[i]
        acc += a * (noise[i] - acc)
        y[i] = acc
    y *= shape
    return (y / np.max(np.abs(y)) * 0.7).astype(np.float32)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    sf.write(OUT / 'wt-pulse.wav', pulse_bed(), SR)
    sf.write(OUT / 'wt-boom.wav', boom(), SR)
    sf.write(OUT / 'wt-swish.wav', swish(), SR)
    print('ok')
