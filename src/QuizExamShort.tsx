// Short-Layout "exam" im Hochformat (seit 25.11.2026, Besitzer: tvshow-Short „gefällt mir gar nicht“).
// Gleicher Look wie die langen Videos (QuizExam.tsx): Holztisch, Prüfungsbogen, Schreibmaschinen-Frage,
// Ankreuz-Kreise, Bleistift malt die Lösung aus, Rotstift-Haken, Stoppuhr, Klebezettel, Stempel.
// Safe-Zone Shorts: unten ≈ 330 px (Titel/Kanal), rechts ≈ 130 px (Buttons) → Wichtiges liegt in x < 940, y < 1580.
import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont as loadType} from '@remotion/google-fonts/SpecialElite';
import {loadFont as loadHand} from '@remotion/google-fonts/Kalam';
import {loadFont as loadSerif} from '@remotion/google-fonts/Fraunces';
import {loadFont as loadMarker} from '@remotion/google-fonts/PermanentMarker';
import type {QuizQuestion, QuizStory} from './Quiz';
import {Drawn, Marked, Pencil, Stamp, noEmoji} from './QuizExam';

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

// Bogen-Geometrie (Bildschirm 1080x1920)
const S = {x: 40, y: 300, w: 1000, h: 1230, rot: -0.8};
const BUB = {x: 70, w: 130, h: 92};

/** Holztisch: Querformat-Textur um 90° gedreht → füllt 1080x1920 ohne Hochskalieren */
const Desk: React.FC = () => (
  <div style={{position: 'absolute', left: (1080 - 1920) / 2, top: (1920 - 1080) / 2, width: 1920, height: 1080, transform: 'rotate(90deg)'}}>
    <Img src={staticFile('exam/desk.jpg')} style={{width: 1920, height: 1080}} />
  </div>
);

const Sheet: React.FC<{story: QuizStory; children?: React.ReactNode; style?: React.CSSProperties; blank?: boolean}> = ({story, children, style, blank}) => (
  <div style={{position: 'absolute', left: S.x, top: S.y, width: S.w, height: S.h, transform: `rotate(${S.rot}deg)`, boxShadow: '0 18px 40px rgba(30,15,5,0.45), 0 2px 4px rgba(0,0,0,0.25)', ...style}}>
    <Img src={staticFile('exam/paper.jpg')} style={{position: 'absolute', inset: 0, width: S.w, height: S.h, objectFit: 'cover'}} />
    <svg width={S.w} height={S.h} style={{position: 'absolute', inset: 0}}>
      {Array.from({length: 18}).map((_, i) => (
        <line key={i} x1={0} x2={S.w} y1={250 + i * 58} y2={250 + i * 58} stroke={K.rule} strokeWidth={2} />
      ))}
      <line x1={46} x2={46} y1={0} y2={S.h} stroke={K.margin} strokeWidth={2.5} />
      <line x1={70} x2={S.w - 40} y1={176} y2={176} stroke={K.ink} strokeWidth={3} />
      <line x1={70} x2={S.w - 40} y1={184} y2={184} stroke={K.ink} strokeWidth={1} />
    </svg>
    {blank ? null : (
      <>
        <div style={{position: 'absolute', left: 72, top: 34, fontFamily: SERIF, fontSize: 72, color: K.ink, letterSpacing: -0.5}}>
          COULD YOU <span style={{color: K.red}}>PASS?</span>
        </div>
        <div style={{position: 'absolute', left: 76, top: 126, fontFamily: TYPE, fontSize: 27, letterSpacing: 3, color: K.grey}}>{noEmoji(story.header || story.title).toUpperCase()} · EXAM</div>
      </>
    )}
    {children}
  </div>
);

/** Stoppuhr oben rechts (wie im Long, kleiner) */
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
    <div style={{position: 'absolute', left: 640, top: 18, width: 340, height: 360, transform: `scale(0.86) rotate(${7 + shake}deg)`, transformOrigin: '50% 0', filter: 'drop-shadow(8px 14px 10px rgba(30,15,5,0.45))'}}>
      <svg width={340} height={360} viewBox="0 0 340 360">
        <rect x={150} y={18} width={40} height={30} rx={6} fill="#9EA3AB" stroke="#5E636B" strokeWidth={3} />
        <rect x={140} y={6} width={60} height={20} rx={8} fill="#C3C7CE" stroke="#5E636B" strokeWidth={3} />
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

