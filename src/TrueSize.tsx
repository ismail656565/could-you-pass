// Layout "atlas" – "This map is lying to you": zwei Länder auf der Mercator-Karte, dann wandert das
// polnahe Land zum anderen und schrumpft dabei auf seine echte Größe (Rechnung auf der Kugel, nicht getrickst).
// Bewusst ohne Emoji, Maskottchen und Template-Kästen: gedruckter Atlas, zwei Druckfarben, eine Kamera.
import React, {useMemo} from 'react';
import {AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont as loadSerif} from '@remotion/google-fonts/Fraunces';
import {loadFont as loadSans} from '@remotion/google-fonts/BarlowCondensed';
import raw from './data/truesize.json';

const serif = loadSerif('normal', {weights: ['600', '900'], subsets: ['latin']}).fontFamily;
const serifItalic = loadSerif('italic', {weights: ['900'], subsets: ['latin']}).fontFamily;
const sans = loadSans('normal', {weights: ['500', '600', '700'], subsets: ['latin']}).fontFamily;

type LL = [number, number];
type Shape = {rings: LL[][]; centroid: LL};
const DATA = raw as unknown as {shapes: Record<string, Shape>; world: LL[][]};

export type TrueSizeSide = {shape: string; name: string; km2: number};
export type TrueSizeRound = {
  level: string;
  a: TrueSizeSide;
  b: TrueSizeSide;
  /** Welche Seite wandert (die polnahe) */
  mover: 'a' | 'b';
  winner: 'a' | 'b';
  /** z. B. "3.5× bigger" */
  verdict: string;
  start: number;
  thinkStart: number;
  reveal: number;
  moveEnd: number;
  aStart: number;
  end: number;
  qAudio?: string;
  aAudio?: string;
};
export type TrueSizeStory = {
  id: string;
  type: 'truesize';
  title: string;
  kicker: string;
  hookText: string[];
  question: string;
  hook: {audio?: string; start: number; end: number};
  rounds: TrueSizeRound[];
  music?: string;
  musicVolume?: number;
  outroText: string;
  outroSub: string;
  durationInSeconds: number;
  brand?: string;
};

const C = {
  paper: '#F1EADB',
  land: '#DDD2BA',
  coast: '#BFB196',
  grid: '#DDD3BE',
  ink: '#1E1A15',
  soft: '#7B7163',
  a: '#E2532F',
  b: '#1F4E79',
};
const W = 1080;
const H = 1920;
// Fenster, in dem die Karte "spielt" (darüber Frage, darunter Namenskarten; frei von der Shorts-Bedienleiste)
const MAP = {cx: 540, cy: 945, w: 880, h: 790};

const D2R = Math.PI / 180;
const mercY = (lat: number) => {
  const l = Math.max(-84.5, Math.min(84.5, lat)) * D2R;
  return (-Math.log(Math.tan(Math.PI / 4 + l / 2)) * 180) / Math.PI;
};
const wrap = (d: number) => ((((d + 180) % 360) + 360) % 360) - 180;

type XY = [number, number];
/** Ringe in Mercator-Grad; Längen relativ zu refLon entfaltet (kein Riss am 180. Längengrad) */
const projectRings = (rings: LL[][], refLon: number): XY[][] => rings.map((r) => r.map(([lon, lat]) => [refLon + wrap(lon - refLon), mercY(lat)] as XY));

/** Verschiebt eine Form auf der Kugel: Schwerpunkt c0 -> c1, Norden bleibt oben. Flächen bleiben echt. */
const moveRings = (rings: LL[][], c0: LL, c1: LL): XY[][] => {
  const d = (c1[1] - c0[1]) * D2R;
  const cd = Math.cos(d);
  const sd = Math.sin(d);
  return rings.map((r) =>
    r.map(([lon, lat]) => {
      const lam = (lon - c0[0]) * D2R;
      const phi = lat * D2R;
      const x = Math.cos(phi) * Math.cos(lam);
      const y = Math.cos(phi) * Math.sin(lam);
      const z = Math.sin(phi);
      const x2 = x * cd - z * sd;
      const z2 = x * sd + z * cd;
      const lat2 = Math.asin(Math.max(-1, Math.min(1, z2))) / D2R;
      const lon2 = Math.atan2(y, x2) / D2R;
      return [c1[0] + lon2, mercY(lat2)] as XY;
    }),
  );
};

