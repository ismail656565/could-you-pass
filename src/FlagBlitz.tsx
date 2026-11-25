// Long-Format "Flag Blitz" (story.type "flagblitz", 16:9) – „Guess the Flag in 3 Seconds – Easy to Impossible“.
// Seit 25.11.2026 nach Besitzer-Referenz (Logo-Quiz: ≈9 s pro Bild, großes Bild statt Text, Farbwechsel je Frage,
// sichtbare Schwierigkeitsleiter, Level-Blende). Look = Flag-Duel-Familie (Nachthimmel, Papier, Gold, Inter + DM Serif).
// Zeiten (hook, rounds[].start/thinkStart/reveal/aStart/end, outro) setzt autopilot/atlas_voice.py.
// Flaggen: public/flags/<iso2>.svg (flag-icons, MIT).
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadSerif} from '@remotion/google-fonts/DMSerifDisplay';

const FONT = loadInter('normal', {weights: ['700', '800', '900'], subsets: ['latin', 'latin-ext']}).fontFamily;
const SERIF = loadSerif('normal', {weights: ['400'], subsets: ['latin']}).fontFamily;

const C = {
  paper: '#F4EEDF',
  ink: '#18213A',
  gold: '#E9B44C',
  green: '#2E8B57',
  red: '#C8312E',
  white: '#FFFFFF',
};
// Hintergrund wechselt jede Frage (gedeckte, satte Töne – kein Neon)
const BG = [
  ['#14213D', '#24386B'],
  ['#0F4C5C', '#16728A'],
  ['#4A1942', '#7A2E6E'],
  ['#1E5631', '#2F7D4F'],
  ['#6B1D1D', '#9C2F2F'],
  ['#3A2A6B', '#5741A0'],
];
const LEVEL_COLORS: Record<string, string> = {EASY: '#3DA56A', MEDIUM: '#E9B44C', HARD: '#E07A2E', IMPOSSIBLE: '#C8312E'};

export type BlitzRound = {
  level: string;
  flag: string;
  name: string;
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
export type FlagBlitzStory = {
  id: string;
  type: 'flagblitz';
  format?: 'long';
  title: string;
  hookLine: string;
  hook: {audio?: string; start: number; end: number};
  rounds: BlitzRound[];
  outro?: {start: number; audio?: string};
  outroLine?: string;
  music?: string;
  musicVolume?: number;
  durationInSeconds: number;
  thumbTexts?: string[];
};

const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const rnd = (i: number) => {
  const x = Math.sin(i * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
};

const Rays: React.FC<{c: string[]; spin: number}> = ({c, spin}) => (
  <AbsoluteFill style={{background: `radial-gradient(circle at 50% 48%, ${c[1]} 0%, ${c[0]} 70%)`}}>
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0, opacity: 0.13}}>
      <g transform={`translate(960 520) rotate(${spin})`}>
        {Array.from({length: 18}).map((_, i) => (
          <path key={i} d="M0 0 L -90 -1400 L 90 -1400 Z" fill="#fff" transform={`rotate(${i * 20})`} />
        ))}
      </g>
    </svg>
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
      {Array.from({length: 40}).map((_, i) => (
        <circle key={i} cx={rnd(i) * 1920} cy={rnd(i + 50) * 1080} r={1 + rnd(i + 99) * 2.4} fill="#fff" opacity={0.1 + rnd(i + 7) * 0.2} />
      ))}
    </svg>
  </AbsoluteFill>
);

const outline = (c: string, w: number) => {
  const s: string[] = [];
  for (let a = 0; a < 16; a++) s.push(`${(Math.cos((a / 16) * Math.PI * 2) * w).toFixed(1)}px ${(Math.sin((a / 16) * Math.PI * 2) * w).toFixed(1)}px 0 ${c}`);
  return s.join(',');
};

const Title: React.FC = () => (
  <div style={{position: 'absolute', left: 0, right: 0, top: 34, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 64, color: C.white, letterSpacing: 1, textShadow: outline(C.ink, 5) + ', 0 8px 0 rgba(0,0,0,0.25)'}}>
    GUESS THE <span style={{color: C.gold}}>FLAG</span>
  </div>
);

