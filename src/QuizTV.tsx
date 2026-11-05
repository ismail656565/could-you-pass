import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadSerif} from '@remotion/google-fonts/DMSerifDisplay';
import type {QuizQuestion, QuizStory} from './Quiz';

// Layout "tvshow" – seit 03.11.2026 im "Editorial"-Look (Besitzer: weniger AI-Look).
//   Vorbild: Trivia Square ("Can You Pass the U.S. Citizenship Test?", 2,6 Mio Views):
//   flacher Nachthimmel-Hintergrund mit feinem Sternenmuster statt Scheinwerfer/Glows,
//   Frage auf cremefarbenem "Papier", Fotos/Clips mit Passepartout wie ein gedrucktes Bild,
//   ruhige flache Antwortzeilen mit Buchstaben-Kreis, Serifen-Wortmarke, dünne Linien,
//   nach der Auflösung optional ein "DID YOU KNOW?"-Feld (q.fact).
//   Keine Verläufe auf Flächen, keine Sechsecke, kein Gold-Chrom, keine Emojis als Deko.
// Enthält: TvScene (Short 1080x1920), TvLongScene + TvLongOutro (1920x1080), TvThumb (1280x720), CompareScene
const inter = loadInter('normal', {weights: ['500', '600', '700', '800', '900'], subsets: ['latin', 'latin-ext']});
const serif = loadSerif('normal', {weights: ['400'], subsets: ['latin', 'latin-ext']});
const FONT = inter.fontFamily;
const SERIF = serif.fontFamily;

export const T = {
  bg: '#14213D',
  navy: '#1B2B4F',
  blue: '#24396B',
  gold: '#E9B44C', // Senf/Ocker statt Chrom-Gold
  goldDark: '#B9842B',
  silver: '#C8CFDB',
  white: '#FFFFFF',
  orange: '#E9B44C',
  green: '#2E8B57',
  greenLight: '#3DA56A',
  red: '#C8312E',
  paper: '#F4EEDF',
  paperDark: '#E6DCC4',
  ink: '#18213A',
  line: 'rgba(244,238,223,0.22)',
};
const LETTERS = ['A', 'B', 'C', 'D'];
const levelColor = (l: string) => (/legend/i.test(l) ? '#B98AE8' : /very/i.test(l) ? '#E07A5F' : /hard|schwer/i.test(l) ? '#E9A06B' : /med|mittel/i.test(l) ? T.gold : '#7FC8A9');

/** Schlüsselwort rot; mit `at` (Sekunden ab Szenenstart) zusätzlich wortgenau zur Stimme: kurzer Pop + Marker-Unterstrich (Idee: video-talkcraft) */
export const TvHighlighted: React.FC<{text: string; accent?: string; at?: number}> = ({text, accent = T.gold, at}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const synced = typeof at === 'number' && at >= 0;
  const f = synced ? frame - Math.round((at as number) * fps) : 0;
  const sweep = synced ? interpolate(f, [0, 7], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const pop = synced ? 1 + 0.09 * Math.sin(Math.PI * interpolate(f, [0, 9], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})) : 1;
  return (
    <>
      {text.split(/(\*\*[^*]+\*\*)/).map((p, i) =>
        p.startsWith('**') ? (
          <span key={i} style={{color: accent, display: synced ? 'inline-block' : undefined, transform: synced ? `scale(${pop})` : undefined, backgroundImage: synced ? `linear-gradient(${accent}38, ${accent}38)` : undefined, backgroundRepeat: 'no-repeat', backgroundPosition: '0 88%', backgroundSize: synced ? `${sweep * 100}% 0.22em` : undefined}}>
            {p.slice(2, -2)}
          </span>
        ) : (
          <span key={i}>{p}</span>
        ),
      )}
    </>
  );
};

/** Hintergrund: flaches Nachtblau mit feinem, ruhigem Sternenmuster (statisch, kein Licht-Effekt) */
const STARS = (() => {
  const out: {x: number; y: number; r: number; o: number}[] = [];
  let s = 7;
  const rnd = () => ((s = (s * 9301 + 49297) % 233280) / 233280);
  for (let i = 0; i < 70; i++) out.push({x: rnd() * 100, y: rnd() * 100, r: rnd() < 0.85 ? 1.6 : 2.6, o: 0.12 + rnd() * 0.22});
  return out;
})();

export const TvBackground: React.FC = () => (
  <AbsoluteFill style={{background: T.bg, overflow: 'hidden'}}>
    <svg width="100%" height="100%" style={{position: 'absolute', inset: 0}}>
      {STARS.map((p, i) => (
        <circle key={i} cx={`${p.x}%`} cy={`${p.y}%`} r={p.r} fill={T.paper} opacity={p.o} />
      ))}
    </svg>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, transparent 65%, rgba(0,0,0,0.28) 100%)'}} />
  </AbsoluteFill>
);

export type LozengeState = 'normal' | 'lock' | 'right' | 'dim';

