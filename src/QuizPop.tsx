// Layout "pop": knalliger Gameshow-Look wie die Thumbnails v2 (Strahlen-Hintergrund, dicke schwarze Konturen,
// harte Schatten, riesiges Rätsel-Motiv, bunte Antwort-Buttons, dicker Countdown-Balken).
//   PopScene      – Short 1080×1920, Mehrfachauswahl
//   PopOutro      – Short-Abspann
//   PopLongScene  – Long 1920×1080
import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, random, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Montserrat';
import type {QuizQuestion, QuizStory} from './Quiz';

const FONT = loadFont('normal', {weights: ['700', '800', '900'], subsets: ['latin', 'latin-ext']}).fontFamily;
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const LETTERS = ['A', 'B', 'C', 'D'];

export const P = {
  ink: '#0B0B14',
  white: '#FFFFFF',
  yellow: '#FFD60A',
  green: '#1FC657',
  red: '#FF3B4E',
  badge: ['#FF3B4E', '#2F80FF', '#FF9F0A', '#B14CFF'],
};

/** Hintergrund-Paletten [innen, außen]; je Video eine (über Themen-Hash), damit der Kanal nicht einfarbig wirkt */
const PALETTES: [string, string][] = [
  ['#3D7BFF', '#1B2FCB'],
  ['#9B4DFF', '#4A14B8'],
  ['#12B8A6', '#0A6E8A'],
  ['#FF5A5F', '#C2185B'],
];
const palette = (story: QuizStory): [string, string] => {
  if (story.cardColors && story.cardColors.length >= 2 && story.layout === 'pop') return [story.cardColors[0], story.cardColors[1]];
  const s = story.header || story.title || '';
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
  return PALETTES[h % PALETTES.length];
};

const useT = (q: QuizQuestion) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const local = frame / fps;
  return {frame, fps, local, t: q.start + local};
};

/** Text mit dicker schwarzer Kontur + hartem Schatten (wie auf den Thumbnails) */
const outline = (size: number): React.CSSProperties => ({
  WebkitTextStroke: `${Math.round(size * 0.2)}px ${P.ink}`,
  paintOrder: 'stroke fill',
  textShadow: `0 ${Math.round(size * 0.09)}px 0 ${P.ink}`,
});

