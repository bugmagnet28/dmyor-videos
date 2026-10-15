#!/bin/bash
# resumable segmented record: each segment kept once valid
cd ~/Documents/dmyor-videos
R=reels/life-in-weeks
B=(0 3 6 9 12 15.2)
for i in 0 1 2 3 4; do
  o=$R/seg/s$i.mp4
  if ffprobe -v error -show_entries format=duration -of csv=p=0 $o >/dev/null 2>&1; then echo "s$i ok"; continue; fi
  caffeinate -dims node record.js --page $R/reel.html --out $o --start ${B[$i]} --end ${B[$((i+1))]} > $R/seg/s$i.log 2>&1 || { echo "s$i FAILED"; exit 1; }
  echo "s$i done $(date +%T)"
done
( for i in 0 1 2 3 4; do echo "file 's$i.mp4'"; done ) > $R/seg/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $R/seg/list.txt -c copy $R/seg/video.mp4 &&
ffmpeg -v error -y -i $R/seg/video.mp4 -i $R/audio_mixed.mp3 -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $R/reel.mp4 &&
ffprobe -v error -show_entries format=duration -of csv=p=0 $R/reel.mp4 && echo ALLDONE
