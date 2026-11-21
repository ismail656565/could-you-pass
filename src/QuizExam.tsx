// Long-Layout "exam" (seit 22.11.2026, Besitzer: tvshow-Long „sieht sehr AI und simpel aus – mach was Kreatives“).
// Idee: der Kanalname wörtlich – „Could You PASS?“ ist eine PRÜFUNG. Draufsicht auf einen Holztisch,
// darauf ein Prüfungsbogen (liniertes Papier, roter Rand, Lochung), Frage in Schreibmaschinenschrift,
// Antworten als Ankreuz-Kreise wie auf einem Multiple-Choice-Bogen. Bei der Auflösung kommt ein echter
// Bleistift und malt den Kreis aus, danach setzt der Rotstift Haken + Kringel. Rechts auf dem Tisch:
// Stoppuhr (Countdown), gelber Klebezettel mit den Runden, Kaffeerand. Rundenwechsel = roter Stempel.
// Alles 2D aus Papier/Holz/Tinte – keine Verläufe-Glow, keine Emoji-Deko (cardText-Emoji wird als Aufkleber gezeigt).
// Texturen: public/exam/desk.jpg (scripts/make_exam_wood.py), paper.jpg + grunge.png (scripts/make_exam_textures.py).
import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont as loadType} from '@remotion/google-fonts/SpecialElite';
import {loadFont as loadHand} from '@remotion/google-fonts/Kalam';
import {loadFont as loadSerif} from '@remotion/google-fonts/Fraunces';
import {loadFont as loadMarker} from '@remotion/google-fonts/PermanentMarker';
import type {QuizQuestion, QuizStory} from './Quiz';

const TYPE = loadType('normal', {weights: ['400'], subsets: ['latin']}).fontFamily;
const HAND = loadHand('normal', {weights: ['400', '700'], subsets: ['latin']}).fontFamily;
const SERIF = loadSerif('normal', {weights: ['900'], subsets: ['latin']}).fontFamily;
const MARKER = loadMarker('normal', {weights: ['400'], subsets: ['latin']}).fontFamily;

const K = {
  ink: '#1F2533',
  pencil: '#3A3A3E',
  red: '#C62828',
  redPen: '#D32F2F',
  rule: 'rgba(70,120,200,0.22)',
  margin: 'rgba(214,64,64,0.45)',
  note: '#FFE66E',
  notePink: '#FFB3C7',
  noteBlue: '#B8E2FF',
  grey: '#7A7466',
};
const EMOJI_FONT = '"Noto Color Emoji", "Apple Color Emoji", sans-serif';
const LETTERS = ['A', 'B', 'C', 'D'];
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
export const noEmoji = (s?: string) => (s ?? '').replace(/[\p{Extended_Pictographic}\u{FE0F}\u{200D}\u{1F3FB}-\u{1F3FF}]/gu, '').replace(/\s+/g, ' ').trim();

// Bogen-Geometrie (Bildschirm): Papier links, Tisch-Requisiten rechts
const P = {x: 96, y: 34, w: 1300, h: 1010, rot: -0.6};
const ANS_Y = 440;
const ROW = 124;
const BUB = {x: 140, w: 88, h: 62};

const Desk: React.FC = () => <Img src={staticFile('exam/desk.jpg')} style={{position: 'absolute', inset: 0, width: 1920, height: 1080}} />;