/** Flache Karte (früher Sechseck-"Lozenge"): abgerundet, 2-px-Rand, keine Verläufe. paper = cremefarbenes Papier. */
export const Lozenge: React.FC<{x: number; y: number; w: number; h: number; state?: LozengeState; children?: React.ReactNode; style?: React.CSSProperties; line?: boolean; paper?: boolean}> = ({
  x,
  y,
  w,
  h,
  state = 'normal',
  children,
  style,
  paper = false,
}) => {
  const fill = state === 'right' ? T.green : state === 'lock' ? T.gold : paper ? T.paper : T.navy;
  const border = state === 'right' ? '#7FD3A2' : state === 'lock' ? '#F6D58E' : paper ? T.paperDark : 'rgba(244,238,223,0.28)';
  const pad = Math.min(h * 0.28, 34);
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width: w,
        height: h,
        boxSizing: 'border-box',
        borderRadius: paper ? 14 : 12,
        background: fill,
        border: `2px solid ${border}`,
        boxShadow: paper ? '0 10px 0 rgba(0,0,0,0.18)' : '0 4px 0 rgba(0,0,0,0.18)',
        opacity: state === 'dim' ? 0.45 : 1,
        display: 'flex',
        alignItems: 'center',
        padding: `0 ${pad}px`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};

const answerState = (revealed: boolean, ok: boolean, since: number): LozengeState => {
  if (!revealed) return 'normal';
  if (!ok) return 'dim';
  return since < 9 ? 'lock' : 'right';
};

/** Countdown: schlichter Kreis wie eine Stoppuhr-Marke (Papier + Tinte) */
export const TvTimer: React.FC<{q: QuizQuestion; x: number; y: number; size: number}> = ({q, x, y, size}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  if (t >= q.reveal) return null;
  const total = Math.max(0.5, q.reveal - q.countdownStart);
  const p = interpolate(t, [q.countdownStart, q.reveal], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const counting = t >= q.countdownStart;
  const left = q.reveal - t;
  const n = counting ? Math.max(1, Math.ceil(left)) : Math.round(total);
  const color = counting && left <= 1 ? T.red : T.ink;
  const r = size / 2 - 10;
  const circ = 2 * Math.PI * r;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: size, height: size}}>
      <svg width={size} height={size}>
        <circle cx={size / 2} cy={size / 2} r={size / 2 - 1} fill={T.paper} stroke={T.paperDark} strokeWidth={2} />
        <circle cx={size / 2} cy={size / 2} r={r} stroke="rgba(24,33,58,0.12)" strokeWidth={7} fill="none" />
        <circle cx={size / 2} cy={size / 2} r={r} stroke={color} strokeWidth={7} fill="none" strokeLinecap="butt" strokeDasharray={circ} strokeDashoffset={circ * (1 - p)} transform={`rotate(-90 ${size / 2} ${size / 2})`} />
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: SERIF, fontSize: size * 0.5, color, lineHeight: 1}}>{n}</div>
    </div>
  );
};

const cardFont = (text: string, maxH: number, maxW: number) => {
  const lines = text.split('\n');
  const longest = Math.max(...lines.map((l) => [...l].length));
  const byWidth = Math.floor(maxW / Math.max(3, longest * 0.62));
  return Math.min(byWidth, Math.floor(maxH / (lines.length * 1.25)), 150);
};

/** "DID YOU KNOW?"-Streifen unten im Bild nach der Auflösung (nur wenn q.fact gesetzt) */
const FactStrip: React.FC<{q: QuizQuestion; w: number; size: number}> = ({q, w, size}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  if (!q.fact || frame < revealFrame + 12) return null;
  const a = interpolate(frame, [revealFrame + 12, revealFrame + 20], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 18, right: 18, bottom: 18, opacity: a, transform: `translateY(${(1 - a) * 16}px)`, background: T.paper, border: `2px solid ${T.paperDark}`, borderRadius: 10, padding: `${size * 0.45}px ${size * 0.7}px`, maxWidth: w - 36, boxSizing: 'border-box'}}>
      <div style={{fontFamily: FONT, fontWeight: 800, fontSize: size * 0.7, letterSpacing: 2, color: T.red, marginBottom: 6}}>DID YOU KNOW?</div>
      <div style={{fontFamily: FONT, fontWeight: 600, fontSize: size, lineHeight: 1.25, color: T.ink}}>{q.fact}</div>
    </div>
  );
};

