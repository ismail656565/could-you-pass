import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Montserrat';
import {NeonScene} from './QuizNeon';
import {TvScene, CompareScene} from './QuizTV';
import {QuizMascot, type MascotSetting} from './components/Mascot';
import {StickScene, StickHostOverlay, StickOutro, K as STICK} from './QuizStick';

// Quiz-Short, Layout B "Knallig & Comic":
//   gelber Hintergrund mit Punktraster, dicke schwarze Ränder, harte Schatten
//   oben: schwarze Chips (Kategorie, Fortschritt, Schwierigkeit)
//   große weiße Karte: oben Foto bzw. Rätsel-Fläche, unten die Frage (Schlüsselwort gelb markiert)
//   roter Countdown-Kreis an der Kartenkante, roter Hook-Sticker in den ersten ~2,5 s
//   unten: 4 bunte Antwort-Kacheln (2x2), rechts Platz für die YouTube-Buttons
const montserrat = loadFont('normal', {weights: ['700', '800', '900'], subsets: ['latin', 'latin-ext']});
const FONT = montserrat.fontFamily;

export type QuizQuestion = {
  /** Fragetext; Wörter in **Sternchen** werden gelb markiert */
  q: string;
  answers: string[];
  /** Index der richtigen Antwort (0 = A) */
  correct: number;
  /** Bild zur Frage (Datei in public/), darf die Antwort nicht verraten */
  image?: string;
  /** Echter Video-Clip (B-Roll, public/broll/…mp4, von der Action aus Wikimedia Commons geladen) – hat Vorrang vor image/cardText */
  video?: string;
  /** Suchbegriff für den B-Roll-Clip (englisch, darf die Antwort nicht verraten) */
  broll?: string;
  /** Statt Bild: großer Text/Emojis, z. B. "2 · 4 · 8 · 16 · ?" (Zeilenumbruch mit \n) */
  cardText?: string;
  /** Bild, das bei der Auflösung in der Karte erscheint (z. B. Foto der Hauptstadt) */
  revealImage?: string;
  /** Beschriftung zum Auflösungsbild, z. B. "CANBERRA" */
  revealCaption?: string;
  /** kurzer Fakt fürs "DID YOU KNOW?"-Feld nach der Auflösung (tvshow, optional) */
  fact?: string;
  /** Schwierigkeit, z. B. "EASY" / "MEDIUM" / "HARD" (Farbe automatisch) */
  level?: string;
  /** Vergleichs-Quiz (genau 2 Antworten): echte Werte für die Balken, z. B. [17098246, 9984670] */
  values?: number[];
  /** Beschriftung der Balken, z. B. ["17.1M km²", "10.0M km²"] */
  valueLabels?: string[];
  /** Emoji je Seite (wenn kein Foto) */
  icons?: string[];
  /** Foto je Seite (public/, nur aus image-credits.json) */
  images?: string[];
  /** Sekunden (absolut): Moment, in dem die Stimme das **Schlüsselwort** spricht (von der Action berechnet) */
  keywordAt?: number;
  /** Sekunden: Frage erscheint */
  start: number;
  /** Sekunden: Countdown beginnt */
  countdownStart: number;
  /** Sekunden: Auflösung */
  reveal: number;
  /** Sekunden: Ende dieser Frage */
  end: number;
};