/** leerer Prüfungsbogen: Papier, Linien, roter Rand, Lochung, Kopf */
const Sheet: React.FC<{story: QuizStory; children?: React.ReactNode; style?: React.CSSProperties; blank?: boolean}> = ({story, children, style, blank}) => (
  <div style={{position: 'absolute', left: P.x, top: P.y, width: P.w, height: P.h, transform: `rotate(${P.rot}deg)`, boxShadow: '0 18px 40px rgba(30,15,5,0.45), 0 2px 4px rgba(0,0,0,0.25)', ...style}}>
    <Img src={staticFile('exam/paper.jpg')} style={{position: 'absolute', inset: 0, width: P.w, height: P.h}} />
    <svg width={P.w} height={P.h} style={{position: 'absolute', inset: 0}}>
      {Array.from({length: 14}).map((_, i) => (
        <line key={i} x1={0} x2={P.w} y1={236 + i * 58} y2={236 + i * 58} stroke={K.rule} strokeWidth={2} />
      ))}
      <line x1={100} x2={100} y1={0} y2={P.h} stroke={K.margin} strokeWidth={2.5} />
      {[180, 500, 820].map((y) => (
        <g key={y}>
          <circle cx={46} cy={y} r={19} fill="#6B4528" />
          <circle cx={46} cy={y} r={19} fill="none" stroke="rgba(0,0,0,0.25)" strokeWidth={3} />
        </g>
      ))}
      <line x1={120} x2={P.w - 50} y1={152} y2={152} stroke={K.ink} strokeWidth={3} />
      <line x1={120} x2={P.w - 50} y1={160} y2={160} stroke={K.ink} strokeWidth={1} />
    </svg>
    {blank ? null : (
      <>
        <div style={{position: 'absolute', left: 124, top: 30, fontFamily: SERIF, fontSize: 56, color: K.ink, letterSpacing: -0.5}}>
          COULD YOU <span style={{color: K.red}}>PASS?</span>
        </div>
        <div style={{position: 'absolute', left: 128, top: 104, fontFamily: TYPE, fontSize: 25, letterSpacing: 3, color: K.grey}}>{noEmoji(story.header || story.title).toUpperCase()} · FINAL EXAM</div>
        <div style={{position: 'absolute', right: 56, top: 34, fontFamily: HAND, fontSize: 34, color: K.ink, textAlign: 'left', lineHeight: 1.45}}>
          <div>Name: <span style={{display: 'inline-block', width: 230, borderBottom: `2px solid ${K.ink}`}} /></div>
          <div>Score: <span style={{display: 'inline-block', width: 110, borderBottom: `2px solid ${K.ink}`}} /> / {story.questions.length}</div>
        </div>
      </>
    )}
    {children}
  </div>
);

/** Schlüsselwort mit gelbem Textmarker, der beim gesprochenen Wort drübergezogen wird */
const Marked: React.FC<{text: string; at?: number}> = ({text, at}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const sweep = at == null ? 1 : interpolate(frame - Math.round(at * fps), [0, 8], [0, 1], clamp);
  return (
    <>
      {text.split(/(\*\*[^*]+\*\*)/).map((p, i) =>
        p.startsWith('**') ? (
          <span key={i} style={{backgroundImage: 'linear-gradient(100deg, rgba(255,226,0,0) 0%, rgba(255,226,0,0.62) 3%, rgba(255,214,0,0.55) 96%, rgba(255,226,0,0) 100%)', backgroundRepeat: 'no-repeat', backgroundPosition: '0 70%', backgroundSize: `${sweep * 100}% 0.72em`, padding: '0 4px', margin: '0 -4px'}}>
            {p.slice(2, -2)}
          </span>
        ) : (
          <span key={i}>{p}</span>
        ),
      )}
    </>
  );
};

/** Handgezogene Linie (leicht zittrig) als SVG-Pfad mit Zeichen-Animation */
const Drawn: React.FC<{d: string; p: number; color?: string; width?: number; len?: number}> = ({d, p, color = K.redPen, width = 9, len = 1400}) => (
  <path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - p)} />
);