/** Bildkarte wie ein gedrucktes Foto: Papier-Passepartout, keine Goldrahmen. Ohne Foto/Clip: Papierkarte mit Tinte. */
const TvCard: React.FC<{q: QuizQuestion; story: QuizStory; x: number; y: number; w: number; h: number; index?: number; factSize?: number}> = ({q, x, y, w, h, index = 0, factSize = 30}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const len = Math.max(1, (q.end - q.start) * fps);
  const zoom = interpolate(frame, [0, len], [1.0, 1.05]);
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const a = frame >= revealFrame ? spring({frame: frame - revealFrame, fps, config: {damping: 20}}) : 0;
  const media = Boolean(q.video || q.image);
  const mat = 14;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 14, padding: mat, boxSizing: 'border-box', background: T.paper, border: `2px solid ${T.paperDark}`, boxShadow: '0 12px 0 rgba(0,0,0,0.2)'}}>
      <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 6, overflow: 'hidden', background: media ? '#0E1528' : T.paper, border: media ? `1px solid ${T.paperDark}` : 'none'}}>
        {q.video ? (
          <OffthreadVideo src={staticFile(q.video)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        ) : q.image ? <Img src={staticFile(q.image)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} /> : null}
        {q.cardText && !media ? (
          <>
            <div style={{position: 'absolute', left: 24, top: 18, fontFamily: SERIF, fontSize: Math.round(h * 0.09), color: 'rgba(24,33,58,0.35)'}}>No. {index + 1}</div>
            <div style={{position: 'absolute', left: 24, right: 24, top: Math.round(h * 0.16), height: 2, background: 'rgba(24,33,58,0.12)'}} />
            <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', whiteSpace: 'pre-line', fontFamily: SERIF, color: T.ink, fontSize: cardFont(q.cardText, h * 0.5, w * 0.78), lineHeight: 1.15, paddingTop: h * 0.06}}>
              {q.cardText}
            </div>
          </>
        ) : null}
        {q.revealImage && a > 0 ? (
          <div style={{position: 'absolute', inset: 0, opacity: a}}>
            <Img src={staticFile(q.revealImage)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          </div>
        ) : null}
        {q.revealImage && q.revealCaption && a > 0 ? (
          <div style={{position: 'absolute', left: 20, bottom: 20, fontFamily: FONT, fontWeight: 800, fontSize: 38, color: T.ink, background: T.paper, borderRadius: 8, padding: '4px 16px', opacity: a}}>{q.revealCaption}</div>
        ) : null}
        <FactStrip q={q} w={w - 2 * mat} size={factSize} />
      </div>
    </div>
  );
};