export type QuizStory = {
  type: 'quiz';
  title: string;
  /** Kategorie oben links, z. B. "CAPITALS" */
  header: string;
  /** Sticker in den ersten Sekunden, z. B. "IT'S A TRAP 😏" */
  hook?: string;
  audio?: string;
  music?: string;
  musicVolume?: number;
  questions: QuizQuestion[];
  outroStart: number;
  outroText: string;
  outroSub?: string;
  outroImage?: string;
  /** Hintergrundfarbe (Standard: Gelb) */
  bg?: string;
  /** Markerfarbe für hervorgehobene Wörter (Standard: Gelb) */
  accent?: string;
  /** Farbe der Rätsel-Fläche ohne Foto [oben, unten] */
  cardColors?: string[];
  /** Farben der 4 Antwort-Kacheln */
  tileColors?: string[];
  /** Sticker an der richtigen Antwort, z. B. "CORRECT!" */
  correctLabel?: string;
  /** Symbol vor der Bildbeschriftung (Standard 📍, z. B. 🎬 für Filme) */
  revealIcon?: string;
  /** Sticker nach dem Hook (Frage 1, ab ~2,8 s), z. B. "WAIT FOR #8 🤯" */
  teaser?: string;
  /** Sticker auf der letzten Frage, z. B. "FINAL QUESTION 🔥" */
  finalLabel?: string;
  /** Sticker in der Mitte des Quiz, z. B. "SCORE SO FAR? 👇" */
  midLabel?: string;
  /** Banner nach der letzten Auflösung, z. B. "How many did you get? Comment 👇" */
  ctaText?: string;
  /** Gesamtlänge; ist sie gleich outroStart, gibt es keinen Abspann (Video loopt direkt) */
  durationInSeconds?: number;
  /** Layout: "comic" (Standard, gelb), "neon" (dunkel, leuchtend) oder "tvshow" (klassische TV-Quizshow) */
  layout?: 'comic' | 'neon' | 'tvshow' | 'stick';
  /** Foto (public/) für Vorschaubild A im tvshow-Look */
  thumbImage?: string;
  /** "long" = normales Video im Querformat (Komposition QuizLong) */
  format?: 'short' | 'long';
  /** Vorschaubild-Text für lange Videos */
  thumbText?: string;
  thumbEmoji?: string;
  thumbVariant?: 'A' | 'B' | 'C';
  thumbPuzzle?: string[];
  thumbTexts?: string[];
  thumbBadge?: string;
  /** langes Video: bei welcher Frage (Index) die Abo-Einblendung kommt */
  midCtaIndex?: number;
  midCtaText?: string;
  subscribeText?: string;
  /** Maskottchen Q-Bit: "auto" (Kostüm nach Thema, Standard), festes Kostüm oder "off" */
  mascot?: MascotSetting;
  /** (alt, ungenutzt) */
  stripe?: string[];
  questionLabel?: string;
  ofLabel?: string;
};

const C = {
  yellow: '#FFD43B',
  black: '#000000',
  white: '#FFFFFF',
  red: '#FF4757',
  blue: '#3742FA',
  green: '#2ED573',
  orange: '#FFA502',
  grey: '#A3A3A3',
};

const BORDER = 8;
const LEFT = 50;
const CARD_W = 980;
const GRID_W = 890; // rechts frei für die YouTube-Buttons
const LETTERS = ['A', 'B', 'C', 'D'];

const TOP_Y = 150;
const CARD_TOP = 232;
const IMG_H = 430;
const Q_H = 290;
const CARD_H = IMG_H + Q_H + BORDER * 3; // Rahmen oben/unten + Trennlinie
const TIMER = 170;
const GRID_TOP = 1020;
const TILE_H = 220;
const TILE_GAP = 26;

const hard = (n = 10) => `${n}px ${n}px 0 ${C.black}`;
const levelColor = (l: string) => (/hard|schwer/i.test(l) ? C.red : /med|mittel/i.test(l) ? C.orange : C.green);

