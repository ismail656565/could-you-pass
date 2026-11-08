import React from 'react';

// Strichmännchen-Moderator für das Layout "stick" (2D-Zeichentrick-Look).
// Reines SVG, alle Bewegungen hängen am Frame. Die Linien "kochen" leicht (alle 3 Frames neue Verzerrung),
// wie bei handgezeichneten 2D-Animationen.

export type StickPose = 'idle' | 'point' | 'think' | 'nervous' | 'cheer' | 'pointDown' | 'wave' | 'shrug';

type P = [number, number];
type Arms = {le: P; lh: P; re: P; rh: P};

// viewBox 400x520 – Kopf (200,110), Schultern (200,198), Hüfte (200,330)
const ARMS: Record<StickPose, Arms> = {
  idle: {le: [168, 258], lh: [160, 318], re: [232, 258], rh: [240, 318]},
  // zeigt nach oben rechts (auf Frage/Karte), linke Hand in der Hüfte
  point: {le: [145, 252], lh: [186, 300], re: [262, 160], rh: [318, 112]},
  // Hand am Kinn, anderer Arm vor dem Bauch
  think: {le: [168, 262], lh: [232, 266], re: [258, 248], rh: [222, 176]},
  nervous: {le: [150, 220], lh: [176, 168], re: [250, 220], rh: [224, 168]},
  cheer: {le: [146, 150], lh: [122, 82], re: [254, 150], rh: [278, 82]},
  // zeigt nach oben auf die Antworten
  pointDown: {le: [145, 252], lh: [186, 300], re: [258, 150], rh: [296, 86]},
  wave: {le: [168, 258], lh: [160, 318], re: [262, 156], rh: [300, 92]},
  shrug: {le: [140, 230], lh: [108, 196], re: [260, 230], rh: [292, 196]},
};

