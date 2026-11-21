import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Montserrat';
import type {QuizQuestion, QuizStory} from './Quiz';
import {QuizMascot} from './components/Mascot';
import {TvLongScene, TvLongOutro, TvThumb} from './QuizTV';
import {ExamLongScene, ExamLongOutro, ExamThumb} from './QuizExam';
import {PopLongScene} from './QuizPop';

// Langes Quiz-Video im Querformat (1920x1080), Neon-Look.
//   oben: Fortschrittsbalken + "TITEL · 7/20" + Level
//   links: Frage groß + Bild-/Emoji-Karte
//   rechts: Countdown + 4 Antwort-Pillen
//   bei jedem neuen Level ein großes "LEVEL 2 · MEDIUM"-Banner
const montserrat = loadFont('normal', {weights: ['700', '800', '900'], subsets: ['latin', 'latin-ext']});
const FONT = montserrat.fontFamily;

const N = {bg: '#07000F', cyan: '#22D3EE', purple: '#A855F7', pink: '#EC4899', pinkLight: '#F0ABFC', yellow: '#FDE047', green: '#22C55E', red: '#EF4444', orange: '#F97316', white: '#FFFFFF'};
const ANS = [N.cyan, N.purple, N.pink, N.yellow];
const LETTERS = ['A', 'B', 'C', 'D'];
const glow = (c: string, r = 30) => `0 0 ${r}px ${c}AA, 0 0 ${r * 2}px ${c}55`;
const levelColor = (l: string) => (/legend/i.test(l) ? N.pink : /hard|schwer/i.test(l) ? N.red : /med|mittel/i.test(l) ? N.orange : N.green);

const W = 1920;
const PAD = 80;
const COL_L = 900; // Breite linke Spalte
const ANS_X = 1060;
const ANS_W = 780;
const ANS_TOP = 380;
const ANS_H = 116;
const ANS_GAP = 30;

const Highlighted: React.FC<{text: string; accent: string}> = ({text, accent}) => (
  <>
    {text.split(/(\*\*[^*]+\*\*)/).map((p, i) =>
      p.startsWith('**') ? (
        <span key={i} style={{color: accent, textShadow: glow(accent, 24)}}>
          {p.slice(2, -2)}
        </span>
      ) : (
        <span key={i}>{p}</span>
      ),
    )}
  </>
);

const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const d = Math.sin(frame / 70) * 6;
  return (
    <AbsoluteFill style={{background: N.bg}}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at ${15 + d}% 20%, rgba(168,85,247,0.5), transparent 40%), radial-gradient(circle at 85% ${70 + d}%, rgba(236,72,153,0.38), transparent 42%), radial-gradient(circle at 50% 110%, rgba(34,211,238,0.35), transparent 45%)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -960,
          top: 760,
          width: 3840,
          height: 1000,
          opacity: 0.2,
          backgroundImage: 'linear-gradient(rgba(255,255,255,0.5) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,0.5) 2px, transparent 2px)',
          backgroundSize: '100px 100px',
          backgroundPosition: `0 ${(frame * 2) % 100}px`,
          transform: 'perspective(700px) rotateX(62deg)',
          transformOrigin: 'top center',
        }}
      />
    </AbsoluteFill>
  );
};

const cardSize = (text: string) => {
  const lines = text.split('\n');
  const longest = Math.max(...lines.map((l) => [...l].length));
  const byWidth = longest > 22 ? 70 : longest > 14 ? 96 : longest > 8 ? 130 : 170;
  return Math.min(byWidth, Math.floor(380 / (lines.length * 1.12)));
};

