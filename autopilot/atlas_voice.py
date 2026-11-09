"""Stimme + Zeitplan für ein Short im Layout "atlas" (Remotion-Komposition "TrueSize").
Aufruf:  python autopilot/atlas_voice.py stories/map-lie-1.json
Liest hookLine und rounds[].lines aus der Story, spricht sie mit der Kanalstimme (Kokoro, kostenlos),
legt die Clips in public/audio/<id>/ ab und schreibt die Zeiten (Sekunden) zurück in die Story."""
import json, subprocess, sys
from pathlib import Path
import imageio_ffmpeg
ap = None  # Modul autopilot (wird von produce_one übergeben; beim direkten Aufruf importiert)

FF = imageio_ffmpeg.get_ffmpeg_exe()
THINK, MOVE, TAIL, HOOK_PAD, OUTRO = 2.4, 1.5, 0.55, 0.25, 2.2


def clip(text, out):
    wav = out.with_suffix('.wav')
    wav.write_bytes(ap.kokoro_wav(text, ap.DEFAULT_VOICE, 1.04))
    # Stille an den Rändern kappen, auf einheitliche Lautheit bringen
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', str(wav), '-af',
                    'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-15:TP=-1.5:LRA=11',
                    '-ar', '44100', '-b:a', '160k', str(out)], check=True)
    wav.unlink()
    r = subprocess.run([FF, '-i', str(out)], capture_output=True, text=True).stderr
    h, m, s = r.split('Duration: ')[1].split(',')[0].split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def main(path, autopilot_module=None):
    global ap
    if autopilot_module is not None:
        ap = autopilot_module
    elif ap is None:
        sys.path.insert(0, str(Path(__file__).parent))
        import autopilot as ap_mod
        ap = ap_mod
    p = Path(path)
    story = json.loads(p.read_text(encoding='utf8'))
    sid = story['id']
    d = ap.ROOT / 'public' / 'audio' / sid
    d.mkdir(parents=True, exist_ok=True)
    t = 0.0
    dur = clip(story['hookLine'], d / 'hook.mp3')
    story['hook'] = {'audio': f'audio/{sid}/hook.mp3', 'start': 0.0, 'end': round(dur + HOOK_PAD, 2)}
    t = story['hook']['end']
    for i, r in enumerate(story['rounds']):
        dq = clip(r['lines']['q'], d / f'q{i + 1}.mp3')
        da = clip(r['lines']['a'], d / f'a{i + 1}.mp3')
        last = i == len(story['rounds']) - 1
        r['start'] = round(t, 2)
        r['qAudio'], r['aAudio'] = f'audio/{sid}/q{i + 1}.mp3', f'audio/{sid}/a{i + 1}.mp3'
        r['thinkStart'] = round(t + dq + 0.1, 2)
        r['reveal'] = round(r['thinkStart'] + THINK, 2)
        r['moveEnd'] = round(r['reveal'] + MOVE, 2)
        # Antwort wird gesprochen, sobald die Form unterwegs ist
        r['aStart'] = round(r['reveal'] + 0.55, 2)
        r['end'] = round(max(r['moveEnd'] + 1.6, r['aStart'] + da) + (OUTRO if last else TAIL), 2)
        t = r['end']
    story['durationInSeconds'] = round(t, 2)
    p.write_text(json.dumps(story, indent=1, ensure_ascii=False), encoding='utf8')
    print('Dauer', story['durationInSeconds'], 's')


if __name__ == '__main__':
    main(sys.argv[1])