const Rays: React.FC<{story: QuizStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const [a, b] = palette(story);
  const d = Math.hypot(width, height) * 1.25;
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 50% 38%, ${a} 0%, ${b} 78%)`, overflow: 'hidden'}}>
      <div
        style={{
          position: 'absolute',
          left: width / 2 - d / 2,
          top: height * 0.38 - d / 2,
          width: d,
          height: d,
          background: 'repeating-conic-gradient(rgba(255,255,255,0.085) 0deg 9deg, rgba(255,255,255,0) 9deg 18deg)',
          transform: `rotate(${frame * 0.12}deg)`,
        }}
      />
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 40%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.38) 100%)'}} />
    </AbsoluteFill>
  );
};

const Marked: React.FC<{text: string}> = ({text}) => (
  <>
    {text.split('**').map((p, i) =>
      i % 2 === 1 ? (
        <span key={i} style={{color: P.yellow}}>
          {p}
        </span>
      ) : (
        <React.Fragment key={i}>{p}</React.Fragment>
      ),
    )}
  </>
);

const Chip: React.FC<{children: React.ReactNode; bg?: string; color?: string; size: number}> = ({children, bg = P.ink, color = P.white, size}) => (
  <div style={{background: bg, color, fontFamily: FONT, fontWeight: 900, fontSize: size, letterSpacing: 1, padding: `${size * 0.22}px ${size * 0.6}px`, borderRadius: size, border: `${Math.max(4, size * 0.13)}px solid ${P.ink}`, whiteSpace: 'nowrap', lineHeight: 1.1}}>{children}</div>
);

/** Fortschritt als Segmente: erledigt = gelb, aktuell = weiß pulsierend */
const Segments: React.FC<{index: number; total: number; local: number; w: number; h: number}> = ({index, total, local, w, h}) => {
  if (total > 12) {
    return (
      <div style={{width: w, height: h, background: 'rgba(0,0,0,0.35)', borderRadius: h, border: `4px solid ${P.ink}`, overflow: 'hidden', boxSizing: 'border-box'}}>
        <div style={{width: `${((index + 1) / total) * 100}%`, height: '100%', background: P.yellow}} />
      </div>
    );
  }
  const gap = 10;
  const sw = (w - gap * (total - 1)) / total;
  return (
    <div style={{display: 'flex', gap, width: w}}>
      {Array.from({length: total}, (_, i) => (
        <div key={i} style={{width: sw, height: h, borderRadius: h, border: `4px solid ${P.ink}`, boxSizing: 'border-box', background: i < index ? P.yellow : i === index ? P.white : 'rgba(0,0,0,0.35)', opacity: i === index ? 0.75 + 0.25 * Math.sin(local * 6) : 1}} />
      ))}
    </div>
  );
};

const emojiOnly = (s: string) => /^[\p{Extended_Pictographic}\u{1F1E6}-\u{1F1FF}\u{FE0F}\u{200D}\u{20E3}\s+=?·]+$/u.test(s);

/** Weiße Sticker-Karte mit dem Rätsel-Motiv: Foto/Video in voller Farbe oder riesige Emojis/Zahlen */
const Hero: React.FC<{q: QuizQuestion; local: number; revealed: boolean; x: number; y: number; w: number; h: number; enter: number; story: QuizStory}> = ({q, local, revealed, x, y, w, h, enter, story}) => {
  const img = revealed && q.revealImage ? q.revealImage : q.image;
  const zoom = interpolate(local, [0, 10], [1.03, 1.16], clamp);
  const media: React.CSSProperties = {width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`};
  const text = q.cardText ?? '';
  const lines = text.split('\n');
  const longest = Math.max(...lines.map((l) => [...l.replace(/[\uFE0F\u200D]/g, '')].length), 1);
  const isEmoji = emojiOnly(text);
  const size = Math.min((h * 0.72) / lines.length, (w * (isEmoji ? 1.3 : 1.5)) / longest);
  const wobble = Math.sin(local * 2.2) * 1.2;
  const [a] = palette(story);
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, transform: `rotate(${-1.2 + (1 - enter) * -6}deg) scale(${0.86 + 0.14 * enter})`, opacity: Math.min(1, enter * 1.5)}}>
      <div style={{position: 'absolute', inset: 0, background: P.ink, borderRadius: 44, transform: 'translate(0px, 16px)'}} />
      <div style={{position: 'absolute', inset: 0, background: P.white, borderRadius: 44, border: `9px solid ${P.ink}`, boxSizing: 'border-box', overflow: 'hidden'}}>
        {q.video && !(revealed && q.revealImage) ? (
          <OffthreadVideo src={staticFile(q.video)} muted style={media} />
        ) : img ? (
          <Img src={staticFile(img)} style={media} />
        ) : (
          <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', background: `radial-gradient(circle at 50% 45%, #FFFFFF 40%, ${a}33 100%)`}}>
            <div style={{fontFamily: FONT, fontWeight: 900, fontSize: text ? size : h * 0.7, lineHeight: 1.08, color: text ? P.ink : a, whiteSpace: 'pre', textAlign: 'center', transform: `rotate(${wobble}deg) scale(${1 + 0.03 * Math.sin(local * 3)})`}}>{text || '?'}</div>
          </AbsoluteFill>
        )}
        {revealed && q.revealCaption ? <div style={{position: 'absolute', left: 0, bottom: 0, background: P.ink, color: P.white, fontFamily: FONT, fontWeight: 900, fontSize: 38, padding: '8px 22px', borderTopRightRadius: 20}}>{q.revealCaption}</div> : null}
      </div>
    </div>
  );
};

