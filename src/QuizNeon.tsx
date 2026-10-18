import React from 'react';
import {AbsoluteFill, Img, Sequence, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Montserrat';
import type {QuizQuestion, QuizStory} from './Quiz';

// Quiz-Layout "neon" (story.layout = "neon"):
//   dunkler Hintergrund mit Neon-Leuchten und Gitter-Boden
//   oben: Verlaufs-Fortschrittsbalken + "QUESTION 3/8" + Schwierigkeit
//   darunter: Frage groß und leuchtend (Schlüsselwort pink)
//   Mitte: Bild-/Rätselkarte mit Neonrand, Countdown-Ring an der Ecke
//   unten: 4 Antwort-Pillen untereinander, jede in eigener Neonfarbe
const montserrat = loadFont('normal', {weights: ['700', '800', '900'], subsets: ['latin', 'latin-ext']});
const FONT = montserrat.fontFamily;

const N = {
  bg: '#07000F',
  cyan: '#22D3EE',
  purple: '#A855F7',
  pink: '#EC4899',
  pinkLight: '#F0ABFC',
  yellow: '#FDE047',
  green: '#22C55E',
  red: '#EF4444',
  orange: '#F97316',
  white: '#FFFFFF',
};
const ANS = [N.cyan, N.purple, N.pink, N.yellow];
const LETTERS = ['A', 'B', 'C', 'D'];

const LEFT = 60;
const FULL_W = 960;
const ANS_W = 880; // rechts frei für die YouTube-Buttons
const BAR_TOP = 150;
const Q_TOP = 250;
const Q_H = 300;
const CARD_TOP = 575;
const CARD_H = 400;
const TIMER = 150;
const ANS_TOP = 1020;
const ANS_H = 104;
const ANS_GAP = 22;

const levelColor = (l: string) => (/hard|schwer/i.test(l) ? N.red : /med|mittel/i.test(l) ? N.orange : N.green);
const glow = (c: string, r = 30) => `0 0 ${r}px ${c}AA, 0 0 ${r * 2}px ${c}55`;

const cardSize = (text: string) => {
  const lines = text.split('\n');
  const longest = Math.max(...lines.map((l) => [...l].length));
  const byWidth = longest > 22 ? 56 : longest > 16 ? 70 : longest > 10 ? 92 : longest > 8 ? 120 : 160;
  return Math.min(byWidth, Math.floor(340 / (lines.length * 1.12)));
};

const Highlighted: React.FC<{text: string; accent: string}> = ({text, accent}) => (
  <>
    {text.split(/(\*\*[^*]+\*\*)/).map((part, i) =>
      part.startsWith('**') ? (
        <span key={i} style={{color: accent, textShadow: glow(accent, 24)}}>
          {part.slice(2, -2)}
        </span>
      ) : (
        <span key={i}>{part}</span>
      ),
    )}
  </>
);

const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const d = Math.sin(frame / 60) * 40;
  return (
    <AbsoluteFill style={{background: N.bg}}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at ${20 + d / 10}% 12%, rgba(168,85,247,0.55), transparent 45%), radial-gradient(circle at 88% ${55 + d / 20}%, rgba(236,72,153,0.4), transparent 45%), radial-gradient(circle at 25% 95%, rgba(34,211,238,0.35), transparent 45%)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -540,
          top: 1250,
          width: 2160,
          height: 1400,
          opacity: 0.22,
          backgroundImage: 'linear-gradient(rgba(255,255,255,0.5) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.5) 2px, transparent 2px)',
          backgroundSize: '90px 90px',
          backgroundPosition: `0 ${(frame * 2) % 90}px`,
          transform: 'perspective(700px) rotateX(60deg)',
          transformOrigin: 'top center',
        }}
      />
    </AbsoluteFill>
  );
};

const TopBar: React.FC<{q: QuizQuestion; index: number; total: number; header: string}> = ({q, index, total, header}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const from = index / total;
  const to = (index + 1) / total;
  const p = index === 0 ? to : interpolate(spring({frame, fps, config: {damping: 20}}), [0, 1], [from, to]);
  return (
    <>
      <div style={{position: 'absolute', top: BAR_TOP, left: LEFT, width: FULL_W, height: 22, borderRadius: 11, background: 'rgba(255,255,255,0.12)', overflow: 'hidden'}}>
        <div style={{width: `${p * 100}%`, height: '100%', borderRadius: 11, background: `linear-gradient(90deg, ${N.cyan}, ${N.purple}, ${N.pink})`, boxShadow: glow(N.pink, 12)}} />
      </div>
      <div style={{position: 'absolute', top: BAR_TOP + 40, left: LEFT, width: FULL_W, display: 'flex', alignItems: 'center', gap: 16}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 36, letterSpacing: 4, color: N.cyan, textShadow: glow(N.cyan, 16)}}>
          {header} · {index + 1}/{total}
        </div>
        {q.level ? (
          <div
            style={{
              fontFamily: FONT,
              fontWeight: 900,
              fontSize: 26,
              letterSpacing: 2,
              color: N.white,
              padding: '4px 14px',
              borderRadius: 10,
              border: `3px solid ${levelColor(q.level)}`,
              boxShadow: glow(levelColor(q.level), 12),
            }}
          >
            {q.level}
          </div>
        ) : null}
      </div>
    </>
  );
};

