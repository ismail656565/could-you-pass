"""Hörproben mit Kokoro (kostenlos, Apache-2.0) für mehrere Stimmen und eigene Mischungen erzeugen."""
import subprocess, sys
from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

M = Path(sys.argv[1])
OUT = Path(__file__).parent / 'voice-samples'
OUT.mkdir(exist_ok=True)
TEXT = ("Welcome back, quiz friends! Forty questions today. Ready? "
        "Which planet has the shortest day? ... "
        "Jupiter! Under ten hours. I'll be honest, that one fooled me too. "
        "How many did you get? Comment your score below!")
VOICES = ['bf_emma', 'bf_isabella', 'bf_alice', 'bf_lily', 'bm_lewis', 'bm_daniel', 'bm_fable', 'af_kore', 'af_aoede', 'am_eric',
          'bf_emma:70+bf_isabella:30', 'bf_emma:60+af_heart:40', 'bm_george:60+bm_lewis:40', 'bf_isabella:60+bf_lily:40']
vs = np.load(str(M / 'voices-v1.0.bin'))
k = Kokoro(str(M / 'kokoro-v1.0.onnx'), str(M / 'voices-v1.0.bin'))
for v in VOICES:
    if '+' in v:
        parts = [(p.split(':')[0], float(p.split(':')[1])) for p in v.split('+')]
        tot = sum(w for _, w in parts)
        voice = sum(vs[n].astype('float32') * (w / tot) for n, w in parts)
    else:
        voice = v
    lang = 'en-gb' if v.startswith('b') else 'en-us'
    samples, sr = k.create(TEXT, voice=voice, speed=1.0, lang=lang)
    name = v.replace(':', '').replace('+', '_')
    wav = OUT / f'{name}.wav'
    sf.write(wav, samples, sr)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-b:a', '128k', str(OUT / f'kokoro-{name}.mp3')], check=True)
    wav.unlink()
    print('ok', v, round(len(samples) / sr, 1), 's')