const Sticker: React.FC<{text: string; x: number; y: number; size: number; k: number; bg?: string; color?: string; rot?: number}> = ({text, x, y, size, k, bg = P.yellow, color = P.ink, rot = -4}) => (
  <div style={{position: 'absolute', left: x, top: y, transform: `rotate(${rot}deg) scale(${k})`, transformOrigin: 'left center', zIndex: 6}}>
    <div style={{background: bg, color, fontFamily: FONT, fontWeight: 900, fontSize: size, padding: `${size * 0.2}px ${size * 0.5}px`, borderRadius: size * 0.35, border: `${Math.max(5, size * 0.12)}px solid ${P.ink}`, boxShadow: `0 ${size * 0.16}px 0 ${P.ink}`, whiteSpace: 'nowrap', lineHeight: 1.1}}>{text}</div>
  </div>
);

/** Welcher Hinweis-Sticker gerade gilt (Hook → Teaser → Mitte → Finale → CTA) */
const tagFor = (q: QuizQuestion, index: number, story: QuizStory, local: number): {text: string; from: number} | null => {
  const n = story.questions.length;
  const cd = q.countdownStart - q.start;
  const rv = q.reveal - q.start;
  if (index === 0 && story.hook && local < 2.8) return {text: story.hook, from: -1};
  if (index === 0 && story.teaser && local < cd) return {text: story.teaser, from: story.hook ? 2.8 : -1};
  if (index === n - 1 && index > 0 && story.ctaText && local >= rv + 0.5) return {text: story.ctaText, from: rv + 0.5};
  if (index === n - 1 && index > 0 && story.finalLabel && local < cd) return {text: story.finalLabel, from: 0};
  if (story.midLabel && index === Math.floor(n / 2) && index !== n - 1 && local >= 0.5 && local < cd) return {text: story.midLabel, from: 0.5};
  return null;
};
const popIn = (local: number, from: number) => (from < 0 ? 1 : interpolate(local, [from, from + 0.28], [0, 1], {...clamp, easing: Easing.out(Easing.back(2.2))}));

/** Dicker Countdown-Balken mit Zahl; wird am Ende rot */
const Timer: React.FC<{q: QuizQuestion; t: number; x: number; y: number; w: number; h: number}> = ({q, t, x, y, w, h}) => {
  if (t >= q.reveal) return null;
  const k = interpolate(t, [q.countdownStart, q.reveal], [1, 0], clamp);
  const left = Math.max(0, Math.ceil(q.reveal - Math.max(t, q.countdownStart)));
  const hot = k < 0.34;
  const active = t >= q.countdownStart;
  const pulse = active ? 1 + 0.12 * Math.max(0, Math.sin((q.reveal - t) * Math.PI * 2)) : 1;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h}}>
      <div style={{position: 'absolute', left: 0, right: h * 0.9, top: h * 0.14, bottom: h * 0.14, background: 'rgba(0,0,0,0.4)', border: `6px solid ${P.ink}`, borderRadius: h, overflow: 'hidden', boxSizing: 'border-box'}}>
        <div style={{width: `${k * 100}%`, height: '100%', background: hot ? P.red : P.yellow, borderRadius: h}} />
      </div>
      <div style={{position: 'absolute', right: 0, top: 0, width: h, height: h, borderRadius: h, background: hot ? P.red : P.yellow, border: `6px solid ${P.ink}`, boxSizing: 'border-box', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: h * 0.56, color: hot ? P.white : P.ink, transform: `scale(${pulse})`}}>{left}</div>
    </div>
  );
};

