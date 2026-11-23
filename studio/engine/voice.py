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


DICT = Path(__file__).with_name('pronunciations.json')


def _core(tok): return re.sub(r"[^\w'-]", '', tok.lower())


def rules(say=None):
    """shared pronunciation dictionary (pronunciations.json) + episode overrides (EPISODE['say']), longest term first"""
    r = {}
    if DICT.exists():
        r.update({k: v for k, v in json.loads(DICT.read_text(encoding='utf-8')).items() if not k.startswith('_')})
    r.update(say or {})
    return sorted(((k.split(), v.split()) for k, v in r.items()), key=lambda kv: -len(kv[0]))


def speak(line, rl):
    """written line -> groups [(written_start, written_end, spoken_tokens)]. Only the voice hears the spoken form;
    captions, cues and display mappings keep using the written words."""
    toks, out, i = line.split(), [], 0
    while i < len(toks):
        for term, spoken in rl:
            n = len(term)
            if [_core(t) for t in toks[i:i + n]] == [_core(t) for t in term]:
                lead = re.match(r"^[^\w]*", toks[i]).group(0)
                trail = re.search(r"[^\w]*$", toks[i + n - 1]).group(0)
                sp = list(spoken); sp[0] = lead + sp[0]; sp[-1] = sp[-1] + trail
                out.append((i, i + n, sp)); i += n
                break
        else:
            out.append((i, i + 1, [toks[i]])); i += 1
    return out


def spoken_text(groups): return ' '.join(w for _, _, sp in groups for w in sp)


def synth(lines, out_dir, voice, speed=1.0, say=None):
    from kokoro_onnx import Kokoro
    k = Kokoro(*models())
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    man, rl = [], rules(say)
    for i, line in enumerate(lines):
        spoken = spoken_text(speak(line, rl))
        audio, sr = k.create(spoken, voice=voice, speed=speed, lang='en-us')
        thr = 0.01 * np.max(np.abs(audio))
        nz = np.where(np.abs(audio) > thr)[0]
        audio = audio[max(0, nz[0] - int(0.04 * sr)):min(len(audio), nz[-1] + int(0.06 * sr))]
        fn = out_dir / f'vo_{i:02d}.wav'
        sf.write(fn, audio, sr)
        man.append(dict(i=i, text=line, spoken=spoken, file=str(fn), dur=len(audio) / sr))
    return man


def _norm(w): return re.sub(r"[^a-z0-9']", '', w.lower())


def align(man, model_size='base.en', say=None):
    from faster_whisper import WhisperModel
    from scipy.signal import resample_poly
    model = WhisperModel(model_size, device='cpu', compute_type='int8')
    rl = rules(say)
    for m in man:
        m['_rules'] = rl
        au, sr = sf.read(m['file'], dtype='float32')
        if au.ndim > 1: au = au.mean(1)
        au = resample_poly(au, 16000, sr).astype('float32')
        segs, _ = model.transcribe(au, word_timestamps=True, language='en', beam_size=5)
        words = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
        groups = speak(m['text'], m.pop('_rules'))
        sw = [w for _, _, sp in groups for w in sp]
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
        written, k = m['text'].split(), 0
        m['words'] = []
        for w0, w1, sp in groups:                         # spoken timing -> the written words it stands for
            t0, t1 = timing[k][0], timing[k + len(sp) - 1][1]; k += len(sp)
            n = w1 - w0
            for j in range(n):
                m['words'].append(dict(w=written[w0 + j], t0=float(t0 + (t1 - t0) * j / n), t1=float(t0 + (t1 - t0) * (j + 1) / n)))
        m['asr'] = ' '.join(w for w, _, _ in words)
        m['match'] = SequenceMatcher(None, a, b).ratio()
    return man


def narrate(lines, out_dir, voice, speed=1.0, say=None):
    p = Path(out_dir) / 'manifest.json'
    rl = rules(say)
    if p.exists():
        man = json.loads(p.read_text())
        if [(m['text'], m.get('spoken', m['text'])) for m in man] == [(l, spoken_text(speak(l, rl))) for l in lines]:
            return man
    man = align(synth(lines, out_dir, voice, speed, say), say=say)
    p.write_text(json.dumps(man, indent=1))
    return man
