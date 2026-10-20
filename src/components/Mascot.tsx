import React from 'react';
import {useCurrentFrame, useVideoConfig, staticFile} from 'remotion';
import {useAudioData, visualizeAudio} from '@remotion/media-utils';
import type {QuizStory} from '../Quiz';

// Q-Bit: Maskottchen von COULD YOU PASS?
//   - Kostüm nach Thema (story.mascot oder automatisch aus header/title)
//   - Mund folgt der Lautstärke des Voiceovers
//   - jubelt bei jeder Auflösung, schaut in den letzten Sekunden nervös zum Countdown
// Alle Bewegungen hängen am Frame (keine CSS-Animationen), damit das Rendern stabil bleibt.

export type Costume = 'standard' | 'halloween' | 'football' | 'christmas' | 'science' | 'history';
export type MascotSetting = Costume | 'auto' | 'off';

const RULES: [Costume, RegExp][] = [
  ['halloween', /hallowe?en|spooky|horror|witch|pumpkin|monster|zombie/i],
  ['christmas', /christmas|xmas|santa|advent|winter holiday/i],
  ['football', /football|soccer|premier league|champions league|world cup|bundesliga|la liga|serie a|\bfifa\b|\bnfl\b|super bowl|euro 20\d\d/i],
  ['science', /science|chemistry|physics|biology|space|planet|element|genius|\biq\b|math/i],
  ['history', /history|ancient|viking|roman|empire|which came first|pharaoh|medieval/i],
];

export const pickCostume = (story: Pick<QuizStory, 'header' | 'title'> & {mascot?: MascotSetting}): Costume | null => {
  const m = story.mascot ?? 'auto';
  if (m === 'off') return null;
  if (m !== 'auto') return m;
  const text = `${story.header ?? ''} ${story.title ?? ''}`;
  for (const [c, re] of RULES) if (re.test(text)) return c;
  return 'standard';
};

export type Mood = 'idle' | 'happy' | 'tense';

const INK = '#2b2250';