const Card: React.FC<{q: QuizQuestion; story: QuizStory}> = ({q, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const len = Math.max(1, (q.end - q.start) * fps);
  const zoom = interpolate(frame, [0, len], [1.02, 1.1]);
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const [c1, c2] = story.cardColors ?? ['#3B0764', '#12001F'];
  const a = frame >= revealFrame ? spring({frame: frame - revealFrame, fps, config: {damping: 18}}) : 0;
  return (
    <div
      style={{
        position: 'absolute',
        left: PAD,
        top: 470,
        width: COL_L,
        height: 500,
        borderRadius: 40,
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
            padding: '0 40px',
            fontFamily: FONT,
            fontWeight: 900,
            fontSize: cardSize(q.cardText),
            lineHeight: 1.12,
            whiteSpace: 'pre-line',
            color: N.white,
            textShadow: glow(N.pink, 20),
            transform: `scale(${zoom})`,
          }}
        >
          {q.cardText}
        </div>
      ) : null}
      {q.revealImage && a > 0 ? (
        <div style={{position: 'absolute', inset: 0, opacity: a}}>
          <Img src={staticFile(q.revealImage)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </div>
      ) : null}
      {a > 0 ? (
        <div
          style={{
            position: 'absolute',
            left: 30,
            right: 30,
            bottom: 30,
            textAlign: 'center',
            fontFamily: FONT,
            fontWeight: 900,
            fontSize: 54,
            color: N.white,
            background: 'rgba(7,0,15,0.85)',
            border: `4px solid ${N.green}`,
            boxShadow: glow(N.green, 18),
            borderRadius: 20,
            padding: '10px 20px',
            transform: `translateY(${(1 - a) * 40}px)`,
            opacity: a,
          }}
        >
          ✓ {q.revealCaption ?? q.answers[q.correct]}
        </div>
      ) : null}
    </div>
  );
};

const TopBar: React.FC<{q: QuizQuestion; index: number; total: number; header: string}> = ({q, index, total, header}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = index === 0 ? 1 / total : interpolate(spring({frame, fps, config: {damping: 20}}), [0, 1], [index / total, (index + 1) / total]);
  return (
    <>
      <div style={{position: 'absolute', top: 50, left: PAD, width: W - 2 * PAD, height: 20, borderRadius: 10, background: 'rgba(255,255,255,0.12)', overflow: 'hidden'}}>
        <div style={{width: `${p * 100}%`, height: '100%', background: `linear-gradient(90deg, ${N.cyan}, ${N.purple}, ${N.pink})`, boxShadow: glow(N.pink, 12)}} />
      </div>
      <div style={{position: 'absolute', top: 92, left: PAD, display: 'flex', alignItems: 'center', gap: 20}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 38, letterSpacing: 4, color: N.cyan, textShadow: glow(N.cyan, 16)}}>
          {header} · {index + 1}/{total}
        </div>
        {q.level ? (
          <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 28, letterSpacing: 3, color: N.white, padding: '4px 16px', borderRadius: 10, border: `3px solid ${levelColor(q.level)}`, boxShadow: glow(levelColor(q.level), 12)}}>
            {q.level}
          </div>
        ) : null}
      </div>
    </>
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
  const n = counting ? Math.max(1, Math.ceil(left)) : Math.ceil(total);
  const color = counting && left <= 1 ? N.red : N.cyan;
  const S = 170;
  const r = 66;
  const circ = 2 * Math.PI * r;
  const pulse = counting ? 1 + 0.12 * Math.max(0, 1 - ((total - left) % 1) * 5) : 1;
  return (
    <div style={{position: 'absolute', top: 170, left: ANS_X + ANS_W / 2 - S / 2, width: S, height: S, transform: `scale(${pulse})`}}>
      <svg width={S} height={S} style={{filter: `drop-shadow(0 0 12px ${color})`}}>
        <circle cx={S / 2} cy={S / 2} r={r + 10} fill="rgba(7,0,15,0.85)" />
        <circle cx={S / 2} cy={S / 2} r={r} stroke="rgba(255,255,255,0.15)" strokeWidth={12} fill="none" />
        <circle cx={S / 2} cy={S / 2} r={r} stroke={color} strokeWidth={12} fill="none" strokeLinecap="round" strokeDasharray={circ} strokeDashoffset={circ * (1 - p)} transform={`rotate(-90 ${S / 2} ${S / 2})`} />
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 80, color: N.white, textShadow: glow(color, 14)}}>{n}</div>
    </div>
  );
};