const Highlighted: React.FC<{text: string; accent: string}> = ({text, accent}) => (
  <>
    {text.split(/(\*\*[^*]+\*\*)/).map((part, i) =>
      part.startsWith('**') ? (
        <span key={i} style={{background: accent, padding: '0 10px', borderRadius: 8, boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone'}}>
          {part.slice(2, -2)}
        </span>
      ) : (
        <span key={i}>{part}</span>
      ),
    )}
  </>
);

/** Rätsel-Text: Größe nach längster Zeile und Zeilenzahl */
const cardSize = (text: string) => {
  const lines = text.split('\n');
  const longest = Math.max(...lines.map((l) => [...l].length));
  const byWidth = longest > 22 ? 56 : longest > 16 ? 70 : longest > 10 ? 92 : longest > 8 ? 120 : 160;
  return Math.min(byWidth, Math.floor(370 / (lines.length * 1.12)));
};

const Background: React.FC<{color: string}> = ({color}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: color}}>
      <AbsoluteFill
        style={{
          opacity: 0.22,
          backgroundImage: `radial-gradient(circle, ${C.black} 3px, transparent 3.5px)`,
          backgroundSize: '44px 44px',
          backgroundPosition: `${frame * 0.5}px ${frame * 0.5}px`,
        }}
      />
    </AbsoluteFill>
  );
};

const chip: React.CSSProperties = {
  fontFamily: FONT,
  fontWeight: 900,
  fontSize: 34,
  letterSpacing: 1.5,
  padding: '8px 20px',
  borderRadius: 14,
  background: C.black,
  color: C.yellow,
};

const TopBar: React.FC<{header: string; level?: string; index: number; total: number}> = ({header, level, index, total}) => (
  <div style={{position: 'absolute', top: TOP_Y, left: LEFT, display: 'flex', gap: 14, alignItems: 'center'}}>
    <div style={chip}>{header}</div>
    <div style={chip}>
      {index + 1}/{total}
    </div>
    {level ? <div style={{...chip, background: levelColor(level), color: C.white, border: `4px solid ${C.black}`, padding: '4px 16px'}}>{level}</div> : null}
    {/* Fortschritt: erledigte Fragen grün, aktuelle weiß, kommende leer */}
    <div style={{display: 'flex', gap: 7, marginLeft: 6}}>
      {Array.from({length: total}, (_, i) => (
        <div
          key={i}
          style={{
            width: i === index ? 34 : 18,
            height: 18,
            borderRadius: 9,
            border: `4px solid ${C.black}`,
            background: i < index ? C.green : i === index ? C.white : 'transparent',
          }}
        />
      ))}
    </div>
  </div>
);

/** Auflösungsbild: blendet mit Zoom über die Bildfläche, Ortsschild unten links */
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
            fontSize: 46,
            color: C.yellow,
            background: C.black,
            padding: '8px 22px',
            borderRadius: 14,
            transform: `translateY(${(1 - a) * 30}px) rotate(-2deg)`,
          }}
        >
          {icon ? `${icon} ` : ''}{caption}
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
  const [c1, c2] = story.cardColors ?? [C.blue, '#1E26B8'];
  const plain = q.q.replace(/\*\*/g, '');
  const qSize = plain.length > 80 ? 48 : plain.length > 60 ? 54 : plain.length > 42 ? 62 : plain.length > 26 ? 72 : 84;
  return (
    <div
      style={{
        position: 'absolute',
        top: CARD_TOP,
        left: LEFT,
        width: CARD_W,
        height: CARD_H,
        background: C.white,
        border: `${BORDER}px solid ${C.black}`,
        borderRadius: 40,
        boxShadow: hard(16),
        overflow: 'hidden',
      }}
    >
      <div style={{position: 'relative', height: IMG_H, overflow: 'hidden', borderBottom: `${BORDER}px solid ${C.black}`, background: `linear-gradient(170deg, ${c1} 0%, ${c2} 100%)`}}>
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
              padding: '0 210px 0 30px', // rechts Platz für den Countdown
              fontFamily: FONT,
              fontWeight: 900,
              fontSize: cardSize(q.cardText),
              lineHeight: 1.12,
              whiteSpace: 'pre-line',
              color: C.white,
              letterSpacing: 1,
              textShadow: `5px 5px 0 ${C.black}`,
              transform: `scale(${0.98 + (zoom - 1.03) * 0.4})`,
            }}
          >
            {q.cardText}
          </div>
        ) : null}
        {q.revealImage && frame >= revealFrame ? <RevealPhoto src={q.revealImage} caption={q.revealCaption} icon={story.revealIcon ?? '📍'} since={frame - revealFrame} /> : null}
      </div>
      <div
        style={{
          height: Q_H,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '0 40px',
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: qSize,
          lineHeight: 1.12,
          letterSpacing: -0.5,
          color: C.black,
        }}
      >
        <span>
          <Highlighted text={q.q} accent={story.accent ?? C.yellow} />
        </span>
      </div>
    </div>
  );
};