const pathOf = (rings: XY[][]) => rings.map((r) => 'M' + r.map(([x, y]) => `${x.toFixed(2)} ${y.toFixed(2)}`).join('L') + 'Z').join('');

type Box = {x0: number; y0: number; x1: number; y1: number};
const boxOf = (...sets: XY[][][]): Box => {
  const b = {x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity};
  for (const rings of sets) for (const r of rings) for (const [x, y] of r) {
    if (x < b.x0) b.x0 = x;
    if (x > b.x1) b.x1 = x;
    if (y < b.y0) b.y0 = y;
    if (y > b.y1) b.y1 = y;
  }
  return b;
};
type View = {x: number; y: number; s: number};
const fit = (b: Box, pad = 1): View => ({
  x: (b.x0 + b.x1) / 2,
  y: (b.y0 + b.y1) / 2,
  s: Math.min(MAP.w / (b.x1 - b.x0), MAP.h / (b.y1 - b.y0)) * pad,
});
const mix = (a: View, b: View, t: number): View => ({x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t, s: a.s * Math.pow(b.s / a.s, t)});
const tf = (v: View) => `translate(${MAP.cx - v.x * v.s} ${MAP.cy - v.y * v.s}) scale(${v.s})`;
const toScreen = (v: View, p: XY): XY => [MAP.cx + (p[0] - v.x) * v.s, MAP.cy + (p[1] - v.y) * v.s];

const ease = Easing.inOut(Easing.cubic);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const lerpLL = (a: LL, b: LL, t: number): LL => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];

const fmtKm2 = (v: number) => (v >= 1e6 ? `${(v / 1e6).toFixed(2)} million km²` : `${Math.round(v).toLocaleString('en-US')} km²`);

/** Alles Geometrische einer Runde, einmal vorberechnet */
const useRound = (r: TrueSizeRound) =>
  useMemo(() => {
    const mover = r[r.mover];
    const target = r[r.mover === 'a' ? 'b' : 'a'];
    const ms = DATA.shapes[mover.shape];
    const ts = DATA.shapes[target.shape];
    const targetXY = projectRings(ts.rings, ts.centroid[0]);
    const moverStart = moveRings(ms.rings, ms.centroid, ms.centroid);
    const moverEnd = moveRings(ms.rings, ms.centroid, ts.centroid);
    const viewA = fit(boxOf(targetXY, moverStart), 0.94);
    const viewB = fit(boxOf(targetXY, moverEnd), 0.8);
    return {mover, target, ms, ts, targetXY, targetPath: pathOf(targetXY), viewA, viewB};
  }, [r]);

// jeder Ring relativ zu seinem ersten Punkt entfaltet (sonst Querstreifen am 180. Längengrad)
const WORLD_PATH = pathOf(DATA.world.flatMap((r) => projectRings([r], r[0][0])));
const HOOK_VIEW: View = {x: 12, y: -70, s: 2.95};

const Graticule: React.FC = () => {
  const lines: React.ReactNode[] = [];
  for (let lon = -540; lon <= 540; lon += 30) lines.push(<line key={'m' + lon} x1={lon} x2={lon} y1={mercY(84.5)} y2={mercY(-84.5)} />);
  for (let lat = -60; lat <= 60; lat += 30) if (lat !== 0) lines.push(<line key={'p' + lat} x1={-540} x2={540} y1={mercY(lat)} y2={mercY(lat)} />);
  return (
    <g stroke={C.grid} strokeWidth={1.5} vectorEffect="non-scaling-stroke" fill="none">
      {lines.map((l) => React.cloneElement(l as React.ReactElement, {vectorEffect: 'non-scaling-stroke'}))}
      <line x1={-540} x2={540} y1={0} y2={0} stroke={C.coast} strokeWidth={2.5} strokeDasharray="10 9" vectorEffect="non-scaling-stroke" />
    </g>
  );
};