/** Etikett oben links im Bild: flach, kein Schatten-Glow */
const Banner: React.FC<{text: string; x: number; y: number; size: number; from?: number; until?: number; color?: string}> = ({text, x, y, size, from = 0, until, color = T.red}) => {
  const frame0 = useCurrentFrame();
  const {fps} = useVideoConfig();
  const frame = frame0 - Math.round(from * fps);
  if (frame < 0) return null;
  const inA = from === 0 ? 1 : interpolate(frame, [0, 6], [0, 1], {extrapolateRight: 'clamp'});
  const out = until === undefined ? 1 : interpolate(frame0, [fps * (until - 0.3), fps * until], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (out <= 0) return null;
  const light = color === T.silver || color === T.paper;
  return (
    <div style={{position: 'absolute', left: x, top: y, opacity: inA * out, background: light ? T.ink : color, color: light ? T.paper : T.white, fontFamily: FONT, fontWeight: 800, fontSize: size, letterSpacing: 0.5, padding: `${size * 0.18}px ${size * 0.5}px`, borderRadius: 6, zIndex: 5, whiteSpace: 'nowrap'}}>
      {text}
    </div>
  );
};

/** Kopfzeile wie bei Trivia Square: Wortmarke | Runde · Level | Q x/y, darunter eine dünne Linie */
const Header: React.FC<{q: QuizQuestion; index: number; total: number; header: string; x: number; y: number; w: number; size: number; round?: number}> = ({q, index, total, header, x, y, w, size, round}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w}}>
    <div style={{display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', fontFamily: FONT, fontWeight: 700, fontSize: size * 0.8, letterSpacing: size * 0.08, color: T.silver}}>
      <span style={{fontFamily: SERIF, fontSize: size * 1.15, letterSpacing: 0.5, color: T.paper}}>
        COULD YOU <span style={{color: T.gold}}>PASS?</span>
      </span>
      <span>
        {header}
        {q.level ? (
          <span>
            {' · '}
            {round ? `ROUND ${round} · ` : ''}
            <span style={{color: levelColor(q.level)}}>{q.level}</span>
          </span>
        ) : null}
      </span>
      <span style={{color: T.paper}}>
        Q {index + 1}/{total}
      </span>
    </div>
    <div style={{marginTop: size * 0.35, height: 2, background: T.line}} />
  </div>
);

const AnswerContent: React.FC<{i: number; text: string; state: LozengeState; size: number; tag?: string}> = ({i, text, state, size, tag}) => {
  const onLight = state === 'lock';
  const ring = state === 'right' ? T.white : onLight ? T.ink : T.paper;
  return (
    <div style={{display: 'flex', alignItems: 'center', width: '100%', fontFamily: FONT}}>
      <span style={{width: size * 1.2, height: size * 1.2, borderRadius: '50%', border: `2px solid ${ring}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: size * 0.62, color: ring, marginRight: size * 0.45, flexShrink: 0, background: state === 'right' ? 'rgba(255,255,255,0.15)' : 'transparent'}}>{state === 'right' ? '✓' : LETTERS[i]}</span>
      <span style={{fontWeight: 700, fontSize: text.length > 24 ? size * 0.78 : text.length > 16 ? size * 0.9 : size, color: onLight ? T.ink : T.white, lineHeight: 1.05, flex: 1}}>{text}</span>
      {tag ? <span style={{fontWeight: 800, fontSize: size * 0.5, letterSpacing: 1.5, color: T.white}}>{tag}</span> : null}
    </div>
  );
};

const qSizeFor = (plain: string, base: number) => (plain.length > 70 ? base * 0.72 : plain.length > 50 ? base * 0.82 : plain.length > 34 ? base * 0.92 : base);


// ---------------------------------------------------------------- Short 1080x1920
const S = {LEFT: 50, FULL_W: 980, CARD_Y: 250, CARD_H: 500, Q_Y: 800, Q_H: 220, ANS_Y: 1060, ANS_W: 890, ANS_H: 116, ANS_GAP: 22};
const sRow = (i: number) => S.ANS_Y + i * (S.ANS_H + S.ANS_GAP);

export const TvScene: React.FC<{q: QuizQuestion; index: number; total: number; story: QuizStory}> = ({q, index, total, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const revealed = t >= q.reveal;
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const since = frame - revealFrame;
  const enter = index === 0 ? 1 : interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const plain = q.q.replace(/\*\*/g, '');
  return (
    <AbsoluteFill>
      <TvBackground />
      <Header q={q} index={index} total={total} header={story.header} x={S.LEFT} y={150} w={S.FULL_W} size={34} />
      <div style={{position: 'absolute', inset: 0, opacity: enter}}>
        <TvCard q={q} story={story} x={S.LEFT} y={S.CARD_Y} w={S.FULL_W} h={S.CARD_H} index={index} factSize={34} />
        <Lozenge x={S.LEFT} y={S.Q_Y} w={S.FULL_W} h={S.Q_H} paper>
          <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: qSizeFor(plain, 76), lineHeight: 1.12, color: T.ink}}>
            <TvHighlighted text={q.q} accent={story.accent ?? T.red} at={q.keywordAt != null ? q.keywordAt - q.start : undefined} />
          </div>
        </Lozenge>
      </div>
      <TvTimer q={q} x={540 - 70} y={S.CARD_Y + S.CARD_H - 100} size={140} />
      {q.answers.map((a, i) => {
        const ok = i === q.correct;
        const st = answerState(revealed, ok, since);
        const appear = index === 0 ? 1 : interpolate(frame, [4 + i * 3, 10 + i * 3], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <Lozenge key={i} x={S.LEFT} y={sRow(i)} w={S.ANS_W} h={S.ANS_H} state={st} style={{opacity: appear * (st === 'dim' ? 0.42 : 1)}}>
            <AnswerContent i={i} text={a} state={st} size={50} tag={st === 'right' ? (story.correctLabel ?? 'CORRECT!') : undefined} />
          </Lozenge>
        );
      })}
      {index === 0 && story.hook ? <Banner text={story.hook} x={S.LEFT + 24} y={S.CARD_Y + 24} size={42} until={2.8} /> : null}
      {index === 0 && story.teaser ? <Banner text={story.teaser} x={S.LEFT + 24} y={S.CARD_Y + 24} size={42} from={story.hook ? 2.8 : 0} color={T.silver} /> : null}
      {index === total - 1 && index > 0 && story.finalLabel ? <Banner text={story.finalLabel} x={S.LEFT + 24} y={S.CARD_Y + 24} size={42} /> : null}
      {story.midLabel && index === Math.floor(total / 2) && index !== total - 1 ? <Banner text={story.midLabel} x={S.LEFT + 24} y={S.CARD_Y + 24} size={42} from={1.2} color={T.silver} /> : null}
      {index === total - 1 && story.ctaText && revealed ? (
        <Lozenge x={S.LEFT} y={sRow(4) - 6} w={S.ANS_W} h={96} state="lock" style={{opacity: interpolate(since, [6, 12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
          <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 42, color: '#040A2C'}}>{story.ctaText}</div>
        </Lozenge>
      ) : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- Long 1920x1080
const L = {X: 70, CARD_Y: 110, CARD_W: 1250, CARD_H: 460, LAD_X: 1380, LAD_W: 470, Q_Y: 610, Q_H: 165, ANS_Y1: 805, ANS_Y2: 930, ANS_W: 870, ANS_H: 104, COL2: 980};

/** Leiter rechts: alle Runden, aktuelle orange, geschaffte gold */
const Ladder: React.FC<{story: QuizStory; index: number}> = ({story, index}) => {
  const qs = story.questions;
  const levels = [...new Set(qs.map((x) => x.level ?? ''))].filter(Boolean);
  const cur = qs[index].level ?? '';
  const ci = levels.indexOf(cur);
  const rows = [...levels].reverse();
  const rowH = Math.min(74, Math.floor((L.CARD_H - 30) / Math.max(1, rows.length)) - 10);
  return (
    <div style={{position: 'absolute', left: L.LAD_X, top: L.CARD_Y, width: L.LAD_W, height: L.CARD_H, borderRadius: 14, background: T.navy, border: `2px solid ${T.line}`, padding: '14px 18px', display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10}}>
      {rows.map((lv) => {
        const li = levels.indexOf(lv);
        const count = qs.filter((x) => x.level === lv).length;
        const first = qs.findIndex((x) => x.level === lv);
        const active = li === ci;
        const done = li < ci;
        return (
          <div key={lv} style={{height: rowH, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 26px', borderRadius: 8, background: active ? T.paper : 'transparent', fontFamily: FONT, fontWeight: 800, fontSize: 30, letterSpacing: 2, color: active ? T.ink : done ? T.gold : T.silver, opacity: active || done ? 1 : 0.7}}>
            <span>{lv}</span>
            <span style={{fontSize: 26}}>{active ? `${index - first + 1}/${count}` : done ? '✓' : `${count} Q`}</span>
          </div>
        );
      })}
    </div>
  );
};

const LevelBanner: React.FC<{level: string; num: number}> = ({level, num}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const out = interpolate(frame, [fps * 1.4, fps * 1.8], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (out <= 0) return null;
  return (
    <AbsoluteFill style={{background: `rgba(20,33,61,${0.85 * out})`, opacity: out}}>
      <Lozenge x={460} y={390} w={1000} h={300} paper style={{opacity: a, flexDirection: 'column', justifyContent: 'center'}}>
        <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 40, letterSpacing: 8, color: T.red}}>ROUND {num}</div>
        <div style={{width: 120, height: 2, background: 'rgba(24,33,58,0.25)', margin: '18px 0'}} />
        <div style={{fontFamily: SERIF, fontSize: 120, lineHeight: 1, color: T.ink}}>{level.charAt(0) + level.slice(1).toLowerCase()}</div>
      </Lozenge>
    </AbsoluteFill>
  );
};

/** Abo-Knopf: Klick + Glocke, ohne Neon */
const TvSubscribe: React.FC<{scale?: number; delay?: number}> = ({scale = 1, delay = 0}) => {
  const frame = useCurrentFrame() - delay;
  const {fps} = useVideoConfig();
  if (frame < 0) return null;
  const inA = interpolate(frame, [0, 8], [0.6, 1], {extrapolateRight: 'clamp'});
  const clickAt = fps * 1.0;
  const clicked = frame >= clickAt;
  const press = frame >= clickAt && frame < clickAt + 5 ? 0.94 : 1;
  const bellAt = fps * 1.8;
  const bellOn = frame >= bellAt;
  const ring = bellOn ? Math.sin((frame - bellAt) * 0.9) * Math.max(0, 18 - (frame - bellAt) * 0.6) : 0;
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 24, transform: `scale(${scale * inA})`}}>
      <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 48, color: T.white, background: clicked ? '#3F3F46' : '#CC0000', padding: '16px 42px', borderRadius: 40, transform: `scale(${press})`}}>{clicked ? 'SUBSCRIBED ✓' : 'SUBSCRIBE'}</div>
      <div style={{fontSize: 60, transform: `rotate(${ring}deg)`, transformOrigin: '50% 10%', filter: bellOn ? 'none' : 'grayscale(1) opacity(0.6)'}}>🔔</div>
    </div>
  );
};

const MidSubscribe: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const out = interpolate(frame, [fps * 4.2, fps * 4.7], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (out <= 0) return null;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: L.CARD_Y + L.CARD_H - 130, display: 'flex', justifyContent: 'center', opacity: out}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 36, background: T.paper, border: `2px solid ${T.paperDark}`, borderRadius: 14, padding: '16px 36px'}}>
        <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 38, color: T.ink, maxWidth: 640, lineHeight: 1.15}}>{text}</div>
        <TvSubscribe scale={0.85} />
      </div>
    </div>
  );
};

export const TvLongScene: React.FC<{q: QuizQuestion; index: number; story: QuizStory}> = ({q, index, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const qs = story.questions;
  const total = qs.length;
  const t = q.start + frame / fps;
  const revealed = t >= q.reveal;
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const since = frame - revealFrame;
  const enter = index === 0 ? 1 : interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const plain = q.q.replace(/\*\*/g, '');
  const levels = [...new Set(qs.map((x) => x.level ?? ''))];
  const newLevel = q.level && (index === 0 || qs[index - 1].level !== q.level);
  const pos = (i: number) => ({x: i % 2 === 0 ? L.X : L.COL2, y: i < 2 ? L.ANS_Y1 : L.ANS_Y2});
  return (
    <AbsoluteFill>
      <TvBackground />
      <Header q={q} index={index} total={total} header={story.header} x={L.X} y={36} w={1780} size={34} round={levels.indexOf(q.level ?? '') + 1} />
      <Ladder story={story} index={index} />
      <div style={{position: 'absolute', inset: 0, opacity: enter}}>
        <TvCard q={q} story={story} x={L.X} y={L.CARD_Y} w={L.CARD_W} h={L.CARD_H} index={index} factSize={36} />
        <Lozenge x={L.X} y={L.Q_Y} w={1780} h={L.Q_H} paper>
          <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: qSizeFor(plain, 70), lineHeight: 1.12, color: T.ink}}>
            <TvHighlighted text={q.q} accent={story.accent ?? T.red} at={q.keywordAt != null ? q.keywordAt - q.start : undefined} />
          </div>
        </Lozenge>
      </div>
      <TvTimer q={q} x={L.X + L.CARD_W / 2 - 75} y={L.CARD_Y + L.CARD_H - 120} size={150} />
      {q.answers.map((a, i) => {
        const ok = i === q.correct;
        const st = answerState(revealed, ok, since);
        const {x, y} = pos(i);
        const appear = index === 0 ? 1 : interpolate(frame, [4 + i * 3, 10 + i * 3], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <Lozenge key={i} x={x} y={y} w={L.ANS_W} h={L.ANS_H} state={st} style={{opacity: appear * (st === 'dim' ? 0.42 : 1)}}>
            <AnswerContent i={i} text={a} state={st} size={46} tag={st === 'right' ? (story.correctLabel ?? 'CORRECT!') : undefined} />
          </Lozenge>
        );
      })}
      {index === 0 && story.hook ? <Banner text={story.hook} x={L.X + 24} y={L.CARD_Y + 24} size={40} until={4} /> : null}
      {index === total - 1 && story.finalLabel ? <Banner text={story.finalLabel} x={L.X + 24} y={L.CARD_Y + 24} size={40} /> : null}
      {index === total - 1 && story.ctaText && revealed ? <Banner text={story.ctaText} x={L.X + 24} y={L.CARD_Y + 24} size={40} from={(q.reveal - q.start) + 0.4} /> : null}
      {story.midCtaIndex === index && revealed ? (
        <Sequence from={revealFrame + Math.round(fps * 1.0)} layout="none">
          <MidSubscribe text={story.midCtaText ?? 'Enjoying the quiz? Subscribe & hit the bell!'} />
        </Sequence>
      ) : null}
      {newLevel && index > 0 ? <LevelBanner level={q.level!} num={levels.indexOf(q.level!) + 1} /> : null}
    </AbsoluteFill>
  );
};

export const TvLongOutro: React.FC<{story: QuizStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill>
      <TvBackground />
      <AbsoluteFill style={{opacity: a}}>
        <div style={{position: 'absolute', top: 120, left: 0, right: 0, textAlign: 'center', fontFamily: SERIF, fontSize: 96, color: T.paper}}>{story.outroText ?? 'How many did you get?'}</div>
        <Lozenge x={660} y={270} w={600} h={200} paper style={{justifyContent: 'center'}}>
          <div style={{fontFamily: SERIF, fontSize: 140, color: T.ink}}>?<span style={{color: T.red}}>/</span>{story.questions.length}</div>
        </Lozenge>
        <div style={{position: 'absolute', top: 520, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 54, color: T.white}}>{story.outroSub ?? 'Comment your score 👇'}</div>
        <div style={{position: 'absolute', top: 640, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
          <TvSubscribe scale={1.2} delay={Math.round(fps * 0.6)} />
        </div>
        <div style={{position: 'absolute', top: 820, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 600, fontSize: 38, color: T.silver}}>{story.subscribeText ?? 'New quiz every day – turn on the bell 🔔'}</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- Vorschaubild 1280x720 (Variante A im TV-Look)
/** Emoji-Rätsel fürs Vorschaubild: Papierkarten "🌧️ + 🎀 = ?" */
const ThumbPuzzle: React.FC<{tiles: string[]; size: number}> = ({tiles, size}) => (
  <div style={{display: 'flex', alignItems: 'center', gap: size * 0.12}}>
    {tiles.map((p, i) => (
      <React.Fragment key={i}>
        {i > 0 ? <div style={{fontFamily: FONT, fontWeight: 900, fontSize: size * 0.45, color: T.paper}}>+</div> : null}
        <div style={{width: size, height: size, borderRadius: 12, background: T.paper, border: `2px solid ${T.paperDark}`, boxShadow: '0 10px 0 rgba(0,0,0,0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: size * 0.62}}>{p}</div>
      </React.Fragment>
    ))}
    <div style={{fontFamily: FONT, fontWeight: 900, fontSize: size * 0.45, color: T.paper}}>=</div>
    <div style={{width: size, height: size, borderRadius: 12, background: T.red, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: SERIF, fontSize: size * 0.7, color: T.white, boxShadow: '0 10px 0 rgba(0,0,0,0.25)'}}>?</div>
  </div>
);

export const TvThumb: React.FC<{story: QuizStory & {thumbImage?: string; thumbBadge?: string; thumbEmoji?: string; thumbPuzzle?: string[]}; text: string; badge: string; variant?: 'A' | 'B' | 'C'}> = ({story, text, badge, variant = 'A'}) => {
  const plain = text.replace(/\*\*/g, '');
  const size = plain.length > 22 ? 104 : plain.length > 14 ? 120 : 136;
  const n = story.questions.length;
  const label = (story.header ?? story.title ?? '').toUpperCase();
  const puzzle = story.thumbPuzzle && story.thumbPuzzle.length ? story.thumbPuzzle : null;
  if (variant === 'B') {
    // wie Trivia Square: Foto vollflächig, dunkler Verlauf links, große Schrift, runder "50 QUESTIONS"-Stempel, rotes Etikett
    return (
      <AbsoluteFill style={{overflow: 'hidden', background: T.bg}}>
        {story.thumbImage ? <Img src={staticFile(story.thumbImage)} style={{position: 'absolute', right: 0, top: 0, width: 760, height: 720, objectFit: 'cover'}} /> : <TvBackground />}
        <AbsoluteFill style={{background: `linear-gradient(90deg, ${T.bg} 0%, ${T.bg} 42%, rgba(20,33,61,0.55) 66%, rgba(20,33,61,0) 100%)`}} />
        {puzzle && !story.thumbImage ? <div style={{position: 'absolute', right: 50, top: 440}}><ThumbPuzzle tiles={puzzle} size={140} /></div> : null}
        <div style={{position: 'absolute', left: 56, top: 54, background: T.red, color: T.white, fontFamily: FONT, fontWeight: 800, fontSize: 34, letterSpacing: 1, padding: '6px 18px', borderRadius: 6}}>{label}</div>
        <div style={{position: 'absolute', left: 56, top: 140, width: 760, fontFamily: FONT, fontWeight: 900, fontSize: size * 1.05, lineHeight: 0.96, letterSpacing: -1, color: T.white, textShadow: '0 5px 0 rgba(0,0,0,0.35)'}}>
          <TvHighlighted text={text} accent={T.gold} />
        </div>
        <div style={{position: 'absolute', left: 56, bottom: 60, fontFamily: FONT, fontWeight: 800, fontSize: 40, color: T.paper}}>{badge}</div>
        <div style={{position: 'absolute', right: 50, top: 46, width: 190, height: 190, borderRadius: '50%', background: T.gold, border: `4px solid ${T.ink}`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: T.ink}}>
          <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 84, lineHeight: 0.9}}>{n}</div>
          <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 22, letterSpacing: 2}}>QUESTIONS</div>
        </div>
      </AbsoluteFill>
    );
  }
  if (variant === 'C') {
    // Papier-Variante: cremefarben, Tinte + Rot, rechts eine Quizkarte mit Antwortzeilen
    return (
      <AbsoluteFill style={{overflow: 'hidden', background: T.paper}}>
        <div style={{position: 'absolute', left: 56, top: 50, fontFamily: SERIF, fontSize: 44, color: T.ink}}>
          COULD YOU <span style={{color: T.red}}>PASS?</span>
        </div>
        <div style={{position: 'absolute', left: 56, top: 112, width: 600, height: 3, background: T.ink, opacity: 0.8}} />
        <div style={{position: 'absolute', left: 56, top: 150, width: 640, fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 0.96, letterSpacing: -1, color: T.ink}}>
          <TvHighlighted text={text} accent={T.red} />
        </div>
        <div style={{position: 'absolute', left: 56, bottom: 56, fontFamily: FONT, fontWeight: 800, fontSize: 38, color: T.ink, opacity: 0.75}}>{badge}</div>
        <div style={{position: 'absolute', left: 740, top: 60, width: 490, height: 600, borderRadius: 16, background: T.bg, boxShadow: '0 14px 0 rgba(24,33,58,0.25)'}}>
          {story.thumbImage ? (
            <div style={{position: 'absolute', left: 24, top: 24, right: 24, height: 230, borderRadius: 8, overflow: 'hidden', border: `8px solid ${T.paper}`}}>
              <Img src={staticFile(story.thumbImage)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
            </div>
          ) : (
            <div style={{position: 'absolute', left: 24, top: 24, right: 24, height: 230, borderRadius: 8, background: T.paper, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 150}}>{story.thumbEmoji ?? '?'}</div>
          )}
          {[0, 1, 2, 3].map((i) => (
            <Lozenge key={i} x={24} y={278 + i * 76} w={442} h={62} state={i === 1 ? 'right' : 'normal'}>
              <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 34, color: T.white}}>
                {LETTERS[i]}
                <span style={{marginLeft: 18}}>{i === 1 ? '✓' : '???'}</span>
              </div>
            </Lozenge>
          ))}
        </div>
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <TvBackground />
      <div style={{position: 'absolute', left: 56, top: 60, width: 700, fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 0.98, letterSpacing: -1, color: T.white, textShadow: '0 5px 0 rgba(0,0,0,0.35)'}}>
        <TvHighlighted text={text} accent={T.gold} />
      </div>
      {puzzle && !story.thumbImage ? (
        <div style={{position: 'absolute', right: 50, top: 200}}>
          <ThumbPuzzle tiles={puzzle} size={puzzle.length > 2 ? 130 : 165} />
        </div>
      ) : story.thumbImage ? (
        <div style={{position: 'absolute', left: 790, top: 70, width: 440, height: 440, borderRadius: 12, padding: 12, boxSizing: 'border-box', background: T.paper, boxShadow: '0 12px 0 rgba(0,0,0,0.25)'}}>
          <Img src={staticFile(story.thumbImage)} style={{width: '100%', height: '100%', objectFit: 'cover', borderRadius: 4}} />
        </div>
      ) : (
        <>
          {[0, 1, 2, 3].map((i) => (
            <Lozenge key={i} x={800} y={80 + i * 118} w={430} h={96} state={i === 2 ? 'right' : 'normal'}>
              <div style={{display: 'flex', alignItems: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 50, color: T.white}}>
                {LETTERS[i]}<span style={{marginLeft: 22, color: T.white}}>{i === 2 ? '✓' : '???'}</span>
              </div>
            </Lozenge>
          ))}
        </>
      )}
      <Lozenge x={56} y={590} w={Math.min(1170, 90 + [...badge].length * 32)} h={92} style={{background: T.red, border: 'none'}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 46, color: T.white, whiteSpace: 'nowrap'}}>{badge}</div>
      </Lozenge>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- Vergleichs-Quiz (Short 1080x1920)
// Frage mit genau 2 Antworten + q.values: zwei Seiten (Foto aus image-credits oder Emoji), Countdown,
// danach wachsen zwei Balken auf die echten Werte (q.valueLabels als Beschriftung), Gewinner wird grün.
const C2 = {COL_W: 470, L_X: 50, R_X: 560, PIC_Y: 500, PIC_H: 330, LBL_Y: 860, LBL_H: 110, BAR_BOTTOM: 1700, BAR_MAX: 560};

const fmtNum = (v: number) => (Math.abs(v) >= 100 ? Math.round(v).toLocaleString('en-US') : (Math.round(v * 10) / 10).toString());

export const CompareScene: React.FC<{q: QuizQuestion; index: number; total: number; story: QuizStory}> = ({q, index, total, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const revealed = t >= q.reveal;
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const since = frame - revealFrame;
  const vals = q.values ?? [1, 1];
  const max = Math.max(...vals, 1e-9);
  const grow = revealed ? spring({frame: since, fps, config: {damping: 18, mass: 0.9}, durationInFrames: Math.round(fps * 1.1)}) : 0;
  const enter = index === 0 ? 1 : interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const plain = q.q.replace(/\*\*/g, '');
  return (
    <AbsoluteFill>
      <TvBackground />
      <Header q={q} index={index} total={total} header={story.header} x={S.LEFT} y={150} w={S.FULL_W} size={34} />
      <div style={{position: 'absolute', inset: 0, opacity: enter}}>
        <Lozenge x={S.LEFT} y={250} w={S.FULL_W} h={210} paper>
          <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: qSizeFor(plain, 76), lineHeight: 1.12, color: T.ink}}>
            <TvHighlighted text={q.q} accent={story.accent ?? T.red} at={q.keywordAt != null ? q.keywordAt - q.start : undefined} />
          </div>
        </Lozenge>
        {q.answers.slice(0, 2).map((a, i) => {
          const x = i === 0 ? C2.L_X : C2.R_X;
          const ok = i === q.correct;
          const st = answerState(revealed, ok, since);
          const img = q.images?.[i];
          const icon = q.icons?.[i];
          const h = Math.max(0.06, vals[i] / max) * C2.BAR_MAX * grow;
          const label = q.valueLabels?.[i] ?? fmtNum(vals[i] * grow);
          return (
            <React.Fragment key={i}>
              <div style={{position: 'absolute', left: x, top: C2.PIC_Y, width: C2.COL_W, height: C2.PIC_H, borderRadius: 14, overflow: 'hidden', border: `12px solid ${st === 'right' || st === 'lock' ? T.gold : T.paper}`, boxSizing: 'border-box', background: T.paper, opacity: st === 'dim' ? 0.5 : 1, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                {img ? <Img src={staticFile(img)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : <div style={{fontSize: 170, lineHeight: 1}}>{icon ?? (i === 0 ? '🅰️' : '🅱️')}</div>}
              </div>
              <Lozenge x={x - 10} y={C2.LBL_Y} w={C2.COL_W + 20} h={C2.LBL_H} state={st} style={{opacity: st === 'dim' ? 0.55 : 1}}>
                <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: a.length > 14 ? 38 : 48, color: st === 'lock' ? T.ink : T.white}}>{a}</div>
              </Lozenge>
              {revealed ? (
                <>
                  <div style={{position: 'absolute', left: x + 85, top: C2.BAR_BOTTOM - h, width: C2.COL_W - 170, height: h, borderRadius: '10px 10px 0 0', background: ok ? T.green : T.silver, border: `2px solid ${ok ? '#7FD3A2' : T.paperDark}`}} />
                  <div style={{position: 'absolute', left: x, width: C2.COL_W, top: C2.BAR_BOTTOM - h - 82, textAlign: 'center', fontFamily: SERIF, fontSize: 64, color: ok ? T.gold : T.paper, opacity: interpolate(since, [2, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>{label}</div>
                </>
              ) : null}
            </React.Fragment>
          );
        })}
        {!revealed ? (
          <div style={{position: 'absolute', left: 540 - 70, top: C2.PIC_Y + C2.PIC_H / 2 - 70, width: 140, height: 140, borderRadius: 70, background: T.paper, border: `2px solid ${T.paperDark}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: SERIF, fontSize: 64, color: T.red, opacity: t >= q.countdownStart ? 0 : 1}}>VS</div>
        ) : null}
        <div style={{position: 'absolute', left: S.LEFT, top: C2.BAR_BOTTOM + 6, width: S.FULL_W, height: 6, background: T.silver, opacity: revealed ? 0.6 : 0}} />
      </div>
      <TvTimer q={q} x={540 - 85} y={1180} size={170} />
      {index === 0 && story.hook ? <Banner text={story.hook} x={S.LEFT + 24} y={C2.PIC_Y - 10} size={42} until={2.8} /> : null}
      {index === 0 && story.teaser ? <Banner text={story.teaser} x={S.LEFT + 24} y={C2.PIC_Y - 10} size={42} from={story.hook ? 2.8 : 0} color={T.silver} /> : null}
      {index === total - 1 && index > 0 && story.finalLabel ? <Banner text={story.finalLabel} x={S.LEFT + 24} y={C2.PIC_Y - 10} size={42} /> : null}
      {story.midLabel && index === Math.floor(total / 2) && index !== total - 1 ? <Banner text={story.midLabel} x={S.LEFT + 24} y={C2.PIC_Y - 10} size={42} from={1.2} color={T.silver} /> : null}
      {index === total - 1 && story.ctaText && revealed ? (
        <Lozenge x={S.LEFT} y={1740} w={S.ANS_W} h={96} state="lock" style={{opacity: interpolate(since, [14, 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
          <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 42, color: '#040A2C'}}>{story.ctaText}</div>
        </Lozenge>
      ) : null}
    </AbsoluteFill>
  );
};
