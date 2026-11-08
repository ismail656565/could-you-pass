import React from 'react';
import {AbsoluteFill, Img, Loop, OffthreadVideo, continueRender, delayRender, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {QuizQuestion, QuizStory} from './Quiz';
import {StickMan, type StickPose} from './components/StickHost';
import {useTalk} from './components/Mascot';

// Layout "stick": 2D-Zeichentrick-Quiz auf Notizbuchpapier, ein Strichmännchen moderiert.
//   Karte oben (16:9) zeigt den LTX-Doodle-Clip (q.video), ein Foto oder große Emojis
//   Frage in Handschrift, Schlüsselwort mit Textmarker; Antworten als skizzierte Kästen (2x2)
//   unten links das Strichmännchen, daneben eine Sprechblase (Level → Countdown → "It's B!")
// Schriften liegen im Repo (public/fonts, OFL) – kein Google-Fonts-Abruf beim Rendern nötig.
const HAND = 'StickHand';
const MARK = 'StickMarker';
if (typeof document !== 'undefined' && typeof FontFace !== 'undefined') {
  const handle = delayRender('Stick-Schriften laden');
  Promise.all(
    [
      new FontFace(HAND, `url(${staticFile('fonts/Kalam-700.woff2')}) format('woff2')`, {weight: '400 900'}),
      new FontFace(MARK, `url(${staticFile('fonts/PermanentMarker-400.woff2')}) format('woff2')`),
    ].map((f) => f.load().then((ff) => document.fonts.add(ff))),
  )
    .catch((e) => console.warn('Stick-Schrift fehlt', e))
    .finally(() => continueRender(handle));
}

export const K = {
  paper: '#FBF7EC',
  line: '#C9DCF2',
  margin: '#F2A6A6',
  ink: '#1B1B1B',
  pencil: '#55514A',
  hi: '#FFE45C',
  green: '#7BE495',
  red: '#E63946',
  blue: '#3D7BF7',
};
const TILE = ['#FFD6E0', '#CDEBFF', '#FFF1B8', '#D7F5DC'];

const X = 60;
const W = 960;
const CARD_Y = 220;
const CARD_H = 540;
const Q_Y = 786;
const Q_H = 206;
const GRID_Y = 1010;
const TILE_W = 430;
const TILE_H = 140;
const GAP = 20;
const LETTERS = ['A', 'B', 'C', 'D'];

// ------------------------------------------------------------ Grundbausteine
export const Paper: React.FC = () => (
  <AbsoluteFill style={{background: K.paper}}>
    <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
      {Array.from({length: 40}, (_, i) => (
        <line key={i} x1={0} x2={1080} y1={120 + i * 46} y2={120 + i * 46} stroke={K.line} strokeWidth={2} />
      ))}
      <line x1={36} x2={36} y1={0} y2={1920} stroke={K.margin} strokeWidth={3} />
    </svg>
  </AbsoluteFill>
);

/** Rechteck mit wackligen, "kochenden" Bleistiftlinien (zweimal nachgezogen) */
const sketchPath = (w: number, h: number, seed: string, amp = 5) => {
  const j = (n: string) => (random(seed + n) - 0.5) * 2 * amp;
  const pts: [number, number][] = [
    [6 + j('a'), 6 + j('b')],
    [w - 6 + j('c'), 6 + j('d')],
    [w - 6 + j('e'), h - 6 + j('f')],
    [6 + j('g'), h - 6 + j('h')],
  ];
  const mid = (p: [number, number], q: [number, number], s: string): string => {
    const mx = (p[0] + q[0]) / 2 + j(s + 'x') * 0.8;
    const my = (p[1] + q[1]) / 2 + j(s + 'y') * 0.8;
    return `Q${mx} ${my} ${q[0]} ${q[1]}`;
  };
  return `M${pts[0][0]} ${pts[0][1]} ${mid(pts[0], pts[1], '1')} ${mid(pts[1], pts[2], '2')} ${mid(pts[2], pts[3], '3')} ${mid(pts[3], pts[0], '4')}`;
};

export const SketchBox: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  seed: string;
  fill?: string;
  stroke?: string;
  sw?: number;
  rotate?: number;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}> = ({x, y, w, h, seed, fill = '#fff', stroke = K.ink, sw = 6, rotate = 0, style, children}) => {
  const frame = useCurrentFrame();
  const b = Math.floor(frame / 3) % 4;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, transform: `rotate(${rotate}deg)`, ...style}}>
      <svg width={w} height={h} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
        <path d={sketchPath(w, h, `${seed}-f`, 3)} fill={fill} stroke="none" />
        <path d={sketchPath(w, h, `${seed}-${b}`)} fill="none" stroke={stroke} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" />
        <path d={sketchPath(w, h, `${seed}-${b}-2`, 6)} fill="none" stroke={stroke} strokeWidth={sw * 0.35} strokeLinecap="round" opacity={0.55} />
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{children}</div>
    </div>
  );
};