const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
const lp = (a: P, b: P, k: number): P => [lerp(a[0], b[0], k), lerp(a[1], b[1], k)];
const ease = (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

export const StickMan: React.FC<{
  frame: number;
  fps: number;
  pose: StickPose;
  prevPose: StickPose;
  /** Sekunden seit Beginn der aktuellen Pose */
  since: number;
  /** 0..1 Lautstärke der Stimme */
  talk: number;
  width: number;
  id: string;
  ink?: string;
  tie?: string;
}> = ({frame, fps, pose, prevPose, since, talk, width, id, ink = '#1b1b1b', tie = '#e63946'}) => {
  const sec = frame / fps;
  const k = ease(since / 0.22);
  const a = ARMS[prevPose];
  const b = ARMS[pose];
  let le = lp(a.le, b.le, k);
  let lh = lp(a.lh, b.lh, k);
  let re = lp(a.re, b.re, k);
  let rh = lp(a.rh, b.rh, k);

  // Leben: Atmen, Gestik beim Sprechen, Winken, Jubel-Sprung
  const breathe = Math.sin(sec * Math.PI * 0.9) * 3;
  if (pose === 'point' || pose === 'idle') {
    const g = talk * 14 * Math.sin(sec * 9);
    lh = [lh[0] - Math.abs(g) * 0.6, lh[1] - Math.abs(g)];
  }
  if (pose === 'wave') {
    const w = Math.sin(sec * Math.PI * 4.4) * 26;
    rh = [rh[0] + w, rh[1] + Math.abs(w) * 0.2];
  }
  if (pose === 'cheer') {
    const pump = Math.abs(Math.sin(since * Math.PI * 3)) * 14;
    lh = [lh[0], lh[1] - pump];
    rh = [rh[0], rh[1] - pump];
  }
  if (pose === 'think') {
    // Finger tippt ans Kinn
    rh = [rh[0], rh[1] + Math.abs(Math.sin(sec * Math.PI * 2.2)) * 5];
  }
  if (pose === 'pointDown' || pose === 'point') {
    const jab = Math.max(0, Math.sin(since * Math.PI * 2.5)) * (since < 0.8 ? 10 : 0);
    rh = [rh[0] + jab * 0.6, rh[1] - jab];
  }
  const jump = pose === 'cheer' && since < 1.2 ? -Math.abs(Math.sin((since / 0.4) * Math.PI)) * 34 : 0;
  const shake = pose === 'nervous' ? Math.sin(frame * 2.1) * 2 : 0;
  const tilt = pose === 'think' ? -6 : pose === 'shrug' ? 5 : Math.sin(sec * 1.3) * 2;

  // Gesicht
  const blink = frame % Math.round(fps * 3.7) < 4;
  const lookX = pose === 'nervous' ? 9 : pose === 'think' ? 6 : pose === 'point' || pose === 'pointDown' ? 6 : 0;
  const lookY = pose === 'think' || pose === 'point' || pose === 'pointDown' ? -6 : 0;
  const happy = pose === 'cheer' || pose === 'wave';
  const open = happy ? Math.max(0.55, talk) : talk;

  // Beine: leichtes Wippen, beim Nervössein Fuß-Tippen
  const tap = pose === 'nervous' || pose === 'think' ? Math.max(0, Math.sin(sec * Math.PI * 4)) * 10 : 0;

  const boil = Math.floor(frame / 3);
  const SW = 9;
  return (
    <svg viewBox="0 0 400 520" width={width} height={(width * 520) / 400} style={{overflow: 'visible'}}>
      <defs>
        <filter id={`boil-${id}`} x="-20%" y="-20%" width="140%" height="140%">
          <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves={2} seed={boil % 7} result="n" />
          <feDisplacementMap in="SourceGraphic" in2="n" scale={4.5} xChannelSelector="R" yChannelSelector="G" />
        </filter>
      </defs>
      <ellipse cx="200" cy="492" rx={78 + jump * 0.5} ry="11" fill="#000" opacity={0.13} />
      <g filter={`url(#boil-${id})`} transform={`translate(${shake} ${jump + breathe * 0.3})`} stroke={ink} strokeWidth={SW} strokeLinecap="round" strokeLinejoin="round" fill="none">
        {/* Beine */}
        <path d={`M200 330 L168 408 L${150 - tap * 0.3} ${482 - tap}`} />
        <path d="M200 330 L232 408 L252 482" />
        <path d={`M${150 - tap * 0.3} ${482 - tap} l-22 0`} />
        <path d="M252 482 l22 0" />
        {/* Körper */}
        <g transform={`rotate(${tilt * 0.4} 200 330)`}>
          <path d={`M200 ${170 + breathe * 0.2} L200 330`} />
          {/* Arme */}
          <path d={`M200 198 L${le[0]} ${le[1]} L${lh[0]} ${lh[1]}`} />
          <path d={`M200 198 L${re[0]} ${re[1]} L${rh[0]} ${rh[1]}`} />
          <circle cx={lh[0]} cy={lh[1]} r={7} fill={ink} />
          <circle cx={rh[0]} cy={rh[1]} r={7} fill={ink} />
          {/* Fliege */}
          <path d="M200 182 L178 170 L178 196 Z M200 182 L222 170 L222 196 Z" fill={tie} strokeWidth={5} />
          <circle cx="200" cy="183" r="6" fill={ink} strokeWidth={2} />
          {/* Kopf */}
          <g transform={`rotate(${tilt} 200 160)`}>
            <circle cx="200" cy="104" r="60" fill="#fff" />
            {/* Haar-Strähne */}
            <path d="M176 48 Q190 30 204 46 Q214 28 230 44" strokeWidth={7} />
            {/* Augenbrauen */}
            {pose === 'nervous' ? (
              <>
                <path d="M162 74 L184 82" strokeWidth={6} />
                <path d="M238 74 L216 82" strokeWidth={6} />
              </>
            ) : pose === 'think' ? (
              <>
                <path d="M164 80 L184 78" strokeWidth={6} />
                <path d="M216 70 Q228 64 238 72" strokeWidth={6} />
              </>
            ) : (
              <>
                <path d={`M164 ${happy ? 70 : 76} Q174 ${happy ? 64 : 70} 186 ${happy ? 70 : 76}`} strokeWidth={6} />
                <path d={`M214 ${happy ? 70 : 76} Q226 ${happy ? 64 : 70} 236 ${happy ? 70 : 76}`} strokeWidth={6} />
              </>
            )}
            {/* Augen */}
            {happy ? (
              <>
                <path d="M164 100 Q175 88 186 100" strokeWidth={7} />
                <path d="M214 100 Q225 88 236 100" strokeWidth={7} />
              </>
            ) : blink ? (
              <>
                <path d="M164 98 L186 98" strokeWidth={6} />
                <path d="M214 98 L236 98" strokeWidth={6} />
              </>
            ) : (
              <>
                <ellipse cx="175" cy="98" rx="12" ry="15" fill="#fff" strokeWidth={5} />
                <ellipse cx="225" cy="98" rx="12" ry="15" fill="#fff" strokeWidth={5} />
                <circle cx={175 + lookX * 0.6} cy={100 + lookY * 0.6} r="6" fill={ink} stroke="none" />
                <circle cx={225 + lookX * 0.6} cy={100 + lookY * 0.6} r="6" fill={ink} stroke="none" />
              </>
            )}
            {/* Mund */}
            {pose === 'think' && talk < 0.1 ? (
              <path d="M186 136 Q196 132 206 138 Q214 142 222 136" strokeWidth={6} />
            ) : pose === 'nervous' && talk < 0.1 ? (
              <path d="M180 138 L188 132 L196 138 L204 132 L212 138 L220 132" strokeWidth={5} />
            ) : open > 0.08 ? (
              <ellipse cx="200" cy={132 + 6 * open} rx={13 + 7 * open} ry={4 + 12 * open} fill="#7a1f2b" strokeWidth={5} />
            ) : (
              <path d="M180 128 Q200 146 220 128" strokeWidth={6} />
            )}
            {pose === 'nervous' ? <path d="M252 70 Q262 88 254 96 Q244 92 252 70 Z" fill="#7cc6ff" strokeWidth={4} /> : null}
          </g>
        </g>
      </g>
    </svg>
  );
};