const Answers: React.FC<{q: QuizQuestion; index: number; story: QuizStory}> = ({q, index, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const revealed = q.start + frame / fps >= q.reveal;
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  return (
    <>
      {q.answers.map((a, i) => {
        const appear = index === 0 ? 1 : spring({frame: frame - 3 - i * 2, fps, config: {damping: 15, stiffness: 220}});
        const ok = i === q.correct;
        const pop = revealed && ok ? spring({frame: frame - revealFrame, fps, config: {damping: 8, stiffness: 280}}) : 0;
        const since = frame - revealFrame;
        const shake = revealed && !ok ? Math.sin(since * 1.6) * Math.max(0, 8 - since) : 0;
        const c = revealed ? (ok ? N.green : 'rgba(255,255,255,0.25)') : ANS[i % 4];
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: ANS_X,
              top: ANS_TOP + i * (ANS_H + ANS_GAP),
              width: ANS_W,
              height: ANS_H,
              borderRadius: ANS_H / 2,
              border: `5px solid ${c}`,
              background: revealed && ok ? `linear-gradient(90deg, ${N.green}, #15803D)` : 'rgba(7,0,15,0.6)',
              boxShadow: revealed && !ok ? 'none' : glow(c, revealed ? 34 : 18),
              display: 'flex',
              alignItems: 'center',
              gap: 30,
              padding: '0 30px',
              opacity: appear * (revealed && !ok ? 0.38 : 1),
              transform: `translateX(${shake + (1 - appear) * 160}px) scale(${1 + 0.05 * pop})`,
            }}
          >
            <div style={{width: 72, height: 72, borderRadius: 36, flexShrink: 0, background: revealed ? (ok ? N.white : 'rgba(255,255,255,0.2)') : c, color: revealed && ok ? '#15803D' : N.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 38}}>
              {revealed ? (ok ? '✓' : '✕') : LETTERS[i]}
            </div>
            <div style={{fontFamily: FONT, fontWeight: 900, fontSize: a.length > 22 ? 40 : a.length > 15 ? 48 : 56, color: N.white, lineHeight: 1.05}}>{a}</div>
            {revealed && ok ? (
              <div style={{position: 'absolute', right: -16, top: -30, fontFamily: FONT, fontWeight: 900, fontSize: 32, color: N.bg, background: N.yellow, padding: '6px 18px', borderRadius: 10, transform: `rotate(5deg) scale(${pop})`, boxShadow: glow(N.yellow, 16)}}>
                {story.correctLabel ?? 'CORRECT!'}
              </div>
            ) : null}
          </div>
        );
      })}
    </>
  );
};

/** großes Level-Banner, wenn ein neues Level beginnt */
const LevelBanner: React.FC<{level: string; num: number}> = ({level, num}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame, fps, config: {damping: 12, stiffness: 200}});
  const out = interpolate(frame, [fps * 1.3, fps * 1.7], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (out <= 0) return null;
  const c = levelColor(level);
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', background: `rgba(7,0,15,${0.55 * out})`, opacity: out}}>
      <div style={{transform: `scale(${0.6 + 0.4 * a}) rotate(-3deg)`, fontFamily: FONT, fontWeight: 900, fontSize: 140, color: N.white, padding: '20px 70px', borderRadius: 40, border: `8px solid ${c}`, boxShadow: glow(c, 60), background: 'rgba(7,0,15,0.85)', textShadow: glow(c, 30)}}>
        LEVEL {num} · {level}
      </div>
    </AbsoluteFill>
  );
};