/** Reines Bild: Q-Bit in einem Zustand. viewBox 300x380. */
export const QBit: React.FC<{
  costume: Costume;
  frame: number;
  fps: number;
  /** 0 = Mund zu, 1 = weit offen */
  talk: number;
  mood: Mood;
  /** Frames seit Beginn der Stimmung (für Sprung/Winken) */
  moodFrame: number;
  /** Blickrichtung bei "tense": -1 links, 1 rechts */
  look?: number;
  width: number;
}> = ({costume, frame, fps, talk, mood, moodFrame, look = 1, width}) => {
  const sec = frame / fps;
  const bob = Math.sin((sec / 2.4) * Math.PI * 2) * 6;
  const blinkPhase = frame % Math.round(fps * 4.2);
  const blink = blinkPhase < 4 ? 0.1 : 1;
  const sway = Math.sin((sec / 3) * Math.PI * 2) * 8;
  const ms = moodFrame / fps;
  const jump = mood === 'happy' && ms < 1 ? -Math.abs(Math.sin((ms / 0.5) * Math.PI)) * 34 : 0;
  const wave = mood === 'happy' && ms < 1.4 ? -40 * Math.abs(Math.sin(ms * Math.PI * 3.2)) : 0;
  const shake = mood === 'tense' ? Math.sin(frame * 1.9) * 1.6 : 0;
  const pupilX = mood === 'tense' ? 7 * look : 0;
  const ball = Math.abs(Math.sin((sec / 1.2) * Math.PI));
  const is = (c: Costume) => costume === c;
  const hat = is('halloween') || is('christmas') || is('history');
  const open = mood === 'happy' ? Math.max(talk, 0.35) : talk;

  return (
    <svg viewBox="0 0 300 380" width={width} height={(width * 380) / 300} style={{overflow: 'visible'}}>
      <defs>
        <clipPath id="qbit-body"><circle cx="150" cy="210" r="100" /></clipPath>
        <radialGradient id="qbit-skin" cx="40%" cy="35%" r="75%">
          <stop offset="0" stopColor="#ffe07a" />
          <stop offset=".6" stopColor="#ffc93c" />
          <stop offset="1" stopColor="#f2a516" />
        </radialGradient>
      </defs>
      <ellipse cx="150" cy="352" rx={90 + jump * 0.6} ry="12" fill="#000" opacity={0.3} />
      <g transform={`translate(${shake} ${bob + jump})`}>
        {is('halloween') && (
          <g>
            <path d="M78 160 L28 338 Q150 312 272 338 L222 160 Z" fill="#3b1858" />
            <path d="M92 170 L52 326 Q150 304 248 326 L208 170 Z" fill="#b3203a" />
          </g>
        )}
        {!hat && (
          <g transform={`rotate(${sway} 150 112)`}>
            <path d="M150 112 Q146 96 150 82" stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" />
            <circle cx="150" cy="62" r="23" fill="#7cf2d4" stroke={INK} strokeWidth={5} />
            <text x="150" y="73" textAnchor="middle" fontFamily="Montserrat, sans-serif" fontWeight={900} fontSize={30} fill={INK}>?</text>
          </g>
        )}
        <ellipse cx="115" cy="314" rx="28" ry="15" fill="#f2a516" stroke={INK} strokeWidth={5} />
        <ellipse cx="185" cy="314" rx="28" ry="15" fill="#f2a516" stroke={INK} strokeWidth={5} />
        <g>
          <ellipse cx="52" cy="232" rx="16" ry="26" transform="rotate(25 52 232)" fill="#ffc93c" stroke={INK} strokeWidth={5} />
          {is('football') && <ellipse cx="58" cy="220" rx="15" ry="13" fill="#e63946" />}
        </g>
        <g transform={`rotate(${wave} 236 248)`}>
          <ellipse cx="248" cy="232" rx="16" ry="26" transform="rotate(-25 248 232)" fill="#ffc93c" stroke={INK} strokeWidth={5} />
          {is('football') && <ellipse cx="242" cy="220" rx="15" ry="13" fill="#e63946" />}
        </g>
        <circle cx="150" cy="210" r="100" fill="url(#qbit-skin)" />
        <g clipPath="url(#qbit-body)">
          {is('football') && (
            <g>
              <rect x="40" y="262" width="220" height="60" fill="#e63946" />
              <path d="M128 262 L150 284 L172 262 Z" fill="#ffc93c" />
              <rect x="40" y="300" width="220" height="7" fill="#fff" />
              <text x="150" y="300" textAnchor="middle" fontFamily="Montserrat, sans-serif" fontWeight={900} fontSize={20} fill="#fff">10</text>
              <rect x="40" y="132" width="220" height="15" fill="#fff" />
              <rect x="40" y="137" width="220" height="5" fill="#e63946" />
            </g>
          )}
          {is('science') && (
            <g>
              <rect x="40" y="268" width="220" height="60" fill="#f4f6ff" />
              <path d="M112 268 L150 300 L188 268 Z" fill="#5aa9e6" />
              <path d="M112 268 L132 320 M188 268 L168 320" stroke="#c8cde8" strokeWidth={4} />
              <rect x="40" y="183" width="220" height="12" fill={INK} />
            </g>
          )}
          {is('christmas') && (
            <g>
              <rect x="40" y="272" width="220" height="22" fill="#1f8a4c" />
              {[70, 120, 170, 220].map((x) => <rect key={x} x={x} y="272" width="10" height="22" fill="#fff" />)}
            </g>
          )}
        </g>
        <circle cx="150" cy="210" r="100" fill="none" stroke={INK} strokeWidth={6} />
        {is('christmas') && <path d="M188 290 L206 334 L226 330 L206 288 Z" fill="#1f8a4c" stroke={INK} strokeWidth={3} />}
        {is('standard') && (
          <g>
            <path d="M150 288 L124 276 L124 300 Z M150 288 L176 276 L176 300 Z" fill="#7cf2d4" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
            <circle cx="150" cy="288" r="6" fill={INK} />
          </g>
        )}
        <ellipse cx="96" cy="236" rx="14" ry="8" fill="#ff8a7a" opacity={mood === 'happy' ? 0.85 : 0.55} />
        <ellipse cx="204" cy="236" rx="14" ry="8" fill="#ff8a7a" opacity={mood === 'happy' ? 0.85 : 0.55} />
        {mood === 'happy' ? (
          <g stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round">
            <path d="M99 202 Q117 180 135 202" />
            <path d="M165 202 Q183 180 201 202" />
          </g>
        ) : (
          <g transform={`translate(0 196) scale(1 ${blink}) translate(0 -196)`}>
            <ellipse cx="117" cy="196" rx="22" ry="26" fill="#fff" stroke={INK} strokeWidth={4} />
            <ellipse cx="183" cy="196" rx="22" ry="26" fill="#fff" stroke={INK} strokeWidth={4} />
            <g transform={`translate(${pupilX} 0)`}>
              <circle cx="121" cy="200" r="11" fill={INK} />
              <circle cx="179" cy="200" r="11" fill={INK} />
              <circle cx="125" cy="195" r="4" fill="#fff" />
              <circle cx="183" cy="195" r="4" fill="#fff" />
            </g>
          </g>
        )}
        {is('science') && (
          <g fill="#9fe3ff" fillOpacity={0.35} stroke="#5aa9e6" strokeWidth={7}>
            <circle cx="117" cy="196" r="30" />
            <circle cx="183" cy="196" r="30" />
          </g>
        )}
        {open > 0.08 ? (
          <ellipse cx="150" cy={246 + 8 * open} rx={14 + 6 * open} ry={4 + 13 * open} fill="#7a1f2b" stroke={INK} strokeWidth={4} />
        ) : mood === 'tense' ? (
          <path d="M132 254 Q141 248 150 254 Q159 260 168 254" fill="none" stroke={INK} strokeWidth={6} strokeLinecap="round" />
        ) : (
          <path d="M126 246 Q150 272 174 246 Q150 256 126 246 Z" fill="#7a1f2b" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
        )}
        {is('halloween') && (
          <g fill="#fff" stroke={INK} strokeWidth={2}>
            <path d="M137 247 L141 260 L145 249 Z" />
            <path d="M155 249 L159 260 L163 247 Z" />
          </g>
        )}
        {is('halloween') && (
          <g>
            <ellipse cx="150" cy="122" rx="82" ry="15" fill="#2a1840" stroke={INK} strokeWidth={4} />
            <path d="M104 120 L168 18 Q182 10 180 30 L196 120 Z" fill="#3b1858" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
            <path d="M110 104 L192 104 L195 118 L106 118 Z" fill="#ff8c1a" />
          </g>
        )}
        {is('christmas') && (
          <g transform={`rotate(${sway * 0.4} 150 130)`}>
            <path d="M84 132 Q140 40 208 64 Q236 74 246 112 L216 132 Z" fill="#d62839" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
            <rect x="74" y="122" width="152" height="24" rx="12" fill="#fff" stroke={INK} strokeWidth={4} />
            <circle cx="248" cy="118" r="15" fill="#fff" stroke={INK} strokeWidth={4} />
          </g>
        )}
        {is('history') && (
          <g>
            <path d="M66 150 Q70 70 150 64 Q230 70 234 150 Z" fill="#9aa3b5" stroke={INK} strokeWidth={5} />
            <rect x="60" y="140" width="180" height="18" rx="6" fill="#c9a24a" stroke={INK} strokeWidth={4} />
            <path d="M70 120 Q34 106 30 58 Q56 90 84 100 Z" fill="#fff5dc" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
            <path d="M230 120 Q266 106 270 58 Q244 90 216 100 Z" fill="#fff5dc" stroke={INK} strokeWidth={4} strokeLinejoin="round" />
            <rect x="143" y="146" width="14" height="44" rx="4" fill="#9aa3b5" stroke={INK} strokeWidth={3} />
          </g>
        )}
      </g>
      {is('football') && (
        <g transform={`translate(0 ${-22 * ball}) rotate(${ball * 180} 262 330)`}>
          <circle cx="262" cy="330" r="20" fill="#fff" stroke={INK} strokeWidth={4} />
          <path d="M262 321 L270 327 L267 337 L257 337 L254 327 Z" fill={INK} />
        </g>
      )}
      {is('halloween') && (
        <g>
          <ellipse cx="262" cy="334" rx="24" ry="19" fill="#ff8c1a" stroke={INK} strokeWidth={4} />
          <path d="M262 316 Q264 306 270 304" stroke="#1f8a4c" strokeWidth={5} fill="none" strokeLinecap="round" />
          <path d="M252 330 L256 324 L260 330 Z M264 330 L268 324 L272 330 Z M252 340 Q262 348 272 340" fill={INK} stroke={INK} strokeWidth={2} />
        </g>
      )}
      {is('science') && (
        <path d="M254 300 L254 316 L240 344 Q238 350 246 350 L278 350 Q286 350 284 344 L270 316 L270 300 Z" fill="#7cf2d4" fillOpacity={0.8} stroke={INK} strokeWidth={4} strokeLinejoin="round" />
      )}
    </svg>
  );
};