const Confetti: React.FC<{since: number; cx: number; cy: number; seed: string; spread: number}> = ({since, cx, cy, seed, spread}) => {
  if (since < 0 || since > 1.6) return null;
  const colors = [P.yellow, P.red, P.green, '#2F80FF', P.white];
  return (
    <>
      {Array.from({length: 26}, (_, i) => {
        const ang = random(`${seed}a${i}`) * Math.PI * 2;
        const sp = (0.45 + random(`${seed}s${i}`) * 0.75) * spread;
        const x = cx + Math.cos(ang) * sp * Math.min(1, since * 1.6);
        const y = cy + Math.sin(ang) * sp * 0.7 * Math.min(1, since * 1.6) + 520 * since * since;
        const s = 16 + random(`${seed}z${i}`) * 18;
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: s, height: s * 0.6, background: colors[i % colors.length], border: `3px solid ${P.ink}`, borderRadius: 4, transform: `rotate(${since * 500 * (random(`${seed}r${i}`) - 0.5) * 2}deg)`, opacity: interpolate(since, [1.1, 1.6], [1, 0], clamp), zIndex: 7}} />;
      })}
    </>
  );
};

/** Antwort-Button: weiß mit farbigem Buchstaben; richtig = grün + Haken, falsch = ausgegraut */
const Button: React.FC<{q: QuizQuestion; i: number; index: number; x: number; y: number; w: number; h: number; local: number; t: number; label?: string}> = ({q, i, index, x, y, w, h, local, t, label}) => {
  const ok = i === q.correct;
  const since = t - q.reveal;
  const rev = since >= 0;
  const appear = index === 0 ? 1 : interpolate(local, [0.1 + i * 0.07, 0.36 + i * 0.07], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.6))});
  const bump = rev && ok ? 1 + 0.07 * Math.sin(Math.min(1, since / 0.45) * Math.PI) + 0.03 * Math.min(1, since / 0.45) : 1;
  const text = q.answers[i] ?? '';
  const base = h * 0.48;
  const size = text.length > 26 ? base * 0.68 : text.length > 18 ? base * 0.82 : base;
  const bw = Math.max(6, Math.round(h * 0.07));
  const badge = h * 0.66;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, opacity: appear * (rev && !ok ? 0.5 : 1), transform: `translateY(${(1 - appear) * 30}px) scale(${bump})`, zIndex: rev && ok ? 5 : 1}}>
      <div style={{position: 'absolute', inset: 0, background: P.ink, borderRadius: h * 0.34, transform: `translateY(${h * 0.1}px)`}} />
      <div style={{position: 'absolute', inset: 0, background: rev && ok ? P.green : rev ? '#D8DBE6' : P.white, border: `${bw}px solid ${P.ink}`, borderRadius: h * 0.34, boxSizing: 'border-box', display: 'flex', alignItems: 'center', padding: `0 ${h * 0.2}px`, gap: h * 0.24}}>
        <div style={{width: badge, height: badge, flexShrink: 0, borderRadius: badge, background: rev && ok ? P.white : P.badge[i], border: `${Math.max(4, bw - 2)}px solid ${P.ink}`, boxSizing: 'border-box', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: badge * 0.56, color: rev && ok ? P.green : P.white}}>{rev && ok ? '✓' : LETTERS[i]}</div>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: size, color: rev && ok ? P.white : P.ink, whiteSpace: 'nowrap', letterSpacing: -0.5}}>{text}</div>
      </div>
      {rev && ok && label && since > 0.2 ? (
        <div style={{position: 'absolute', right: h * 0.2, top: -h * 0.26, background: P.yellow, color: P.ink, fontFamily: FONT, fontWeight: 900, fontSize: h * 0.3, padding: `${h * 0.04}px ${h * 0.16}px`, borderRadius: h * 0.12, border: `5px solid ${P.ink}`, transform: `rotate(4deg) scale(${interpolate(since, [0.2, 0.42], [0.4, 1], {...clamp, easing: Easing.out(Easing.back(2.4))})})`}}>{label}</div>
      ) : null}
    </div>
  );
};