const Sticker: React.FC<{text: string; until?: number; color?: string}> = ({text, until, color = N.yellow}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const out = until === undefined ? 1 : interpolate(frame, [fps * (until - 0.4), fps * until], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (out <= 0) return null;
  return (
    <div style={{position: 'absolute', top: 432, left: PAD + 24, transform: `rotate(${5 + Math.sin(frame / 3) * 1.5}deg)`, opacity: out, background: color, color: N.bg, fontFamily: FONT, fontWeight: 900, fontSize: 46, padding: '10px 26px', borderRadius: 14, boxShadow: glow(color, 24), zIndex: 5}}>
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
      {Array.from({length: 50}, (_, i) => {
        const r = (k: string) => random(`${seed}-${i}-${k}`);
        const angle = -Math.PI / 2 + (r('a') - 0.5) * Math.PI * 1.4;
        const speed = 900 + r('s') * 900;
        const w = 16 + r('w') * 14;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: cx + Math.cos(angle) * speed * t,
              top: cy + Math.sin(angle) * speed * t + 1600 * t * t,
              width: w,
              height: w * 0.5,
              background: colors[i % colors.length],
              transform: `rotate(${r('r') * 360 + t * 720}deg)`,
              opacity: interpolate(t, [1.1, 1.6], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};


/** Abo-Knopf mit Klick-Animation + Glocke */
const SubscribeButton: React.FC<{scale?: number; delay?: number}> = ({scale = 1, delay = 0}) => {
  const frame = useCurrentFrame() - delay;
  const {fps} = useVideoConfig();
  if (frame < 0) return null;
  const inA = spring({frame, fps, config: {damping: 12, stiffness: 200}});
  const clickAt = fps * 1.0;
  const clicked = frame >= clickAt;
  const press = frame >= clickAt && frame < clickAt + 5 ? 0.92 : 1;
  const bellAt = fps * 1.8;
  const bellOn = frame >= bellAt;
  const ring = bellOn ? Math.sin((frame - bellAt) * 0.9) * Math.max(0, 20 - (frame - bellAt) * 0.6) : 0;
  const cursorX = interpolate(frame, [0, clickAt, bellAt - 4, bellAt], [260, 120, 120, 330], {extrapolateRight: 'clamp'});
  const cursorY = interpolate(frame, [0, clickAt, bellAt - 4, bellAt], [120, 40, 40, 40], {extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'relative', display: 'flex', alignItems: 'center', gap: 28, transform: `scale(${scale * inA})`}}>
      <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 52, letterSpacing: 2, color: N.white, background: clicked ? '#3F3F46' : '#FF0033', padding: '18px 44px', borderRadius: 50, transform: `scale(${press})`, boxShadow: clicked ? 'none' : glow('#FF0033', 30)}}>
        {clicked ? 'SUBSCRIBED ✓' : 'SUBSCRIBE'}
      </div>
      <div style={{fontSize: 84, transform: `rotate(${ring}deg)`, transformOrigin: '50% 10%', filter: bellOn ? 'drop-shadow(0 0 18px #FDE047)' : 'grayscale(1) opacity(0.6)'}}>🔔</div>
      <div style={{position: 'absolute', left: cursorX, top: cursorY, fontSize: 64, opacity: frame < bellAt + fps ? 1 : 0}}>👆</div>
    </div>
  );
};

/** Einblendung in der Mitte des Videos */
const MidSubscribe: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const out = interpolate(frame, [fps * 4.2, fps * 4.7], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (out <= 0) return null;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 24, display: 'flex', justifyContent: 'center', opacity: out}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 40, background: 'rgba(7,0,15,0.92)', border: `4px solid ${N.pink}`, boxShadow: glow(N.pink, 30), borderRadius: 30, padding: '18px 40px'}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 40, color: N.white, maxWidth: 620, lineHeight: 1.1}}>{text}</div>
        <SubscribeButton scale={0.85} />
      </div>
    </div>
  );
};

