import React from 'react';
import {AbsoluteFill, useCurrentFrame, staticFile, continueRender, delayRender} from 'remotion';
import {
  FPS, SHOTS, DROP, DURATION, billsLanded, bundlesLanded, colsLanded, STRAP_T, bundleLand, LAST_COL,
  clamp, easeOut, smooth,
} from './timeline';

// load fonts once
const fontHandle = typeof window !== 'undefined' ? delayRender('fonts') : null;
if (typeof window !== 'undefined') {
  const faces = [
    new FontFace('InterDisplay', `url(${staticFile('fonts/InterDisplay-Black.otf')})`, {weight: '900'}),
    new FontFace('InterUI', `url(${staticFile('fonts/Inter-SemiBold.otf')})`, {weight: '600'}),
    new FontFace('InterUI', `url(${staticFile('fonts/Inter-Medium.otf')})`, {weight: '500'}),
  ];
  Promise.all(faces.map((f) => f.load().then((ff) => (document as any).fonts.add(ff))))
    .catch(() => null)
    .finally(() => fontHandle !== null && continueRender(fontHandle));
}

const INK = '#16181b';
const SUB = '#3d4148';
const SRC = '#5d626a';
const ACC = '#e8572a';
const money = (v: number) => '$' + Math.floor(v).toLocaleString('en-US');

type Seg = {
  s: number; e: number;
  main: (t: number) => string;
  sub: string; subAt: number; src?: string;
  milestone?: number; // time the number reaches its final value (punch)
};

const SEGS: Seg[] = [
  {s: 0, e: SHOTS.B, main: () => '$100', sub: 'One bill.', subAt: 0.25},
  {s: SHOTS.B, e: SHOTS.C, main: (t) => money(100 * Math.max(1, billsLanded(t))), sub: '100 bills.\nFits in your pocket.', subAt: STRAP_T, milestone: STRAP_T - 0.3},
  {s: SHOTS.C, e: DROP, main: (t) => money(10000 * bundlesLanded(t)), sub: '100 bundles.\nAbout waist high.', subAt: bundleLand(99) + 0.15, milestone: bundleLand(99)},
  {s: DROP, e: SHOTS.E, main: (t) => money(1e6 * colsLanded(t)), sub: '1,000 stacks.\nA block about 10 × 11 feet.', subAt: LAST_COL + 0.15, milestone: LAST_COL},
  {s: SHOTS.E, e: SHOTS.F, main: (t) => `${(31.7 * easeOut((t - SHOTS.E - 0.15) / 1.3, 3)).toFixed(1)} years`, sub: 'to spend it at $1\nevery single second.', subAt: SHOTS.E + 0.35, src: 'Non-stop. No sleep.', milestone: SHOTS.E + 1.45},
  {s: SHOTS.F, e: SHOTS.G, main: (t) => `${Math.round(66313 * easeOut((t - SHOTS.F - 0.15) / 1.4, 3)).toLocaleString('en-US')} years`, sub: 'to earn it at the\nUS minimum wage.', subAt: SHOTS.F + 0.35, src: '$7.25/h × 40 h/week × 52 weeks', milestone: SHOTS.F + 1.55},
  {s: SHOTS.G, e: DURATION, main: () => '936×', sub: "That's how many of these\nthe richest person owns.", subAt: SHOTS.G + 0.5, src: 'Elon Musk, $936B · Forbes, Oct 1, 2026', milestone: SHOTS.G + 0.2},
];

const Main: React.FC<{text: string; t: number; seg: Seg}> = ({text, t, seg}) => {
  const inU = seg.s === 0 ? 1 : easeOut((t - seg.s) / 0.32, 4);
  const outU = seg.e < DURATION ? clamp((t - (seg.e - 0.16)) / 0.16) : 0;
  const punch = seg.milestone !== undefined ? Math.exp(-Math.max(0, t - seg.milestone) * 7) * (t >= seg.milestone ? 1 : 0) : 0;
  const scale = 1 + 0.05 * punch;
  const chars = text.split('');
  return (
    <div style={{overflow: 'hidden', paddingBottom: 6}}>
      <div
        style={{
          fontFamily: 'InterDisplay', fontWeight: 900, fontSize: 116, lineHeight: 1.0, letterSpacing: -3,
          color: INK, whiteSpace: 'nowrap',
          transform: `translateY(${(1 - inU) * 110 - outU * 110}%) scale(${scale})`,
          transformOrigin: 'left center',
        }}
      >
        {chars.map((c, i) => (
          <span key={i} style={{color: c === '$' || c === '×' ? ACC : INK}}>{c}</span>
        ))}
      </div>
    </div>
  );
};

const Sub: React.FC<{seg: Seg; t: number}> = ({seg, t}) => {
  if (t < seg.subAt) return null;
  const outU = seg.e < DURATION ? clamp((t - (seg.e - 0.16)) / 0.16) : 0;
  const lines = seg.sub.split('\n');
  return (
    <div style={{marginTop: 22}}>
      {lines.map((ln, i) => {
        const u = easeOut((t - seg.subAt - i * 0.07) / 0.35, 4);
        return (
          <div key={i} style={{overflow: 'hidden'}}>
            <div style={{
              fontFamily: 'InterUI', fontWeight: 600, fontSize: 50, lineHeight: 1.18, color: SUB,
              transform: `translateY(${(1 - u) * 100}%)`, opacity: (0.2 + 0.8 * u) * (1 - outU),
            }}>{ln}</div>
          </div>
        );
      })}
      {seg.src ? (
        <div style={{
          marginTop: 18, fontFamily: 'InterUI', fontWeight: 500, fontSize: 30, color: SRC,
          opacity: easeOut((t - seg.subAt - 0.3) / 0.4) * (1 - outU),
        }}>{seg.src}</div>
      ) : null}
    </div>
  );
};

export const Overlay: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const seg = SEGS.find((s) => t >= s.s && t < s.e) ?? SEGS[SEGS.length - 1];
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {/* soft light wash behind the text so it reads on any background */}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(246,247,248,0.86) 0%, rgba(246,247,248,0.62) 24%, rgba(246,247,248,0) 40%)'}} />
      <div style={{position: 'absolute', left: 76, top: 205, right: 60}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 14, marginBottom: 22}}>
          <div style={{width: 14, height: 14, background: ACC}} />
          <div style={{fontFamily: 'InterUI', fontWeight: 600, fontSize: 32, letterSpacing: 2.5, color: INK, opacity: 0.85}}>
            $1 BILLION, TO SCALE
          </div>
        </div>
        <Main text={seg.main(t)} t={t} seg={seg} />
        <Sub seg={seg} t={t} />
      </div>
    </AbsoluteFill>
  );
};
