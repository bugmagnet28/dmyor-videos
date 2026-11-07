#!/bin/bash
# Render one pixel-series episode end to end (from the project root):
#   reels/pixel-series/render.sh <slug> "<title>" [review-dir]
# needs reels/<slug>/{lines.json,episode.js,make_audio.py}; voice must already be built (build_audio.py).
set -e
# one render at a time (parallel record.js runs clobber each other)
LOCK=/tmp/dmyor-pixel-render.lock; until mkdir $LOCK 2>/dev/null; do sleep 5; done; trap "rmdir $LOCK" EXIT
S=$1; T=$2; OUT=${3:-}
python3 reels/pixel-series/make_page.py reels/$S "$T" >/dev/null
tts/.venv/bin/python reels/$S/make_audio.py >/dev/null
caffeinate -i node record.js --page reels/$S/pixel.html --out reels/$S/$S.mp4 --audio reels/$S/audio_mixed.mp3 --fps 30 > reels/$S/record.log 2>&1
ffmpeg -loglevel error -y -i reels/$S/$S.mp4 -c:v libx264 -crf 24 -maxrate 1800k -bufsize 3600k -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart reels/$S/$S-upload.mp4
if [ -n "$OUT" ]; then mkdir -p "$OUT"; cp reels/$S/$S-upload.mp4 "$OUT/video.mp4"; fi
echo "rendered $S $(ffprobe -v error -show_entries format=duration -of csv=p=0 reels/$S/$S-upload.mp4)s $(du -h reels/$S/$S-upload.mp4 | cut -f1)"
