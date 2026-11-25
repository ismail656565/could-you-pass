// Short-Format "Mom or Dad?" (story.type "momdad", 1080x1920) – Besitzer-Referenz „Who Is Most Likely To – Parents Edition“.
// Keine richtige Antwort: Mitmach-/Kommentar-Spiel. Gezeichnete 2D-Figuren (Mama links, Papa rechts) im Wohnzimmer,
// Fragekarte mit Emoji-Aufkleber, 3-s-Balkentimer; bei der Auflösung zeigen beide aufeinander und „COMMENT“ springt auf.
// Zeiten (hook, rounds[].start/thinkStart/reveal/aStart/end) setzt autopilot/atlas_voice.py.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadSerif} from '@remotion/google-fonts/DMSerifDisplay';

const FONT = loadInter('normal', {weights: ['700', '800', '900'], subsets: ['latin']}).fontFamily;
const SERIF = loadSerif('normal', {weights: ['400'], subsets: ['latin']}).fontFamily;
const EMOJI = '"Noto Color Emoji", "Apple Color Emoji", sans-serif';

const C = {
  wall: '#F3D9B1',
  wall2: '#EBC891',
  floor: '#9A6A43',
  floor2: '#875A36',
  sofa: '#3E6B8C',
  sofa2: '#335A76',
  paper: '#FFF8EC',
  ink: '#1D2333',
  gold: '#E9B44C',
  red: '#C8312E',
  mom: '#E8508A',
  momDark: '#B8336A',
  dad: '#2F6FD6',
  dadDark: '#1F4FA0',
  skin: '#F2C29B',
  skin2: '#C98B62',
  white: '#FFFFFF',
};

