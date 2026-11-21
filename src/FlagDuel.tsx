// Format "Flag Duel" (story.type "flagduel") – "Who is CHAD? Left or right?"
// Zwei fast gleiche Flaggen, darunter zwei Länder-Bälle (flache 2D-Bälle mit der Flagge als Haut),
// Countdown 3-2-1, in dem die Bälle sich anrempeln, dann Auflösung: richtige Flagge grün mit Haken,
// falsche gedimmt mit rotem X, Gewinner-Ball springt, Verlierer wird weggeschubst.
// Farben/Schrift aus dem tvshow-Look (Nachthimmel, Papier-Karten, Inter + DM Serif) – kein 3D, keine KI-Bilder.
// Flaggen: public/flags/<iso2>.svg (flag-icons, MIT; Flaggen selbst gemeinfrei).
// Zeiten (start/thinkStart/reveal/moveEnd/aStart/end, hook) setzt autopilot/atlas_voice.py.
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadSerif} from '@remotion/google-fonts/DMSerifDisplay';

const FONT = loadInter('normal', {weights: ['700', '800', '900'], subsets: ['latin', 'latin-ext']}).fontFamily;
const SERIF = loadSerif('normal', {weights: ['400'], subsets: ['latin']}).fontFamily;

const C = {
  sky: '#14213D',
  sky2: '#1B2B4F',
  paper: '#F4EEDF',
  paperDark: '#E6DCC4',
  ink: '#18213A',
  gold: '#E9B44C',
  green: '#2E8B57',
  greenLight: '#3DA56A',
  hill: '#2F7D4F',
  hill2: '#3B9460',
  red: '#C8312E',
  white: '#FFFFFF',
};

export type FlagSide = {flag: string; name: string};
export type FlagRound = {
  level?: string;
  /** Name, nach dem gefragt wird (Großbuchstaben im Bild), z. B. "CHAD" */
  target: string;
  a: FlagSide; // links
  b: FlagSide; // rechts
  winner: 'a' | 'b';
  lines: {q: string; a: string};
  start: number;
  thinkStart: number;
  reveal: number;
  moveEnd: number;
  aStart: number;
  end: number;
  qAudio?: string;
  aAudio?: string;
};
export type FlagDuelStory = {
  id: string;
  type: 'flagduel';
  title: string;
  /** Zeile über "WHO IS", z. B. "CAN YOU GET 4/4?" (nur Runde 1) */
  kicker?: string;
  hookLine: string;
  hook: {audio?: string; start: number; end: number};
  rounds: FlagRound[];
  music?: string;
  musicVolume?: number;
  outroText: string;
  outroSub: string;
  durationInSeconds: number;
  brand?: string;
};

const W = 1080;
const BALL_Y = 1430;
const BALL_R = 185;
const BALL_X = [292, 788];
const CARD = {w: 476, h: 357, y: 540, x: [44, 560]};

const outline = (c: string, w: number) => {
  const s: string[] = [];
  for (let a = 0; a < 16; a++) s.push(`${(Math.cos((a / 16) * Math.PI * 2) * w).toFixed(1)}px ${(Math.sin((a / 16) * Math.PI * 2) * w).toFixed(1)}px 0 ${c}`);
  return s.join(',');
};

