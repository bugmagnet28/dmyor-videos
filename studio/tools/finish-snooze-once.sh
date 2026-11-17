cd ~/Documents/dmyor-videos
while pgrep -f "render.sh roast-snooze" >/dev/null; do sleep 30; done
D=ready-to-post/2026-11-19-roast-snooze
if [ -f $D/video.mp4 ]; then
  cp reels/roast-snooze/post.md $D/post.md
  ffmpeg -loglevel error -y -i $D/video.mp4 -i reels/roast-snooze/audio_nomusic.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart $D/video-nomusic.mp4
  echo "packaged $(date)" > $D/PACKAGED-unchecked.txt
fi