/** Abspann: Ergebnis kommentieren + abonnieren + Glocke */
const LongOutro: React.FC<{story: QuizStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const a = spring({frame, fps, config: {damping: 12, stiffness: 180}});
  const beat = 1 + 0.03 * Math.sin(frame / 4);
  return (
    <AbsoluteFill>
      <Background />
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 46, opacity: a}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 96, color: N.white, textShadow: glow(N.pink, 30), transform: `scale(${0.8 + 0.2 * a})`}}>{story.outroText ?? 'How many did you get?'}</div>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 150, color: N.bg, background: N.yellow, padding: '6px 60px', borderRadius: 36, transform: `rotate(-3deg) scale(${beat})`, boxShadow: glow(N.yellow, 40)}}>?/{story.questions.length}</div>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 56, color: N.white}}>{story.outroSub ?? 'Comment your score 👇'}</div>
        <SubscribeButton scale={1.25} delay={Math.round(fps * 0.6)} />
        <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 40, color: N.cyan, textShadow: glow(N.cyan, 16)}}>{story.subscribeText ?? 'New quiz every day – turn on the bell 🔔'}</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const LongScene: React.FC<{q: QuizQuestion; index: number; story: QuizStory}> = ({q, index, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const qs = story.questions;
  const total = qs.length;
  const t = q.start + frame / fps;
  const enter = index === 0 ? 1 : spring({frame, fps, config: {damping: 15, stiffness: 180}});
  const plain = q.q.replace(/\*\*/g, '');
  const qSize = plain.length > 70 ? 56 : plain.length > 50 ? 64 : plain.length > 34 ? 74 : 86;
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const flash = frame < revealFrame ? 0 : interpolate(frame, [revealFrame, revealFrame + 6], [0.22, 0], {extrapolateRight: 'clamp'});
  const lastSec = t >= q.reveal - 1 && t < q.reveal ? 0.5 + 0.5 * Math.sin((t - (q.reveal - 1)) * Math.PI * 4) : 0;
  const levels = [...new Set(qs.map((x) => x.level ?? ''))];
  const newLevel = q.level && (index === 0 || qs[index - 1].level !== q.level);
  return (
    <AbsoluteFill>
      <Background />
      <TopBar q={q} index={index} total={total} header={story.header} />
      <div style={{position: 'absolute', inset: 0, opacity: enter, transform: `translateY(${(1 - enter) * 40}px)`}}>
        <div style={{position: 'absolute', top: 160, left: PAD, width: COL_L, height: 290, display: 'flex', alignItems: 'center', fontFamily: FONT, fontWeight: 900, fontSize: qSize, lineHeight: 1.06, letterSpacing: -1, color: N.white, textShadow: '0 0 30px rgba(236,72,153,0.6)'}}>
          <span>
            <Highlighted text={q.q} accent={story.accent ?? N.pinkLight} />
          </span>
        </div>
        <Card q={q} story={story} />
      </div>
      <Timer q={q} />
      <Answers q={q} index={index} story={story} />
      {index === 0 && story.hook ? <Sticker text={story.hook} until={4} /> : null}
      {index === total - 1 && story.finalLabel ? <Sticker text={story.finalLabel} color={N.pink} /> : null}
      {index === total - 1 && story.ctaText && t >= q.reveal ? (
        <div style={{position: 'absolute', left: ANS_X, top: 940, width: ANS_W, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 40, color: N.bg, background: N.yellow, padding: '12px 20px', borderRadius: 18, boxShadow: glow(N.yellow, 24)}}>
          {story.ctaText}
        </div>
      ) : null}
      {story.midCtaIndex === index && t >= q.reveal ? (
        <Sequence from={revealFrame + Math.round(fps * 1.0)} layout="none">
          <MidSubscribe text={story.midCtaText ?? 'Enjoying the quiz? Subscribe & hit the bell!'} />
        </Sequence>
      ) : null}
      {newLevel && index > 0 ? <LevelBanner level={q.level!} num={levels.indexOf(q.level!) + 1} /> : null}
      <AbsoluteFill style={{pointerEvents: 'none', boxShadow: `inset 0 0 200px rgba(239,68,68,${0.55 * lastSec})`}} />
      <AbsoluteFill style={{pointerEvents: 'none', background: 'white', opacity: flash}} />
      <Sequence from={revealFrame} layout="none">
        <Confetti cx={ANS_X + ANS_W / 2} cy={ANS_TOP + q.correct * (ANS_H + ANS_GAP) + ANS_H / 2} seed={`l${index}`} />
      </Sequence>
    </AbsoluteFill>
  );
};

export const QuizLong: React.FC<QuizStory> = (story) => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  return (
    <AbsoluteFill style={{backgroundColor: N.bg, overflow: 'hidden'}}>
      {story.questions.map((q, i) => (
        <Sequence key={i} from={f(q.start)} durationInFrames={Math.max(1, f(q.end) - f(q.start))} name={`Frage ${i + 1}`}>
          {story.layout === 'exam' ? <ExamLongScene q={q} index={i} story={story} /> : story.layout === 'pop' ? <PopLongScene q={q} index={i} story={story} /> : story.layout === 'tvshow' ? <TvLongScene q={q} index={i} story={story} /> : <LongScene q={q} index={i} story={story} />}
        </Sequence>
      ))}
      {(story.durationInSeconds ?? 0) - story.outroStart > 0.5 ? (
        <Sequence from={f(story.outroStart)} name="Abspann">
          {story.layout === 'exam' ? <ExamLongOutro story={story} /> : story.layout === 'tvshow' || story.layout === 'pop' ? <TvLongOutro story={story} /> : <LongOutro story={story} />}
        </Sequence>
      ) : null}
      {story.layout === 'tvshow' || story.layout === 'pop' || story.layout === 'exam' ? null : <QuizMascot story={story} x={1606} y={80} width={236} look={-1} />}
      {story.audio ? <Audio src={staticFile(story.audio)} /> : null}
      {story.music ? <Audio src={staticFile(story.music)} volume={story.musicVolume ?? 0.1} loop /> : null}
      {story.questions.map((q, i) => (
        <React.Fragment key={`s${i}`}>
          {i > 0 ? (
            <Sequence from={Math.max(0, f(q.start) - 3)} durationInFrames={f(0.8)}>
              <Audio src={staticFile('sfx/whoosh.wav')} volume={0.3} />
            </Sequence>
          ) : null}
          {Array.from({length: Math.max(0, Math.ceil(q.reveal - q.countdownStart - 0.3))}, (_, k) => (
            <Sequence key={k} from={f(q.countdownStart + k)} durationInFrames={f(0.3)}>
              <Audio src={staticFile('sfx/tick.wav')} volume={0.55} />
            </Sequence>
          ))}
          <Sequence from={f(q.reveal)} durationInFrames={f(1.2)}>
            <Audio src={staticFile('sfx/ding.wav')} volume={0.5} />
          </Sequence>
        </React.Fragment>
      ))}
    </AbsoluteFill>
  );
};