/** Text mit **Markierung**: Textmarker wischt ab dem Moment, in dem die Stimme das Wort sagt */
const Marked: React.FC<{text: string; at?: number}> = ({text, at}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const k = at == null ? interpolate(t, [0.4, 0.8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : interpolate(t, [at, at + 0.35], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      {text.split(/(\*\*[^*]+\*\*)/g).map((part, i) =>
        part.startsWith('**') ? (
          <span
            key={i}
            style={{
              backgroundImage: `linear-gradient(100deg, transparent 0%, ${K.hi} 2%, ${K.hi} 97%, transparent 100%)`,
              backgroundSize: `${k * 100}% 62%`,
              backgroundPosition: '0 78%',
              backgroundRepeat: 'no-repeat',
              padding: '0 4px',
            }}
          >
            {part.slice(2, -2)}
          </span>
        ) : (
          <span key={i}>{part}</span>
        ),
      )}
    </>
  );
};

const qSize = (s: string) => (s.length > 90 ? 52 : s.length > 64 ? 60 : s.length > 40 ? 68 : 76);
const aSize = (s: string) => (s.length > 22 ? 38 : s.length > 14 ? 46 : 54);

/** Klebezettel mit Tesafilm (Hook, Teaser, Final, CTA) */
const Sticky: React.FC<{text: string; x: number; y: number; from?: number; until?: number; color?: string; rot?: number; size?: number}> = ({text, x, y, from = 0, until, color = K.hi, rot = -3, size = 46}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  if (t < from || (until != null && t >= until)) return null;
  const s = spring({frame: frame - Math.round(from * fps), fps, config: {damping: 11, stiffness: 210}});
  const out = until != null ? interpolate(t, [until - 0.15, until], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `rotate(${rot}deg) scale(${s * out})`, transformOrigin: 'left top', zIndex: 20}}>
      <div style={{position: 'absolute', left: '50%', top: -18, width: 120, height: 36, marginLeft: -60, background: 'rgba(255,255,255,0.65)', border: '1px solid rgba(0,0,0,0.08)', transform: 'rotate(4deg)'}} />
      <div style={{background: color, padding: '16px 30px', fontFamily: MARK, fontSize: size, color: K.ink, boxShadow: '6px 8px 0 rgba(0,0,0,0.18)', whiteSpace: 'nowrap'}}>{text}</div>
    </div>
  );
};