/** Bleistift (Spitze im Ursprung, Körper nach rechts) */
const Pencil: React.FC<{x: number; y: number; angle: number}> = ({x, y, angle}) => (
  <div style={{position: 'absolute', left: x, top: y - 18, width: 400, height: 36, transformOrigin: '0px 18px', transform: `rotate(${angle}deg)`, filter: 'drop-shadow(6px 10px 6px rgba(30,15,5,0.4))'}}>
    <svg width={400} height={36} viewBox="0 0 400 36">
      <path d="M0 18 L52 2 L52 34 Z" fill="#E9C893" />
      <path d="M0 18 L16 13 L16 23 Z" fill="#2E2E33" />
      <rect x={52} y={2} width={270} height={32} fill="#F2B705" />
      <rect x={52} y={2} width={270} height={10} fill="#F7CB3A" />
      <rect x={52} y={24} width={270} height={10} fill="#D99A00" />
      <rect x={322} y={1} width={30} height={34} fill="#B9BCC2" />
      <line x1={330} x2={330} y1={1} y2={35} stroke="#8D9096" strokeWidth={2} />
      <line x1={344} x2={344} y1={1} y2={35} stroke="#8D9096" strokeWidth={2} />
      <rect x={352} y={2} width={42} height={32} rx={7} fill="#EF8A9C" />
      <text x={190} y={23} fontFamily={TYPE} fontSize={13} fill="#5A4300" textAnchor="middle">HB · COULD YOU PASS?</text>
    </svg>
  </div>
);

/** Stoppuhr: roter Keil = Restzeit, Zeiger läuft einmal rum */
const Stopwatch: React.FC<{q: QuizQuestion; t: number}> = ({q, t}) => {
  const dur = Math.max(0.1, q.reveal - q.countdownStart);
  const p = interpolate(t, [q.countdownStart, q.reveal], [0, 1], clamp);
  const counting = t >= q.countdownStart && t < q.reveal;
  const left = Math.ceil(dur - (t - q.countdownStart));
  const cx = 170;
  const cy = 190;
  const r = 128;
  const a = p * Math.PI * 2;
  const wedge = p >= 1 || p <= 0 ? '' : `M${cx} ${cy} L${cx} ${cy - r + 10} A${r - 10} ${r - 10} 0 ${1 - p > 0.5 ? 1 : 0} 0 ${cx + (r - 10) * Math.sin(-(1 - p) * Math.PI * 2)} ${cy - (r - 10) * Math.cos((1 - p) * Math.PI * 2)} Z`;
  const shake = counting && left <= 2 ? Math.sin(t * 60) * 2.5 : 0;
  return (
    <div style={{position: 'absolute', left: 1500, top: 40, width: 340, height: 360, transform: `rotate(${6 + shake}deg)`, filter: 'drop-shadow(8px 14px 10px rgba(30,15,5,0.45))'}}>
      <svg width={340} height={360} viewBox="0 0 340 360">
        <rect x={150} y={18} width={40} height={30} rx={6} fill="#9EA3AB" stroke="#5E636B" strokeWidth={3} />
        <rect x={140} y={6} width={60} height={20} rx={8} fill="#C3C7CE" stroke="#5E636B" strokeWidth={3} />
        <rect x={250} y={58} width={34} height={22} rx={6} fill="#C3C7CE" stroke="#5E636B" strokeWidth={3} transform="rotate(40 267 69)" />
        <circle cx={cx} cy={cy} r={r + 22} fill="#B8BDC5" stroke="#5E636B" strokeWidth={4} />
        <circle cx={cx} cy={cy} r={r + 8} fill="#E7E9ED" />
        <circle cx={cx} cy={cy} r={r} fill="#FDFCF7" stroke="#2E3138" strokeWidth={3} />
        {wedge ? <path d={wedge} fill={K.red} opacity={0.85} /> : null}
        {Array.from({length: 60}).map((_, i) => {
          const an = (i / 60) * Math.PI * 2;
          const l = i % 5 === 0 ? 16 : 7;
          return <line key={i} x1={cx + Math.sin(an) * (r - 4)} y1={cy - Math.cos(an) * (r - 4)} x2={cx + Math.sin(an) * (r - 4 - l)} y2={cy - Math.cos(an) * (r - 4 - l)} stroke="#2E3138" strokeWidth={i % 5 === 0 ? 3.5 : 1.6} />;
        })}
        {counting ? (
          <text x={cx} y={cy + 32} textAnchor="middle" fontFamily={SERIF} fontSize={96} fill={K.ink} stroke="#FDFCF7" strokeWidth={6} paintOrder="stroke">
            {left}
          </text>
        ) : null}
        <line x1={cx} y1={cy + 18} x2={cx + Math.sin(a) * (r - 18)} y2={cy - Math.cos(a) * (r - 18)} stroke={K.ink} strokeWidth={5} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={9} fill={K.red} stroke={K.ink} strokeWidth={3} />
      </svg>
    </div>
  );
};