/** Vorschaubild 1280x720 */
type ThumbProps = QuizStory & {thumbText?: string; thumbEmoji?: string; thumbVariant?: 'A' | 'B' | 'C'; thumbPuzzle?: string[]; thumbTexts?: string[]; thumbBadge?: string};

const EMOJI_FONT = '"Noto Color Emoji", "Apple Color Emoji", "Segoe UI Emoji", sans-serif';

const PuzzleRow: React.FC<{tiles: string[]; size: number; tile: React.CSSProperties; q: React.CSSProperties; op: string}> = ({tiles, size, tile, q, op}) => (
  <div style={{display: 'flex', alignItems: 'center', gap: size * 0.1}}>
    {tiles.map((t, i) => (
      <React.Fragment key={i}>
        {i > 0 && <div style={{fontFamily: FONT, fontWeight: 900, fontSize: size * 0.5, color: op, textShadow: '0 6px 0 #000'}}>+</div>}
        <div style={{width: size, height: size, borderRadius: size * 0.17, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: EMOJI_FONT, fontSize: t.length > 4 ? size * 0.3 : size * 0.7, ...tile}}>{t}</div>
      </React.Fragment>
    ))}
    <div style={{fontFamily: FONT, fontWeight: 900, fontSize: size * 0.5, color: op, textShadow: '0 6px 0 #000'}}>=</div>
    <div style={{width: size, height: size, borderRadius: size * 0.17, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: size * 0.75, ...q}}>?</div>
  </div>
);