const World: React.FC<{view: View}> = ({view}) => (
  <g transform={tf(view)}>
    <Graticule />
    {[-360, 0, 360].map((dx) => (
      <path key={dx} d={WORLD_PATH} transform={`translate(${dx} 0)`} fill={C.land} stroke={C.coast} strokeWidth={1.4} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
    ))}
  </g>
);

const MapLabel: React.FC<{x: number; y: number; text: string; color: string; opacity: number}> = ({x, y, text, color, opacity}) => (
  <text x={x} y={y} textAnchor="middle" fontFamily={sans} fontWeight={700} fontSize={40} letterSpacing={3} fill={color} stroke={C.paper} strokeWidth={10} strokeLinejoin="round" paintOrder="stroke" opacity={opacity}>
    {text.toUpperCase()}
  </text>
);

const RoundMap: React.FC<{r: TrueSizeRound; prev: View; isLast: boolean}> = ({r, prev, isLast}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps + r.start;
  const g = useRound(r);
  const move = ease(interpolate(t, [r.reveal, r.moveEnd], [0, 1], clamp));
  const arrive = ease(interpolate(t, [r.start, r.start + 0.7], [0, 1], clamp));
  const drift = interpolate(t, [r.moveEnd, r.end], [1, 1.05], clamp);
  let view = mix(mix(prev, g.viewA, arrive), g.viewB, move);
  view = {...view, s: view.s * drift};

  const c = lerpLL(g.ms.centroid, g.ts.centroid, move);
  const moverXY = moveRings(g.ms.rings, g.ms.centroid, c);
  const lift = Math.sin(Math.PI * move);
  const fadeIn = interpolate(t, [r.start + 0.15, r.start + 0.55], [0, 1], clamp);
  const fadeOut = isLast ? 1 : interpolate(t, [r.end - 0.22, r.end], [1, 0], clamp);
  const show = fadeIn * fadeOut;
  const moverColor = r.mover === 'a' ? C.a : C.b;
  const targetColor = r.mover === 'a' ? C.b : C.a;
  const labels = interpolate(t, [r.reveal - 0.1, r.reveal + 0.3], [1, 0], clamp) * show;

  const mb = boxOf(moverXY);
  const tb = boxOf(g.targetXY);
  const mTop = toScreen(view, [(mb.x0 + mb.x1) / 2, mb.y0]);
  const tBot = toScreen(view, [(tb.x0 + tb.x1) / 2, tb.y1]);
  // Atmen während der Bedenkzeit, damit nie ein Standbild steht
  const breathe = 1 + 0.012 * Math.sin((t - r.start) * 4.2) * (1 - move);
  const mc = toScreen(view, [c[0], mercY(c[1])]);

  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
      <World view={view} />
      <g opacity={show}>
        <g transform={tf(view)}>
          <path d={g.targetPath} fill={targetColor} stroke={targetColor} strokeWidth={2} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
        </g>
        <g transform={`translate(${mc[0]} ${mc[1]}) scale(${breathe}) translate(${-mc[0]} ${-mc[1]})`}>
          <g transform={`translate(${10 * lift} ${22 * lift})`} opacity={0.22 * lift}>
            <g transform={tf(view)}>
              <path d={pathOf(moverXY)} fill="#000" />
            </g>
          </g>
          <g transform={`translate(0 ${-10 * lift})`} opacity={interpolate(move, [0.6, 1], [1, 0.86], clamp)}>
            <g transform={tf(view)}>
              <path d={pathOf(moverXY)} fill={moverColor} stroke={moverColor} strokeWidth={2} strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
            </g>
          </g>
        </g>
        <MapLabel x={Math.max(170, Math.min(910, mTop[0]))} y={Math.max(545, mTop[1] - 22)} text={g.mover.name} color={moverColor} opacity={labels} />
        <MapLabel x={Math.max(170, Math.min(910, tBot[0]))} y={Math.min(1345, tBot[1] + 54)} text={g.target.name} color={targetColor} opacity={labels} />
      </g>
    </svg>
  );
};

