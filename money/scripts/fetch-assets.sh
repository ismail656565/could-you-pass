#!/usr/bin/env bash
# Downloads CC0 assets from Poly Haven (https://polyhaven.com, CC0 licence) into public/env.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p public/env
get() { [ -s "$2" ] || curl -sSL --retry 3 -o "$2" "$1"; ls -la "$2"; }
get https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/4k/kloofendal_48d_partly_cloudy_puresky_4k.hdr public/env/sky.hdr
get https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/concrete_floor_02/concrete_floor_02_diff_2k.jpg public/env/concrete_diff.jpg
get https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/concrete_floor_02/concrete_floor_02_nor_gl_2k.jpg public/env/concrete_nor.jpg
get https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/concrete_floor_02/concrete_floor_02_rough_2k.jpg public/env/concrete_rough.jpg
