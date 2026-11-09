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
  /** "long" = 16:9-Video (Komposition TrueSizeLong) mit Runden-Bannern, Abo-Hinweis und Abspann */
  format?: 'short' | 'long';
  timing?: {think?: number; move?: number; tail?: number};
  midCtaIndex?: number;
  midCtaText?: string;
  subscribeText?: string;
  /** Abspann (nur lang): Startzeit + gesprochene Zeile, von atlas_voice.py gesetzt */
  outro?: {start: number; audio?: string};
  thumbText?: string[];
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
// Zwei Formate: Short (9:16) und langes Video (16:9). map = Fenster, in dem die Karte "spielt".
type Layout = {wide: boolean; W: number; H: number; map: {cx: number; cy: number; w: number; h: number}; hook: {x: number; y: number; s: number}; lab: {x0: number; x1: number; y0: number; y1: number}; padB: number};
const PORTRAIT: Layout = {wide: false, W: 1080, H: 1920, map: {cx: 540, cy: 945, w: 880, h: 790}, hook: {x: 12, y: -70, s: 2.95}, lab: {x0: 170, x1: 910, y0: 545, y1: 1345}, padB: 0.8};
const WIDE: Layout = {wide: true, W: 1920, H: 1080, map: {cx: 1360, cy: 545, w: 1000, h: 800}, hook: {x: 12, y: -34, s: 2.9}, lab: {x0: 1010, x1: 1790, y0: 70, y1: 1040}, padB: 0.74};
let MAP = PORTRAIT.map;
/** Layout nach Bildformat; setzt das Kartenfenster für die Rechenfunktionen (pro Render-Prozess gibt es nur ein Format) */
const useLayout = (): Layout => {
  const {width, height} = useVideoConfig();
  const L = width > height ? WIDE : PORTRAIT;
  MAP = L.map;
  return L;
};

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
const useRound = (r: TrueSizeRound, L: Layout) =>
  useMemo(() => {
    MAP = L.map;
    const mover = r[r.mover];
    const target = r[r.mover === 'a' ? 'b' : 'a'];
    const ms = DATA.shapes[mover.shape];
    const ts = DATA.shapes[target.shape];
    const targetXY = projectRings(ts.rings, ts.centroid[0]);
    const moverStart = moveRings(ms.rings, ms.centroid, ms.centroid);
    const moverEnd = moveRings(ms.rings, ms.centroid, ts.centroid);
    const viewA = fit(boxOf(targetXY, moverStart), 0.94);
    const viewB = fit(boxOf(targetXY, moverEnd), L.padB);
    return {mover, target, ms, ts, targetXY, targetPath: pathOf(targetXY), viewA, viewB};
  }, [r, L]);

// jeder Ring relativ zu seinem ersten Punkt entfaltet (sonst Querstreifen am 180. Längengrad)
const WORLD_PATH = pathOf(DATA.world.flatMap((r) => projectRings([r], r[0][0])));

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
  const L = useLayout();
  const g = useRound(r, L);
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
    <svg width={L.W} height={L.H} style={{position: 'absolute', inset: 0}}>
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
        <MapLabel x={Math.max(L.lab.x0, Math.min(L.lab.x1, mTop[0]))} y={Math.max(L.lab.y0, mTop[1] - 22)} text={g.mover.name} color={moverColor} opacity={labels} />
        <MapLabel x={Math.max(L.lab.x0, Math.min(L.lab.x1, tBot[0]))} y={Math.min(L.lab.y1, tBot[1] + 54)} text={g.target.name} color={targetColor} opacity={labels} />
      </g>
    </svg>
  );
};