/** Gelber Klebezettel mit den Runden, aktuelle Runde rot umkringelt */
const RoundsNote: React.FC<{story: QuizStory; index: number}> = ({story, index}) => {
  const qs = story.questions;
  const q = qs[index];
  const levels = [...new Set(qs.map((x) => x.level ?? ''))].filter(Boolean);
  const cur = levels.indexOf(q.level ?? '');
  return (
    <div style={{position: 'absolute', left: 1490, top: 430, width: 360, height: 400, background: K.note, transform: 'rotate(2.5deg)', boxShadow: '0 14px 22px rgba(30,15,5,0.4)', padding: '26px 34px', boxSizing: 'border-box'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 34, background: 'rgba(0,0,0,0.05)'}} />
      <div style={{fontFamily: HAND, fontWeight: 700, fontSize: 40, color: K.ink, marginTop: 6}}>Rounds</div>
      {levels.map((lv, i) => (
        <div key={lv} style={{position: 'relative', fontFamily: HAND, fontSize: 34, color: i < cur ? K.grey : K.ink, lineHeight: 1.35, textDecoration: i < cur ? 'line-through' : 'none'}}>
          {i + 1}. {lv.charAt(0) + lv.slice(1).toLowerCase()} {i < cur ? <span style={{color: '#2E7D32', textDecoration: 'none', display: 'inline-block'}}>✓</span> : null}
          {i === cur ? (
            <svg width={300} height={66} style={{position: 'absolute', left: -18, top: -4}}>
              <path d="M18 34 C 18 8, 270 4, 282 28 C 292 54, 60 64, 24 46 C 10 38, 30 20, 60 14" fill="none" stroke={K.redPen} strokeWidth={4} strokeLinecap="round" />
            </svg>
          ) : null}
        </div>
      ))}
      <div style={{position: 'absolute', right: 30, bottom: 20, fontFamily: MARKER, fontSize: 44, color: K.ink}}>
        {index + 1}<span style={{color: K.grey, fontSize: 30}}> / {qs.length}</span>
      </div>
    </div>
  );
};

const CoffeeRing: React.FC = () => (
  <svg width={260} height={260} style={{position: 'absolute', left: 1640, top: 860}}>
    <circle cx={130} cy={130} r={92} fill="none" stroke="rgba(70,35,12,0.33)" strokeWidth={11} strokeDasharray="420 60 90 40" />
    <circle cx={130} cy={130} r={84} fill="none" stroke="rgba(70,35,12,0.14)" strokeWidth={4} />
  </svg>
);