// deterministischer Zufall
const rnd = (i: number) => {
  const x = Math.sin(i * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
};

const Stars: React.FC = () => (
  <svg width={W} height={1920} style={{position: 'absolute', inset: 0}}>
    {Array.from({length: 70}).map((_, i) => (
      <circle key={i} cx={rnd(i) * W} cy={rnd(i + 100) * 1150} r={1 + rnd(i + 200) * 2.2} fill={C.paper} opacity={0.12 + rnd(i + 300) * 0.25} />
    ))}
  </svg>
);

const Ground: React.FC = () => (
  <svg width={W} height={1920} style={{position: 'absolute', inset: 0}}>
    <path d={`M0 1215 C 260 1140, 520 1170, 760 1150 C 900 1138, 1000 1155, ${W} 1175 L ${W} 1920 L 0 1920 Z`} fill={C.hill2} />
    <path d={`M0 1300 C 300 1250, 700 1270, ${W} 1240 L ${W} 1920 L 0 1920 Z`} fill={C.hill} />
    {Array.from({length: 26}).map((_, i) => (
      <path key={i} d={`M${rnd(i + 500) * W} ${1400 + rnd(i + 600) * 480} l 6 -22 l 6 22`} stroke={C.hill2} strokeWidth={5} fill="none" strokeLinecap="round" />
    ))}
  </svg>
);

type Mood = 'calm' | 'angry' | 'happy' | 'sad';

/** Länder-Ball: Kreis mit Flagge als Haut, schwarze Kontur, Augen je nach Stimmung */
const Ball: React.FC<{flag: string; mood: Mood; facing: 1 | -1; id: string}> = ({flag, mood, facing, id}) => {
  const r = BALL_R;
  const s = r * 2 + 24;
  const cx = s / 2;
  const cy = s / 2;
  const ex = (k: number) => cx + facing * 20 + k * 58;
  const ey = cy - 22;
  return (
    <svg width={s} height={s} viewBox={`0 0 ${s} ${s}`} style={{overflow: 'visible'}}>
      <defs>
        <clipPath id={`clip-${id}`}>
          <circle cx={cx} cy={cy} r={r} />
        </clipPath>
        <radialGradient id={`shade-${id}`} cx="35%" cy="30%" r="75%">
          <stop offset="0%" stopColor="#fff" stopOpacity={0.28} />
          <stop offset="55%" stopColor="#fff" stopOpacity={0} />
          <stop offset="100%" stopColor="#000" stopOpacity={0.32} />
        </radialGradient>
      </defs>
      <g clipPath={`url(#clip-${id})`}>
        {/* Flagge als Haut: Höhe = Durchmesser, Breite 4:3, mittig */}
        <image href={staticFile(`flags/${flag}.svg`)} x={cx - r * 1.34} y={cy - r} width={r * 2.68} height={r * 2} preserveAspectRatio="none" />
        <circle cx={cx} cy={cy} r={r} fill={`url(#shade-${id})`} />
      </g>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#111" strokeWidth={9} />
      {/* Augen */}
      {[-1, 1].map((k) => {
        const x = ex(k);
        if (mood === 'happy') {
          return <path key={k} d={`M${x - 24} ${ey + 8} Q ${x} ${ey - 26} ${x + 24} ${ey + 8}`} stroke="#111" strokeWidth={10} fill="none" strokeLinecap="round" />;
        }
        return (
          <g key={k}>
            <ellipse cx={x} cy={ey} rx={24} ry={mood === 'sad' ? 26 : 30} fill="#fff" stroke="#111" strokeWidth={7} />
            {mood === 'angry' ? (
              <path d={`M${x - 36} ${ey - 40 + (k === facing ? 20 : 0)} L ${x + 36} ${ey - 40 + (k === facing ? 0 : 20)} L ${x + 36} ${ey - 14} L ${x - 36} ${ey - 14} Z`} fill="#111" />
            ) : null}
            {mood === 'sad' ? <path d={`M${x - 30} ${ey - 30 + (k > 0 ? 12 : 0)} L ${x + 30} ${ey - 30 + (k > 0 ? 0 : 12)}`} stroke="#111" strokeWidth={9} strokeLinecap="round" /> : null}
          </g>
        );
      })}
      {mood === 'sad' ? <path d={`M${ex(-1) - 4} ${ey + 34} q -12 26 0 36 q 12 -10 0 -36 Z`} fill="#6EC3FF" stroke="#111" strokeWidth={4} /> : null}
    </svg>
  );
};

const FlagCard: React.FC<{side: FlagSide; x: number; state: 'idle' | 'right' | 'wrong'; pop: number; label: string; reveal: number}> = ({side, x, state, pop, label, reveal}) => {
  const dim = state === 'wrong' ? interpolate(reveal, [0, 1], [1, 0.42]) : 1;
  const scale = state === 'right' ? 1 + 0.06 * Math.sin(Math.min(1, reveal) * Math.PI) : 1;
  const border = state === 'right' ? C.greenLight : state === 'wrong' ? C.red : C.paperDark;
  return (
    <div style={{position: 'absolute', left: x, top: CARD.y, width: CARD.w, transform: `scale(${pop * scale})`, transformOrigin: '50% 60%'}}>
      <div style={{width: CARD.w, height: CARD.h, background: C.paper, borderRadius: 14, padding: 16, boxSizing: 'border-box', border: `6px solid ${reveal > 0 ? border : C.paper}`, boxShadow: '0 14px 0 rgba(0,0,0,0.35)'}}>
        <Img src={staticFile(`flags/${side.flag}.svg`)} style={{width: '100%', height: '100%', objectFit: 'fill', borderRadius: 4, opacity: dim, filter: state === 'wrong' ? `grayscale(${0.6 * reveal})` : 'none', border: '1px solid rgba(0,0,0,0.15)', boxSizing: 'border-box'}} />
      </div>
      {/* Haken / X */}
      {reveal > 0 ? (
        <div style={{position: 'absolute', right: -18, top: -26, width: 104, height: 104, borderRadius: '50%', background: state === 'right' ? C.green : C.red, border: '6px solid #fff', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${Math.min(1, reveal * 1.4)}) rotate(${state === 'right' ? 0 : -8}deg)`, boxShadow: '0 6px 0 rgba(0,0,0,0.35)'}}>
          <svg width={58} height={58} viewBox="0 0 58 58">
            {state === 'right' ? <path d="M8 30 L23 45 L51 12" stroke="#fff" strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" /> : <path d="M12 12 L46 46 M46 12 L12 46" stroke="#fff" strokeWidth={10} strokeLinecap="round" />}
          </svg>
        </div>
      ) : null}
      {/* Etikett: LEFT/RIGHT, nach der Auflösung der Ländername */}
      <div style={{display: 'flex', justifyContent: 'center', marginTop: 26}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 46, letterSpacing: 1, color: reveal > 0 ? C.white : C.ink, background: reveal > 0 ? (state === 'right' ? C.green : C.red) : C.paper, padding: '10px 34px', borderRadius: 40, boxShadow: '0 6px 0 rgba(0,0,0,0.35)', whiteSpace: 'nowrap'}}>
          {label}
        </div>
      </div>
    </div>
  );
};

const Confetti: React.FC<{t: number; cx: number}> = ({t, cx}) => {
  if (t <= 0 || t > 1.6) return null;
  const cols = [C.gold, C.greenLight, C.paper, '#E07A5F', '#7FC8A9'];
  return (
    <svg width={W} height={1920} style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
      {Array.from({length: 46}).map((_, i) => {
        const ang = rnd(i + 900) * Math.PI * 2;
        const sp = 260 + rnd(i + 950) * 420;
        const x = cx + Math.cos(ang) * sp * t;
        const y = CARD.y + 150 + Math.sin(ang) * sp * t * 0.8 + 520 * t * t;
        return <rect key={i} x={x} y={y} width={14} height={22} fill={cols[i % cols.length]} transform={`rotate(${(rnd(i) * 360 + t * 600) % 360} ${x + 7} ${y + 11})`} opacity={interpolate(t, [1.1, 1.6], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />;
      })}
    </svg>
  );
};

export const FlagDuel: React.FC<FlagDuelStory> = (story) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const rounds = story.rounds;
  const n = rounds.length;
  let idx = rounds.findIndex((r) => t < r.end);
  if (idx < 0) idx = n - 1;
  const r = rounds[idx];
  const last = rounds[n - 1];
  const outroStart = last.moveEnd + 1.7;
  const inOutro = t >= outroStart;
  const sinceStart = t - (idx === 0 ? 0 : r.start);
  const revealT = t - r.reveal;
  const revealed = revealT >= 0;
  const rv = revealed ? Math.min(1, revealT / 0.35) : 0;
  const thinking = t >= r.thinkStart && !revealed;

  // Auftritt der Karten pro Runde
  const pop = idx === 0 ? 1 : spring({frame: Math.round(sinceStart * fps), fps, config: {damping: 13, stiffness: 160}});
  // Runde endet: kurz ausblenden (nicht nach der letzten)
  const fadeOut = idx < n - 1 ? interpolate(t, [r.end - 0.22, r.end], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;

  // Bälle: Einfallen, Wippen, Anrempeln im Countdown, Sieg/Niederlage
  const drop = idx === 0 ? 1 : spring({frame: Math.round(Math.max(0, sinceStart - 0.1) * fps), fps, config: {damping: 9, stiffness: 120}});
  const ballState = (side: 'a' | 'b') => {
    const k = side === 'a' ? -1 : 1; // Richtung nach außen
    let x = BALL_X[side === 'a' ? 0 : 1];
    let y = BALL_Y - (1 - drop) * 900;
    let rot = 0;
    let sq = 1;
    let mood: Mood = 'calm';
    // Wippen
    y += Math.sin(t * 5 + (side === 'a' ? 0 : 1.6)) * 8;
    if (thinking) {
      mood = 'angry';
      const p = (t - r.thinkStart) % 1; // jede Sekunde ein Rempler
      const bump = p < 0.35 ? Math.sin((p / 0.35) * Math.PI) : 0;
      x += -k * bump * 70;
      rot = -k * bump * 10;
      sq = 1 - bump * 0.08;
      if (bump > 0.85) x += Math.sin(t * 90) * 6;
    }
    if (revealed) {
      const win = r.winner === side;
      const u = Math.min(1, revealT / 0.7);
      if (win) {
        mood = 'happy';
        y -= Math.sin(Math.min(1, revealT / 0.6) * Math.PI) * 190;
        rot = Math.sin(revealT * 6) * 6;
      } else {
        mood = 'sad';
        x += k * 85 * Math.sin((u * Math.PI) / 2);
        rot = k * 35 * u;
        y += 30 * u;
        sq = 1 - 0.1 * u;
      }
    }
    return {x, y, rot, sq, mood};
  };

  const header = inOutro ? ['HOW MANY', 'DID YOU GET?'] : ['WHO IS', `${r.target}?`];
  const targetSize = header[1].length > 11 ? 112 : header[1].length > 8 ? 132 : 158;
  const countdown = thinking ? Math.max(1, 3 - Math.floor(t - r.thinkStart)) : 0;
  const cdP = thinking ? (t - r.thinkStart) % 1 : 0;
  const winX = r.winner === 'a' ? CARD.x[0] + CARD.w / 2 : CARD.x[1] + CARD.w / 2;

  return (
    <AbsoluteFill style={{background: `linear-gradient(${C.sky}, ${C.sky2})`, overflow: 'hidden'}}>
      <Stars />
      <Ground />

      {/* Kopfzeile: Fortschritt + Wortmarke */}
      <div style={{position: 'absolute', left: 48, top: 64, fontFamily: FONT, fontWeight: 900, fontSize: 46, color: C.ink, background: C.gold, padding: '6px 24px', borderRadius: 30}}>
        {idx + 1}/{n}
      </div>
      <div style={{position: 'absolute', right: 52, top: 70, fontFamily: SERIF, fontSize: 44, color: C.paper}}>{story.brand ?? 'Could You Pass?'}</div>

      {/* Frage */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 170, textAlign: 'center', opacity: fadeOut}}>
        {idx === 0 && story.kicker && !inOutro ? (
          <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 52, color: C.gold, textShadow: outline('#0B1226', 4), marginBottom: 6}}>{story.kicker}</div>
        ) : (
          <div style={{height: 68}} />
        )}
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 70, color: C.paper, textShadow: outline('#0B1226', 5), lineHeight: 1}}>{header[0]}</div>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: inOutro ? 112 : targetSize, color: C.gold, textShadow: `${outline('#0B1226', 8)}, 0 12px 0 #0B1226`, lineHeight: 1.08, transform: `scale(${idx === 0 || inOutro ? 1 : pop})`}}>{header[1]}</div>
      </div>

      {/* Flaggen */}
      <div style={{position: 'absolute', inset: 0, opacity: fadeOut}}>
        {(['a', 'b'] as const).map((s, i) => (
          <FlagCard
            key={s + idx}
            side={r[s]}
            x={CARD.x[i]}
            pop={pop}
            reveal={rv}
            state={!revealed ? 'idle' : r.winner === s ? 'right' : 'wrong'}
            label={revealed ? r[s].name.toUpperCase() : i === 0 ? 'LEFT' : 'RIGHT'}
          />
        ))}
      </div>
      <Confetti t={revealed ? revealT : 0} cx={winX} />

      {/* Countdown */}
      {thinking ? (
        <div style={{position: 'absolute', left: W / 2 - 95, top: 1010, width: 190, height: 190, borderRadius: '50%', background: C.gold, border: '8px solid #0B1226', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${1 + 0.25 * Math.max(0, 1 - cdP * 4)})`, boxShadow: '0 10px 0 #0B1226'}}>
          <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 130, color: C.ink, lineHeight: 1}}>{countdown}</div>
        </div>
      ) : null}

      {/* Bälle */}
      <div style={{position: 'absolute', inset: 0, opacity: fadeOut}}>
        {(['a', 'b'] as const).map((s) => {
          const b = ballState(s);
          const size = BALL_R * 2 + 24;
          return (
            <React.Fragment key={s + idx}>
              <div style={{position: 'absolute', left: b.x - 130, top: BALL_Y + BALL_R - 22, width: 260, height: 44, borderRadius: '50%', background: 'rgba(0,0,0,0.28)', transform: `scale(${interpolate(BALL_Y - b.y, [0, 300], [1, 0.5], {extrapolateRight: 'clamp'})})`}} />
              <div style={{position: 'absolute', left: b.x - size / 2, top: b.y - size / 2, width: size, height: size, transform: `rotate(${b.rot}deg) scale(${1 / b.sq}, ${b.sq})`, transformOrigin: '50% 100%'}}>
                <Ball id={`${s}${idx}`} flag={r[s].flag} mood={b.mood} facing={s === 'a' ? 1 : -1} />
              </div>
            </React.Fragment>
          );
        })}
      </div>

      {/* Abspann */}
      {inOutro ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 1640, display: 'flex', flexDirection: 'column', alignItems: 'center', transform: `scale(${spring({frame: Math.round((t - outroStart) * fps), fps, config: {damping: 12}})})`}}>
          <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 44, color: C.paper, textShadow: outline('#0B1226', 4), marginBottom: 18}}>{story.outroSub}</div>
          <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 48, color: C.white, background: '#CC0000', padding: '14px 44px', borderRadius: 40, boxShadow: '0 8px 0 rgba(0,0,0,0.35)'}}>SUBSCRIBE</div>
        </div>
      ) : null}

      {/* Ton */}
      {story.music ? <Audio src={staticFile(story.music)} volume={story.musicVolume ?? 0.08} loop /> : null}
      {story.hook?.audio ? (
        <Sequence from={0}>
          <Audio src={staticFile(story.hook.audio)} />
        </Sequence>
      ) : null}
      {rounds.map((rd, i) => (
        <React.Fragment key={i}>
          {rd.qAudio ? (
            <Sequence from={Math.round(rd.start * fps)}>
              <Audio src={staticFile(rd.qAudio)} />
            </Sequence>
          ) : null}
          {[0, 1, 2].map((k) => (
            <Sequence key={k} from={Math.round((rd.thinkStart + k) * fps)} durationInFrames={Math.round(0.6 * fps)}>
              <Audio src={staticFile('sfx/tick.wav')} volume={0.4} />
            </Sequence>
          ))}
          <Sequence from={Math.round(rd.reveal * fps)} durationInFrames={Math.round(1.5 * fps)}>
            <Audio src={staticFile('sfx/ding.wav')} volume={0.3} />
          </Sequence>
          {rd.aAudio ? (
            <Sequence from={Math.round(rd.aStart * fps)}>
              <Audio src={staticFile(rd.aAudio)} />
            </Sequence>
          ) : null}
        </React.Fragment>
      ))}
    </AbsoluteFill>
  );
};
