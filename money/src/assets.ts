import * as THREE from 'three';
import {RGBELoader} from 'three/examples/jsm/loaders/RGBELoader.js';
import {staticFile} from 'remotion';

export type Assets = {
  tex: Record<string, THREE.Texture>;
  hdr: THREE.DataTexture | null;
};

let cache: Promise<Assets> | null = null;

const TEX = ['bill_top', 'bundle_top', 'bundle_long', 'bundle_short', 'stack_long', 'stack_short'];
const GROUND = ['concrete_diff', 'concrete_nor', 'concrete_rough'];

function loadTex(url: string, srgb: boolean): Promise<THREE.Texture | null> {
  return new Promise((res) => {
    new THREE.TextureLoader().load(
      url,
      (t) => {
        t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace;
        t.anisotropy = 8;
        res(t);
      },
      undefined,
      () => res(null),
    );
  });
}

export function loadAssets(): Promise<Assets> {
  if (cache) return cache;
  cache = (async () => {
    const tex: Record<string, THREE.Texture> = {};
    await Promise.all(
      TEX.map(async (n) => {
        const t = await loadTex(staticFile(`tex/${n}.png`), true);
        if (t) tex[n] = t;
      }),
    );
    await Promise.all(
      GROUND.map(async (n) => {
        const t = await loadTex(staticFile(`env/${n}.jpg`), n === 'concrete_diff');
        if (t) {
          t.wrapS = t.wrapT = THREE.RepeatWrapping;
          tex[n] = t;
        }
      }),
    );
    let hdr: THREE.DataTexture | null = null;
    try {
      hdr = await new RGBELoader().loadAsync(staticFile('env/sky.hdr'));
      hdr.mapping = THREE.EquirectangularReflectionMapping;
    } catch (e) {
      hdr = null;
    }
    return {tex, hdr};
  })();
  return cache;
}