/** Schwierigkeitsleiter links */
const Ladder: React.FC<{levels: string[]; cur: number; index: number; total: number}> = ({levels, cur, index, total}) => (
  <div style={{position: 'absolute', left: 48, top: 230, width: 290}}>
    <div style={{fontFamily: SERIF, fontSize: 70, color: C.white, lineHeight: 1, textShadow: '0 5px 0 rgba(0,0,0,0.3)'}}>
      #{index + 1}
      <span style={{fontFamily: FONT, fontWeight: 800, fontSize: 30, opacity: 0.6}}> / {total}</span>
    </div>
    <div style={{marginTop: 26, display: 'flex', flexDirection: 'column', gap: 14}}>
      {levels.map((lv, i) => {
        const on = i === cur;
        const done = i < cur;
        return (
          <div key={lv} style={{display: 'flex', alignItems: 'center', gap: 14, opacity: on ? 1 : done ? 0.55 : 0.35}}>
            <div style={{width: on ? 30 : 20, height: on ? 30 : 20, borderRadius: '50%', background: LEVEL_COLORS[lv] ?? C.gold, border: `4px solid ${C.white}`}} />
            <div style={{fontFamily: FONT, fontWeight: 900, fontSize: on ? 40 : 30, color: C.white, letterSpacing: 1, textDecoration: done ? 'line-through' : 'none'}}>{lv}</div>
          </div>
        );
      })}
    </div>
  </div>
);

const ScoreNote: React.FC<{total: number}> = ({total}) => (
  <div style={{position: 'absolute', right: 56, top: 250, width: 270, padding: '20px 22px', background: C.paper, borderRadius: 14, transform: 'rotate(3deg)', boxShadow: '0 10px 0 rgba(0,0,0,0.25)', textAlign: 'center'}}>
    <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 28, color: C.ink}}>Keep score</div>
    <div style={{fontFamily: SERIF, fontSize: 58, color: C.red, lineHeight: 1.1}}>?/{total}</div>
    <div style={{fontFamily: FONT, fontWeight: 700, fontSize: 22, color: C.ink, opacity: 0.7}}>comment it at the end</div>
  </div>
);

export const BlitzScene: React.FC<{r: BlitzRound; index: number; story: FlagBlitzStory; levels: string[]}> = ({r, index, story, levels}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = r.start + frame / fps;
  const total = story.rounds.length;
  const cur = levels.indexOf(r.level);
  const newLevel = index === 0 || story.rounds[index - 1].level !== r.level;
  const pop = spring({frame, fps, config: {damping: 12, stiffness: 160}});
  const revealed = t >= r.reveal;
  const rv = t - r.reveal;
  const think = interpolate(t, [r.thinkStart, r.reveal], [1, 0], clamp);
  const counting = t >= r.thinkStart && t < r.reveal;
  const left = Math.max(1, Math.ceil(r.reveal - t));
  const ribbon = revealed ? spring({frame: Math.round(rv * fps), fps, config: {damping: 11, stiffness: 180}}) : 0;
  const shake = counting && left <= 1 ? Math.sin(frame * 1.7) * 3 : 0;
  const bg = BG[index % BG.length];
  const lvlColor = LEVEL_COLORS[r.level] ?? C.gold;
  // Level-Blende am Anfang eines neuen Levels (über der Frage, 1,1 s)
  const card = newLevel ? interpolate(frame, [0, 4, Math.round(fps * 0.9), Math.round(fps * 1.15)], [1, 1, 1, 0], clamp) : 0;
  const cardX = newLevel ? interpolate(frame, [Math.round(fps * 0.9), Math.round(fps * 1.15)], [0, -1920], clamp) : 0;
  const FW = 720;
  const FH = 540;

  return (
    <AbsoluteFill>
      <Rays c={bg} spin={frame * 0.15} />
      <Title />
      <Ladder levels={levels} cur={cur} index={index} total={total} />
      <ScoreNote total={total} />

      {/* Flagge im Papier-Rahmen */}
      <div style={{position: 'absolute', left: 960 - FW / 2 - 22, top: 160, width: FW + 44, height: FH + 44, background: C.paper, borderRadius: 22, boxShadow: '0 16px 0 rgba(0,0,0,0.28)', transform: `scale(${0.6 + 0.4 * pop}) rotate(${(1 - pop) * -6 + shake * 0.3}deg)`, opacity: pop}}>
        <Img src={staticFile(`flags/${r.flag}.svg`)} style={{position: 'absolute', left: 22, top: 22, width: FW, height: FH, objectFit: 'cover', borderRadius: 6, border: '3px solid rgba(0,0,0,0.25)'}} />
        {revealed ? (
          <div style={{position: 'absolute', right: -40, top: -40, width: 110, height: 110, borderRadius: '50%', background: C.green, border: `7px solid ${C.white}`, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${ribbon})`}}>
            <svg width={60} height={60} viewBox="0 0 60 60"><path d="M10 32 L25 46 L51 14" stroke="#fff" strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </div>
        ) : null}
      </div>

      {/* Timer-Balken oder Name */}
      <div style={{position: 'absolute', left: 960 - 380, top: 790, width: 760, height: 150, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        {!revealed ? (
          <div style={{position: 'relative', width: 760, height: 64, borderRadius: 32, background: 'rgba(0,0,0,0.35)', border: `5px solid ${C.white}`, overflow: 'hidden'}}>
            <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${(counting ? think : 1) * 100}%`, background: left <= 1 && counting ? C.red : C.gold, transition: 'none'}} />
            <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 42, color: C.white, textShadow: outline(C.ink, 3)}}>
              {counting ? `${left}` : '3'}
            </div>
          </div>
        ) : (
          <div style={{background: C.paper, borderRadius: 16, padding: '10px 48px', boxShadow: `0 10px 0 ${C.green}`, transform: `scale(${ribbon}) rotate(-2deg)`, fontFamily: SERIF, fontSize: r.name.length > 16 ? 66 : 84, color: C.ink, whiteSpace: 'nowrap'}}>
            {r.name}
          </div>
        )}
      </div>

      {/* Level-Blende */}
      {card > 0 ? (
        <AbsoluteFill style={{transform: `translateX(${cardX}px)`, background: `linear-gradient(135deg, ${lvlColor} 0%, ${bg[0]} 100%)`, alignItems: 'center', justifyContent: 'center'}}>
          <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 58, color: C.white, opacity: 0.85}}>Level {cur + 1}</div>
          <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 200, color: C.white, lineHeight: 1, textShadow: outline(C.ink, 8), transform: `scale(${0.8 + 0.2 * spring({frame, fps, config: {damping: 10}})})`}}>{r.level}</div>
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};

