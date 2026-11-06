# Pixel series kit (Kabir vs. Kabir)

Reusable pixel-story pipeline, made from the pixel-destiny engine. One folder per episode (`reels/pixel-kabir-<n>/`) holds only
`lines.json` (narration), `episode.js` (scenes + EP config) and `make_audio.py` (object sounds). Everything else is shared here.

Build an episode (from the project root):
1. `tts/.venv/bin/python reels/pixel-series/build_audio.py reels/<ep>`: Kokoro voice per line, writes `audio.mp3`, `timeline.json`, `timeline.js`.
2. Write `episode.js`: scene functions `sX(u, a, b)` draw into the 270x480 world and return a camera (`camAt` keys). Set `SCENES` and `EP`
   (`badge`, `hook`, `hookEnd`, `endAt()`, `endQ`, `titles` = [text, from, to, y, block]). `whyScene` gives the series-question scene.
3. `python3 reels/pixel-series/make_page.py reels/<ep> "<title>"` then `EP=reels/<ep> node reels/pixel-series/snap.js 0 3 10 ...` and look at `snaps/`.
4. `tts/.venv/bin/python reels/<ep>/make_audio.py` (uses `sfxmix.py`: object sounds + CC0 room tone, no music).
5. `node record.js --page reels/<ep>/pixel.html --out reels/<ep>/<ep>.mp4 --audio reels/<ep>/audio_mixed.mp3 --fps 30`, then the CRF 24 upload copy.

Rules: every episode answers "Why do we stop doing things we know are good for us?" with the next "Reason #n" (card right after the hook),
45-55 s, sarcastic narrator, real mechanism shown as a picture, a concrete fix, ending loops to frame 0, comment question on the end card.
Scripts: `scripts-v1.md`. Next reason number: #4.