const RevealPhoto: React.FC<{src: string; caption?: string; icon: string; since: number}> = ({src, caption, icon, since}) => {
  const {fps} = useVideoConfig();
  const a = spring({frame: since, fps, config: {damping: 18, stiffness: 160}});
  const zoom = interpolate(since, [0, fps * 3], [1.2, 1.06], {extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', inset: 0, opacity: a}}>
      <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />
      {caption ? (
        <div
          style={{
            position: 'absolute',
            left: 24,
            bottom: 24,
            fontFamily: FONT,
            fontWeight: 900,
            fontSize: 44,
            color: N.white,
            background: 'rgba(7,0,15,0.8)',
            border: `3px solid ${N.green}`,
            boxShadow: glow(N.green, 16),
            padding: '6px 20px',
            borderRadius: 14,
            transform: `translateY(${(1 - a) * 30}px)`,
          }}
        >
          {icon ? `${icon} ` : ''}
          {caption}
        </div>
      ) : null}
    </div>
  );
};

const Card: React.FC<{q: QuizQuestion; story: QuizStory}> = ({q, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const len = Math.max(1, (q.end - q.start) * fps);
  const zoom = interpolate(frame, [0, len], [1.03, 1.12]);
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const [c1, c2] = story.cardColors ?? ['#3B0764', '#12001F'];
  return (
    <div
      style={{
        position: 'absolute',
        top: CARD_TOP,
        left: LEFT,
        width: FULL_W,
        height: CARD_H,
        borderRadius: 36,
        overflow: 'hidden',
        border: `5px solid ${N.purple}`,
        boxShadow: glow(N.purple, 40),
        background: `radial-gradient(circle at 50% 35%, ${c1} 0%, ${c2} 100%)`,
      }}
    >
      {q.image ? <Img src={staticFile(q.image)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} /> : null}
      {q.cardText ? (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            padding: '0 190px 0 30px',
            fontFamily: FONT,
            fontWeight: 900,
            fontSize: cardSize(q.cardText),
            lineHeight: 1.12,
            whiteSpace: 'pre-line',
            color: N.white,
            textShadow: glow(N.pink, 20),
            transform: `scale(${0.98 + (zoom - 1.03) * 0.4})`,
          }}
        >
          {q.cardText}
        </div>
      ) : null}
      {q.revealImage && frame >= revealFrame ? <RevealPhoto src={q.revealImage} caption={q.revealCaption} icon={story.revealIcon ?? '📍'} since={frame - revealFrame} /> : null}
    </div>
  );
};

const Timer: React.FC<{q: QuizQuestion}> = ({q}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  if (t >= q.reveal) return null;
  const total = Math.max(0.5, q.reveal - q.countdownStart);
  const p = interpolate(t, [q.countdownStart, q.reveal], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const counting = t >= q.countdownStart;
  const left = q.reveal - t;
  const n = counting ? Math.max(1, Math.ceil(left)) : Math.round(total);
  const color = counting && left <= 1 ? N.red : N.cyan;
  const r = 58;
  const circ = 2 * Math.PI * r;
  const pulse = counting ? 1 + 0.15 * Math.max(0, 1 - ((total - left) % 1) * 5) : 1;
  return (
    <div style={{position: 'absolute', top: CARD_TOP + CARD_H - TIMER - 20, left: LEFT + FULL_W - TIMER - 20, width: TIMER, height: TIMER, transform: `scale(${pulse})`}}>
      <svg width={TIMER} height={TIMER} style={{filter: `drop-shadow(0 0 12px ${color})`}}>
        <circle cx={TIMER / 2} cy={TIMER / 2} r={r + 8} fill="rgba(7,0,15,0.85)" />
        <circle cx={TIMER / 2} cy={TIMER / 2} r={r} stroke="rgba(255,255,255,0.15)" strokeWidth={10} fill="none" />
        <circle
          cx={TIMER / 2}
          cy={TIMER / 2}
          r={r}
          stroke={color}
          strokeWidth={10}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={circ * (1 - p)}
          transform={`rotate(-90 ${TIMER / 2} ${TIMER / 2})`}
        />
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 70, color: N.white, textShadow: glow(color, 14)}}>
        {n}
      </div>
    </div>
  );
};