const Intro: React.FC<{story: FlagBlitzStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const flags = story.rounds.slice(0, 24).map((r) => r.flag);
  const s = spring({frame, fps, config: {damping: 12}});
  const sub = spring({frame: frame - Math.round(fps * 2.2), fps, config: {damping: 10}});
  return (
    <AbsoluteFill>
      <Rays c={BG[0]} spin={frame * 0.3} />
      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0, opacity: 0.35}}>
        {flags.map((f, i) => (
          <image key={i} href={staticFile(`flags/${f}.svg`)} x={(i % 8) * 250 - 40 + ((frame * 1.2) % 250)} y={Math.floor(i / 8) * 380 - 60} width={200} height={150} preserveAspectRatio="none" />
        ))}
      </svg>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', transform: `scale(${0.7 + 0.3 * s})`, opacity: s}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 130, color: C.white, lineHeight: 1, textShadow: outline(C.ink, 7)}}>
          GUESS THE <span style={{color: C.gold}}>FLAG</span>
        </div>
        <div style={{marginTop: 22, fontFamily: SERIF, fontSize: 92, color: C.white, textShadow: outline(C.ink, 5)}}>in 3 seconds</div>
        <div style={{marginTop: 34, display: 'flex', gap: 18}}>
          {Object.entries(LEVEL_COLORS).map(([lv, c]) => (
            <div key={lv} style={{background: c, color: C.white, fontFamily: FONT, fontWeight: 900, fontSize: 38, padding: '8px 24px', borderRadius: 12, border: `4px solid ${C.white}`}}>{lv}</div>
          ))}
        </div>
      </AbsoluteFill>
      {sub > 0.01 ? (
        <div style={{position: 'absolute', right: 70, bottom: 60, transform: `scale(${sub}) rotate(-4deg)`, background: '#CC0000', color: C.white, fontFamily: FONT, fontWeight: 900, fontSize: 46, padding: '14px 34px', borderRadius: 14, boxShadow: '0 8px 0 rgba(0,0,0,0.3)'}}>SUBSCRIBE</div>
      ) : null}
    </AbsoluteFill>
  );
};

