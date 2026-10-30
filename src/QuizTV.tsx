import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Montserrat';
import type {QuizQuestion, QuizStory} from './Quiz';

// Layout "tvshow" (story.layout = "tvshow"): klassische TV-Quizshow statt Neon.
//   dunkelblaues Studio mit Scheinwerferlicht, keine Glows/Konfetti/Wackeln, kein Maskottchen
//   Frage und Antworten in sechseckigen "Lozenge"-Balken mit Gold/Silber-Rand
//   Auflösung: richtige Antwort kurz orange ("eingeloggt"), dann grün; falsche werden blass
// Enthält: TvScene (Short 1080x1920), TvLongScene + TvLongOutro (1920x1080), TvThumb (1280x720)
const montserrat = loadFont('normal', {weights: ['600', '700', '800', '900'], subsets: ['latin', 'latin-ext']});
const FONT = montserrat.fontFamily;

export const T = {
  bg: '#030616',
  navy: '#0B1446',
  blue: '#1E3A8A',
  gold: '#F5C542',
  goldDark: '#B8862B',
  silver: '#C9D3E6',
  white: '#FFFFFF',
  orange: '#F59E0B',
  green: '#16A34A',
  greenLight: '#22C55E',
  red: '#DC2626',
};
const LETTERS = ['A', 'B', 'C', 'D'];
const levelColor = (l: string) => (/legend/i.test(l) ? '#E879F9' : /very/i.test(l) ? T.red : /hard|schwer/i.test(l) ? '#F87171' : /med|mittel/i.test(l) ? T.orange : T.greenLight);

export const TvHighlighted: React.FC<{text: string; accent?: string}> = ({text, accent = T.gold}) => (
  <>
    {text.split(/(\*\*[^*]+\*\*)/).map((p, i) =>
      p.startsWith('**') ? (
        <span key={i} style={{color: accent}}>
          {p.slice(2, -2)}
        </span>
      ) : (
        <span key={i}>{p}</span>
      ),
    )}
  </>
);

/** Studio-Hintergrund: Scheinwerfer von oben, leichte Lichtkegel, Vignette */
export const TvBackground: React.FC = () => {
  const frame = useCurrentFrame();
  const sway = Math.sin(frame / 90) * 4;
  return (
    <AbsoluteFill style={{background: T.bg, overflow: 'hidden'}}>
      <AbsoluteFill style={{background: `radial-gradient(ellipse 80% 60% at 50% 0%, ${T.blue} 0%, ${T.navy} 45%, ${T.bg} 85%)`}} />
      <AbsoluteFill
        style={{
          opacity: 0.1,
          background: `conic-gradient(from ${180 + sway}deg at 50% -10%, transparent 0deg, #ffffff 4deg, transparent 9deg, transparent 18deg, #ffffff 22deg, transparent 27deg, transparent 333deg, #ffffff 338deg, transparent 342deg, transparent 351deg, #ffffff 355deg, transparent 360deg)`,
        }}
      />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,0,0.6) 100%)'}} />
    </AbsoluteFill>
  );
};

const hex = (w: number, h: number, p: number) => `polygon(${p}px 0, ${w - p}px 0, ${w}px 50%, ${w - p}px 100%, ${p}px 100%, 0 50%)`;

export type LozengeState = 'normal' | 'lock' | 'right' | 'dim';