/** Gelber Klebezettel oben links: Fortschritt */
const ProgressNote: React.FC<{index: number; total: number; label: string}> = ({index, total, label}) => (
  <div style={{position: 'absolute', left: 50, top: 60, width: 360, height: 230, background: K.note, transform: 'rotate(-4deg)', boxShadow: '0 14px 22px rgba(30,15,5,0.4)', padding: '22px 30px', boxSizing: 'border-box'}}>
    <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 30, background: 'rgba(0,0,0,0.05)'}} />
    <div style={{fontFamily: HAND, fontWeight: 700, fontSize: 40, color: K.ink, marginTop: 4}}>{label}</div>
    <div style={{fontFamily: MARKER, fontSize: 96, color: K.ink, lineHeight: 1.05}}>
      {index + 1}
      <span style={{color: K.grey, fontSize: 60}}> / {total}</span>
    </div>
  </div>
);

const qSize = (s: string, wide: boolean) => {
  const n = s.length;
  if (n > 80) return wide ? 62 : 58;
  if (n > 55) return wide ? 72 : 68;
  return wide ? 86 : 80;
};

export const ExamShortScene: React.FC<{q: QuizQuestion; index: number; total: number; story: QuizStory}> = ({q, index, total, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = q.start + frame / fps;
  const local = frame / fps;
  const revealed = t >= q.reveal;
  const rv = t - q.reveal;
  const hasPic = !!(q.image || q.video);
  const sticker = !hasPic && q.cardText && q.cardText.length <= 8 && /\p{Extended_Pictographic}/u.test(q.cardText) ? q.cardText : null;
  const plain = q.q.replace(/\*\*/g, '');
  const qW = sticker ? 640 : 860;
  const n = q.answers.length;
  const row = n <= 2 ? 190 : 128;
  const ansY = n <= 2 ? 790 : 660;

  // Bleistift liegt unten; bei der Auflösung malt er den richtigen Kreis aus
  const bubbleScreen = {x: S.x + BUB.x + BUB.w / 2 - 14, y: S.y + ansY + q.correct * row + BUB.h / 2 - 8};
  const rest = {x: 640, y: 1650, a: -14};
  const go = interpolate(rv, [0, 0.28], [0, 1], clamp);
  const back = interpolate(rv, [0.78, 1.15], [0, 1], clamp);
  const move = revealed ? Math.min(go, 1 - back) : 0;
  const wig = revealed && rv > 0.26 && rv < 0.8 ? {x: Math.sin(rv * 70) * 16, y: Math.cos(rv * 47) * 6} : {x: 0, y: 0};
  const pencil = {
    x: interpolate(move, [0, 1], [rest.x, bubbleScreen.x]) + wig.x,
    y: interpolate(move, [0, 1], [rest.y, bubbleScreen.y]) + wig.y,
    a: interpolate(move, [0, 1], [rest.a, -38]),
  };
  const shade = interpolate(rv, [0.28, 0.78], [0, 1], clamp);
  const check = interpolate(rv, [0.8, 1.05], [0, 1], clamp);
  const loop = interpolate(rv, [0.95, 1.35], [0, 1], clamp);
  const dimOthers = interpolate(rv, [0.3, 0.6], [1, 0.4], clamp);

  const swipe = index === 0 ? 1 : interpolate(frame, [0, 10], [0, 1], {...clamp, easing: (x) => 1 - Math.pow(1 - x, 3)});
  const contentIn = index === 0 ? 1 : interpolate(frame, [4, 10], [0, 1], clamp);
  const drift = 1 + 0.015 * interpolate(local, [0, Math.max(1, q.end - q.start)], [0, 1], clamp);
  const label = noEmoji(q.level || story.header || 'Question');
  const lastQ = index === total - 1;

  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${drift})`, transformOrigin: '45% 45%'}}>
        <Desk />
        <ProgressNote index={index} total={total} label={label.charAt(0) + label.slice(1).toLowerCase()} />
        <Stopwatch q={q} t={t} />

        <Sheet story={story}>
          <div style={{opacity: contentIn}}>
            <div style={{position: 'absolute', left: 44, top: 222, width: 90, textAlign: 'right', fontFamily: TYPE, fontSize: 64, color: K.red}}>{index + 1}.</div>
            <div style={{position: 'absolute', left: 150, top: 222, width: qW, fontFamily: TYPE, fontSize: qSize(plain, !sticker), lineHeight: 1.2, color: K.ink}}>
              <Marked text={q.q} at={q.keywordAt != null ? q.keywordAt - q.start : undefined} />
            </div>
            {sticker ? (
              <div style={{position: 'absolute', left: 790, top: 220, width: 180, height: 180, borderRadius: '50%', background: '#fff', boxShadow: '0 6px 10px rgba(0,0,0,0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `rotate(9deg) scale(${index === 0 ? 1 : spring({frame: frame - 8, fps, config: {damping: 11}})})`}}>
                <div style={{fontFamily: EMOJI_FONT, fontSize: 110, lineHeight: 1}}>{sticker}</div>
              </div>
            ) : null}
            {hasPic ? (
              <div style={{position: 'absolute', left: 560, top: 520, width: 360, padding: '14px 14px 50px', background: '#fff', boxShadow: '0 8px 16px rgba(0,0,0,0.3)', transform: 'rotate(4deg)'}}>
                <div style={{width: 332, height: 280, overflow: 'hidden', background: '#ddd'}}>
                  {q.video ? <OffthreadVideo src={staticFile(q.video)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : <Img src={staticFile(q.image!)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}
                </div>
              </div>
            ) : null}
            {q.answers.map((a, i) => {
              const ok = i === q.correct;
              const y = ansY + i * row;
              const appear = index === 0 ? 1 : interpolate(frame, [7 + i * 3, 13 + i * 3], [0, 1], clamp);
              const op = appear * (revealed && !ok ? dimOthers : 1);
              const aSize = a.length > 22 ? 56 : a.length > 14 ? 68 : n <= 2 ? 92 : 78;
              return (
                <div key={i} style={{position: 'absolute', left: BUB.x, top: y, height: BUB.h, display: 'flex', alignItems: 'center', opacity: op}}>
                  <svg width={BUB.w} height={BUB.h} style={{flexShrink: 0, overflow: 'visible'}}>
                    <defs>
                      <clipPath id={`sbub-${index}-${i}`}>
                        <ellipse cx={BUB.w / 2} cy={BUB.h / 2} rx={BUB.w / 2 - 4} ry={BUB.h / 2 - 4} />
                      </clipPath>
                    </defs>
                    <ellipse cx={BUB.w / 2} cy={BUB.h / 2} rx={BUB.w / 2 - 3} ry={BUB.h / 2 - 3} fill="none" stroke={K.ink} strokeWidth={4} />
                    <text x={BUB.w / 2} y={BUB.h / 2 + 13} textAnchor="middle" fontFamily={TYPE} fontSize={44} fill={K.ink}>
                      {LETTERS[i]}
                    </text>
                    {ok && shade > 0 ? (
                      <g clipPath={`url(#sbub-${index}-${i})`}>
                        <path d={Array.from({length: 11}, (_, k) => `${k === 0 ? 'M' : 'L'}${4 + k * 12} ${k % 2 ? 2 : BUB.h - 2}`).join(' ')} stroke={K.pencil} strokeWidth={16} fill="none" strokeLinejoin="round" strokeDasharray={900} strokeDashoffset={900 * (1 - shade)} opacity={0.92} />
                      </g>
                    ) : null}
                  </svg>
                  <div style={{position: 'relative', marginLeft: 36, fontFamily: TYPE, fontSize: aSize, color: K.ink, whiteSpace: 'nowrap'}}>
                    {a}
                    {ok && revealed ? (
                      <svg width={600} height={160} style={{position: 'absolute', left: -34, top: -40, overflow: 'visible'}}>
                        <Drawn d={`M10 78 C 10 18, ${Math.min(560, a.length * 54 + 40)} 10, ${Math.min(580, a.length * 54 + 60)} 64 C ${Math.min(590, a.length * 54 + 70)} 124, 60 136, 20 106 C 6 92, 14 56, 70 38`} p={loop} width={6} />
                      </svg>
                    ) : null}
                  </div>
                  {ok && revealed ? (
                    <svg width={140} height={128} style={{marginLeft: 30, overflow: 'visible'}}>
                      <Drawn d="M10 68 L48 108 L130 8" p={check} width={13} len={240} />
                    </svg>
                  ) : null}
                </div>
              );
            })}
            {q.fact && revealed && rv > 1.0 ? (
              <div style={{position: 'absolute', left: 90, top: ansY + n * row + 10, width: 760, fontFamily: HAND, fontSize: 40, color: K.redPen, lineHeight: 1.2, transform: 'rotate(-1.5deg)', opacity: interpolate(rv, [1.0, 1.25], [0, 1], clamp)}}>
                {noEmoji(q.fact)}
              </div>
            ) : null}
            <div style={{position: "absolute", right: 50, top: 1180, fontFamily: TYPE, fontSize: 26, letterSpacing: 3, color: K.grey}}>PAGE {index + 1} OF {total}</div>
          </div>
        </Sheet>

        {swipe < 1 ? <Sheet story={story} style={{transform: `translate(${-swipe * 1300}px, ${-swipe * 160}px) rotate(${S.rot - swipe * 16}deg)`}} /> : null}

        <Pencil x={pencil.x} y={pencil.y} angle={pencil.a} />

        {index === 0 && story.hook ? <Stamp text={noEmoji(story.hook)} x={520} y={1475} rot={-7} size={66} from={0.15} until={Math.min(q.countdownStart - q.start, 2.6)} /> : null}
        {lastQ && index > 0 && story.finalLabel && !revealed ? <Stamp text={noEmoji(story.finalLabel)} x={520} y={1475} rot={-7} size={66} from={0.15} until={q.countdownStart - q.start} /> : null}
        {lastQ && story.ctaText && revealed && rv > 1.2 ? <Stamp text="SCORE?" sub="COMMENT BELOW" x={520} y={1480} rot={-7} size={84} from={q.reveal - q.start + 1.2} /> : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const ExamShortOutro: React.FC<{story: QuizStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const sec = frame / 30;
  const loop = interpolate(sec, [0.2, 0.7], [0, 1], clamp);
  const n = story.questions.length;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Desk />
      <Sheet story={story}>
        <div style={{position: 'absolute', left: 0, right: 0, top: 250, textAlign: 'center', fontFamily: TYPE, fontSize: 44, letterSpacing: 8, color: K.grey}}>RESULTS</div>
        <div style={{position: 'absolute', left: 40, right: 40, top: 320, textAlign: 'center', fontFamily: HAND, fontWeight: 700, fontSize: 92, lineHeight: 1.1, color: K.redPen, transform: 'rotate(-2deg)'}}>{noEmoji(story.outroText) || 'How many did you get?'}</div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 580, display: 'flex', justifyContent: 'center'}}>
          <div style={{position: 'relative', fontFamily: MARKER, fontSize: 230, color: K.redPen, lineHeight: 1}}>
            ?<span style={{fontSize: 180}}>/{n}</span>
            <svg width={600} height={320} style={{position: 'absolute', left: -120, top: -50, overflow: 'visible'}}>
              <Drawn d="M60 160 C 40 40, 520 10, 560 130 C 600 250, 140 320, 70 220 C 40 180, 80 90, 170 70" p={loop} width={9} len={1700} />
            </svg>
          </div>
        </div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 900, textAlign: 'center', fontFamily: HAND, fontSize: 60, color: K.ink}}>{noEmoji(story.outroSub) || 'Comment your score'}</div>
      </Sheet>
    </AbsoluteFill>
  );
};