export const QuizThumb: React.FC<ThumbProps> = (story) => {
  const v = story.thumbVariant ?? 'A';
  const texts = story.thumbTexts ?? [];
  const text = (v === 'A' ? texts[0] : v === 'B' ? texts[1] : texts[2]) ?? story.thumbText ?? story.title;
  const emoji = story.thumbEmoji ?? '🏆';
  const puzzle = story.thumbPuzzle && story.thumbPuzzle.length ? story.thumbPuzzle : null;
  const badge = story.thumbBadge ?? story.hook ?? `${story.questions.length} QUESTIONS`;
  if (story.layout === 'exam') return <ExamThumb story={story} text={text} badge={badge} variant={v} />;
  if (story.layout === 'tvshow' || story.layout === 'pop') return <TvThumb story={story} text={text} badge={badge} variant={v} />;
  if (v === 'B') {
    return (
      <AbsoluteFill style={{background: '#FFD400', overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: -660, top: -800, width: 2600, height: 2600, background: 'repeating-conic-gradient(from 0deg at 50% 50%, #FFE45C 0 10deg, #FFD400 10deg 20deg)'}} />
        <div style={{position: 'absolute', left: 30, right: 30, top: 30, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 112, lineHeight: 0.95, color: '#111', textShadow: '6px 6px 0 #fff'}}>
          <Highlighted text={text} accent="#E11D48" />
        </div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 290, display: 'flex', justifyContent: 'center'}}>
          {puzzle ? (
            <PuzzleRow tiles={puzzle} size={230} op="#111" tile={{background: '#fff', border: '8px solid #111', boxShadow: '12px 12px 0 #111'}} q={{background: '#E11D48', color: '#fff', border: '8px solid #111', boxShadow: '12px 12px 0 #111'}} />
          ) : (
            <div style={{fontFamily: EMOJI_FONT, fontSize: 260, lineHeight: 1}}>{emoji}</div>
          )}
        </div>
        <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 96, background: '#111', color: '#FFD400', fontFamily: FONT, fontWeight: 900, fontSize: 46, display: 'flex', alignItems: 'center', justifyContent: 'center', whiteSpace: 'nowrap', paddingRight: 230}}>{badge}</div>
      </AbsoluteFill>
    );
  }
  if (v === 'C') {
    return (
      <AbsoluteFill style={{background: '#0A0A0A', overflow: 'hidden'}}>
        <AbsoluteFill style={{background: 'radial-gradient(circle at 75% 45%, rgba(239,68,68,0.8), transparent 55%)'}} />
        <div style={{position: 'absolute', right: 30, top: 40, fontFamily: EMOJI_FONT, fontSize: 420, lineHeight: 1, filter: 'drop-shadow(0 0 60px rgba(239,68,68,0.9))'}}>🤯</div>
        <div style={{position: 'absolute', left: 56, top: 56, width: 860, fontFamily: FONT, fontWeight: 900, fontSize: 132, lineHeight: 0.95, color: N.white, textShadow: '0 8px 0 #000'}}>
          <Highlighted text={text} accent={N.red} />
        </div>
        <div style={{position: 'absolute', left: 56, bottom: 56}}>
          {puzzle ? (
            <PuzzleRow tiles={puzzle} size={170} op="#fff" tile={{background: '#1f1f1f', border: '5px solid #fff'}} q={{background: '#fff', color: '#0A0A0A'}} />
          ) : (
            <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 46, color: N.white, background: N.red, padding: '10px 28px', borderRadius: 16, border: '5px solid #fff', whiteSpace: 'nowrap'}}>{badge}</div>
          )}
        </div>
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{background: N.bg, overflow: 'hidden'}}>
      <AbsoluteFill style={{background: 'radial-gradient(circle at 20% 25%, rgba(168,85,247,0.75), transparent 50%), radial-gradient(circle at 85% 80%, rgba(236,72,153,0.65), transparent 50%)'}} />
      <div style={{position: 'absolute', right: 36, top: 50, fontFamily: EMOJI_FONT, fontSize: puzzle ? 250 : 380, lineHeight: 1, transform: 'rotate(8deg)', filter: 'drop-shadow(0 0 40px rgba(253,224,71,0.6))'}}>{emoji}</div>
      <div style={{position: 'absolute', left: 56, top: puzzle ? 40 : 110, width: puzzle ? 900 : 760, fontFamily: FONT, fontWeight: 900, fontSize: puzzle ? 112 : 124, lineHeight: 0.96, color: N.white, textShadow: '0 7px 0 #000, 0 0 40px rgba(236,72,153,0.9)'}}>
        <Highlighted text={text} accent={N.yellow} />
      </div>
      {puzzle && (
        <div style={{position: 'absolute', left: 56, top: 330}}>
          <PuzzleRow tiles={puzzle} size={200} op="#fff" tile={{background: 'rgba(255,255,255,0.08)', border: `6px solid ${N.cyan}`, boxShadow: glow(N.cyan, 30)}} q={{background: N.yellow, color: N.bg, boxShadow: glow(N.yellow, 30)}} />
        </div>
      )}
      <div style={{position: 'absolute', left: 50, bottom: 40, fontFamily: FONT, fontWeight: 900, fontSize: 46, whiteSpace: 'nowrap', color: N.white, background: N.red, padding: '10px 30px', borderRadius: 18, transform: 'rotate(-4deg)', border: '5px solid #fff', boxShadow: '0 8px 0 #000'}}>
        {badge}
      </div>
    </AbsoluteFill>
  );
};
