import React, {useEffect, useLayoutEffect, useMemo, useRef, useState} from 'react';
import * as THREE from 'three';
import {useThree} from '@react-three/fiber';
import {useCurrentFrame, delayRender, continueRender} from 'remotion';
import {loadAssets, Assets} from './assets';
import {cameraAt} from './camera';
import {
  FPS, BL, BW, BT, BUNDLE_H, COL_H, PX, PZ, NX, NZ, BLOCK_W, BLOCK_D, SHOTS, DROP,
  BILL1_LAND, BILL_FALL, billLand, billsLanded, STRAP_T, BUNDLE_DROP_H, BUNDLE_FALL, bundleLand,
  PERSON_IN, CELLS, colLand, COL_FALL, COL_DROP_H, COL_G, BLOCKS_X, BLOCKS_Z, BLOCK_GAP, blockRise,
  rand, clamp, smooth, easeOut, easeInOut,
} from './timeline';

const SUN = new THREE.Vector3(0.62, 1.05, -0.72).normalize();
const tmpM = new THREE.Matrix4();
const tmpQ = new THREE.Quaternion();
const tmpE = new THREE.Euler();
const tmpP = new THREE.Vector3();
const tmpS = new THREE.Vector3();

function texClone(t: THREE.Texture, rx: number, ry: number, flipU = false) {
  const c = t.clone();
  c.wrapS = c.wrapT = THREE.RepeatWrapping;
  c.repeat.set(flipU ? -rx : rx, ry);
  if (flipU) c.offset.x = 1;
  c.needsUpdate = true;
  return c;
}

function std(map: THREE.Texture | undefined, rough = 0.88, color = '#ffffff') {
  return new THREE.MeshStandardMaterial({map: map ?? null, roughness: rough, metalness: 0, color});
}

// landing squash: quick compression then settle
function squash(dt: number) {
  if (dt < 0 || dt > 0.25) return 1;
  return 1 - 0.06 * Math.exp(-dt * 18) * Math.cos(dt * 40);
}

function useAssets() {
  const [a, setA] = useState<Assets | null>(null);
  const [handle] = useState(() => delayRender('scene assets'));
  const advance = useThree((s) => s.advance);
  useEffect(() => {
    loadAssets().then(setA);
  }, []);
  useEffect(() => {
    if (!a) return;
    // the canvas only redraws on frame changes, so draw once now that everything exists
    requestAnimationFrame(() => {
      advance(performance.now());
      requestAnimationFrame(() => {
        advance(performance.now());
        continueRender(handle);
      });
    });
  }, [a]);
  return a;
}