/** Roter Gummistempel (Fleck-Maske = public/exam/grunge.png) */
export const Stamp: React.FC<{text: string; sub?: string; x: number; y: number; rot?: number; size?: number; from?: number; until?: number; color?: string}> = ({text, sub, x, y, rot = -7, size = 64, from = 0, until, color = K.red}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const f = frame - Math.round(from * fps);
  if (f < 0) return null;
  const slam = interpolate(f, [0, 5], [1.9, 1], clamp);
  const op = interpolate(f, [0, 3], [0, 1], clamp) * (until != null ? interpolate(frame, [Math.round(until * fps) - 6, Math.round(until * fps)], [1, 0], clamp) : 1);
  if (op <= 0) return null;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${slam})`, opacity: op * 0.92, WebkitMaskImage: `url(${staticFile('exam/grunge.png')})`, WebkitMaskSize: '420px 210px', maskImage: `url(${staticFile('exam/grunge.png')})`, maskSize: '420px 210px', mixBlendMode: 'multiply'}}>
      <div style={{border: `${Math.round(size / 9)}px solid ${color}`, borderRadius: 14, padding: `${size * 0.12}px ${size * 0.4}px`, textAlign: 'center', color, whiteSpace: 'nowrap'}}>
        <div style={{fontFamily: SERIF, fontSize: size, lineHeight: 1.05, letterSpacing: 3}}>{text}</div>
        {sub ? <div style={{fontFamily: TYPE, fontSize: size * 0.42, letterSpacing: 6, marginTop: 4}}>{sub}</div> : null}
      </div>
    </div>
  );
};

const qSize = (s: string, wide: boolean) => {
  const n = s.length;
  if (n > 95) return wide ? 44 : 40;
  if (n > 70) return wide ? 50 : 46;
  return wide ? 58 : 54;
};

export const ExamLongScene: React.FC<{q: QuizQuestion; index: number; story: QuizStory}> = ({q, index, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const qs = story.questions;
  const total = qs.length;
  const t = q.start + frame / fps;
  const local = frame / fps;
  const revealed = t >= q.reveal;
  const rv = t - q.reveal; // Sekunden seit Auflösung
  const levels = [...new Set(qs.map((x) => x.level ?? ''))].filter(Boolean);
  const newLevel = !!q.level && index > 0 && qs[index - 1].level !== q.level;
  const hasPic = !!(q.image || q.video);
  const sticker = !hasPic && q.cardText && q.cardText.length <= 8 && /\p{Extended_Pictographic}/u.test(q.cardText) ? q.cardText : null;
  const plain = q.q.replace(/\*\*/g, '');
  const qW = hasPic || sticker ? 900 : 1080;

  // Bleistift: liegt rechts unten; bei der Auflösung malt er den richtigen Kreis aus
  const bubbleScreen = {x: P.x + BUB.x + BUB.w / 2 - 14, y: P.y + ANS_Y + q.correct * ROW + BUB.h / 2 - 8};
  const rest = {x: 1470, y: 1000, a: -9};
  const go = interpolate(rv, [0, 0.28], [0, 1], clamp);
  const back = interpolate(rv, [0.78, 1.15], [0, 1], clamp);
  const move = revealed ? Math.min(go, 1 - back) : 0;
  const wig = revealed && rv > 0.26 && rv < 0.8 ? {x: Math.sin(rv * 70) * 16, y: Math.cos(rv * 47) * 6} : {x: 0, y: 0};
  const pencil = {
    x: interpolate(move, [0, 1], [rest.x, bubbleScreen.x]) + wig.x,
    y: interpolate(move, [0, 1], [rest.y, bubbleScreen.y]) + wig.y,
    a: interpolate(move, [0, 1], [rest.a, -42]),
  };
  const shade = interpolate(rv, [0.28, 0.78], [0, 1], clamp);
  const check = interpolate(rv, [0.8, 1.05], [0, 1], clamp);
  const loop = interpolate(rv, [0.95, 1.35], [0, 1], clamp);
  const dimOthers = interpolate(rv, [0.3, 0.6], [1, 0.42], clamp);

  // neuer Bogen: der alte wird nach links weggezogen
  const swipe = index === 0 ? 1 : interpolate(frame, [0, 11], [0, 1], {...clamp, easing: (x) => 1 - Math.pow(1 - x, 3)});
  const contentIn = index === 0 ? 1 : interpolate(frame, [5, 12], [0, 1], clamp);
  const drift = 1 + 0.012 * interpolate(local, [0, Math.max(1, q.end - q.start)], [0, 1], clamp);
  const levelShake = newLevel ? Math.sin(frame * 2.2) * interpolate(frame, [10, 22], [5, 0], clamp) * (frame >= 10 ? 1 : 0) : 0;

  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${drift}) translate(${levelShake}px, ${levelShake * 0.5}px)`, transformOrigin: '42% 50%'}}>
        <Desk />
        <CoffeeRing />
        <Stopwatch q={q} t={t} />
        <RoundsNote story={story} index={index} />

        <Sheet story={story}>
          <div style={{opacity: contentIn}}>
            {/* Frage */}
            <div style={{position: 'absolute', left: 104, top: 196, width: 88, textAlign: 'right', fontFamily: TYPE, fontSize: index >= 9 ? 46 : 52, color: K.red}}>{index + 1}.</div>
            <div style={{position: 'absolute', left: 206, top: 196, width: qW, fontFamily: TYPE, fontSize: qSize(plain, !sticker && !hasPic), lineHeight: 1.18, color: K.ink}}>
              <Marked text={q.q} at={q.keywordAt != null ? q.keywordAt - q.start : undefined} />
            </div>
            {/* Antworten als Ankreuz-Kreise */}
            {q.answers.map((a, i) => {
              const ok = i === q.correct;
              const y = ANS_Y + i * ROW;
              const appear = index === 0 ? 1 : interpolate(frame, [8 + i * 3, 14 + i * 3], [0, 1], clamp);
              const op = appear * (revealed && !ok ? dimOthers : 1);
              const textW = hasPic ? 640 : 900;
              const aSize = a.length > 30 ? 40 : a.length > 22 ? 46 : 52;
              return (
                <div key={i} style={{position: 'absolute', left: BUB.x, top: y, height: BUB.h, display: 'flex', alignItems: 'center', opacity: op}}>
                  <svg width={BUB.w} height={BUB.h} style={{flexShrink: 0, overflow: 'visible'}}>
                    <defs>
                      <clipPath id={`bub-${index}-${i}`}>
                        <ellipse cx={BUB.w / 2} cy={BUB.h / 2} rx={BUB.w / 2 - 4} ry={BUB.h / 2 - 4} />
                      </clipPath>
                    </defs>
                    <ellipse cx={BUB.w / 2} cy={BUB.h / 2} rx={BUB.w / 2 - 3} ry={BUB.h / 2 - 3} fill="none" stroke={K.ink} strokeWidth={3.5} />
                    <text x={BUB.w / 2} y={BUB.h / 2 + 11} textAnchor="middle" fontFamily={TYPE} fontSize={32} fill={K.ink}>
                      {LETTERS[i]}
                    </text>
                    {ok && shade > 0 ? (
                      <g clipPath={`url(#bub-${index}-${i})`}>
                        <path
                          d={Array.from({length: 9}, (_, k) => `${k === 0 ? 'M' : 'L'}${4 + k * 10} ${k % 2 ? 2 : BUB.h - 2}`).join(' ')}
                          stroke={K.pencil}
                          strokeWidth={14}
                          fill="none"
                          strokeLinejoin="round"
                          strokeDasharray={700}
                          strokeDashoffset={700 * (1 - shade)}
                          opacity={0.92}
                        />
                      </g>
                    ) : null}
                  </svg>
                  <div style={{position: 'relative', marginLeft: 34, maxWidth: textW, fontFamily: TYPE, fontSize: aSize, color: K.ink, whiteSpace: 'nowrap'}}>
                    {a}
                    {ok && revealed ? (
                      <svg width={600} height={140} style={{position: 'absolute', left: -30, top: -36, overflow: 'visible'}}>
                        <Drawn d={`M10 70 C 10 18, ${Math.min(560, a.length * 29 + 40)} 10, ${Math.min(580, a.length * 29 + 60)} 58 C ${Math.min(590, a.length * 29 + 70)} 110, 60 122, 20 96 C 6 84, 14 50, 70 34`} p={loop} width={5} />
                      </svg>
                    ) : null}
                  </div>
                  {ok && revealed ? (
                    <svg width={120} height={110} style={{marginLeft: 24, overflow: 'visible'}}>
                      <Drawn d="M10 58 L42 92 L112 8" p={check} width={11} len={200} />
                    </svg>
                  ) : null}
                </div>
              );
            })}
            {/* Aufkleber (Emoji aus cardText) oben rechts, Foto als Polaroid */}
            {sticker ? (
              <div style={{position: 'absolute', left: 1090, top: 176, width: 170, height: 170, borderRadius: '50%', background: '#fff', boxShadow: '0 6px 10px rgba(0,0,0,0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `rotate(9deg) scale(${index === 0 ? 1 : spring({frame: frame - 8, fps, config: {damping: 11}})})`}}>
                <div style={{fontFamily: EMOJI_FONT, fontSize: 104, lineHeight: 1}}>{sticker}</div>
              </div>
            ) : null}
            {hasPic ? (
              <div style={{position: 'absolute', left: 960, top: 420, width: 290, padding: '14px 14px 52px', background: '#fff', boxShadow: '0 8px 16px rgba(0,0,0,0.3)', transform: 'rotate(4deg)'}}>
                <div style={{width: 262, height: 230, overflow: 'hidden', background: '#ddd'}}>
                  {q.video ? <OffthreadVideo src={staticFile(q.video)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : <Img src={staticFile(q.image!)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}
                </div>
                <div style={{position: 'absolute', left: 95, top: -16, width: 110, height: 34, background: 'rgba(240,228,190,0.8)', transform: 'rotate(-4deg)'}} />
              </div>
            ) : null}
            {/* Fußzeile */}
            <div style={{position: 'absolute', left: 128, top: 955, fontFamily: TYPE, fontSize: 24, letterSpacing: 3, color: K.grey}}>
              SECTION {levels.indexOf(q.level ?? '') + 1} · {(q.level ?? '').toUpperCase()}
            </div>
            <div style={{position: 'absolute', right: 60, top: 955, fontFamily: TYPE, fontSize: 24, letterSpacing: 3, color: K.grey}}>
              PAGE {index + 1} OF {total}
            </div>
          </div>
        </Sheet>

        {/* alter Bogen fliegt weg */}
        {swipe < 1 ? <Sheet story={story} style={{transform: `translate(${-swipe * 1700}px, ${-swipe * 120}px) rotate(${P.rot - swipe * 14}deg)`}} /> : null}

        {/* Fakt nach der Auflösung: blauer Zettel */}
        {q.fact && revealed && rv > 1.0 ? (
          <div style={{position: 'absolute', left: 1480, top: 760, width: 380, minHeight: 200, background: K.noteBlue, transform: `rotate(-3deg) scale(${spring({frame: Math.round((rv - 1.0) * fps), fps, config: {damping: 12}})})`, boxShadow: '0 12px 20px rgba(30,15,5,0.4)', padding: '20px 26px', boxSizing: 'border-box'}}>
            <div style={{fontFamily: HAND, fontWeight: 700, fontSize: 32, color: K.ink}}>Did you know?</div>
            <div style={{fontFamily: HAND, fontSize: 27, color: K.ink, lineHeight: 1.25}}>{noEmoji(q.fact)}</div>
          </div>
        ) : null}

        <Pencil x={pencil.x} y={pencil.y} angle={pencil.a} />

        {/* Stempel */}
        {index === 0 && story.hook ? <Stamp text={noEmoji(story.hook)} x={1060} y={690} rot={-9} size={50} from={0.25} until={4.2} /> : null}
        {index === total - 1 && story.finalLabel && !revealed ? <Stamp text={noEmoji(story.finalLabel)} x={1060} y={690} rot={-9} size={50} from={0.2} /> : null}
        {index === total - 1 && story.ctaText && revealed ? <Stamp text={noEmoji(story.ctaText)} x={1060} y={690} rot={-8} size={48} from={q.reveal - q.start + 1.3} /> : null}
        {newLevel ? <Stamp text={`SECTION ${levels.indexOf(q.level!) + 1}`} sub={q.level!.toUpperCase()} x={760} y={560} rot={-8} size={120} from={0.3} until={2.3} /> : null}
        {story.midCtaIndex === index && revealed && rv > 1.2 ? (
          <div style={{position: 'absolute', left: 1475, top: 455, width: 380, height: 360, background: K.notePink, transform: `rotate(-4deg) scale(${spring({frame: Math.round((rv - 1.2) * fps), fps, config: {damping: 11}})})`, boxShadow: '0 14px 22px rgba(30,15,5,0.45)', padding: '28px 30px', boxSizing: 'border-box', textAlign: 'center'}}>
            <div style={{fontFamily: HAND, fontWeight: 700, fontSize: 38, color: K.ink, lineHeight: 1.2}}>Enjoying the exam?</div>
            <div style={{display: 'inline-block', marginTop: 22, background: '#CC0000', color: '#fff', fontFamily: SERIF, fontSize: 40, padding: '10px 26px', borderRadius: 10, transform: 'rotate(2deg)'}}>SUBSCRIBE</div>
            <div style={{fontFamily: HAND, fontSize: 32, color: K.ink, marginTop: 20}}>…and hit the bell!</div>
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const ExamLongOutro: React.FC<{story: QuizStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = story.questions.length;
  const sec = frame / fps;
  const loop = interpolate(sec, [0.5, 1.1], [0, 1], clamp);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Desk />
      <CoffeeRing />
      <Sheet story={story}>
        <div style={{position: 'absolute', left: 0, right: 0, top: 210, textAlign: 'center', fontFamily: TYPE, fontSize: 40, letterSpacing: 8, color: K.grey}}>RESULTS</div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 270, textAlign: 'center', fontFamily: HAND, fontWeight: 700, fontSize: 92, color: K.redPen, transform: 'rotate(-2deg)'}}>{noEmoji(story.outroText) || 'How many did you get?'}</div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 430, display: 'flex', justifyContent: 'center'}}>
          <div style={{position: 'relative', fontFamily: MARKER, fontSize: 190, color: K.redPen, lineHeight: 1}}>
            ?<span style={{fontSize: 150}}>/{n}</span>
            <svg width={560} height={300} style={{position: 'absolute', left: -110, top: -50, overflow: 'visible'}}>
              <Drawn d="M60 150 C 40 40, 480 10, 520 120 C 560 240, 140 300, 70 210 C 40 170, 80 90, 160 70" p={loop} width={8} len={1600} />
            </svg>
          </div>
        </div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 700, textAlign: 'center', fontFamily: HAND, fontSize: 58, color: K.ink}}>{noEmoji(story.outroSub) || 'Comment your score'} below!</div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 820, textAlign: 'center', fontFamily: TYPE, fontSize: 30, letterSpacing: 2, color: K.grey}}>{noEmoji(story.subscribeText) || 'New quiz every day'}</div>
      </Sheet>
      <Stopwatch q={{...story.questions[0], countdownStart: 1e9, reveal: 1e9 + 1}} t={0} />
      <div style={{position: 'absolute', left: 1500, top: 520, width: 340, height: 300, background: K.notePink, transform: `rotate(-3deg) scale(${spring({frame: frame - 12, fps, config: {damping: 12}})})`, boxShadow: '0 14px 22px rgba(30,15,5,0.45)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center'}}>
        <div style={{fontFamily: HAND, fontWeight: 700, fontSize: 38, color: K.ink}}>New quiz every day</div>
        <div style={{marginTop: 18, background: '#CC0000', color: '#fff', fontFamily: SERIF, fontSize: 42, padding: '10px 28px', borderRadius: 10}}>SUBSCRIBE</div>
      </div>
      <Pencil x={1470} y={1000} angle={-9} />
    </AbsoluteFill>
  );
};