const HookMap: React.FC<{story: TrueSizeStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const L = useLayout();
  const view = {...L.hook, s: L.hook.s * interpolate(t, [0, story.hook.end], [1, 1.07])};
  const gl = DATA.shapes.greenland;
  const af = DATA.shapes.africa;
  const glPath = useMemo(() => pathOf(projectRings(gl.rings, gl.centroid[0])), [gl]);
  const afPath = useMemo(() => pathOf(projectRings(af.rings, af.centroid[0])), [af]);
  const gc = toScreen(view, [gl.centroid[0], mercY(gl.centroid[1])]);
  // Grönland "löst sich" wie ein lockerer Aufkleber
  const wob = Math.sin(t * 7) * 2.6 * interpolate(t, [0.2, 0.7], [0, 1], clamp);
  return (
    <svg width={L.W} height={L.H} style={{position: 'absolute', inset: 0}}>
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

// ------------------------------------------------------------ 16:9 (langes Video): Text links, Karte rechts
const PX = 90;
const PW = 640;
const LEVEL_COLOR: Record<string, string> = {EASY: '#1F4E79', MEDIUM: '#8A6A12', HARD: '#B4401F', LEGEND: '#1E1A15'};

const WideRoundUI: React.FC<{r: TrueSizeRound; index: number; total: number; story: TrueSizeStory}> = ({r, index, total, story}) => {
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
  const qIn = interpolate(t, [r.start, r.start + 0.3], [0, 1], clamp);
  const [q1, q2] = story.question.split(/really /i);
  const wl = winner.name.length;
  const newLevel = index > 0 && story.rounds[index - 1].level !== r.level;
  const banner = newLevel ? interpolate(t, [r.start, r.start + 0.25, r.start + 1.5, r.start + 1.8], [0, 1, 1, 0], clamp) : 0;
  const cta = story.midCtaIndex === index && story.midCtaText ? interpolate(t, [r.aStart + 1.2, r.aStart + 1.5], [0, 1], clamp) : 0;
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: PX, top: 78, width: PW, fontFamily: sans, fontWeight: 600, fontSize: 30, letterSpacing: 5, color: C.soft, whiteSpace: 'nowrap'}}>
        {(story.brand ?? 'COULD YOU PASS?').toUpperCase()} <span style={{color: C.coast}}>/</span> {story.kicker}
      </div>
      <div style={{position: 'absolute', left: PX, top: 128, width: PW, display: 'flex', alignItems: 'center', gap: 18, fontFamily: sans, fontWeight: 700, fontSize: 34, letterSpacing: 4, color: C.ink}}>
        <span>ROUND {index + 1} OF {total}</span>
        <span style={{background: LEVEL_COLOR[r.level] ?? C.ink, color: C.paper, padding: '2px 14px 4px', borderRadius: 5, fontSize: 28}}>{r.level}</span>
      </div>
      <div style={{position: 'absolute', left: PX, top: 204, width: PW}}>
        {!revealed ? (
          <div style={{fontFamily: serif, fontWeight: 900, fontSize: 98, lineHeight: 1, letterSpacing: -2, color: C.ink, opacity: index === 0 ? 1 : qIn}}>
            {q1}
            <span style={{fontFamily: serifItalic, fontStyle: 'italic', color: C.a}}>really</span> {q2}
          </div>
        ) : (
          <>
            <div style={{fontFamily: serif, fontWeight: 900, fontSize: wl > 13 ? 78 : wl > 9 ? 98 : 124, lineHeight: 1, letterSpacing: -2, color: wColor, opacity: Math.min(1, pop * 1.4), transform: `translateY(${(1 - pop) * 22}px)`}}>{winner.name}.</div>
            <div style={{marginTop: 20, fontFamily: sans, fontWeight: 600, fontSize: 44, letterSpacing: 1, color: C.ink, opacity: interpolate(t, [r.aStart + 0.25, r.aStart + 0.55], [0, 1], clamp)}}>
              {r.verdict} than {loser.name}
            </div>
          </>
        )}
        {thinking ? (
          <div style={{marginTop: 34, width: 520, height: 8, background: C.grid, borderRadius: 4, overflow: 'hidden'}}>
            <div style={{width: `${think * 100}%`, height: '100%', background: C.ink}} />
          </div>
        ) : null}
      </div>
      {cta > 0 ? (
        <div style={{position: 'absolute', left: PX, top: 520, opacity: cta, transform: `translateX(${(1 - cta) * -20}px)`}}>
          <span style={{display: 'inline-block', background: C.ink, color: C.paper, fontFamily: sans, fontWeight: 700, fontSize: 34, letterSpacing: 3, padding: '6px 18px 8px', borderRadius: 6}}>{story.midCtaText!.toUpperCase()}</span>
        </div>
      ) : null}
      <div style={{position: 'absolute', left: PX - 4, width: PW, top: 600, display: 'flex', flexDirection: 'column', gap: 20, opacity: interpolate(t, [r.start + 0.1, r.start + 0.45], [0, 1], clamp)}}>
        {(['a', 'b'] as const).map((k) => (
          <div key={k} style={{display: 'flex', height: 150}}>
            <Card side={r[k]} color={k === 'a' ? C.a : C.b} state={!revealed ? 'open' : r.winner === k ? 'win' : 'lose'} grow={r.winner === k ? pop * 0.6 : 0} count={count} />
          </div>
        ))}
      </div>
      {/* Fortschritt: ein Strich je Runde */}
      <div style={{position: 'absolute', left: PX, top: 978, width: PW, display: 'flex', gap: 6}}>
        {story.rounds.map((_, i) => (
          <div key={i} style={{flex: 1, height: 10, borderRadius: 3, background: i < index ? C.ink : i === index ? C.a : C.grid}} />
        ))}
      </div>
      {banner > 0 ? (
        <div style={{position: 'absolute', left: 800, right: 0, top: 0, bottom: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: banner}}>
          <div style={{background: C.paper, border: `5px solid ${C.ink}`, borderRadius: 10, padding: '26px 70px 34px', textAlign: 'center', transform: `rotate(-2deg) scale(${0.9 + 0.1 * banner})`, boxShadow: '0 18px 40px rgba(30,26,21,0.25)'}}>
            <div style={{fontFamily: sans, fontWeight: 700, fontSize: 44, letterSpacing: 8, color: C.soft}}>NEXT LEVEL</div>
            <div style={{fontFamily: serifItalic, fontStyle: 'italic', fontWeight: 900, fontSize: 170, lineHeight: 1, color: C.a}}>{r.level[0] + r.level.slice(1).toLowerCase()}</div>
          </div>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

const WideHookUI: React.FC<{story: TrueSizeStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const out = interpolate(t, [story.hook.end - 0.25, story.hook.end], [1, 0], clamp);
  return (
    <AbsoluteFill style={{opacity: out}}>
      <div style={{position: 'absolute', left: PX, top: 150, fontFamily: sans, fontWeight: 600, fontSize: 34, letterSpacing: 5, color: C.soft, whiteSpace: 'nowrap'}}>
        {(story.brand ?? 'COULD YOU PASS?').toUpperCase()} <span style={{color: C.coast}}>/</span> {story.kicker} <span style={{color: C.coast}}>/</span> <span style={{color: C.ink}}>{story.rounds.length} ROUNDS</span>
      </div>
      <div style={{position: 'absolute', left: PX, top: 230, fontFamily: serif, fontWeight: 900, fontSize: 168, lineHeight: 0.94, letterSpacing: -5, color: C.ink}}>
        {story.hookText.map((line, i) => {
          const lying = /lying/i.test(line);
          return (
            <div key={i} style={{whiteSpace: 'nowrap'}}>
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
      <div style={{position: 'absolute', left: PX + 4, top: 790, fontFamily: sans, fontWeight: 600, fontSize: 50, letterSpacing: 1, color: C.ink, opacity: interpolate(t, [1.6, 2.0], [0, 1], clamp)}}>
        Which is <span style={{color: C.a}}>really</span> bigger? Keep score.
      </div>
    </AbsoluteFill>
  );
};

const WideOutro: React.FC<{story: TrueSizeStory}> = ({story}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const L = useLayout();
  const k = interpolate(t, [0, 0.4], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const view = {...L.hook, s: L.hook.s * interpolate(t, [0, 12], [1.0, 1.1], clamp)};
  return (
    <AbsoluteFill style={{backgroundColor: C.paper}}>
      <svg width={L.W} height={L.H} style={{position: 'absolute', inset: 0, opacity: 0.8}}>
        <World view={view} />
      </svg>
      <AbsoluteFill style={{background: `linear-gradient(to right, ${C.paper} 0px, ${C.paper} 780px, rgba(241,234,219,0) 900px)`}} />
      <div style={{position: 'absolute', left: PX, top: 150, width: 700, opacity: k, transform: `translateY(${(1 - k) * 22}px)`}}>
        <div style={{fontFamily: serif, fontWeight: 900, fontSize: 104, lineHeight: 1, letterSpacing: -2, color: C.ink}}>{story.outroText}</div>
        <div style={{marginTop: 26, fontFamily: serifItalic, fontStyle: 'italic', fontWeight: 900, fontSize: 250, lineHeight: 1, color: C.a}}>?/{story.rounds.length}</div>
        <div style={{marginTop: 24, fontFamily: sans, fontWeight: 600, fontSize: 52, letterSpacing: 1, color: C.ink}}>{story.outroSub}</div>
        {story.subscribeText ? <div style={{marginTop: 14, fontFamily: sans, fontWeight: 600, fontSize: 40, letterSpacing: 1, color: C.soft}}>{story.subscribeText}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

/** Vorschaubild 1280×720: Grönland in echter Größe auf Afrika */
export const TrueSizeThumb: React.FC<TrueSizeStory> = (story) => {
  const g = useMemo(() => {
    MAP = {cx: 965, cy: 368, w: 560, h: 610};
    const gl = DATA.shapes.greenland;
    const af = DATA.shapes.africa;
    const afXY = projectRings(af.rings, af.centroid[0]);
    const view = fit(boxOf(afXY), 1);
    const real = moveRings(gl.rings, gl.centroid, [af.centroid[0] - 2, af.centroid[1] + 4]);
    return {t: tf(view), af: pathOf(afXY), real: pathOf(real)};
  }, []);
  const lines = story.thumbText ?? ['THE MAP', 'IS LYING'];
  return (
    <AbsoluteFill style={{backgroundColor: C.paper, overflow: 'hidden'}}>
      <svg width={1280} height={720} style={{position: 'absolute', inset: 0}}>
        <g transform={g.t}>
          <path d={g.af} fill={C.b} />
          <path d={g.real} fill={C.a} stroke={C.paper} strokeWidth={4} vectorEffect="non-scaling-stroke" />
        </g>
      </svg>
      <div style={{position: 'absolute', left: 54, top: 150, fontFamily: serif, fontWeight: 900, fontSize: 122, lineHeight: 0.95, letterSpacing: -4, color: C.ink}}>
        {lines.map((line, i) => {
          const m = line.match(/lying/i);
          return (
            <div key={i} style={{whiteSpace: 'nowrap'}}>
              {m ? (
                <>
                  {line.replace(/lying/i, '').trim()} <span style={{fontFamily: serifItalic, fontStyle: 'italic', color: C.a}}>{m[0]}</span>
                </>
              ) : (
                line
              )}
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: 60, top: 440, background: C.ink, color: C.paper, fontFamily: sans, fontWeight: 700, fontSize: 50, letterSpacing: 3, padding: '6px 22px 10px', borderRadius: 8, transform: 'rotate(-2deg)'}}>GREENLAND'S REAL SIZE</div>
      <AbsoluteFill style={{mixBlendMode: 'multiply', opacity: 0.9}}>
        <Img src={staticFile('bilder/paper-grain.jpg')} style={{width: 1280, height: 720}} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const TrueSize: React.FC<TrueSizeStory> = (story) => {
  const {fps} = useVideoConfig();
  const L = useLayout();
  const f = (s: number) => Math.round(s * fps);
  const views = useMemo(() => {
    MAP = L.map;
    // Endansicht jeder Runde = Startansicht der nächsten (eine durchgehende Kamerafahrt statt Schnitte)
    const out: View[] = [{...L.hook, s: L.hook.s * 1.07}];
    for (const r of story.rounds) {
      const mover = DATA.shapes[r[r.mover].shape];
      const target = DATA.shapes[r[r.mover === 'a' ? 'b' : 'a'].shape];
      const v = fit(boxOf(projectRings(target.rings, target.centroid[0]), moveRings(mover.rings, mover.centroid, target.centroid)), L.padB);
      out.push({...v, s: v.s * 1.05});
    }
    return out;
  }, [story.rounds, L]);

  return (
    <AbsoluteFill style={{backgroundColor: C.paper, overflow: 'hidden'}}>
      <Sequence durationInFrames={f(story.hook.end)} layout="none">
        <HookMap story={story} />
      </Sequence>
      {story.rounds.map((r, i) => (
        <Sequence key={i} from={f(r.start)} durationInFrames={f(r.end) - f(r.start)} layout="none">
          <RoundMap r={r} prev={views[i]} isLast={!L.wide && i === story.rounds.length - 1} />
        </Sequence>
      ))}

      {/* Papier über der Karte: oben und unten deckend, damit Text ruhig steht */}
      <AbsoluteFill style={{background: L.wide ? `linear-gradient(to right, ${C.paper} 0px, ${C.paper} 760px, rgba(241,234,219,0) 880px)` : `linear-gradient(to bottom, ${C.paper} 0px, ${C.paper} 440px, rgba(241,234,219,0) 540px, rgba(241,234,219,0) 1310px, ${C.paper} 1385px, ${C.paper} 1920px)`}} />

      <Sequence durationInFrames={f(story.hook.end)} layout="none">
        {L.wide ? <WideHookUI story={story} /> : <HookUI story={story} />}
        {story.hook.audio ? <Audio src={staticFile(story.hook.audio)} /> : null}
      </Sequence>
      {story.rounds.map((r, i) => (
        <Sequence key={i} from={f(r.start)} durationInFrames={f(r.end) - f(r.start)} layout="none">
          {L.wide ? <WideRoundUI r={r} index={i} total={story.rounds.length} story={story} /> : <RoundUI r={r} index={i} total={story.rounds.length} story={story} isLast={i === story.rounds.length - 1} />}
          {r.qAudio ? <Audio src={staticFile(r.qAudio)} /> : null}
          {Array.from({length: Math.max(1, Math.round((r.reveal - r.thinkStart) / 0.8))}, (_, k) => k).map((k) => (
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
      {L.wide && story.outro ? (
        <Sequence from={f(story.outro.start)} layout="none">
          <WideOutro story={story} />
          {story.outro.audio ? <Audio src={staticFile(story.outro.audio)} /> : null}
        </Sequence>
      ) : null}
      {story.music ? <Audio src={staticFile(story.music)} volume={story.musicVolume ?? 0.09} loop /> : null}

      {/* Druckkörnung */}
      <AbsoluteFill style={{mixBlendMode: 'multiply', opacity: 0.9}}>
        <Img src={staticFile('bilder/paper-grain.jpg')} style={{width: L.W, height: L.H}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(60,45,20,0.16) 100%)'}} />
    </AbsoluteFill>
  );
};