export const Scene: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const assets = useAssets();
  const {camera, scene, gl} = useThree();

  // ---------- materials ----------
  const M = useMemo(() => {
    if (!assets) return null;
    const T = assets.tex;
    const topFlip = (n: string, rx = 1, ry = 1) => texClone(T[n], rx, ry, true);
    const bill = new THREE.MeshStandardMaterial({map: T.bill_top, roughness: 0.82, side: THREE.DoubleSide});
    const stack = [std(T.stack_short), std(T.stack_short), std(topFlip('bill_top')), std(T.bill_top), std(T.stack_long), std(T.stack_long)];
    const bundle = [std(T.bundle_short), std(T.bundle_short), std(topFlip('bundle_top')), std(T.bundle_top), std(T.bundle_long), std(T.bundle_long)];
    const column = [
      std(texClone(T.bundle_short, 1, 100)), std(texClone(T.bundle_short, 1, 100)),
      std(topFlip('bundle_top')), std(T.bundle_top),
      std(texClone(T.bundle_long, 1, 100)), std(texClone(T.bundle_long, 1, 100)),
    ];
    const block = [
      std(texClone(T.bundle_short, NZ, 100)), std(texClone(T.bundle_short, NZ, 100)),
      std(topFlip('bundle_top', NX, NZ)), std(T.bundle_top),
      std(texClone(T.bundle_long, NX, 100)), std(texClone(T.bundle_long, NX, 100)),
    ];
    const strap = new THREE.MeshStandardMaterial({color: '#c9a24e', roughness: 0.6});
    const skin = new THREE.MeshStandardMaterial({color: '#ece8e2', roughness: 0.55});
    const ground = new THREE.MeshStandardMaterial({
      color: '#e6e2db',
      roughness: 1,
      map: T.concrete_diff ? texClone(T.concrete_diff, 4300, 4300) : null,
      normalMap: T.concrete_nor ? texClone(T.concrete_nor, 4300, 4300) : null,
      roughnessMap: T.concrete_rough ? texClone(T.concrete_rough, 4300, 4300) : null,
    });
    if (ground.map) ground.map.colorSpace = THREE.SRGBColorSpace;
    ground.normalScale.set(0.45, 0.45);
    return {bill, stack, bundle, column, block, strap, skin, ground};
  }, [assets]);

  // ---------- geometries ----------
  const G = useMemo(() => {
    const bill = new THREE.PlaneGeometry(BL, BW, 24, 2);
    bill.rotateX(-Math.PI / 2);
    bill.rotateY(Math.PI);
    const pos = bill.attributes.position as THREE.BufferAttribute;
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i) / (BL / 2);
      pos.setY(i, 0.004 * x * x); // slight paper curl
    }
    bill.computeVertexNormals();
    const box = new THREE.BoxGeometry(1, 1, 1);
    box.translate(0, 0.5, 0); // origin at the bottom
    return {bill, box};
  }, []);

  // ---------- environment ----------
  useLayoutEffect(() => {
    if (!assets) return;
    if (assets.hdr) {
      scene.background = assets.hdr;
      scene.environment = assets.hdr;
      (scene as any).environmentIntensity = 0.7;
      (scene as any).backgroundIntensity = 1.0;
    } else {
      scene.background = new THREE.Color('#cfd9e3');
    }
    scene.fog = new THREE.Fog('#d7dee5', 140, 700);
    gl.toneMapping = THREE.ACESFilmicToneMapping;
    gl.toneMappingExposure = 1.0;
    gl.shadowMap.enabled = true;
    gl.shadowMap.type = THREE.PCFSoftShadowMap;
  }, [assets, scene, gl]);

  // ---------- camera ----------
  const pose = cameraAt(t);
  useLayoutEffect(() => {
    const cam = camera as THREE.PerspectiveCamera;
    cam.position.copy(pose.eye);
    cam.near = Math.max(0.005, pose.eye.distanceTo(pose.target) * 0.02);
    cam.far = 2000;
    cam.fov = pose.fov;
    cam.lookAt(pose.target);
    cam.updateProjectionMatrix();
  });

  // ---------- sun ----------
  const sun = useRef<THREE.DirectionalLight>(null);
  useLayoutEffect(() => {
    const L = sun.current;
    if (!L) return;
    const s = pose.shadowSize;
    L.position.copy(pose.target).addScaledVector(SUN, s * 3 + 2);
    L.target.position.copy(pose.target);
    L.target.updateMatrixWorld();
    const c = L.shadow.camera as THREE.OrthographicCamera;
    c.left = -s; c.right = s; c.top = s; c.bottom = -s;
    c.near = 0.01; c.far = s * 8 + 10;
    c.updateProjectionMatrix();
    L.shadow.bias = -0.00015;
    L.shadow.normalBias = 0.0004 * s;
    L.shadow.radius = 3;
  });

  // ---------- instanced: hero column (100 bundles) ----------
  const heroRef = useRef<THREE.InstancedMesh>(null);
  useLayoutEffect(() => {
    const m = heroRef.current;
    if (!m) return;
    let n = 0;
    for (let k = 0; k < 100; k++) {
      const land = k === 0 ? -1 : bundleLand(k);
      if (t < land - BUNDLE_FALL) continue;
      let y = k * BUNDLE_H;
      let tilt = 0;
      if (t < land) {
        const fall = land - t; // time left until impact
        y += 0.5 * 9.81 * fall * fall;
        tilt = 0.12 * fall;
      }
      const jx = (rand(k, 1) - 0.5) * 0.003, jz = (rand(k, 2) - 0.5) * 0.0024, yaw = (rand(k, 3) - 0.5) * 0.035;
      const sq = squash(t - land);
      tmpE.set(tilt, yaw + tilt * 0.7, tilt * 0.4);
      tmpQ.setFromEuler(tmpE);
      tmpP.set(BL / 2 + jx, y, BW / 2 + jz);
      tmpS.set(BL, BUNDLE_H * sq, BW);
      tmpM.compose(tmpP, tmpQ, tmpS);
      m.setMatrixAt(n, tmpM);
      m.setColorAt(n, new THREE.Color().setScalar(0.94 + rand(k, 4) * 0.1));
      n++;
    }
    m.count = n;
    m.instanceMatrix.needsUpdate = true;
    if (m.instanceColor) m.instanceColor.needsUpdate = true;
  });

  // ---------- instanced: 999 columns ----------
  const colRef = useRef<THREE.InstancedMesh>(null);
  useLayoutEffect(() => {
    const m = colRef.current;
    if (!m) return;
    let n = 0;
    for (let k = 0; k < CELLS.length; k++) {
      const land = colLand(k);
      if (t < land - COL_FALL) continue;
      const {i, j} = CELLS[k];
      let y = 0, tilt = 0;
      if (t < land) {
        const fall = land - t;
        y = 0.5 * COL_G * fall * fall;
        tilt = (rand(k, 5) - 0.5) * 0.12 * fall;
      }
      const yaw = (rand(k, 6) - 0.5) * 0.02;
      const sq = squash(t - land);
      tmpE.set(tilt, yaw, tilt * 0.6);
      tmpQ.setFromEuler(tmpE);
      tmpP.set(i * PX + BL / 2 + (rand(k, 7) - 0.5) * 0.002, y, j * PZ + BW / 2 + (rand(k, 8) - 0.5) * 0.002);
      tmpS.set(BL, COL_H * sq, BW);
      tmpM.compose(tmpP, tmpQ, tmpS);
      m.setMatrixAt(n, tmpM);
      m.setColorAt(n, new THREE.Color().setScalar(0.93 + rand(k, 9) * 0.12));
      n++;
    }
    m.count = n;
    m.instanceMatrix.needsUpdate = true;
    if (m.instanceColor) m.instanceColor.needsUpdate = true;
  });

  // ---------- instanced: 935 more $1B blocks ----------
  const blockRef = useRef<THREE.InstancedMesh>(null);
  const HX = Math.floor(BLOCKS_X / 2), HZ = Math.floor(BLOCKS_Z / 2);
  useLayoutEffect(() => {
    const m = blockRef.current;
    if (!m) return;
    let n = 0;
    if (t >= SHOTS.G) {
      for (let ix = 0; ix < BLOCKS_X; ix++)
        for (let iz = 0; iz < BLOCKS_Z; iz++) {
          if (ix === HX && iz === HZ) continue;
          const x = (ix - HX) * (BLOCK_W + BLOCK_GAP), z = (iz - HZ) * (BLOCK_D + BLOCK_GAP);
          const start = blockRise(Math.hypot(x, z) * 0.7) + rand(ix * 53 + iz, 11) * 0.15;
          const u = (t - start) / 0.45;
          if (u <= 0) continue;
          const s = clamp(easeOut(u, 3) + 0.08 * Math.sin(clamp(u) * Math.PI) * (1 - clamp(u)), 0, 1.1);
          tmpQ.identity();
          tmpP.set(x + BLOCK_W / 2, 0, z + BLOCK_D / 2);
          tmpS.set(BLOCK_W, COL_H * Math.max(0.001, s), BLOCK_D);
          tmpM.compose(tmpP, tmpQ, tmpS);
          m.setMatrixAt(n, tmpM);
          n++;
        }
    }
    m.count = n;
    m.instanceMatrix.needsUpdate = true;
  });

  if (!assets || !M) return null;

  // ---------- shot A/B: single bill, stack, falling bills, strap ----------
  const billEls: React.ReactNode[] = [];
  if (t < SHOTS.C) {
    const n = billsLanded(t);
    if (n <= 1) {
      // the first bill flutters down
      const u = clamp(t / BILL1_LAND);
      const y = BT + 0.06 * Math.pow(1 - u, 1.6);
      const wob = (1 - easeOut(u, 2));
      billEls.push(
        <mesh key="b1" geometry={G.bill} material={M.bill} castShadow receiveShadow
          position={[BL / 2 + 0.02 * wob * Math.sin(t * 5), y, BW / 2 + 0.012 * wob * Math.cos(t * 4)]}
          rotation={[0.5 * wob * Math.sin(t * 7.5), 0.6 * wob, 0.35 * wob * Math.sin(t * 6 + 1)]} />,
      );
    } else {
      const h = n * BT;
      billEls.push(<mesh key="stack" geometry={G.box} material={M.stack} castShadow receiveShadow position={[BL / 2, 0, BW / 2]} scale={[BL, h, BW]} />);
    }
    // bills in the air
    for (let k = 1; k <= 99; k++) {
      const land = billLand(k);
      if (t < land - BILL_FALL || t >= land) continue;
      const p = (land - t) / BILL_FALL; // 1 -> 0
      const y = k * BT + 0.11 * Math.pow(p, 1.3);
      const sx = (rand(k, 12) - 0.5) * 0.05 * p, sz = (rand(k, 13) - 0.5) * 0.03 * p;
      billEls.push(
        <mesh key={'f' + k} geometry={G.bill} material={M.bill} castShadow
          position={[BL / 2 + sx, y, BW / 2 + sz]}
          rotation={[0.6 * p * Math.sin(k + t * 9), (rand(k, 14) - 0.5) * 1.2 * p, 0.45 * p * Math.sin(k * 2 + t * 8)]} />,
      );
    }
    // the strap wraps the finished bundle
    if (t >= STRAP_T) {
      const u = easeOut((t - STRAP_T) / 0.18, 3);
      const h = 100 * BT;
      billEls.push(
        <mesh key="strap" geometry={G.box} material={M.strap} castShadow
          position={[BL / 2, -0.0002, BW / 2]} scale={[0.032 * u, h + 0.0006, BW + 0.0008]} />,
      );
    }
  }

  // ---------- person (walks in, then idles) ----------
  const person = t >= PERSON_IN - 2.2 && t < SHOTS.G + 2 ? <Person t={t} mat={M.skin} /> : null;

  return (
    <>
      <directionalLight ref={sun} intensity={3.3} color="#fff2e0" castShadow
        shadow-mapSize-width={4096} shadow-mapSize-height={4096} />
      <hemisphereLight args={['#dfe9f5', '#b9b2a6', 0.25]} />
      <mesh geometry={G.box} material={M.ground} receiveShadow position={[0, -0.02, 0]} scale={[3000, 0.02, 3000]} />
      {billEls}
      {t >= SHOTS.C ? (
        <instancedMesh ref={heroRef} args={[G.box, M.bundle, 100]} castShadow receiveShadow />
      ) : null}
      {t >= DROP - 0.5 ? <instancedMesh ref={colRef} args={[G.box, M.column, CELLS.length]} castShadow receiveShadow /> : null}
      {t >= SHOTS.G ? <instancedMesh ref={blockRef} args={[G.box, M.block, BLOCKS_X * BLOCKS_Z]} castShadow receiveShadow /> : null}
      {person}
    </>
  );
};

