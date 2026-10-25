import * as THREE from 'three';
import {
  SHOTS, DROP, BEAT, BLOCK_W, BLOCK_D, LAST_COL, clamp, smooth, easeInOut, easeOut, rand, colLand, CELLS, COL_FALL,
} from './timeline';

export type CamPose = {eye: THREE.Vector3; target: THREE.Vector3; fov: number; shadowSize: number};

const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
const C0 = V(0.078, 0, 0.033);
const CENTER = V(BLOCK_W / 2, 0.4, BLOCK_D / 2);

function lerpPose(a: [THREE.Vector3, THREE.Vector3], b: [THREE.Vector3, THREE.Vector3], u: number) {
  return [a[0].clone().lerp(b[0], u), a[1].clone().lerp(b[1], u)] as const;
}

// slow organic drift, like a gimbal operator (very small)
function handheld(t: number, amp: number) {
  const n = (f: number, p: number) => Math.sin(t * f + p);
  return V(
    amp * (0.6 * n(0.9, 1.3) + 0.4 * n(2.3, 0.2)),
    amp * (0.6 * n(1.1, 2.1) + 0.4 * n(2.9, 4.0)),
    amp * (0.6 * n(0.7, 0.4) + 0.4 * n(1.9, 3.3)),
  );
}

// impact shake when stacks land in shot D (decays fast)
function shake(t: number) {
  if (t < DROP || t > LAST_COL + 1.2) return 0;
  let s = 0;
  // the final landing gets a stronger hit
  const dtLast = t - LAST_COL;
  if (dtLast >= 0) s += 0.05 * Math.exp(-dtLast * 7);
  // beat pulses during the rain
  const ph = ((t - DROP) % (BEAT / 2)) / (BEAT / 2);
  if (t < LAST_COL) s += 0.012 * Math.exp(-ph * 6);
  return s;
}

export function cameraAt(t: number): CamPose {
  let eye: THREE.Vector3, target: THREE.Vector3, fov = 35, shadowSize = 4;
  if (t < SHOTS.B) {
    // A: the first bill floats down
    const u = smooth(t / SHOTS.B);
    [eye, target] = lerpPose(
      [C0.clone().add(V(-0.17, 0.25, -0.31)), C0.clone().add(V(0, 0.02, 0))],
      [C0.clone().add(V(-0.12, 0.17, -0.24)), C0.clone().add(V(0, 0.008, 0))],
      u,
    );
    fov = 32;
    shadowSize = 0.6;
  } else if (t < SHOTS.C) {
    // B: low side angle, bills settle into a stack
    const u = smooth((t - SHOTS.B) / (SHOTS.C - SHOTS.B));
    [eye, target] = lerpPose(
      [C0.clone().add(V(0.2, 0.36, -0.6)), C0.clone().add(V(0, 0.03, 0))],
      [C0.clone().add(V(-0.14, 0.38, -0.58)), C0.clone().add(V(0, 0.03, 0))],
      u,
    );
    fov = 34;
    shadowSize = 0.6;
  } else if (t < DROP) {
    // C: crane up with the growing stack, the person walks in, then a slow tense push
    const reveal = DROP - 1.9;
    if (t < reveal) {
      const u = easeInOut((t - SHOTS.C) / (reveal - SHOTS.C));
      // log-distance interpolation keeps the move feeling even as scale explodes
      const a = [C0.clone().add(V(-0.22, 0.11, -0.4)), C0.clone().add(V(0, 0.03, 0))] as const;
      const b = [V(-2.78, 2.23, -4.63), V(0.3, 1.05, -0.1)] as const;
      target = a[1].clone().lerp(b[1], u);
      const oa = a[0].clone().sub(a[1]), ob = b[0].clone().sub(b[1]);
      const la = oa.length(), lb = ob.length();
      const dir = oa.normalize().multiplyScalar(1 - u).add(ob.normalize().multiplyScalar(u)).normalize();
      eye = target.clone().add(dir.multiplyScalar(Math.exp(Math.log(la) * (1 - u) + Math.log(lb) * u)));
    } else {
      const u = (t - reveal) / (DROP - reveal);
      [eye, target] = lerpPose([V(-2.78, 2.23, -4.63), V(0.3, 1.05, -0.1)], [V(-2.45, 2.08, -4.15), V(0.3, 1.02, -0.08)], u * u);
    }
    fov = 36;
    shadowSize = 3.5;
  } else if (t < SHOTS.E) {
    // D: the drop — high wide shot, slow orbit while 999 stacks rain down
    const u = smooth((t - DROP) / (SHOTS.E - DROP));
    const ang = THREE.MathUtils.degToRad(-8 + 30 * u);
    const r = 9.6 - 1.4 * u, h = 6.4 - 1.2 * u;
    const base = V(-Math.cos(ang) * r * 0.72, h, -Math.sin(ang + 0.9) * r * 0.72);
    target = CENTER.clone().add(V(-0.3, -0.2, -0.4));
    eye = target.clone().add(base);
    fov = 38;
    shadowSize = 7;
  } else if (t < SHOTS.F) {
    // E: low tracking shot along the wall of money, person in the foreground
    const u = easeInOut((t - SHOTS.E) / (SHOTS.F - SHOTS.E));
    // low fly-over just above the surface of the money, toward the far corner
    [eye, target] = lerpPose([V(0.25, 1.32, 0.15), V(1.6, 0.95, 1.9)], [V(2.2, 1.27, 2.35), V(3.6, 0.9, 4.4)], u);
    fov = 44;
    shadowSize = 6;
  } else if (t < SHOTS.G) {
    // F: top-down drone, slow rotation
    const u = (t - SHOTS.F) / (SHOTS.G - SHOTS.F);
    const ang = THREE.MathUtils.degToRad(-35 + 28 * smooth(u));
    const h = 7.4 + 0.8 * u;
    target = CENTER.clone().setY(0);
    eye = target.clone().add(V(Math.sin(ang) * 1.2, h, -Math.cos(ang) * 1.2));
    fov = 40;
    shadowSize = 6;
  } else {
    // G: rise into the sky as 935 more blocks appear
    const u = easeInOut((t - SHOTS.G) / (SHOTS.END - SHOTS.G - 0.3));
    const d = Math.exp(Math.log(9) * (1 - u) + Math.log(150) * u);
    target = CENTER.clone().setY(0);
    eye = target.clone().add(V(-0.55, 0.78, -0.62).normalize().multiplyScalar(d));
    fov = 40;
    shadowSize = 12 + 200 * u;
  }
  return {eye, target, fov, shadowSize};
}