const HookMap: React.FC<{story: TrueSizeStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const view = {...HOOK_VIEW, s: HOOK_VIEW.s * interpolate(t, [0, story.hook.end], [1, 1.07])};
  const gl = DATA.shapes.greenland;
  const af = DATA.shapes.africa;
  const glPath = useMemo(() => pathOf(projectRings(gl.rings, gl.centroid[0])), [gl]);
  const afPath = useMemo(() => pathOf(projectRings(af.rings, af.centroid[0])), [af]);
  const gc = toScreen(view, [gl.centroid[0], mercY(gl.centroid[1])]);
  // Grönland "löst sich" wie ein lockerer Aufkleber
  const wob = Math.sin(t * 7) * 2.6 * interpolate(t, [0.2, 0.7], [0, 1], clamp);
  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
      <World view={view} />
      <g transform={tf(view)}>
        <path d={afPath} fill={C.b} />
      </g>
      <g transform={`rotate(${wob} ${gc[0]} ${gc[1]})`}>
        <g transform={`translate(8 14)`} opacity={0.2}>
          <g transform={tf(view)}>
            <path d={glPath} fill="#000" />
          </g>
        </g>
        <g transform={tf(view)}>
          <path d={glPath} fill={C.a} />
        </g>
      </g>
    </svg>
  );
};

const Kicker: React.FC<{story: TrueSizeStory; right?: string}> = ({story, right}) => (
  <div style={{position: 'absolute', left: 64, right: 64, top: 176, display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontFamily: sans, fontWeight: 600, fontSize: 34, letterSpacing: 5, color: C.soft}}>
    <span>
      {(story.brand ?? 'COULD YOU PASS?').toUpperCase()} <span style={{color: C.coast}}>/</span> {story.kicker}
    </span>
    <span style={{color: C.ink}}>{right}</span>
  </div>
);

const Headline: React.FC<{children: React.ReactNode; size?: number; opacity?: number; y?: number}> = ({children, size = 92, opacity = 1, y = 0}) => (
  <div style={{position: 'absolute', left: 64, right: 64, top: 236, fontFamily: serif, fontWeight: 900, fontSize: size, lineHeight: 1.0, letterSpacing: -2, color: C.ink, opacity, transform: `translateY(${y}px)`}}>{children}</div>
);

const Card: React.FC<{side: TrueSizeSide; color: string; state: 'open' | 'win' | 'lose'; grow: number; count: number}> = ({side, color, state, grow, count}) => {
  const win = state === 'win';
  const bg = win ? color : C.paper;
  return (
    <div
      style={{
        flex: 1,
        height: 168,
        borderRadius: 10,
        border: `4px solid ${state === 'lose' ? C.coast : color}`,
        background: bg,
        padding: '18px 24px',
        boxSizing: 'border-box',
        opacity: state === 'lose' ? 0.62 : 1,
        transform: `scale(${1 + 0.05 * grow})`,
        boxShadow: win ? `0 ${10 * grow}px ${26 * grow}px rgba(30,26,21,0.22)` : 'none',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
      }}
    >
      <div style={{fontFamily: sans, fontWeight: 700, fontSize: 60, lineHeight: 1, letterSpacing: 1.5, color: win ? C.paper : state === 'lose' ? C.soft : color, whiteSpace: 'nowrap'}}>{side.name.toUpperCase()}</div>
      <div style={{fontFamily: sans, fontWeight: 500, fontSize: 37, marginTop: 10, color: win ? C.paper : C.soft, whiteSpace: 'nowrap', fontVariantNumeric: 'tabular-nums'}}>{state === 'open' ? 'km² ?' : fmtKm2(side.km2 * count)}</div>
    </div>
  );
};