const rowTop = (i: number) => ANS_TOP + i * (ANS_H + ANS_GAP);

const Answers: React.FC<{q: QuizQuestion; index: number; story: QuizStory}> = ({q, index, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const revealed = t >= q.reveal;
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  return (
    <>
      {q.answers.map((a, i) => {
        const appear = index === 0 ? 1 : spring({frame: frame - 3 - i * 2, fps, config: {damping: 15, stiffness: 220}});
        const isRight = i === q.correct;
        const pop = revealed && isRight ? spring({frame: frame - revealFrame, fps, config: {damping: 8, stiffness: 280}}) : 0;
        const since = frame - revealFrame;
        const shake = revealed && !isRight ? Math.sin(since * 1.6) * Math.max(0, 8 - since) : 0;
        const c = revealed ? (isRight ? N.green : 'rgba(255,255,255,0.25)') : ANS[i % 4];
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: LEFT,
              top: rowTop(i),
              width: ANS_W,
              height: ANS_H,
              borderRadius: ANS_H / 2,
              border: `4px solid ${c}`,
              background: revealed && isRight ? `linear-gradient(90deg, ${N.green}, #15803D)` : 'rgba(7,0,15,0.55)',
              boxShadow: revealed && !isRight ? 'none' : glow(c, revealed ? 34 : 18),
              display: 'flex',
              alignItems: 'center',
              gap: 26,
              padding: '0 26px',
              opacity: appear * (revealed && !isRight ? 0.4 : 1),
              transform: `translateX(${shake + (1 - appear) * -120}px) scale(${1 + 0.05 * pop})`,
            }}
          >
            <div
              style={{
                width: 64,
                height: 64,
                borderRadius: 32,
                flexShrink: 0,
                background: revealed ? (isRight ? N.white : 'rgba(255,255,255,0.2)') : c,
                color: revealed && isRight ? '#15803D' : N.bg,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontFamily: FONT,
                fontWeight: 900,
                fontSize: 34,
              }}
            >
              {revealed ? (isRight ? '✓' : '✕') : LETTERS[i]}
            </div>
            <div style={{fontFamily: FONT, fontWeight: 900, fontSize: a.length > 24 ? 38 : a.length > 16 ? 44 : 52, color: N.white, lineHeight: 1.05}}>{a}</div>
            {revealed && isRight ? (
              <div
                style={{
                  position: 'absolute',
                  right: -18,
                  top: -28,
                  fontFamily: FONT,
                  fontWeight: 900,
                  fontSize: 30,
                  letterSpacing: 1,
                  color: N.bg,
                  background: N.yellow,
                  padding: '6px 16px',
                  borderRadius: 10,
                  transform: `rotate(6deg) scale(${pop})`,
                  boxShadow: glow(N.yellow, 16),
                }}
              >
                {story.correctLabel ?? 'CORRECT!'}
              </div>
            ) : null}
          </div>
        );
      })}
    </>
  );
};

