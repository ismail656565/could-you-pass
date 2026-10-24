"""Spricht jede Zeile einzeln mit Kokoro, misst die Länge und schreibt narration.wav + timings.json."""
import json, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
cfg = json.load(open(sys.argv[1])); models = sys.argv[2]; out = sys.argv[3]
k = Kokoro(f"{models}/kokoro-v1.0.onnx", f"{models}/voices-v1.0.bin")
def voice(v):
    if '+' not in v and ':' not in v: return v
    vs = np.load(f"{models}/voices-v1.0.bin")
    parts = [(p.split(':')[0], float(p.split(':')[1])) for p in v.split('+')]
    tot = sum(w for _, w in parts)
    return sum(vs[n].astype('float32') * (w / tot) for n, w in parts)
v = voice(cfg['voice']); lang = 'en-gb' if cfg['voice'].startswith('b') else 'en-us'
sr = 24000; lead = 0.4; gap = 0.35
audio = [np.zeros(int(sr * lead), dtype=np.float32)]; t = lead; timings = []
for line in cfg['lines']:
    s, sr = k.create(line['text'], voice=v, speed=cfg.get('speed', 1.0), lang=lang)
    timings.append(round(t, 3)); audio += [s.astype(np.float32), np.zeros(int(sr * gap), dtype=np.float32)]
    t += len(s) / sr + gap
sf.write(f"{out}/narration.wav", np.concatenate(audio), sr)
json.dump({"starts": timings, "end": round(t + 1.2, 3)}, open(f"{out}/timings.json", "w"))
print(timings, t)