const RoundUI: React.FC<{r: TrueSizeRound; index: number; total: number; story: TrueSizeStory; isLast: boolean}> = ({r, index, total, story, isLast}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps + r.start;
  const revealed = t >= r.aStart;
  const pop = interpolate(t, [r.aStart, r.aStart + 0.35], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.6))});
  const count = interpolate(t, [r.aStart, r.aStart + 0.7], [0.6, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const think = interpolate(t, [r.thinkStart, r.reveal], [1, 0], clamp);
  const thinking = t >= r.thinkStart - 0.2 && t < r.reveal + 0.15;
  const winner = r[r.winner];
  const loser = r[r.winner === 'a' ? 'b' : 'a'];
  const wColor = r.winner === 'a' ? C.a : C.b;
  const outroAt = r.end - 2.0;
  const outro = isLast ? interpolate(t, [outroAt, outroAt + 0.35], [0, 1], clamp) : 0;
  const qIn = interpolate(t, [r.start, r.start + 0.3], [0, 1], clamp);
  const [q1, q2] = story.question.split(/really /i);

  return (
    <AbsoluteFill>
      <Kicker story={story} right={`${index + 1}/${total}  ${r.level}`} />
      {!revealed ? (
        <Headline opacity={index === 0 ? 1 : qIn}>
          {q1}
          <span style={{fontFamily: serifItalic, fontStyle: 'italic', color: C.a}}>really</span> {q2}
        </Headline>
      ) : (
        <div style={{opacity: 1 - outro}}>
          <Headline size={winner.name.length > 9 ? 108 : 124} y={(1 - pop) * 26} opacity={Math.min(1, pop * 1.4)}>
            <span style={{color: wColor}}>{winner.name}.</span>
          </Headline>
          <div style={{position: 'absolute', left: 68, top: 376, fontFamily: sans, fontWeight: 600, fontSize: 46, letterSpacing: 1, color: C.ink, opacity: interpolate(t, [r.aStart + 0.25, r.aStart + 0.55], [0, 1], clamp)}}>
            {r.verdict} than {loser.name}
          </div>
        </div>
      )}
      {outro > 0 ? (
        <div style={{opacity: outro}}>
          <Headline size={80} y={(1 - outro) * 20}>
            {story.outroText}
          </Headline>
          <div style={{position: 'absolute', left: 68, top: 348, fontFamily: sans, fontWeight: 600, fontSize: 46, letterSpacing: 1, color: C.a}}>{story.outroSub}</div>
        </div>
      ) : null}
      {thinking ? (
        <div style={{position: 'absolute', left: 68, top: 452, width: 520, height: 8, background: C.grid, borderRadius: 4, overflow: 'hidden'}}>
          <div style={{width: `${think * 100}%`, height: '100%', background: C.ink}} />
        </div>
      ) : null}
      <div style={{position: 'absolute', left: 60, width: 850, top: 1408, display: 'flex', gap: 22, opacity: interpolate(t, [r.start + 0.1, r.start + 0.45], [index === 0 ? 0 : 0.0, 1], clamp)}}>
        {(['a', 'b'] as const).map((k) => (
          <Card key={k} side={r[k]} color={k === 'a' ? C.a : C.b} state={!revealed ? 'open' : r.winner === k ? 'win' : 'lose'} grow={r.winner === k ? pop : 0} count={count} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

const HookUI: React.FC<{story: TrueSizeStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const out = interpolate(t, [story.hook.end - 0.25, story.hook.end], [1, 0], clamp);
  return (
    <AbsoluteFill style={{opacity: out}}>
      <Kicker story={story} right={`${story.rounds.length} ROUNDS`} />
      <div style={{position: 'absolute', left: 64, top: 232, fontFamily: serif, fontWeight: 900, fontSize: 132, lineHeight: 0.94, letterSpacing: -4, color: C.ink}}>
        {story.hookText.map((line, i) => {
          // Zeile 2 und 3 schieben minimal nach – Frame 0 zeigt trotzdem schon den ganzen Satz
          const s = interpolate(t, [0.04 * i, 0.04 * i + 0.22], [14, 0], {...clamp, easing: Easing.out(Easing.cubic)});
          const lying = /lying/i.test(line);
          return (
            <div key={i} style={{transform: `translateY(${s}px)`}}>
              {lying ? (
                <>
                  {line.replace(/lying/i, '').trim()} <span style={{fontFamily: serifItalic, fontStyle: 'italic', color: C.a}}>{line.match(/lying/i)![0]}</span>
                </>
              ) : (
                line
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export const TrueSize: React.FC<TrueSizeStory> = (story) => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const views = useMemo(() => {
    // Endansicht jeder Runde = Startansicht der nächsten (eine durchgehende Kamerafahrt statt Schnitte)
    const out: View[] = [{...HOOK_VIEW, s: HOOK_VIEW.s * 1.07}];
    for (const r of story.rounds) {
      const mover = DATA.shapes[r[r.mover].shape];
      const target = DATA.shapes[r[r.mover === 'a' ? 'b' : 'a'].shape];
      const v = fit(boxOf(projectRings(target.rings, target.centroid[0]), moveRings(mover.rings, mover.centroid, target.centroid)), 0.8);
      out.push({...v, s: v.s * 1.05});
    }
    return out;
  }, [story.rounds]);

  return (
    <AbsoluteFill style={{backgroundColor: C.paper, overflow: 'hidden'}}>
      <Sequence durationInFrames={f(story.hook.end)} layout="none">
        <HookMap story={story} />
      </Sequence>
      {story.rounds.map((r, i) => (
        <Sequence key={i} from={f(r.start)} durationInFrames={f(r.end) - f(r.start)} layout="none">
          <RoundMap r={r} prev={views[i]} isLast={i === story.rounds.length - 1} />
        </Sequence>
      ))}

      {/* Papier über der Karte: oben und unten deckend, damit Text ruhig steht */}
      <AbsoluteFill style={{background: `linear-gradient(to bottom, ${C.paper} 0px, ${C.paper} 440px, rgba(241,234,219,0) 540px, rgba(241,234,219,0) 1310px, ${C.paper} 1385px, ${C.paper} 1920px)`}} />

      <Sequence durationInFrames={f(story.hook.end)} layout="none">
        <HookUI story={story} />
        {story.hook.audio ? <Audio src={staticFile(story.hook.audio)} /> : null}
      </Sequence>
      {story.rounds.map((r, i) => (
        <Sequence key={i} from={f(r.start)} durationInFrames={f(r.end) - f(r.start)} layout="none">
          <RoundUI r={r} index={i} total={story.rounds.length} story={story} isLast={i === story.rounds.length - 1} />
          {r.qAudio ? <Audio src={staticFile(r.qAudio)} /> : null}
          {[0, 1, 2].map((k) => (
            <Sequence key={k} from={f(r.thinkStart - r.start + k * 0.8)} layout="none">
              <Audio src={staticFile('sfx/tick.wav')} volume={0.4} />
            </Sequence>
          ))}
          <Sequence from={f(r.reveal - r.start)} layout="none">
            <Audio src={staticFile('sfx/whoosh.wav')} volume={0.32} />
          </Sequence>
          <Sequence from={f(r.aStart - r.start)} layout="none">
            {r.aAudio ? <Audio src={staticFile(r.aAudio)} /> : null}
          </Sequence>
          <Sequence from={f(r.moveEnd - r.start)} layout="none">
            <Audio src={staticFile('sfx/ding.wav')} volume={0.28} />
          </Sequence>
        </Sequence>
      ))}
      {story.music ? <Audio src={staticFile(story.music)} volume={story.musicVolume ?? 0.09} loop /> : null}

      {/* Druckkörnung */}
      <AbsoluteFill style={{mixBlendMode: 'multiply', opacity: 0.9}}>
        <Img src={staticFile('bilder/paper-grain.jpg')} style={{width: W, height: H}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(60,45,20,0.16) 100%)'}} />
    </AbsoluteFill>
  );
};