const Sticker: React.FC<{text: string; from?: number; until?: number; color?: string}> = ({text, from = 0, until, color = N.yellow}) => {
  const frame0 = useCurrentFrame();
  const {fps} = useVideoConfig();
  const frame = frame0 - Math.round(from * fps);
  if (frame < 0) return null;
  const slam = from === 0 ? interpolate(frame, [0, 6], [1.15, 1], {extrapolateRight: 'clamp'}) : spring({frame, fps, config: {damping: 9, stiffness: 260}});
  const out = until === undefined ? 1 : interpolate(frame0, [fps * (until - 0.4), fps * until], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (out <= 0) return null;
  return (
    <div
      style={{
        position: 'absolute',
        top: CARD_TOP - 46,
        right: 40,
        transform: `rotate(${6 + Math.sin(frame / 3) * 1.5}deg) scale(${slam * (0.7 + 0.3 * out)})`,
        transformOrigin: 'right center',
        opacity: out,
        background: color,
        color: N.bg,
        fontFamily: FONT,
        fontWeight: 900,
        fontSize: 44,
        padding: '10px 24px',
        borderRadius: 14,
        boxShadow: glow(color, 24),
      }}
    >
      {text}
    </div>
  );
};

const Cta: React.FC<{text: string; since: number}> = ({text, since}) => {
  const {fps} = useVideoConfig();
  const a = spring({frame: since - 6, fps, config: {damping: 10, stiffness: 220}});
  return (
    <div
      style={{
        position: 'absolute',
        top: rowTop(4) + 6,
        left: LEFT,
        width: ANS_W,
        textAlign: 'center',
        fontFamily: FONT,
        fontWeight: 900,
        fontSize: 44,
        color: N.bg,
        background: N.yellow,
        padding: '12px 20px',
        borderRadius: 18,
        transform: `scale(${a})`,
        boxShadow: glow(N.yellow, 24),
      }}
    >
      {text}
    </div>
  );
};

const Confetti: React.FC<{cx: number; cy: number; seed: string}> = ({cx, cy, seed}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  if (t > 1.6) return null;
  const colors = [N.cyan, N.purple, N.pink, N.yellow, N.green, N.white];
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {Array.from({length: 46}, (_, i) => {
        const r = (k: string) => random(`${seed}-${i}-${k}`);
        const angle = -Math.PI / 2 + (r('a') - 0.5) * Math.PI * 1.3;
        const speed = 900 + r('s') * 900;
        const w = 14 + r('w') * 14;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: cx + Math.cos(angle) * speed * t + (r('x') - 0.5) * 200,
              top: cy + Math.sin(angle) * speed * t + 1700 * t * t,
              width: w,
              height: w * 0.5,
              background: colors[i % colors.length],
              boxShadow: `0 0 10px ${colors[i % colors.length]}`,
              transform: `rotate(${r('r') * 360 + t * 720 * (r('d') > 0.5 ? 1 : -1)}deg)`,
              opacity: interpolate(t, [1.1, 1.6], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
              borderRadius: 3,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

export const NeonScene: React.FC<{q: QuizQuestion; index: number; total: number; story: QuizStory}> = ({q, index, total, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const enter = index === 0 ? 1 : spring({frame, fps, config: {damping: 15, stiffness: 180}});
  const plain = q.q.replace(/\*\*/g, '');
  const qSize = plain.length > 70 ? 60 : plain.length > 50 ? 68 : plain.length > 34 ? 78 : 90;
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const flash = frame < revealFrame ? 0 : interpolate(frame, [revealFrame, revealFrame + 6], [0.25, 0], {extrapolateRight: 'clamp'});
  const lastSec = t >= q.reveal - 1 && t < q.reveal ? 0.5 + 0.5 * Math.sin((t - (q.reveal - 1)) * Math.PI * 4) : 0;
  return (
    <AbsoluteFill>
      <Background />
      <TopBar q={q} index={index} total={total} header={story.header} />
      <div style={{position: 'absolute', inset: 0, opacity: enter, transform: `translateY(${(1 - enter) * 50}px)`}}>
        <div
          style={{
            position: 'absolute',
            top: Q_TOP,
            left: LEFT,
            width: FULL_W,
            height: Q_H,
            display: 'flex',
            alignItems: 'center',
            fontFamily: FONT,
            fontWeight: 900,
            fontSize: qSize,
            lineHeight: 1.05,
            letterSpacing: -1,
            color: N.white,
            textShadow: '0 0 30px rgba(236,72,153,0.6)',
          }}
        >
          <span>
            <Highlighted text={q.q} accent={story.accent ?? N.pinkLight} />
          </span>
        </div>
        <Card q={q} story={story} />
      </div>
      <Timer q={q} />
      <Answers q={q} index={index} story={story} />
      {index === 0 && story.hook ? <Sticker text={story.hook} until={2.8} /> : null}
      {index === 0 && story.teaser ? <Sticker text={story.teaser} from={story.hook ? 2.8 : 0} color={N.cyan} /> : null}
      {index === total - 1 && index > 0 && story.finalLabel ? <Sticker text={story.finalLabel} color={N.pink} /> : null}
      {story.midLabel && index === Math.floor(total / 2) && index !== total - 1 ? <Sticker text={story.midLabel} from={1.2} color={N.cyan} /> : null}
      {index === total - 1 && story.ctaText && t >= q.reveal ? <Cta text={story.ctaText} since={frame - revealFrame} /> : null}
      <AbsoluteFill style={{pointerEvents: 'none', boxShadow: `inset 0 0 160px rgba(239,68,68,${0.6 * lastSec})`}} />
      <AbsoluteFill style={{pointerEvents: 'none', background: 'white', opacity: flash}} />
      <Sequence from={revealFrame} layout="none">
        <Confetti cx={LEFT + ANS_W / 2} cy={rowTop(q.correct) + ANS_H / 2} seed={`n${index}`} />
      </Sequence>
    </AbsoluteFill>
  );
};