// ---------- a clean matte mannequin, 1.75 m ----------
const Limb: React.FC<{a: [number, number, number]; len: number; r: number; rot: [number, number, number]; mat: THREE.Material}> = ({a, len, r, rot, mat}) => (
  <group position={a} rotation={rot}>
    <mesh material={mat} castShadow receiveShadow position={[0, -len / 2, 0]}>
      <capsuleGeometry args={[r, Math.max(0.001, len - 2 * r), 6, 14]} />
    </mesh>
  </group>
);

const Person: React.FC<{t: number; mat: THREE.Material}> = ({t, mat}) => {
  // walk path: from screen-left toward the stack, stop beside it, turn to camera
  const end = new THREE.Vector3(0.55, 0, -0.3);
  const dir = new THREE.Vector3(-0.82, 0, 0.57).normalize();
  const walkDist = 1.9;
  const t0 = PERSON_IN - 2.2, t1 = PERSON_IN;
  const u = clamp((t - t0) / (t1 - t0));
  const eased = 1 - Math.pow(1 - u, 1.6); // decelerate into the stop
  const pos = end.clone().addScaledVector(dir, -walkDist * (1 - eased));
  const walking = u < 1;
  const phase = (t - t0) * 7.2 * (walking ? 1 : 0);
  const stride = walking ? 0.42 * (1 - Math.pow(u, 4)) : 0;
  const swing = Math.sin(phase) * stride;
  // heading: face walking direction, then turn toward camera
  const walkYaw = Math.atan2(dir.x, dir.z);
  const faceYaw = Math.atan2(-0.6, -0.8);
  const turn = smooth((t - t1) / 0.6);
  const yaw = walkYaw + (faceYaw - walkYaw) * turn;
  const bob = walking ? Math.abs(Math.cos(phase)) * 0.025 * stride * 2 : 0;
  const breathe = Math.sin(t * 2.1) * 0.004;
  const hipY = 0.9 + bob;
  return (
    <group position={pos} rotation={[0, yaw, 0]}>
      {/* legs */}
      <Limb a={[-0.09, hipY, 0]} len={0.88} r={0.058} rot={[swing, 0, 0.02]} mat={mat} />
      <Limb a={[0.09, hipY, 0]} len={0.88} r={0.058} rot={[-swing, 0, -0.02]} mat={mat} />
      {/* pelvis + torso */}
      <mesh material={mat} castShadow position={[0, hipY + 0.05, 0]} scale={[1, 0.6, 0.75]}>
        <sphereGeometry args={[0.15, 20, 14]} />
      </mesh>
      <mesh material={mat} castShadow position={[0, hipY + 0.32 + breathe, 0]} scale={[1.18, 1, 0.6]}>
        <capsuleGeometry args={[0.165, 0.3, 6, 18]} />
      </mesh>
      {/* arms */}
      <Limb a={[-0.255, hipY + 0.53, 0]} len={0.62} r={0.045} rot={[-swing * 0.8, 0, 0.09]} mat={mat} />
      <Limb a={[0.255, hipY + 0.53, 0]} len={0.62} r={0.045} rot={[swing * 0.8, 0, -0.09]} mat={mat} />
      {/* neck + head */}
      <mesh material={mat} castShadow position={[0, hipY + 0.62, 0]}>
        <cylinderGeometry args={[0.045, 0.05, 0.08, 12]} />
      </mesh>
      <mesh material={mat} castShadow position={[0, hipY + 0.76 + breathe, 0.005]} scale={[0.88, 1.08, 0.98]}>
        <sphereGeometry args={[0.105, 24, 18]} />
      </mesh>
    </group>
  );
};
