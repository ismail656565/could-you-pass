"""Narration: Kokoro-82M (Apache-2.0, local ONNX) + word timings from faster-whisper (MIT). No paid API."""
import json, os, re, urllib.request
from difflib import SequenceMatcher
from pathlib import Path
import numpy as np, soundfile as sf

MODELS = Path(os.environ.get('KOKORO_DIR', Path.home() / '.cache' / 'kokoro'))
URLS = {'kokoro-v1.0.onnx': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx',
        'voices-v1.0.bin': 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin'}


def models():
    MODELS.mkdir(parents=True, exist_ok=True)
    for name, url in URLS.items():
        p = MODELS / name
        if not p.exists():
            print('download', name, flush=True)
            urllib.request.urlretrieve(url, p)
    return str(MODELS / 'kokoro-v1.0.onnx'), str(MODELS / 'voices-v1.0.bin')


def synth(lines, out_dir, voice, speed=1.0):
    from kokoro_onnx import Kokoro
    k = Kokoro(*models())
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    man = []
    for i, line in enumerate(lines):
        audio, sr = k.create(line, voice=voice, speed=speed, lang='en-us')
        thr = 0.01 * np.max(np.abs(audio))
        nz = np.where(np.abs(audio) > thr)[0]
        audio = audio[max(0, nz[0] - int(0.04 * sr)):min(len(audio), nz[-1] + int(0.06 * sr))]
        fn = out_dir / f'vo_{i:02d}.wav'
        sf.write(fn, audio, sr)
        man.append(dict(i=i, text=line, file=str(fn), dur=len(audio) / sr))
    return man


def _norm(w): return re.sub(r"[^a-z0-9']", '', w.lower())


def align(man, model_size='base.en'):
    from faster_whisper import WhisperModel
    from scipy.signal import resample_poly
    model = WhisperModel(model_size, device='cpu', compute_type='int8')
    for m in man:
        au, sr = sf.read(m['file'], dtype='float32')
        if au.ndim > 1: au = au.mean(1)
        au = resample_poly(au, 16000, sr).astype('float32')
        segs, _ = model.transcribe(au, word_timestamps=True, language='en', beam_size=5)
        words = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
        sw = m['text'].split()
        a = [_norm(w) for w in sw]; b = [_norm(w) for w, _, _ in words]
        timing = [None] * len(sw)
        for tag, i1, i2, j1, j2 in SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag == 'equal':
                for k in range(i2 - i1): timing[i1 + k] = (words[j1 + k][1], words[j1 + k][2])
            elif tag == 'replace':
                t0, t1 = words[j1][1], words[j2 - 1][2]
                for k in range(i2 - i1): timing[i1 + k] = (t0 + (t1 - t0) * k / (i2 - i1), t0 + (t1 - t0) * (k + 1) / (i2 - i1))
        for i in range(len(timing)):
            if timing[i] is None:
                prev = next((timing[j][1] for j in range(i - 1, -1, -1) if timing[j]), 0.0)
                nxt = next((timing[j][0] for j in range(i + 1, len(timing)) if timing[j]), m['dur'])
                timing[i] = (prev, nxt)
        m['words'] = [dict(w=w, t0=float(a_), t1=float(b_)) for w, (a_, b_) in zip(sw, timing)]
        m['asr'] = ' '.join(w for w, _, _ in words)
        m['match'] = SequenceMatcher(None, a, b).ratio()
    return man


def narrate(lines, out_dir, voice, speed=1.0):
    p = Path(out_dir) / 'manifest.json'
    if p.exists():
        man = json.loads(p.read_text())
        if [m['text'] for m in man] == list(lines):
            return man
    man = align(synth(lines, out_dir, voice, speed))
    p.write_text(json.dumps(man, indent=1))
    return man
