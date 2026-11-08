#!/bin/bash
# Finishes the Mon Nov 9 batch renders if the run's own chain dies (session end). Safe to re-run.
cd ~/Documents/dmyor-videos
while pgrep -f "make_reel.py reels/ill-(out-of-sight|sunday-practice)" >/dev/null; do sleep 30; done
for s in ill-out-of-sight ill-sunday-practice; do
  if [ ! -s ready-to-post/2026-11-09-$s/video.mp4 ]; then
    echo "$(date +%T) rendering $s"
    caffeinate -i python3 .claude/skills/animated-illustration-explainer/scripts/make_reel.py reels/$s --skip-voice --record --package 2026-11-09 > reels/$s/record.log 2>&1
  fi
  ls -la ready-to-post/2026-11-09-$s/video.mp4 2>&1
done
mkdir -p studio/state/frames-2026-11-09
for s in ill-out-of-sight ill-sunday-practice; do
  [ -s ready-to-post/2026-11-09-$s/video.mp4 ] && bash studio/tools/frames.sh ready-to-post/2026-11-09-$s/video.mp4 0 0.5 2 12 20 30 45 > studio/state/frames-2026-11-09/$s.txt 2>&1
done
python3 studio/tools/reel_library.py >/dev/null 2>&1
echo "$(date +%T) finisher done"