/** Roter Countdown-Kreis an der Kartenkante. Ab Frame 0 voll, läuft dann ab. */
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
  const r = 62;
  const circ = 2 * Math.PI * r;
  const pulse = counting ? 1 + 0.16 * Math.max(0, 1 - ((total - left) % 1) * 5) : 1;
  const shake = counting && left <= 1 ? Math.sin(frame * 2.2) * 6 : 0;
  // unten rechts in der Bildfläche, damit er nie die Frage verdeckt
  const top = CARD_TOP + BORDER + IMG_H - TIMER - 18;
  return (
    <div style={{position: 'absolute', top, left: LEFT + CARD_W - TIMER - 24, width: TIMER, height: TIMER, transform: `scale(${pulse}) rotate(${shake}deg)`}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: C.red, border: `${BORDER}px solid ${C.black}`, boxShadow: hard(8)}} />
      <svg width={TIMER} height={TIMER} style={{position: 'absolute', inset: 0}}>
        <circle
          cx={TIMER / 2}
          cy={TIMER / 2}
          r={r}
          stroke={C.white}
          strokeWidth={10}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={circ * (1 - p)}
          transform={`rotate(-90 ${TIMER / 2} ${TIMER / 2})`}
          opacity={0.9}
        />
      </svg>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: FONT,
          fontWeight: 900,
          fontSize: 88,
          color: C.white,
          textShadow: `4px 4px 0 ${C.black}`,
        }}
      >
        {n}
      </div>
    </div>
  );
};

