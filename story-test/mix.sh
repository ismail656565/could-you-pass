#!/usr/bin/env bash
# Stimme + leise Musik + Whoosh an jedem Szenenwechsel.
set -euo pipefail
video="$1"; voice="$2"; tim="$3"; sfx="$4"; out="$5"
dur=$(python3 -c "import json;print(json.load(open('$tim'))['end'])")
inputs=(-i "$video" -i "$voice" -i "$sfx/brain-pulse.wav")
f="[1:a]volume=1.0[v];[2:a]aloop=loop=-1:size=2e9,atrim=0:$dur,volume=0.16,afade=t=out:st=$(python3 -c "print($dur-1.5)"):d=1.5[m]"
labels="[v][m]"; n=3
for t in $(python3 -c "import json;print(' '.join(str(x) for x in json.load(open('$tim'))['starts'][1:]))"); do
  ms=$(python3 -c "print(int(max(0,$t-0.15)*1000))"); inputs+=(-i "$sfx/whoosh.wav")
  f+=";[$n:a]volume=0.35,adelay=${ms}|${ms}[w$n]"; labels+="[w$n]"; n=$((n+1))
done
f+=";${labels}amix=inputs=$((n-1)):normalize=0,alimiter=limit=0.95[a]"
ffmpeg -y "${inputs[@]}" -filter_complex "$f" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t "$dur" "$out"