/** Lautstärke des Voiceovers im aktuellen Frame (0..1). Ohne Audio: 0. */
const useTalk = (audio: string | undefined, frame: number, fps: number) => {
  const data = useAudioData(audio ? staticFile(audio) : staticFile('sfx/tick.wav'));
  if (!audio || !data) return 0;
  const bins = visualizeAudio({fps, frame, audioData: data, numberOfSamples: 32});
  // Sprachbereich: untere Bänder mitteln, etwas verstärken
  const v = bins.slice(1, 10).reduce((a, b) => a + b, 0) / 9;
  return Math.max(0, Math.min(1, (v - 0.012) * 14));
};

/**
 * Q-Bit über dem ganzen Video. Stimmung ergibt sich aus der aktuellen Frage:
 * letzte 3 s vor der Auflösung "tense", danach 1,4 s "happy", im Abspann winkt er.
 */
export const QuizMascot: React.FC<{
  story: QuizStory & {mascot?: MascotSetting};
  /** Position der linken oberen Ecke und Breite in Pixel */
  x: number;
  y: number;
  width: number;
  /** wohin er bei "tense" schaut (Richtung Countdown) */
  look: number;
}> = ({story, x, y, width, look}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const costume = pickCostume(story);
  const talk = useTalk(story.audio, frame, fps);
  if (!costume) return null;
  const t = frame / fps;
  let mood: Mood = 'idle';
  let since = 0;
  const q = story.questions.find((qq) => t >= qq.start && t < qq.end);
  if (q) {
    if (t >= q.reveal && t < q.reveal + 1.4) {
      mood = 'happy';
      since = t - q.reveal;
    } else if (t >= q.reveal - 3 && t < q.reveal) {
      mood = 'tense';
      since = t - (q.reveal - 3);
    }
  } else if (t >= story.outroStart) {
    mood = 'happy';
    since = (t - story.outroStart) % 2.5;
  }
  return (
    <div style={{position: 'absolute', left: x, top: y, width, pointerEvents: 'none'}}>
      <QBit costume={costume} frame={frame} fps={fps} talk={talk} mood={mood} moodFrame={Math.round(since * fps)} look={look} width={width} />
    </div>
  );
};