// ------------------------------------------------------------ Szene je Frage
const Card: React.FC<{q: QuizQuestion; index: number}> = ({q, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const revealed = t >= q.reveal;
  const pop = spring({frame: frame - 2, fps, config: {damping: 12, stiffness: 160}});
  return (
    <SketchBox x={X} y={CARD_Y} w={W} h={CARD_H} seed={`card${index}`} sw={7}>
      <div style={{position: 'absolute', left: 16, top: 16, right: 16, bottom: 16, overflow: 'hidden', borderRadius: 6, background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        {revealed && q.revealImage ? (
          <Img src={staticFile(q.revealImage)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        ) : q.video ? (
          <Loop durationInFrames={Math.round(5.9 * fps)}>
            <OffthreadVideo src={staticFile(q.video)} muted style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'saturate(0.9) contrast(1.05)'}} />
          </Loop>
        ) : q.image ? (
          <Img src={staticFile(q.image)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'grayscale(0.15) contrast(1.05)'}} />
        ) : (
          <div style={{fontFamily: q.cardText && /\p{Extended_Pictographic}/u.test(q.cardText) ? 'Noto Color Emoji, sans-serif' : MARK, fontSize: (q.cardText ?? '?').length > 6 ? 120 : 230, color: K.ink, textAlign: 'center', whiteSpace: 'pre-line', lineHeight: 1.1, transform: `scale(${pop}) rotate(${Math.sin(frame / 14) * 3}deg)`}}>
            {q.cardText ?? '?'}
          </div>
        )}
        {revealed && q.revealCaption ? (
          <div style={{position: 'absolute', bottom: 18, left: 18, background: K.ink, color: '#fff', fontFamily: MARK, fontSize: 40, padding: '6px 18px', transform: 'rotate(-2deg)'}}>{q.revealCaption}</div>
        ) : null}
      </div>
    </SketchBox>
  );
};

const Answer: React.FC<{q: QuizQuestion; i: number; index: number; correctLabel?: string}> = ({q, i, index, correctLabel}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const since = (t - q.reveal) * fps;
  const ok = i === q.correct;
  const col = i % 2;
  const row = Math.floor(i / 2);
  const x = X + col * (TILE_W + GAP);
  const y = GRID_Y + row * (TILE_H + GAP);
  const appear = index === 0 ? 1 : spring({frame: frame - 3 - i * 3, fps, config: {damping: 13, stiffness: 200}});
  const rev = since >= 0;
  const fillK = rev && ok ? interpolate(since, [0, 8], [0, 1], {extrapolateRight: 'clamp'}) : 0;
  const strikeK = rev && !ok ? interpolate(since, [2 + i * 2, 9 + i * 2], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const bump = rev && ok ? 1 + 0.08 * Math.max(0, Math.sin((since / fps) * Math.PI * 3)) * interpolate(since, [0, 20], [1, 0], {extrapolateRight: 'clamp'}) : 1;
  const text = q.answers[i] ?? '';
  return (
    <div style={{position: 'absolute', left: 0, top: 0, opacity: appear * (rev && !ok ? 0.55 : 1), transform: `translateY(${(1 - appear) * 40}px)`}}>
      <SketchBox x={x} y={y} w={TILE_W} h={TILE_H} seed={`a${index}-${i}`} fill={rev && ok ? '#fff' : TILE[i]} rotate={((i % 3) - 1) * 0.8} style={{transform: `rotate(${((i % 3) - 1) * 0.8}deg) scale(${bump})`}}>
        {fillK > 0 ? (
          <svg width={TILE_W} height={TILE_H} style={{position: 'absolute', inset: 0}}>
            <rect x={10} y={10} width={(TILE_W - 20) * fillK} height={TILE_H - 20} fill={K.green} rx={8} />
          </svg>
        ) : null}
        <div style={{position: 'relative', display: 'flex', alignItems: 'center', gap: 18, width: '100%', padding: '0 26px'}}>
          <div style={{width: 62, height: 62, borderRadius: 31, border: `5px solid ${K.ink}`, background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: MARK, fontSize: 36, color: K.ink, flexShrink: 0}}>{LETTERS[i]}</div>
          <div style={{fontFamily: HAND, fontWeight: 700, fontSize: aSize(text), lineHeight: 1.05, color: K.ink}}>{text}</div>
        </div>
        {strikeK > 0 ? (
          <svg width={TILE_W} height={TILE_H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
            <path d={`M30 ${TILE_H * 0.62} Q${TILE_W / 2} ${TILE_H * 0.4} ${30 + (TILE_W - 60) * strikeK} ${TILE_H * 0.48}`} stroke={K.red} strokeWidth={8} fill="none" strokeLinecap="round" />
          </svg>
        ) : null}
        {rev && ok && since > 6 ? (
          <div style={{position: 'absolute', right: -14, top: -30, fontFamily: MARK, fontSize: 34, background: K.ink, color: '#fff', padding: '4px 14px', transform: `rotate(6deg) scale(${spring({frame: since - 6, fps, config: {damping: 9, stiffness: 240}})})`}}>
            {correctLabel ?? 'CORRECT!'}
          </div>
        ) : null}
      </SketchBox>
    </div>
  );
};

export const StickScene: React.FC<{q: QuizQuestion; index: number; total: number; story: QuizStory}> = ({q, index, total, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const enter = index === 0 ? 1 : spring({frame, fps, config: {damping: 14, stiffness: 180}});
  const plain = q.q.replace(/\*\*/g, '');
  const n = story.questions.length;
  return (
    <AbsoluteFill>
      <Paper />
      {/* Kopfzeile */}
      <div style={{position: 'absolute', left: X, top: 120, width: W, display: 'flex', alignItems: 'center', gap: 18}}>
        <div style={{fontFamily: MARK, fontSize: 40, color: K.ink, transform: 'rotate(-2deg)'}}>{story.header}</div>
        <div style={{flex: 1}} />
        <div style={{display: 'flex', gap: 10}}>
          {Array.from({length: total}, (_, i) => (
            <div key={i} style={{width: 26, height: 26, borderRadius: 13, border: `4px solid ${K.ink}`, background: i < index ? K.ink : i === index ? K.hi : 'transparent'}} />
          ))}
        </div>
      </div>
      <div style={{position: 'absolute', inset: 0, opacity: enter, transform: `translateX(${(1 - enter) * 140}px) rotate(${(1 - enter) * 2}deg)`}}>
        <Card q={q} index={index} />
        <div style={{position: 'absolute', left: X + 10, top: Q_Y, width: W - 20, height: Q_H, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center'}}>
          <div style={{fontFamily: HAND, fontWeight: 700, fontSize: qSize(plain), lineHeight: 1.12, color: K.ink}}>
            <Marked text={q.q} at={q.keywordAt != null ? q.keywordAt - q.start : undefined} />
          </div>
        </div>
      </div>
      {q.answers.slice(0, 4).map((_, i) => (
        <Answer key={i} q={q} i={i} index={index} correctLabel={story.correctLabel} />
      ))}
      {index === 0 && story.hook ? <Sticky text={story.hook} x={X + 30} y={CARD_Y + 40} until={2.8} /> : null}
      {index === 0 && story.teaser ? <Sticky text={story.teaser} x={X + 30} y={CARD_Y + 40} from={story.hook ? 2.8 : 0} until={q.countdownStart - q.start + 0.01} color="#BDE3FF" rot={2} /> : null}
      {index === n - 1 && index > 0 && story.finalLabel ? <Sticky text={story.finalLabel} x={X + 30} y={CARD_Y + 40} until={q.countdownStart - q.start} color="#FFB3C1" /> : null}
      {story.midLabel && index === Math.floor(n / 2) && index !== n - 1 ? <Sticky text={story.midLabel} x={X + 30} y={CARD_Y + 40} from={0.6} until={q.countdownStart - q.start} color="#BDE3FF" rot={2} /> : null}
      {index === n - 1 && story.ctaText && t >= q.reveal + 0.5 ? <Sticky text={story.ctaText} x={X + 60} y={CARD_Y + CARD_H - 140} from={q.reveal - q.start + 0.5} size={44} rot={-2} /> : null}
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------ Moderator (liegt über allen Fragen, damit er nie "neu startet")
type Phase = {pose: StickPose; start: number; bubble?: {kind: 'count' | 'text'; text: string}};

const phaseAt = (story: QuizStory, t: number): Phase => {
  const qs = story.questions;
  const i = qs.findIndex((q) => t >= q.start && t < q.end);
  if (i < 0) {
    if (t >= story.outroStart) return {pose: 'wave', start: story.outroStart};
    return {pose: 'idle', start: 0};
  }
  const q = qs[i];
  if (t < q.countdownStart) return {pose: 'point', start: q.start, bubble: q.level ? {kind: 'text', text: q.level.toUpperCase() === 'HARD' ? 'HARD ONE!' : q.level.toUpperCase()} : undefined};
  if (t < q.reveal) {
    const left = Math.ceil(q.reveal - t);
    const nervousFrom = Math.max(q.countdownStart, q.reveal - 1.6);
    return t >= nervousFrom
      ? {pose: 'nervous', start: nervousFrom, bubble: {kind: 'count', text: String(left)}}
      : {pose: 'think', start: q.countdownStart, bubble: {kind: 'count', text: String(left)}};
  }
  const it = `IT'S ${LETTERS[q.correct]}!`;
  if (t < q.reveal + 1.3) return {pose: 'cheer', start: q.reveal, bubble: {kind: 'text', text: it}};
  return {pose: 'pointDown', start: q.reveal + 1.3, bubble: {kind: 'text', text: it}};
};

export const StickHostOverlay: React.FC<{story: QuizStory; x: number; y: number; width: number}> = ({story, x, y, width}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const talk = useTalk(story.audio, frame, fps);
  const ph = phaseAt(story, t);
  const prev = phaseAt(story, ph.start - 0.001);
  const since = t - ph.start;
  const outro = t >= story.outroStart && (story.durationInSeconds ?? 0) - story.outroStart > 0.3;
  const bx = x + width * 0.86;
  const by = y + 20;
  const b = ph.bubble;
  const pop = spring({frame: Math.round(since * fps), fps, config: {damping: 10, stiffness: 260}});
  const countPulse = b?.kind === 'count' ? 1 + 0.12 * Math.max(0, 1 - ((t % 1) * 4)) : 1;
  return (
    <>
      <div style={{position: 'absolute', left: outro ? 540 - 230 : x, top: outro ? 880 : y, width: outro ? 460 : width, pointerEvents: 'none', zIndex: 30}}>
        <StickMan frame={frame} fps={fps} pose={ph.pose} prevPose={prev.pose === ph.pose ? 'idle' : prev.pose} since={since} talk={talk} width={outro ? 460 : width} id="host" />
      </div>
      {b && !outro ? (
        <div style={{position: 'absolute', left: bx, top: by, zIndex: 31, transform: `scale(${pop * countPulse})`, transformOrigin: '0% 100%'}}>
          <svg width={300} height={190} style={{position: 'absolute', left: -20, top: -10, overflow: 'visible'}}>
            {b.kind === 'count' ? (
              <>
                <circle cx={10} cy={182} r={9} fill="#fff" stroke={K.ink} strokeWidth={5} />
                <circle cx={36} cy={160} r={14} fill="#fff" stroke={K.ink} strokeWidth={5} />
                <path d="M70 120 Q40 70 90 50 Q110 6 160 26 Q205 0 236 40 Q290 50 270 100 Q290 140 240 150 Q210 180 160 160 Q120 180 96 150 Q50 150 70 120 Z" fill="#fff" stroke={K.ink} strokeWidth={6} strokeLinejoin="round" />
              </>
            ) : (
              <path d="M40 30 Q40 10 70 10 L250 10 Q280 10 280 40 L280 110 Q280 140 250 140 L90 140 L20 182 L56 140 Q40 140 40 110 Z" fill="#fff" stroke={K.ink} strokeWidth={6} strokeLinejoin="round" />
            )}
          </svg>
          <div style={{position: 'absolute', left: b.kind === 'count' ? 52 : 20, top: b.kind === 'count' ? 14 : 0, width: b.kind === 'count' ? 230 : 260, height: 140, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: MARK, fontSize: b.kind === 'count' ? 96 : b.text.length > 7 ? 44 : 54, color: b.kind === 'count' && Number(b.text) <= 1 ? K.red : K.ink}}>
            {b.text}
          </div>
        </div>
      ) : null}
    </>
  );
};

export const StickOutro: React.FC<{story: QuizStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 12, stiffness: 200}});
  return (
    <AbsoluteFill>
      <Paper />
      <div style={{position: 'absolute', top: 300, width: 1080, textAlign: 'center', opacity: s}}>
        <div style={{fontFamily: HAND, fontWeight: 700, fontSize: 92, color: K.ink, lineHeight: 1.05}}>{story.outroText}</div>
        <div style={{display: 'inline-block', marginTop: 40, fontFamily: MARK, fontSize: 170, color: K.ink, background: K.hi, padding: '0 50px', transform: `rotate(-3deg) scale(${interpolate(s, [0, 1], [0.7, 1])})`}}>?/{story.questions.length}</div>
        {story.outroSub ? <div style={{fontFamily: HAND, fontWeight: 700, fontSize: 56, marginTop: 30, color: K.ink}}>{story.outroSub}</div> : null}
      </div>
    </AbsoluteFill>
  );
};
