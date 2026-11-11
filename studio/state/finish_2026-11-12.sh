#!/bin/bash
# Renders + packages ill-just-today and ill-mixed-practice (run 2026-11-11). Safe to re-run.
# Each reel waits for studio/state/ok_<slug> (scene check) up to 2 h, then renders anyway with a warning.
cd ~/Documents/dmyor-videos
D=2026-11-12
for s in ill-just-today ill-mixed-practice; do
  while pgrep -f "make_reel.py reels/$s" >/dev/null; do sleep 30; done
  n=0; while [ ! -f studio/state/ok_$s ] && [ $n -lt 240 ]; do sleep 30; n=$((n+1)); done; [ -f studio/state/ok_$s ] || echo "$(date +%T) WARNING: $s rendered without scene-check flag"
  if [ ! -s ready-to-post/$D-$s/video.mp4 ]; then
    echo "$(date +%T) rendering $s"
    caffeinate -i python3 .claude/skills/animated-illustration-explainer/scripts/make_reel.py reels/$s --skip-voice --record --package $D > reels/$s/record.log 2>&1
  fi
  ls -la ready-to-post/$D-$s/video.mp4 2>&1
done
mkdir -p studio/state/frames-$D
for s in ill-just-today ill-mixed-practice; do
  [ -s ready-to-post/$D-$s/video.mp4 ] && bash studio/tools/frames.sh ready-to-post/$D-$s/video.mp4 0 0.5 2 12 20 30 45 > studio/state/frames-$D/$s.txt 2>&1
done
python3 studio/tools/reel_library.py >/dev/null 2>&1
echo "$(date +%T) finisher done"
