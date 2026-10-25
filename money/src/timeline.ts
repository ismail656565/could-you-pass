// All timing in seconds, locked to the music: "Cutscene Crush" (Blue Deer Studio), ~161.5 BPM, drop at 12.5 s.
export const FPS = 30;
export const DURATION = 34;
export const TOTAL = DURATION * FPS;

export const BEAT = 60 / 161.5;
export const DROP = 12.5;
export const snap = (t: number, div = 1) => DROP + Math.round((t - DROP) / (BEAT / div)) * (BEAT / div);

// real-world sizes (meters) of a US $100 bill
export const BL = 0.156;
export const BW = 0.0663;
export const BT = 0.000109;
export const BUNDLE_H = BT * 100; // 10.9 mm
export const COL_H = BUNDLE_H * 100; // 1.09 m
export const NX = 20;
export const NZ = 50;
export const PX = BL + 0.004;
export const PZ = BW + 0.004;
export const BLOCK_W = NX * PX;
export const BLOCK_D = NZ * PZ;

// shot boundaries (cuts land on beats)
export const SHOTS = {
  A: 0,
  B: snap(3.0),
  C: snap(6.2),
  D: DROP,
  E: snap(20.0),
  F: snap(25.0),
  G: snap(29.6),
  END: DURATION,
};

// deterministic random
export const rand = (i: number, salt = 0) => {
  const x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453;
  return x - Math.floor(x);
};

export const clamp = (x: number, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const smooth = (u: number) => {
  u = clamp(u);
  return u * u * u * (u * (u * 6 - 15) + 10);
};
export const easeOut = (u: number, p = 3) => 1 - Math.pow(1 - clamp(u), p);
export const easeInOut = (u: number) => {
  u = clamp(u);
  return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
};

// ---------- shot A: the first bill ----------
export const BILL1_LAND = 1.05;

// ---------- shot B: 99 bills flutter onto the first ----------
export const BILL_FALL = 0.34;
export const billLand = (k: number) => SHOTS.B + 0.45 + 1.75 * Math.pow(k / 99, 0.85); // k = 1..99
export const billsLanded = (t: number) => {
  if (t < BILL1_LAND) return 0;
  let n = 1;
  for (let k = 1; k <= 99; k++) if (t >= billLand(k)) n++;
  return n;
};
export const STRAP_T = billLand(99) + 0.3;

// ---------- shot C: 99 bundles drop onto the first ----------
export const G = 9.81;
export const BUNDLE_DROP_H = 0.45;
export const BUNDLE_FALL = Math.sqrt((2 * BUNDLE_DROP_H) / G);
export const bundleLand = (k: number) => SHOTS.C + 0.55 + (DROP - 1.9 - (SHOTS.C + 0.55)) * Math.sqrt(k / 99); // k = 1..99
export const bundlesLanded = (t: number) => {
  let n = 1;
  for (let k = 1; k <= 99; k++) if (t >= bundleLand(k)) n++;
  return n;
};
export const PERSON_IN = DROP - 2.6;

// ---------- shot D: 999 stacks rain down on the beat ----------
export const COL_DROP_H = 5.5;
export const COL_G = 16;
export const COL_FALL = Math.sqrt((2 * COL_DROP_H) / COL_G);

type Cell = {i: number; j: number};
const cells: Cell[] = [];
for (let i = 0; i < NX; i++) for (let j = 0; j < NZ; j++) if (i || j) cells.push({i, j});
cells.sort((a, b) => Math.hypot(a.i * PX, a.j * PZ) + rand(a.i * 97 + a.j, 3) * 0.25 - (Math.hypot(b.i * PX, b.j * PZ) + rand(b.i * 97 + b.j, 3) * 0.25));
export const CELLS = cells;
const COL_START = DROP + 2 * BEAT;
const COL_SPAN = 16 * BEAT;
export const colLand = (k: number) => {
  const raw = COL_START + COL_SPAN * Math.pow(k / (CELLS.length - 1), 0.8);
  return COL_START + Math.round((raw - COL_START) / (BEAT / 2)) * (BEAT / 2);
};
export const LAST_COL = colLand(CELLS.length - 1);
export const colsLanded = (t: number) => {
  let n = 1;
  for (let k = 0; k < CELLS.length; k++) if (t >= colLand(k)) n++;
  return n;
};

// ---------- shot G: 936 blocks ----------
export const BLOCKS_X = 36;
export const BLOCKS_Z = 26; // 36 * 26 = 936
export const BLOCK_GAP = 1.6;
export const blockRise = (dist: number) => SHOTS.G + 0.9 + dist * 0.028;
