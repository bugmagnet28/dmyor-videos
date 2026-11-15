# Music library

Background music for reels, mixed quietly under the voice (owner 2026-11-15: Pixabay approved; plus a phone trending-audio test).

- `tracks/<mood>-NN.mp3`: the approved tracks. Moods: `comedy`, `mystery`, `investigate`, `resolve` (see OWNER-RULES, Background music).
- `LICENSES.md`: source page for every track (keep it updated when adding one).
- `candidates/`: everything downloaded for screening (not used directly). Tracks with vocals were dropped after a whisper check.
- Mixing: `reels/pixel-series/sfxmix.py` `Mix.write(music=[(mood, start_s), ...])` builds an emotion arc: one track per section (same reel = same tracks), crossfaded at each turn, gently ducked under the voice (about 9-10 dB under while speaking, about 6 dB in pauses).
- Every reel also keeps a no-music version (`video-nomusic.mp4`) for posts where Sanyam adds trending audio from the phone.