/** Sechseckiger Balken mit Metallrand (wie in TV-Quizshows) */
export const Lozenge: React.FC<{x: number; y: number; w: number; h: number; state?: LozengeState; children?: React.ReactNode; style?: React.CSSProperties; line?: boolean}> = ({
  x,
  y,
  w,
  h,
  state = 'normal',
  children,
  style,
  line = false,
}) => {
  const b = 4;
  const p = Math.min(h * 0.32, 44);
  const fill =
    state === 'right'
      ? `linear-gradient(180deg, ${T.greenLight} 0%, ${T.green} 55%, #0E6B30 100%)`
      : state === 'lock'
        ? `linear-gradient(180deg, #FCD34D 0%, ${T.orange} 55%, #B45309 100%)`
        : `linear-gradient(180deg, #13246E 0%, #08124A 50%, #040A2C 100%)`;
  const rim = state === 'right' ? '#BBF7D0' : state === 'lock' ? '#FEF3C7' : `linear-gradient(180deg, #F8E7A8 0%, ${T.gold} 35%, ${T.goldDark} 65%, ${T.silver} 100%)`;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, opacity: state === 'dim' ? 0.42 : 1, ...style}}>
      {line ? <div style={{position: 'absolute', left: -400, right: -400, top: h / 2 - 2, height: 4, background: `linear-gradient(90deg, transparent, ${T.silver}88 25%, ${T.silver}88 75%, transparent)`}} /> : null}
      <div style={{position: 'absolute', inset: 0, background: rim, clipPath: hex(w, h, p)}} />
      <div style={{position: 'absolute', left: b, top: b, width: w - 2 * b, height: h - 2 * b, background: fill, clipPath: hex(w - 2 * b, h - 2 * b, p - b * 0.45)}} />
      <div style={{position: 'absolute', left: p, right: p, top: 0, bottom: 0, display: 'flex', alignItems: 'center'}}>{children}</div>
    </div>
  );
};

const answerState = (revealed: boolean, ok: boolean, since: number): LozengeState => {
  if (!revealed) return 'normal';
  if (!ok) return 'dim';
  return since < 9 ? 'lock' : 'right';
};

/** Countdown-Uhr: Goldring, ruhige Zahl */
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
  const color = counting && left <= 1 ? T.red : T.gold;
  const r = size / 2 - 12;
  const circ = 2 * Math.PI * r;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: size, height: size}}>
      <svg width={size} height={size}>
        <circle cx={size / 2} cy={size / 2} r={size / 2 - 2} fill="#040A2C" stroke={T.silver} strokeWidth={3} />
        <circle cx={size / 2} cy={size / 2} r={r} stroke="rgba(255,255,255,0.12)" strokeWidth={10} fill="none" />
        <circle cx={size / 2} cy={size / 2} r={r} stroke={color} strokeWidth={10} fill="none" strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - p)} transform={`rotate(-90 ${size / 2} ${size / 2})`} />
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 800, fontSize: size * 0.42, color: T.white}}>{n}</div>
    </div>
  );
};

const cardFont = (text: string, maxH: number, maxW: number) => {
  const lines = text.split('\n');
  const longest = Math.max(...lines.map((l) => [...l].length));
  const byWidth = Math.floor(maxW / Math.max(3, longest * 0.62));
  return Math.min(byWidth, Math.floor(maxH / (lines.length * 1.25)), 190);
};

/** Bild-/Emoji-Karte mit Goldrahmen, Foto bekommt langsamen Zoom */
const TvCard: React.FC<{q: QuizQuestion; story: QuizStory; x: number; y: number; w: number; h: number}> = ({q, story, x, y, w, h}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const len = Math.max(1, (q.end - q.start) * fps);
  const zoom = interpolate(frame, [0, len], [1.0, 1.06]);
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const a = frame >= revealFrame ? spring({frame: frame - revealFrame, fps, config: {damping: 20}}) : 0;
  const [c1, c2] = story.cardColors ?? [T.blue, '#0B0B2E'];
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 22, padding: 5, background: `linear-gradient(160deg, #F8E7A8, ${T.gold} 40%, ${T.goldDark} 70%, ${T.silver})`, boxShadow: '0 20px 50px rgba(0,0,0,0.55)'}}>
      <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 18, overflow: 'hidden', background: `radial-gradient(circle at 50% 40%, ${c1} 0%, ${c2} 100%)`}}>
        {q.video ? (
          <OffthreadVideo src={staticFile(q.video)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        ) : q.image ? <Img src={staticFile(q.image)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} /> : null}
        {q.cardText && !q.video ? (
          <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', whiteSpace: 'pre-line', fontFamily: FONT, fontWeight: 800, color: T.white, fontSize: cardFont(q.cardText, h * 0.6, w * 0.8), lineHeight: 1.2}}>
            {q.cardText}
          </div>
        ) : null}
        {q.revealImage && a > 0 ? (
          <div style={{position: 'absolute', inset: 0, opacity: a}}>
            <Img src={staticFile(q.revealImage)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          </div>
        ) : null}
        {q.revealImage && q.revealCaption && a > 0 ? (
          <div style={{position: 'absolute', left: 20, bottom: 20, fontFamily: FONT, fontWeight: 800, fontSize: 40, color: T.white, background: 'rgba(4,10,44,0.85)', border: `3px solid ${T.gold}`, borderRadius: 10, padding: '4px 18px', opacity: a}}>{q.revealCaption}</div>
        ) : null}
      </div>
    </div>
  );
};