export type MomDadRound = {
  q: string;
  emoji: string;
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
export type MomDadStory = {
  id: string;
  type: 'momdad';
  title: string;
  episode?: number;
  hookLine: string;
  hook: {audio?: string; start: number; end: number};
  rounds: MomDadRound[];
  music?: string;
  musicVolume?: number;
  durationInSeconds: number;
};

const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const outline = (c: string, w: number) => {
  const s: string[] = [];
  for (let a = 0; a < 16; a++) s.push(`${(Math.cos((a / 16) * Math.PI * 2) * w).toFixed(1)}px ${(Math.sin((a / 16) * Math.PI * 2) * w).toFixed(1)}px 0 ${c}`);
  return s.join(',');
};

const Room: React.FC = () => (
  <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
    <rect width={1080} height={1920} fill={C.wall} />
    {Array.from({length: 12}).map((_, i) => (
      <rect key={i} x={i * 96} y={0} width={48} height={1340} fill={C.wall2} opacity={0.35} />
    ))}
    {/* Boden */}
    <rect x={0} y={1340} width={1080} height={580} fill={C.floor} />
    {Array.from({length: 7}).map((_, i) => (
      <line key={i} x1={0} x2={1080} y1={1380 + i * 80} y2={1380 + i * 80} stroke={C.floor2} strokeWidth={6} />
    ))}
    {/* Sofa hinter den Figuren */}
    <rect x={60} y={1080} width={960} height={230} rx={50} fill={C.sofa} />
    <rect x={30} y={1180} width={1020} height={190} rx={40} fill={C.sofa2} />
    <rect x={20} y={1120} width={110} height={260} rx={40} fill={C.sofa} />
    <rect x={950} y={1120} width={110} height={260} rx={40} fill={C.sofa} />
  </svg>
);

type Pose = 'idle' | 'think' | 'point';

/** Gezeichnete Figur (flach, Kontur) – who: mom | dad; pointDir: Richtung, in die bei 'point' gezeigt wird */
const Person: React.FC<{who: 'mom' | 'dad'; pose: Pose; t: number; x: number}> = ({who, pose, t, x}) => {
  const mom = who === 'mom';
  const shirt = mom ? C.mom : C.dad;
  const shirtD = mom ? C.momDark : C.dadDark;
  const bob = Math.sin(t * (pose === 'think' ? 9 : 3) + (mom ? 0 : 1.3)) * (pose === 'think' ? 6 : 3);
  const toward = mom ? 1 : -1; // zeigt zur anderen Person
  const armA = pose === 'point' ? -12 * toward : pose === 'think' ? -120 * toward : 80 * toward;
  const eyeDX = pose === 'point' ? 9 * toward : pose === 'think' ? Math.sin(t * 4) * 6 : 0;
  return (
    <svg width={420} height={620} viewBox="0 0 420 620" style={{position: 'absolute', left: x - 210, top: 820 + bob, overflow: 'visible'}}>
      {/* Beine */}
      <rect x={160} y={470} width={42} height={140} rx={18} fill="#2B2F3A" stroke={C.ink} strokeWidth={6} />
      <rect x={218} y={470} width={42} height={140} rx={18} fill="#2B2F3A" stroke={C.ink} strokeWidth={6} />
      {/* Körper */}
      <path d="M120 300 Q 210 250 300 300 L 290 490 Q 210 510 130 490 Z" fill={shirt} stroke={C.ink} strokeWidth={8} />
      <path d="M180 290 L210 330 L240 290" fill="none" stroke={shirtD} strokeWidth={8} strokeLinecap="round" />
      {/* Arm, der zeigt / am Kinn denkt */}
      <g transform={`rotate(${armA} ${mom ? 290 : 130} 320)`}>
        <rect x={mom ? 280 : 50} y={305} width={110} height={38} rx={19} fill={shirt} stroke={C.ink} strokeWidth={7} />
        <circle cx={mom ? 395 : 45} cy={324} r={24} fill={C.skin} stroke={C.ink} strokeWidth={6} />
      </g>
      {/* anderer Arm */}
      <rect x={mom ? 92 : 290} y={310} width={38} height={150} rx={19} fill={shirt} stroke={C.ink} strokeWidth={7} />
      {/* Hals + Kopf */}
      <rect x={190} y={240} width={40} height={50} fill={C.skin} stroke={C.ink} strokeWidth={6} />
      {mom ? <path d="M95 175 Q 90 40 210 30 Q 330 40 325 175 Q 330 285 290 300 L 130 300 Q 90 285 95 175 Z" fill="#7A3E1D" stroke={C.ink} strokeWidth={7} /> : null}
      <circle cx={210} cy={165} r={98} fill={C.skin} stroke={C.ink} strokeWidth={8} />
      {mom ? (
        <>
          <path d="M115 150 Q 130 60 210 62 Q 290 60 305 150 Q 260 100 210 108 Q 160 100 115 150 Z" fill="#7A3E1D" stroke={C.ink} strokeWidth={6} />
          <circle cx={210} cy={50} r={36} fill="#7A3E1D" stroke={C.ink} strokeWidth={6} />
        </>
      ) : (
        <>
          <path d="M112 145 Q 120 62 210 60 Q 300 62 308 145 Q 290 105 210 100 Q 130 105 112 145 Z" fill="#3B2A1E" stroke={C.ink} strokeWidth={6} />
          <path d="M150 215 Q 210 262 270 215" fill="#3B2A1E" opacity={0.25} />
          {/* Brille */}
          <circle cx={172} cy={160} r={30} fill="none" stroke={C.ink} strokeWidth={6} />
          <circle cx={248} cy={160} r={30} fill="none" stroke={C.ink} strokeWidth={6} />
          <line x1={202} x2={218} y1={160} y2={160} stroke={C.ink} strokeWidth={6} />
        </>
      )}
      {/* Augen */}
      <circle cx={172 + eyeDX} cy={162} r={10} fill={C.ink} />
      <circle cx={248 + eyeDX} cy={162} r={10} fill={C.ink} />
      {/* Mund */}
      {pose === 'point' ? (
        <path d="M180 212 Q 210 245 240 212 Z" fill="#8A2B2B" stroke={C.ink} strokeWidth={5} />
      ) : pose === 'think' ? (
        <ellipse cx={210} cy={218} rx={16} ry={10} fill="#8A2B2B" stroke={C.ink} strokeWidth={5} />
      ) : (
        <path d="M182 210 Q 210 232 238 210" fill="none" stroke={C.ink} strokeWidth={6} strokeLinecap="round" />
      )}
      {mom ? <circle cx={150} cy={195} r={14} fill={C.mom} opacity={0.35} /> : null}
      {mom ? <circle cx={270} cy={195} r={14} fill={C.mom} opacity={0.35} /> : null}
    </svg>
  );
};

const Button: React.FC<{label: string; color: string; dark: string; x: number; pulse: number}> = ({label, color, dark, x, pulse}) => (
  <div style={{position: 'absolute', left: x - 170, top: 1470, width: 340, height: 150, transform: `scale(${1 + 0.06 * pulse})`}}>
    <div style={{position: 'absolute', left: 0, right: 0, top: 18, bottom: 0, borderRadius: 75, background: dark}} />
    <div style={{position: 'absolute', left: 0, right: 0, top: 0, bottom: 18, borderRadius: 75, background: color, border: `8px solid ${C.white}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 84, color: C.white, letterSpacing: 2, textShadow: outline(dark, 4)}}>{label}</div>
  </div>
);

export const MomDadScene: React.FC<{r: MomDadRound; index: number; story: MomDadStory}> = ({r, index, story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = r.start + frame / fps;
  const total = story.rounds.length;
  const pop = index === 0 ? 1 : spring({frame, fps, config: {damping: 12, stiffness: 170}});
  const counting = t >= r.thinkStart && t < r.reveal;
  const revealed = t >= r.reveal;
  const rv = t - r.reveal;
  const p = interpolate(t, [r.thinkStart, r.reveal], [1, 0], clamp);
  const left = Math.max(1, Math.ceil(r.reveal - t));
  const pose: Pose = revealed ? 'point' : counting ? 'think' : 'idle';
  const cta = revealed ? spring({frame: Math.round(rv * fps), fps, config: {damping: 9, stiffness: 200}}) : 0;
  const pulse = counting ? (Math.sin(t * 10) + 1) / 2 : 0;
  return (
    <AbsoluteFill>
      <Room />
      {/* Kopf */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 70, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 92, color: C.white, textShadow: outline(C.ink, 7)}}>
        <span style={{color: C.mom}}>MOM</span> or <span style={{color: C.dad}}>DAD</span>?
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 190, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 36, color: C.ink, letterSpacing: 4}}>
        WHO IS MOST LIKELY TO… · {index + 1}/{total}
      </div>
      {/* Fragekarte */}
      <div style={{position: 'absolute', left: 70, top: 270, width: 940, minHeight: 290, background: C.paper, borderRadius: 34, boxShadow: '0 14px 0 rgba(60,35,10,0.35)', border: `6px solid ${C.ink}`, padding: '44px 50px 44px 50px', boxSizing: 'border-box', transform: `scale(${0.7 + 0.3 * pop}) rotate(${(1 - pop) * 4 - 1}deg)`, opacity: pop}}>
        <div style={{fontFamily: SERIF, fontSize: r.q.length > 40 ? 70 : 82, lineHeight: 1.08, color: C.ink, width: 650}}>…{r.q}</div>
        <div style={{position: 'absolute', right: 34, top: 50, width: 210, height: 210, borderRadius: '50%', background: '#fff', border: `6px solid ${C.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: 'rotate(8deg)'}}>
          <div style={{fontFamily: EMOJI, fontSize: 130, lineHeight: 1}}>{r.emoji}</div>
        </div>
      </div>
      {/* Timer */}
      <div style={{position: 'absolute', left: 140, top: 680, width: 800, height: 64, borderRadius: 32, background: 'rgba(29,35,51,0.25)', border: `6px solid ${C.ink}`, overflow: 'hidden', opacity: revealed ? 0 : 1}}>
        <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${(counting ? p : 1) * 100}%`, background: counting && left <= 1 ? C.red : C.gold}} />
        <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 40, color: C.white, textShadow: outline(C.ink, 3)}}>{counting ? left : 3}</div>
      </div>
      {revealed ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 650, display: 'flex', justifyContent: 'center'}}>
          <div style={{background: C.red, color: C.white, fontFamily: FONT, fontWeight: 900, fontSize: 58, padding: '12px 40px', borderRadius: 20, border: `6px solid ${C.white}`, transform: `scale(${cta}) rotate(-3deg)`, boxShadow: '0 10px 0 rgba(0,0,0,0.3)'}}>COMMENT YOUR PICK 👇</div>
        </div>
      ) : null}
      <Person who="mom" pose={pose} t={t} x={290} />
      <Person who="dad" pose={pose} t={t} x={790} />
      <Button label="MOM" color={C.mom} dark={C.momDark} x={290} pulse={pulse} />
      <Button label="DAD" color={C.dad} dark={C.dadDark} x={790} pulse={1 - pulse} />
    </AbsoluteFill>
  );
};

export const MomDad: React.FC<MomDadStory> = (story) => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  return (
    <AbsoluteFill style={{backgroundColor: C.wall}}>
      {story.hook.end > 0.05 ? (
        <Sequence from={0} durationInFrames={Math.max(1, f(story.hook.end))} name="Hook">
          <MomDadScene r={{...story.rounds[0], start: 0, thinkStart: 1e9, reveal: 1e9, end: story.hook.end}} index={0} story={story} />
        </Sequence>
      ) : null}
      {story.rounds.map((r, i) => (
        <Sequence key={i} from={f(r.start)} durationInFrames={Math.max(1, f(r.end) - f(r.start))} name={`Frage ${i + 1}`}>
          <MomDadScene r={r} index={i} story={story} />
          {r.qAudio ? <Audio src={staticFile(r.qAudio)} /> : null}
          {r.aAudio ? (
            <Sequence from={f(r.aStart - r.start)} layout="none">
              <Audio src={staticFile(r.aAudio)} />
            </Sequence>
          ) : null}
          {Array.from({length: Math.max(0, Math.floor(r.reveal - r.thinkStart))}).map((_, k) => (
            <Sequence key={k} from={f(r.thinkStart - r.start + k)} durationInFrames={f(0.3)} layout="none">
              <Audio src={staticFile('sfx/tick.wav')} volume={0.45} />
            </Sequence>
          ))}
          <Sequence from={f(r.reveal - r.start)} durationInFrames={f(1)} layout="none">
            <Audio src={staticFile('sfx/blip.wav')} volume={0.5} />
          </Sequence>
        </Sequence>
      ))}
      {story.hook.audio ? <Audio src={staticFile(story.hook.audio)} /> : null}
      {story.music ? <Audio src={staticFile(story.music)} volume={story.musicVolume ?? 0.08} loop /> : null}
    </AbsoluteFill>
  );
};