// ------------------------------------------------------------------ Short 1080×1920
export const PopScene: React.FC<{q: QuizQuestion; index: number; total: number; story: QuizStory}> = ({q, index, total, story}) => {
  const {local, t} = useT(q);
  const since = t - q.reveal;
  const revealed = since >= 0;
  const enter = index === 0 ? 1 : interpolate(local, [0, 0.32], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.4))});
  const plain = q.q.replace(/\*\*/g, '');
  const qSize = plain.length > 70 ? 58 : plain.length > 46 ? 68 : plain.length > 28 ? 80 : 92;
  const n = Math.min(4, q.answers.length);
  const rowH = 104;
  const gap = 20;
  const listY = 1530 - (n * rowH + (n - 1) * gap);
  const tag = tagFor(q, index, story, local);
  const shake = revealed && since < 0.25 ? Math.sin(since * 80) * 5 * (1 - since / 0.25) : 0;
  return (
    <AbsoluteFill>
      <Rays story={story} />
      <AbsoluteFill style={{transform: `translateX(${shake}px)`}}>
        <div style={{position: 'absolute', left: 60, right: 60, top: 168, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <Chip size={38}>{story.header}</Chip>
          <div style={{display: 'flex', gap: 12}}>
            {q.level ? <Chip size={38} bg={P.white} color={P.ink}>{q.level.toUpperCase()}</Chip> : null}
            <Chip size={38} bg={P.yellow} color={P.ink}>
              {index + 1}/{total}
            </Chip>
          </div>
        </div>
        <div style={{position: 'absolute', left: 60, top: 258}}>
          <Segments index={index} total={total} local={local} w={960} h={24} />
        </div>
        <Hero q={q} local={local} revealed={revealed} x={70} y={326} w={940} h={470} enter={enter} story={story} />
        {tag ? <Sticker text={tag.text} x={46} y={292} size={46} k={popIn(local, tag.from)} bg={P.red} color={P.white} /> : null}
        <div style={{position: 'absolute', left: 50, right: 50, top: 826, height: listY - 100 - 826, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: Math.min(1, enter * 1.4), transform: `translateY(${(1 - enter) * 24}px)`}}>
          <div style={{fontFamily: FONT, fontWeight: 900, fontSize: qSize, lineHeight: 1.08, color: P.white, textAlign: 'center', letterSpacing: -1, ...outline(qSize)}}>
            <Marked text={q.q} />
          </div>
        </div>
        <Timer q={q} t={t} x={60} y={listY - 92} w={850} h={64} />
        {revealed && q.fact ? (
          <div style={{position: 'absolute', left: 60, top: listY - 96, width: 850, height: 72, display: 'flex', alignItems: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 34, lineHeight: 1.1, color: P.white, opacity: interpolate(since, [0.4, 0.8], [0, 1], clamp), ...outline(22)}}>{q.fact}</div>
        ) : null}
        {Array.from({length: n}, (_, i) => (
          <Button key={i} q={q} i={i} index={index} x={60} y={listY + i * (rowH + gap)} w={850} h={rowH} local={local} t={t} label={story.correctLabel} />
        ))}
        <Confetti since={since} cx={485} cy={listY + q.correct * (rowH + gap) + rowH / 2} seed={`c${index}`} spread={520} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const PopOutro: React.FC<{story: QuizStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = frame / fps;
  const k = interpolate(s, [0, 0.35], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.6))});
  return (
    <AbsoluteFill>
      <Rays story={story} />
      <AbsoluteFill style={{alignItems: 'center', paddingTop: 380, transform: `scale(${0.9 + 0.1 * k})`, opacity: Math.min(1, k * 1.5)}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 112, lineHeight: 1.04, color: P.white, textAlign: 'center', padding: '0 70px', ...outline(112)}}>{story.outroText}</div>
        <div style={{marginTop: 50, fontFamily: FONT, fontWeight: 900, fontSize: 340, lineHeight: 1, color: P.yellow, transform: `rotate(-4deg) scale(${1 + 0.04 * Math.sin(s * 5)})`, ...outline(240)}}>?/{story.questions.length}</div>
        {story.outroSub ? (
          <div style={{marginTop: 70, background: P.white, border: `8px solid ${P.ink}`, boxShadow: `0 12px 0 ${P.ink}`, borderRadius: 40, padding: '20px 44px', fontFamily: FONT, fontWeight: 900, fontSize: 56, color: P.ink}}>{story.outroSub}</div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ Long 1920×1080
export const PopLongScene: React.FC<{q: QuizQuestion; index: number; story: QuizStory}> = ({q, index, story}) => {
  const {local, t} = useT(q);
  const total = story.questions.length;
  const since = t - q.reveal;
  const revealed = since >= 0;
  const enter = index === 0 ? 1 : interpolate(local, [0, 0.35], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.4))});
  const plain = q.q.replace(/\*\*/g, '');
  const qSize = plain.length > 60 ? 54 : plain.length > 36 ? 62 : 70;
  const n = Math.min(4, q.answers.length);
  const rowH = 100;
  const gap = 22;
  const colX = 1010;
  const colW = 840;
  const listY = 792 - (n * rowH + (n - 1) * gap);
  const tag = tagFor(q, index, story, local);
  const factIn = interpolate(since, [0.5, 0.9], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  return (
    <AbsoluteFill>
      <Rays story={story} />
      <div style={{position: 'absolute', left: 70, right: 70, top: 34, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <Chip size={34}>
          COULD YOU <span style={{color: P.yellow}}>PASS?</span>
        </Chip>
        <div style={{display: 'flex', gap: 14, alignItems: 'center'}}>
          <Chip size={34} bg={P.white} color={P.ink}>{story.header}</Chip>
          {q.level ? <Chip size={34} bg={P.red}>{q.level.toUpperCase()}</Chip> : null}
          <Chip size={34} bg={P.yellow} color={P.ink}>
            {index + 1}/{total}
          </Chip>
        </div>
      </div>
      <div style={{position: 'absolute', left: 70, top: 110}}>
        <Segments index={index} total={total} local={local} w={1780} h={18} />
      </div>
      <Hero q={q} local={local} revealed={revealed} x={80} y={166} w={860} h={626} enter={enter} story={story} />
      {tag ? <Sticker text={tag.text} x={56} y={140} size={40} k={popIn(local, tag.from)} bg={P.red} color={P.white} /> : null}
      <div style={{position: 'absolute', left: colX, width: colW, top: 160, height: listY - 24 - 160, display: 'flex', alignItems: 'center', opacity: Math.min(1, enter * 1.4), transform: `translateX(${(1 - enter) * 30}px)`}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: qSize, lineHeight: 1.08, color: P.white, letterSpacing: -1, ...outline(qSize)}}>
          <Marked text={q.q} />
        </div>
      </div>
      {Array.from({length: n}, (_, i) => (
        <Button key={i} q={q} i={i} index={index} x={colX} y={listY + i * (rowH + gap)} w={colW} h={rowH} local={local} t={t} label={story.correctLabel} />
      ))}
      <Timer q={q} t={t} x={80} y={864} w={1770} h={96} />
      {revealed && q.fact ? (
        <div style={{position: 'absolute', left: 80, top: 850, width: 1770, opacity: factIn, transform: `translateY(${(1 - factIn) * 20}px)`}}>
          <div style={{position: 'absolute', left: 0, right: 0, top: 14, height: 124, background: P.ink, borderRadius: 34}} />
          <div style={{position: 'relative', height: 124, background: P.white, border: `8px solid ${P.ink}`, borderRadius: 34, boxSizing: 'border-box', display: 'flex', alignItems: 'center', gap: 26, padding: '0 30px'}}>
            <div style={{background: P.yellow, border: `6px solid ${P.ink}`, borderRadius: 20, padding: '8px 20px', fontFamily: FONT, fontWeight: 900, fontSize: 32, color: P.ink, whiteSpace: 'nowrap'}}>DID YOU KNOW?</div>
            <div style={{fontFamily: FONT, fontWeight: 800, fontSize: q.fact.length > 70 ? 34 : 40, lineHeight: 1.12, color: P.ink}}>{q.fact}</div>
          </div>
        </div>
      ) : null}
      <Confetti since={since} cx={colX + colW / 2} cy={listY + q.correct * (rowH + gap) + rowH / 2} seed={`l${index}`} spread={560} />
    </AbsoluteFill>
  );
};