/** ruhiges Banner (kein Wackeln) */
const Banner: React.FC<{text: string; x: number; y: number; size: number; from?: number; until?: number; color?: string}> = ({text, x, y, size, from = 0, until, color = T.gold}) => {
  const frame0 = useCurrentFrame();
  const {fps} = useVideoConfig();
  const frame = frame0 - Math.round(from * fps);
  if (frame < 0) return null;
  const inA = from === 0 ? 1 : interpolate(frame, [0, 6], [0, 1], {extrapolateRight: 'clamp'});
  const out = until === undefined ? 1 : interpolate(frame0, [fps * (until - 0.3), fps * until], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (out <= 0) return null;
  return (
    <div style={{position: 'absolute', left: x, top: y, opacity: inA * out, background: color, color: '#040A2C', fontFamily: FONT, fontWeight: 900, fontSize: size, letterSpacing: 1, padding: `${size * 0.2}px ${size * 0.55}px`, borderRadius: 8, boxShadow: '0 8px 24px rgba(0,0,0,0.5)', zIndex: 5, whiteSpace: 'nowrap'}}>
      {text}
    </div>
  );
};

const Header: React.FC<{q: QuizQuestion; index: number; total: number; header: string; x: number; y: number; w: number; size: number}> = ({q, index, total, header, x, y, w, size}) => (
  <div style={{position: 'absolute', left: x, top: y, width: w, display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontFamily: FONT, fontWeight: 800, fontSize: size, letterSpacing: size * 0.12, color: T.silver}}>
    <div style={{display: 'flex', alignItems: 'center', gap: size * 0.6}}>
      <span>{header}</span>
      {q.level ? (
        <span style={{fontSize: size * 0.75, letterSpacing: 2, color: T.white, padding: `${size * 0.1}px ${size * 0.4}px`, borderRadius: 6, border: `3px solid ${levelColor(q.level)}`}}>{q.level}</span>
      ) : null}
    </div>
    <span style={{color: T.gold}}>
      {index + 1} / {total}
    </span>
  </div>
);

const AnswerContent: React.FC<{i: number; text: string; state: LozengeState; size: number; tag?: string}> = ({i, text, state, size, tag}) => (
  <div style={{display: 'flex', alignItems: 'center', width: '100%', fontFamily: FONT}}>
    <span style={{fontWeight: 900, fontSize: size, color: state === 'normal' || state === 'dim' ? T.gold : '#040A2C', marginRight: size * 0.45}}>{LETTERS[i]}:</span>
    <span style={{fontWeight: 700, fontSize: text.length > 24 ? size * 0.78 : text.length > 16 ? size * 0.9 : size, color: state === 'lock' ? '#040A2C' : T.white, lineHeight: 1.05, flex: 1}}>{text}</span>
    {tag ? <span style={{fontWeight: 900, fontSize: size * 0.6, color: T.white, background: '#0E6B30', borderRadius: 6, padding: '4px 12px'}}>{tag}</span> : null}
  </div>
);

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
      <Header q={q} index={index} total={total} header={story.header} x={S.LEFT + 10} y={160} w={S.FULL_W - 20} size={36} />
      <div style={{position: 'absolute', inset: 0, opacity: enter}}>
        <TvCard q={q} story={story} x={S.LEFT} y={S.CARD_Y} w={S.FULL_W} h={S.CARD_H} />
        <Lozenge x={S.LEFT - 20} y={S.Q_Y} w={S.FULL_W + 40} h={S.Q_H}>
          <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: qSizeFor(plain, 76), lineHeight: 1.12, color: T.white}}>
            <TvHighlighted text={q.q} accent={story.accent ?? T.gold} />
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
  const rowH = Math.min(78, Math.floor((L.CARD_H - 30) / Math.max(1, rows.length)) - 10);
  return (
    <div style={{position: 'absolute', left: L.LAD_X, top: L.CARD_Y, width: L.LAD_W, height: L.CARD_H, borderRadius: 18, background: 'rgba(4,10,44,0.75)', border: `3px solid ${T.silver}55`, padding: '14px 18px', display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 10}}>
      {rows.map((lv) => {
        const li = levels.indexOf(lv);
        const count = qs.filter((x) => x.level === lv).length;
        const first = qs.findIndex((x) => x.level === lv);
        const active = li === ci;
        const done = li < ci;
        return (
          <div key={lv} style={{height: rowH, borderRadius: rowH / 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 26px', background: active ? `linear-gradient(180deg, #FCD34D, ${T.orange})` : 'transparent', fontFamily: FONT, fontWeight: 800, fontSize: 32, letterSpacing: 2, color: active ? '#040A2C' : done ? T.gold : T.silver, opacity: active || done ? 1 : 0.7}}>
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
    <AbsoluteFill style={{background: `rgba(3,6,22,${0.7 * out})`, opacity: out}}>
      <Lozenge x={360} y={440} w={1200} h={200} state="normal" line style={{opacity: a}}>
        <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 96, color: T.white, letterSpacing: 4}}>
          ROUND {num} · <span style={{color: levelColor(level)}}>{level}</span>
        </div>
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
      <div style={{fontSize: 70, transform: `rotate(${ring}deg)`, transformOrigin: '50% 10%', filter: bellOn ? 'none' : 'grayscale(1) opacity(0.6)'}}>🔔</div>
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
      <div style={{display: 'flex', alignItems: 'center', gap: 36, background: 'rgba(4,10,44,0.95)', border: `4px solid ${T.gold}`, borderRadius: 20, padding: '16px 36px', boxShadow: '0 12px 40px rgba(0,0,0,0.6)'}}>
        <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 38, color: T.white, maxWidth: 640, lineHeight: 1.15}}>{text}</div>
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
      <Header q={q} index={index} total={total} header={story.header} x={L.X + 10} y={42} w={L.CARD_W - 20} size={34} />
      <Ladder story={story} index={index} />
      <div style={{position: 'absolute', inset: 0, opacity: enter}}>
        <TvCard q={q} story={story} x={L.X} y={L.CARD_Y} w={L.CARD_W} h={L.CARD_H} />
        <Lozenge x={L.X - 10} y={L.Q_Y} w={1800} h={L.Q_H} line>
          <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: qSizeFor(plain, 70), lineHeight: 1.12, color: T.white}}>
            <TvHighlighted text={q.q} accent={story.accent ?? T.gold} />
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
        <div style={{position: 'absolute', top: 120, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 84, color: T.white}}>{story.outroText ?? 'How many did you get?'}</div>
        <Lozenge x={610} y={260} w={700} h={200} state="lock" line>
          <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 130, color: '#040A2C'}}>?/{story.questions.length}</div>
        </Lozenge>
        <div style={{position: 'absolute', top: 520, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 54, color: T.white}}>{story.outroSub ?? 'Comment your score 👇'}</div>
        <div style={{position: 'absolute', top: 640, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
          <TvSubscribe scale={1.2} delay={Math.round(fps * 0.6)} />
        </div>
        <div style={{position: 'absolute', top: 820, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 700, fontSize: 40, color: T.gold}}>{story.subscribeText ?? 'New quiz every day – turn on the bell 🔔'}</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- Vorschaubild 1280x720 (Variante A im TV-Look)
export const TvThumb: React.FC<{story: QuizStory & {thumbImage?: string; thumbBadge?: string}; text: string; badge: string}> = ({story, text, badge}) => {
  const plain = text.replace(/\*\*/g, '');
  const size = plain.length > 22 ? 104 : plain.length > 14 ? 120 : 136;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <TvBackground />
      <div style={{position: 'absolute', left: 56, top: 60, width: 700, fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 0.98, color: T.white, textShadow: '0 6px 0 #000, 0 0 30px rgba(0,0,0,0.6)'}}>
        <TvHighlighted text={text} accent={T.gold} />
      </div>
      {story.thumbImage ? (
        <div style={{position: 'absolute', left: 790, top: 70, width: 440, height: 440, borderRadius: 24, padding: 8, background: `linear-gradient(160deg, #F8E7A8, ${T.gold} 40%, ${T.goldDark})`, transform: 'rotate(3deg)'}}>
          <Img src={staticFile(story.thumbImage)} style={{width: '100%', height: '100%', objectFit: 'cover', borderRadius: 18}} />
        </div>
      ) : (
        <>
          {[0, 1, 2, 3].map((i) => (
            <Lozenge key={i} x={800} y={80 + i * 118} w={430} h={96} state={i === 2 ? 'lock' : 'normal'}>
              <div style={{display: 'flex', alignItems: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 50, color: i === 2 ? '#040A2C' : T.gold}}>
                {LETTERS[i]}:<span style={{marginLeft: 22, color: i === 2 ? '#040A2C' : T.white}}>???</span>
              </div>
            </Lozenge>
          ))}
        </>
      )}
      <Lozenge x={40} y={580} w={Math.min(1200, 120 + [...badge].length * 34)} h={100} state="lock">
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 48, color: '#040A2C', whiteSpace: 'nowrap'}}>{badge}</div>
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
      <Header q={q} index={index} total={total} header={story.header} x={S.LEFT + 10} y={160} w={S.FULL_W - 20} size={36} />
      <div style={{position: 'absolute', inset: 0, opacity: enter}}>
        <Lozenge x={S.LEFT - 20} y={250} w={S.FULL_W + 40} h={210}>
          <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: qSizeFor(plain, 76), lineHeight: 1.12, color: T.white}}>
            <TvHighlighted text={q.q} accent={story.accent ?? T.gold} />
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
              <div style={{position: 'absolute', left: x, top: C2.PIC_Y, width: C2.COL_W, height: C2.PIC_H, borderRadius: 22, overflow: 'hidden', border: `4px solid ${st === 'right' || st === 'lock' ? T.gold : T.silver}`, background: `linear-gradient(180deg, ${T.blue}, ${T.navy})`, opacity: st === 'dim' ? 0.5 : 1, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                {img ? <Img src={staticFile(img)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : <div style={{fontSize: 170, lineHeight: 1}}>{icon ?? (i === 0 ? '🅰️' : '🅱️')}</div>}
              </div>
              <Lozenge x={x - 10} y={C2.LBL_Y} w={C2.COL_W + 20} h={C2.LBL_H} state={st} style={{opacity: st === 'dim' ? 0.55 : 1}}>
                <div style={{width: '100%', textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: a.length > 14 ? 38 : 48, color: st === 'normal' || st === 'dim' ? T.white : '#040A2C'}}>{a}</div>
              </Lozenge>
              {revealed ? (
                <>
                  <div style={{position: 'absolute', left: x + 85, top: C2.BAR_BOTTOM - h, width: C2.COL_W - 170, height: h, borderRadius: '18px 18px 4px 4px', background: ok ? `linear-gradient(180deg, ${T.greenLight}, ${T.green})` : `linear-gradient(180deg, ${T.silver}, #7C8AA5)`, border: `3px solid ${ok ? T.gold : T.silver}`}} />
                  <div style={{position: 'absolute', left: x, width: C2.COL_W, top: C2.BAR_BOTTOM - h - 82, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 56, color: ok ? T.gold : T.white, opacity: interpolate(since, [2, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>{label}</div>
                </>
              ) : null}
            </React.Fragment>
          );
        })}
        {!revealed ? (
          <div style={{position: 'absolute', left: 540 - 70, top: C2.PIC_Y + C2.PIC_H / 2 - 70, width: 140, height: 140, borderRadius: 70, background: '#040A2C', border: `4px solid ${T.gold}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 56, color: T.gold, opacity: t >= q.countdownStart ? 0 : 1}}>VS</div>
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
