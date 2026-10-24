#!/usr/bin/env bash
# Legt Sounds aus public/sfx unter das stumme Hypit-Video.
set -euo pipefail
in="$1"; out="$2"; sfx="$3"
inputs=(-i "$in" -i "$sfx/game-show.wav")
filters="[1:a]volume=0.22,atrim=0:23,afade=t=out:st=21.5:d=1.5[bed]"
labels="[bed]"; n=2
add() { # datei sekunden lautstärke
  inputs+=(-i "$sfx/$1"); local ms; ms=$(python3 -c "print(int($2*1000))")
  filters+=";[$n:a]volume=$3,adelay=${ms}|${ms}[s$n]"; labels+="[s$n]"; n=$((n+1))
}
for base in 0 6.2 12.4; do
  add whoosh.wav "$(python3 -c "print(1.8+$base)")" 0.9
  for t in 3.27 4.38 5.49; do add tick.wav "$(python3 -c "print($t+$base)")" 1.0; done
  add ding.wav "$(python3 -c "print(6.6+$base)")" 1.0
done
add whoosh.wav 0.1 0.9
add ding.wav 20.4 0.8
filters+=";${labels}amix=inputs=$((n-1)):normalize=0,alimiter=limit=0.95[a]"
ffmpeg -y "${inputs[@]}" -filter_complex "$filters" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest "$out"