const Confetti: React.FC<{cx: number; cy: number; seed: string}> = ({cx, cy, seed}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  if (t > 1.6) return null;
  const colors = [C.red, C.blue, C.green, C.orange, C.black, C.white];
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {Array.from({length: 48}, (_, i) => {
        const r = (k: string) => random(`${seed}-${i}-${k}`);
        const angle = -Math.PI / 2 + (r('a') - 0.5) * Math.PI * 1.3;
        const speed = 900 + r('s') * 900;
        const x = cx + Math.cos(angle) * speed * t + (r('x') - 0.5) * 200;
        const y = cy + Math.sin(angle) * speed * t + 1700 * t * t;
        const rot = r('r') * 360 + t * 720 * (r('d') > 0.5 ? 1 : -1);
        const w = 16 + r('w') * 14;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: w,
              height: w * 0.5,
              background: colors[i % colors.length],
              border: `2px solid ${C.black}`,
              transform: `rotate(${rot}deg)`,
              opacity: interpolate(t, [1.1, 1.6], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

const tilePos = (i: number) => {
  const w = (GRID_W - TILE_GAP) / 2;
  return {left: LEFT + (i % 2) * (w + TILE_GAP), top: GRID_TOP + Math.floor(i / 2) * (TILE_H + TILE_GAP), w};
};

const Answers: React.FC<{q: QuizQuestion; index: number; story: QuizStory}> = ({q, index, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const revealed = t >= q.reveal;
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  const colors = story.tileColors ?? [C.red, C.blue, C.green, C.orange];
  const label = story.correctLabel ?? 'CORRECT!';
  return (
    <>
      {q.answers.map((a, i) => {
        const {left, top, w} = tilePos(i);
        // Frage 1: steht sofort, danach ploppen die Kacheln nacheinander auf
        const appear = index === 0 ? 1 : spring({frame: frame - 3 - i * 2, fps, config: {damping: 12, stiffness: 240}});
        const isRight = i === q.correct;
        const pop = revealed && isRight ? spring({frame: frame - revealFrame, fps, config: {damping: 8, stiffness: 280}}) : 0;
        const since = frame - revealFrame;
        const shake = revealed && !isRight ? Math.sin(since * 1.6) * Math.max(0, 9 - since) : 0;
        const bg = revealed ? (isRight ? C.green : C.grey) : colors[i % colors.length];
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left,
              top,
              width: w,
              height: TILE_H,
              borderRadius: 30,
              background: bg,
              border: `${BORDER}px solid ${C.black}`,
              boxShadow: hard(revealed && isRight ? 14 : 10),
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '0 20px',
              opacity: appear * (revealed && !isRight ? 0.6 : 1),
              transform: `translateX(${shake}px) scale(${(0.8 + 0.2 * appear) * (1 + 0.08 * pop)}) rotate(${revealed && isRight ? -2 * pop : 0}deg)`,
            }}
          >
            <div
              style={{
                position: 'absolute',
                left: 16,
                top: 14,
                width: 50,
                height: 50,
                borderRadius: 25,
                background: C.black,
                color: revealed ? (isRight ? C.green : C.white) : C.white,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontFamily: FONT,
                fontWeight: 900,
                fontSize: 28,
              }}
            >
              {revealed ? (isRight ? '✓' : '✕') : LETTERS[i]}
            </div>
            <div
              style={{
                fontFamily: FONT,
                fontWeight: 900,
                fontSize: a.length > 20 ? 38 : a.length > 12 ? 46 : 58,
                lineHeight: 1.05,
                textAlign: 'center',
                color: C.white,
                textShadow: `3px 3px 0 ${C.black}`,
                WebkitTextStroke: `1.5px ${C.black}`,
              }}
            >
              {a}
            </div>
            {revealed && isRight ? (
              <div
                style={{
                  position: 'absolute',
                  right: -18,
                  top: -30,
                  fontFamily: FONT,
                  fontWeight: 900,
                  fontSize: 32,
                  letterSpacing: 1,
                  color: C.yellow,
                  background: C.black,
                  padding: '6px 16px',
                  borderRadius: 10,
                  transform: `rotate(8deg) scale(${pop})`,
                }}
              >
                {label}
              </div>
            ) : null}
          </div>
        );
      })}
    </>
  );
};

/** Sticker oben rechts. Ohne `until`: bleibt stehen. Mit `until` (Sek.): verschwindet danach. `from`: erscheint ab (Sek.) */
const HookSticker: React.FC<{text: string; from?: number; until?: number; color?: string}> = ({text, from = 0, until, color = C.red}) => {
  const frame0 = useCurrentFrame();
  const {fps} = useVideoConfig();
  const frame = frame0 - Math.round(from * fps);
  if (frame < 0) return null;
  const slam = from === 0 ? interpolate(frame, [0, 6], [1.15, 1], {extrapolateRight: 'clamp'}) : spring({frame, fps, config: {damping: 9, stiffness: 260}});
  const out = until === undefined ? 1 : interpolate(frame0, [fps * (until - 0.4), fps * until], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const wiggle = Math.sin(frame / 3) * 1.5;
  if (out <= 0) return null;
  return (
    <div
      style={{
        position: 'absolute',
        top: CARD_TOP - 50,
        right: 30,
        transform: `rotate(${7 + wiggle}deg) scale(${slam * (0.7 + 0.3 * out)})`,
        transformOrigin: 'right center',
        opacity: out,
        background: color,
        color: C.white,
        fontFamily: FONT,
        fontWeight: 900,
        fontSize: 46,
        padding: '12px 24px',
        borderRadius: 16,
        border: `6px solid ${C.black}`,
        boxShadow: hard(8),
        textShadow: `3px 3px 0 ${C.black}`,
      }}
    >
      {text}
    </div>
  );
};

/** Banner unter den Antworten nach der letzten Auflösung (statt Abspann) */
const Cta: React.FC<{text: string; since: number}> = ({text, since}) => {
  const {fps} = useVideoConfig();
  const a = spring({frame: since - 6, fps, config: {damping: 10, stiffness: 220}});
  return (
    <div
      style={{
        position: 'absolute',
        top: GRID_TOP + 2 * TILE_H + TILE_GAP + 34,
        left: LEFT,
        width: GRID_W,
        textAlign: 'center',
        fontFamily: FONT,
        fontWeight: 900,
        fontSize: 46,
        color: C.yellow,
        background: C.black,
        padding: '14px 20px',
        borderRadius: 18,
        transform: `scale(${a}) rotate(-1.5deg)`,
        boxShadow: `8px 8px 0 ${C.red}`,
      }}
    >
      {text}
    </div>
  );
};

const QuestionScene: React.FC<{q: QuizQuestion; index: number; total: number; story: QuizStory}> = ({q, index, total, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const enter = index === 0 ? 1 : spring({frame, fps, config: {damping: 13, stiffness: 190}});
  const revealFrame = Math.round((q.reveal - q.start) * fps);
  // Blitz NUR ab der Auflösung
  const flash = frame < revealFrame ? 0 : interpolate(frame, [revealFrame, revealFrame + 6], [0.35, 0], {extrapolateRight: 'clamp'});
  const lastSec = t >= q.reveal - 1 && t < q.reveal ? 0.5 + 0.5 * Math.sin((t - (q.reveal - 1)) * Math.PI * 4) : 0;
  const tp = tilePos(q.correct);
  return (
    <AbsoluteFill>
      <Background color={story.bg ?? C.yellow} />
      <TopBar header={story.header} level={q.level} index={index} total={total} />
      <div style={{position: 'absolute', inset: 0, opacity: enter, transform: `translateY(${(1 - enter) * 60}px) rotate(${(1 - enter) * -2}deg)`}}>
        <Card q={q} story={story} />
      </div>
      <Timer q={q} />
      <Answers q={q} index={index} story={story} />
      {index === 0 && story.hook ? <HookSticker text={story.hook} until={2.8} /> : null}
      {index === 0 && story.teaser ? <HookSticker text={story.teaser} from={story.hook ? 2.8 : 0} color={C.blue} /> : null}
      {index === total - 1 && index > 0 && story.finalLabel ? <HookSticker text={story.finalLabel} /> : null}
      {index === total - 1 && story.ctaText && t >= q.reveal ? <Cta text={story.ctaText} since={frame - revealFrame} /> : null}
      <AbsoluteFill style={{pointerEvents: 'none', boxShadow: `inset 0 0 160px rgba(255,71,87,${0.6 * lastSec})`}} />
      <AbsoluteFill style={{pointerEvents: 'none', background: 'white', opacity: flash}} />
      <Sequence from={revealFrame} layout="none">
        <Confetti cx={tp.left + tp.w / 2} cy={tp.top + TILE_H / 2} seed={`c${index}`} />
      </Sequence>
    </AbsoluteFill>
  );
};

const Outro: React.FC<{story: QuizStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 12, stiffness: 200}});
  const beat = 1 + 0.04 * Math.sin(frame / 4);
  const total = story.questions.length;
  return (
    <AbsoluteFill>
      <Background color={story.bg ?? C.yellow} />
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
        <div style={{width: 960, marginLeft: -60, textAlign: 'center', opacity: s, transform: `scale(${interpolate(s, [0, 1], [0.8, 1])})`}}>
          <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 92, lineHeight: 1.05, color: C.black}}>{story.outroText}</div>
          <div
            style={{
              display: 'inline-block',
              marginTop: 50,
              fontFamily: FONT,
              fontWeight: 900,
              fontSize: 190,
              color: C.yellow,
              background: C.black,
              padding: '10px 60px',
              borderRadius: 40,
              transform: `scale(${beat}) rotate(-3deg)`,
              boxShadow: `16px 16px 0 ${C.red}`,
            }}
          >
            ?/{total}
          </div>
          {story.outroSub ? <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 54, marginTop: 60, color: C.black}}>{story.outroSub}</div> : null}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Sfx: React.FC<{questions: QuizQuestion[]; outroStart: number}> = ({questions, outroStart}) => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  return (
    <>
      {questions.map((q, i) => {
        const ticks: number[] = [];
        for (let t = q.countdownStart; t < q.reveal - 0.3; t += 1) ticks.push(t);
        return (
          <React.Fragment key={i}>
            {i > 0 ? (
              <Sequence from={Math.max(0, f(q.start) - 3)} durationInFrames={f(0.8)} name="SFX Wechsel">
                <Audio src={staticFile('sfx/whoosh.wav')} volume={0.3} />
              </Sequence>
            ) : null}
            {ticks.map((t, k) => (
              <Sequence key={k} from={f(t)} durationInFrames={f(0.3)} name="SFX Tick">
                <Audio src={staticFile('sfx/tick.wav')} volume={0.55} />
              </Sequence>
            ))}
            <Sequence from={f(q.reveal)} durationInFrames={f(1.2)} name="SFX Richtig">
              <Audio src={staticFile('sfx/ding.wav')} volume={0.5} />
            </Sequence>
          </React.Fragment>
        );
      })}
      {outroStart >= 0 ? (
        <Sequence from={Math.max(0, f(outroStart) - 3)} durationInFrames={f(0.8)} name="SFX Outro">
          <Audio src={staticFile('sfx/whoosh.wav')} volume={0.3} />
        </Sequence>
      ) : null}
    </>
  );
};

