"""Hörproben mit Kokoro (kostenlos, Apache-2.0) für mehrere Stimmen erzeugen."""
import subprocess, sys
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro

M = Path(sys.argv[1])
OUT = Path(__file__).parent / 'voice-samples'
OUT.mkdir(exist_ok=True)
TEXT = ("Which planet is the hottest in our solar system? ... "
        "Venus! Not Mercury. Its thick clouds trap the heat. "
        "If you got that right, you're smarter than ninety percent of people. Comment your score below!")
VOICES = ['af_heart', 'af_bella', 'am_michael', 'am_fenrir', 'am_puck', 'am_onyx', 'bm_george', 'bf_emma']
k = Kokoro(str(M / 'kokoro-v1.0.onnx'), str(M / 'voices-v1.0.bin'))
for v in VOICES:
    lang = 'en-gb' if v.startswith('b') else 'en-us'
    samples, sr = k.create(TEXT, voice=v, speed=1.05, lang=lang)
    wav = OUT / f'{v}.wav'
    sf.write(wav, samples, sr)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-b:a', '128k', str(OUT / f'kokoro-{v}.mp3')], check=True)
    wav.unlink()
    print('ok', v)