const Outro: React.FC<{story: FlagBlitzStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 12}});
  return (
    <AbsoluteFill>
      <Rays c={BG[2]} spin={frame * 0.2} />
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', transform: `scale(${0.8 + 0.2 * s})`, opacity: s}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 96, color: C.white, textShadow: outline(C.ink, 6)}}>How many did you get?</div>
        <div style={{marginTop: 30, background: C.paper, borderRadius: 26, padding: '6px 70px', fontFamily: SERIF, fontSize: 200, color: C.red, boxShadow: '0 14px 0 rgba(0,0,0,0.3)', transform: 'rotate(-3deg)'}}>?/{story.rounds.length}</div>
        <div style={{marginTop: 46, fontFamily: FONT, fontWeight: 800, fontSize: 48, color: C.white}}>Comment your score – new flag quiz every day</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const FlagBlitz: React.FC<FlagBlitzStory> = (story) => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const levels = [...new Set(story.rounds.map((r) => r.level))];
  const outroStart = story.outro?.start ?? story.durationInSeconds;
  return (
    <AbsoluteFill style={{backgroundColor: BG[0][0]}}>
      {story.hook.end > 0.05 ? (
        <Sequence from={0} durationInFrames={Math.max(1, f(story.hook.end))} name="Intro">
          <Intro story={story} />
        </Sequence>
      ) : null}
      {story.rounds.map((r, i) => (
        <Sequence key={i} from={f(r.start)} durationInFrames={Math.max(1, f(r.end) - f(r.start))} name={`Flagge ${i + 1}`}>
          <BlitzScene r={r} index={i} story={story} levels={levels} />
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
          <Sequence from={f(r.reveal - r.start)} durationInFrames={f(1.2)} layout="none">
            <Audio src={staticFile('sfx/ding.wav')} volume={0.45} />
          </Sequence>
        </Sequence>
      ))}
      {story.durationInSeconds - outroStart > 0.3 ? (
        <Sequence from={f(outroStart)} name="Outro">
          <Outro story={story} />
          {story.outro?.audio ? <Audio src={staticFile(story.outro.audio)} /> : null}
        </Sequence>
      ) : null}
      {story.hook.audio ? <Audio src={staticFile(story.hook.audio)} /> : null}
      {story.music ? <Audio src={staticFile(story.music)} volume={story.musicVolume ?? 0.07} loop /> : null}
    </AbsoluteFill>
  );
};

/** Vorschaubild 1280x720: Flaggen-Collage + „GUESS THE FLAG IN 3 SECONDS“ + Hürde */
export const FlagBlitzThumb: React.FC<FlagBlitzStory & {variant?: string}> = (story) => {
  const t = story.thumbTexts ?? ['GUESS THE **FLAG**', 'IN **3** SECONDS', 'EASY → IMPOSSIBLE'];
  const pick = story.rounds.filter((r) => r.level === 'IMPOSSIBLE' || r.level === 'HARD').slice(0, 4).map((r) => r.flag);
  const md = (s: string) => s.split(/(\*\*[^*]+\*\*)/).map((p, i) => (p.startsWith('**') ? <span key={i} style={{color: C.gold}}>{p.slice(2, -2)}</span> : <span key={i}>{p}</span>));
  return (
    <AbsoluteFill style={{background: `radial-gradient(circle at 70% 50%, ${BG[0][1]} 0%, ${BG[0][0]} 75%)`}}>
      {pick.map((f, i) => (
        <div key={f} style={{position: 'absolute', left: 700 + (i % 2) * 280, top: 70 + Math.floor(i / 2) * 300, width: 250, height: 188, background: C.paper, padding: 10, borderRadius: 12, transform: `rotate(${i % 2 ? 6 : -5}deg)`, boxShadow: '0 10px 0 rgba(0,0,0,0.3)'}}>
          <Img src={staticFile(`flags/${f}.svg`)} style={{width: 230, height: 168, objectFit: 'cover'}} />
        </div>
      ))}
      <div style={{position: 'absolute', left: 50, top: t[1] ? 70 : 150, width: 680, fontFamily: FONT, fontWeight: 900, fontSize: t[1] ? 108 : 140, lineHeight: 1.02, color: C.white, textShadow: outline(C.ink, 6)}}>
        <div>{md(t[0])}</div>
        {t[1] ? <div>{md(t[1])}</div> : null}
      </div>
      <div style={{position: 'absolute', left: 54, top: 520, background: C.red, color: C.white, fontFamily: FONT, fontWeight: 900, fontSize: 52, padding: '10px 26px', borderRadius: 14, transform: 'rotate(-3deg)', border: `5px solid ${C.white}`}}>{t[2]}</div>
    </AbsoluteFill>
  );
};