export const Quiz: React.FC<QuizStory> = (story) => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const total = story.questions.length;
  const hasOutro = (story.durationInSeconds ?? Infinity) - story.outroStart > 0.3;
  return (
    <AbsoluteFill style={{backgroundColor: story.layout === 'stick' ? STICK.paper : story.layout === 'tvshow' ? '#14213D' : story.layout === 'neon' ? '#07000F' : story.bg ?? C.yellow, overflow: 'hidden'}}>
      {story.questions.map((q, i) => (
        <Sequence key={i} from={f(q.start)} durationInFrames={Math.max(1, f(q.end) - f(q.start))} name={`Frage ${i + 1}`}>
          {q.values && q.answers.length === 2 ? <CompareScene q={q} index={i} total={total} story={story} /> : story.layout === 'stick' ? <StickScene q={q} index={i} total={total} story={story} /> : story.layout === 'tvshow' ? <TvScene q={q} index={i} total={total} story={story} /> : story.layout === 'neon' ? <NeonScene q={q} index={i} total={total} story={story} /> : <QuestionScene q={q} index={i} total={total} story={story} />}
        </Sequence>
      ))}
      {hasOutro ? (
        <Sequence from={f(story.outroStart)} name="Outro">
          {story.layout === 'stick' ? <StickOutro story={story} /> : <Outro story={story} />}
        </Sequence>
      ) : null}
      {story.layout === 'stick' ? <StickHostOverlay story={story} x={30} y={1318} width={400} /> : null}
      {story.layout === 'neon' ? <QuizMascot story={story} x={44} y={748} width={228} look={1} /> : null}
      {story.audio ? <Audio src={staticFile(story.audio)} /> : null}
      {story.music ? <Audio src={staticFile(story.music)} volume={story.musicVolume ?? 0.1} loop /> : null}
      <Sfx questions={story.questions} outroStart={hasOutro ? story.outroStart : -1} />
    </AbsoluteFill>
  );
};
