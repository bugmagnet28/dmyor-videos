#!/usr/bin/env bash
# Contact sheet of frames from a video so the agent can look at its own work.
#   studio/tools/frames.sh <video.mp4> <t1> [t2 ...]     -> prints path of a PNG
# Times in seconds. Frames are laid out left to right at 360x640 each.
set -euo pipefail
VID="$1"; shift
OUT="$(dirname "$0")/../state/frames_$(basename "${VID%.*}")_$(date +%H%M%S).png"
ARGS=(); FILTER=""; i=0
for t in "$@"; do ARGS+=(-ss "$t" -i "$VID"); FILTER+="[$i:v]scale=360:640,setsar=1[f$i];"; i=$((i+1)); done
INS=""; for ((k=0;k<i;k++)); do INS+="[f$k]"; done
ffmpeg -v error -y "${ARGS[@]}" -filter_complex "${FILTER}${INS}hstack=inputs=$i" -frames:v 1 "$OUT" 2>/dev/null \
  || ffmpeg -v error -y "${ARGS[@]}" -filter_complex "${FILTER}${INS}concat=n=$i:v=1:a=0" -frames:v 1 "$OUT"
echo "$OUT"
