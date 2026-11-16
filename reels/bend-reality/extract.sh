#!/bin/bash
# name src start dur speed  -> frames/<name>/0001.jpg ... (1080x1920 cover crop, 30 fps, slowed by 1/speed)
set -e
x() { mkdir -p frames/$1; rm -f frames/$1/*.jpg
  ffmpeg -loglevel error -ss $3 -t $4 -i pex/v$2.mp4 -vf "setpts=PTS/$5,fps=30,scale=1440:2560:force_original_aspect_ratio=increase,crop=1440:2560" -q:v 4 frames/$1/%04d.jpg
  echo "$1 $(ls frames/$1 | wc -l)"; }
x cosmos 16998437 0 9 0.5
x fork 40433618 4 7 1
x phone 7279035 2 11 1
x read 7062988 0 11.3 0.8
x bed 6943536 3 6 0.9
x wing 16865644 4 6 1
x cafe 8428492 8 4 1
x family 8524227 0.5 4.2 0.85
x summit 8644064 2 6 1
