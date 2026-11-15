# Music library

Background music for reels, mixed quietly under the voice (owner 2026-11-15: Pixabay approved; plus a phone trending-audio test).

- `tracks/<mood>-NN.mp3`: the approved tracks. Moods: `playful` (Habit Roast, Kabir), `lofi` (Small Stories), `ambient` (Straight Answer).
- `LICENSES.md`: source page for every track (keep it updated when adding one).
- `candidates/`: everything downloaded for screening (not used directly). Tracks with vocals were dropped after a whisper check.
- Mixing: `reels/pixel-series/sfxmix.py` `Mix.write(music="playful")` picks a track for the reel (same reel = same track), starts it a few seconds in, loops if needed, ducks it under the voice and fades it out at the end. Level: about 20 dB under the voice; it lifts slightly in pauses.
- Every reel also keeps a no-music version (`video-nomusic.mp4`) for posts where Sanyam adds trending audio from the phone.
