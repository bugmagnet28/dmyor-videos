#!/bin/bash
# Footage -> frame sequences the page can draw frame-exact (run inside reels/<slug>).
#   x <name> <pexels id> <start s> <dur s> <speed>   (speed < 1 = slower, calmer)
# 1440x2560 so the push-in zoom (up to ~1.4x) stays sharp. Frames are gitignored.
set -e
x() { mkdir -p frames/$1; rm -f frames/$1/*.jpg
  ffmpeg -loglevel error -ss $3 -t $4 -i pex/v$2.mp4 -vf "setpts=PTS/$5,fps=30,scale=1440:2560:force_original_aspect_ratio=increase,crop=1440:2560" -q:v 4 frames/$1/%04d.jpg
  echo "$1 $(ls frames/$1 | wc -l)"; }
# x fork 40433618 4 7 1
