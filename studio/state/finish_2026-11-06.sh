#!/bin/bash
# Finishes the Nov 6 batch renders if the run's own chain dies (session end). Safe to re-run.
cd ~/Documents/dmyor-videos
while pgrep -f "make_reel.py reels/ill-(ten-minute-reset|same-weight)" >/dev/null; do sleep 30; done
for s in ill-ten-minute-reset ill-same-weight; do
  if [ ! -s ready-to-post/2026-11-06-$s/video.mp4 ]; then
    echo "$(date +%T) rendering $s"
    caffeinate -i python3 .claude/skills/animated-illustration-explainer/scripts/make_reel.py reels/$s --skip-voice --record --package 2026-11-06 >/dev/null 2>&1
  fi
  ls -la ready-to-post/2026-11-06-$s/video.mp4 2>&1
done
echo "$(date +%T) finisher done"
