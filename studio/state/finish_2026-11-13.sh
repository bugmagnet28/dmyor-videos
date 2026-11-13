#!/bin/bash
cd ~/Documents/dmyor-videos
for pair in "ill-autopilot 2026-11-16" "ill-good-day 2026-11-17" "ill-middle 2026-11-17"; do set -- $pair
  echo "$(date +%T) start $1"
  python3 .claude/skills/animated-illustration-explainer/scripts/make_reel.py reels/$1 --skip-voice --record --package $2 > reels/$1/record.log 2>&1
  echo "$(date +%T) $1 exit $?"
done
echo DONE
