---
name: cinematic-motion
description: Premium cinematic motion film (target look - @anmoldoesmotion's OpenAI piece). One continuous camera where every scene becomes the next (cards converge into a point of light, threads spiral into a ring, a tunnel flashes into light, a card shrinks into a seed that grows into a tree), with depth blur, glow, frosted-glass UI over a calm sky, painted-paper textures, two-tone words. Narration (Kokoro am_eric) + a composed score (pads, plucks, risers, impacts, all synthesised) + sound design, voice ducks the score. 1080x1920, 30 fps, about 40 s. Use for brand films and flagship reels; first film - "One place" (reels/brand-one-place).
---

# Cinematic motion

Reference and beat sheet: `studio/analysis/2026-10-25-reference-anmoldoesmotion-openai.md`. Owner rules (`studio/quality-bar.md`) still apply: Graphite & Sage palette, logical content, value close, no em dashes. **Unlike the explainer styles, this one has a soundtrack** (owner, 2026-10-25: the reference has narration and a score, and so do we).

## Make a film
From `~/Documents/dmyor-videos`:
1. `reels/<slug>/narration.json`:
   - `spoken`: thoughts split by `||`, with stage tags;
   - optional texts: `dream`, `dreamShort`, `milestones[3]`, `steps[4]`, `archived`, `reopen`, `handle`;
   - `page`: defaults to `one-place.html`.
2. `tts/.venv/bin/python .claude/skills/cinematic-motion/scripts/make_film.py reels/<slug> --record`. Add `--skip-voice` to rebuild picture and sound without re-voicing. It writes:
   - `film.html`;
   - `config.json`, the beat times;
   - `score.wav`, `sfx.wav`, `audio_mixed.mp3`;
   - `film.mp4`.
3. Check frames with `node shots.js reels/<slug>/film.html <dir> <t...>` before recording (recording is about 6 min).

## How it is built
- **Beats come from spoken words** (`BEATS` in `make_film.py`: hook, notes, head, fade, turn, one, write, keeps, years, started, breakdown, milestones, steps, week, step1, grow, close, archive, tomorrow, breakit, link). Picture, score and sound effects all read the same beat times, so a new script with the same shape re-times itself. A different story needs a new page plus its own `BEATS`.
- **Page** (`assets/one-place.html`, canvas 2D):
  - scene A: dreams floating at depth, with blur by depth;
  - the point of light, then threads that close into a ring, then a tunnel and a white flash;
  - scene B: the glass card over the sky, with typing, an "Archived" seal and a reopen date;
  - scene C: the card becomes a seed and a tree grows on paper, with milestone and step labels, leaves and blossoms;
  - scene D: the camera tilts up to the sky for the value close;
  - scene E: the wordmark builds on a grid.
  - Plates (sky, meadow, paper grain) are generated once at load.
- **Score** (`score()`):
  - D minor pad and drone with sparse "thought" plucks in the dark;
  - a riser into the point of light, then a whoosh and an impact into the light;
  - D major add9 once the scene is bright;
  - a G-A-Bm-G-A chord walk with a rising pluck arpeggio while the tree grows;
  - a warm resolve with bells on the wordmark.
  - Everything goes through a reverb, and the voice ducks the score (sidechain).
- **Sound effects** (`sfx()`): whooshes on every camera move, typing clicks, the stamp and correct chime on "keeps it", a clock on "years from now", a seed tap, a soft growth rustle, pops on labels and blossoms, the chime on "this week", and ticks as the letters land. Kit: `animated-illustration-explainer/scripts/sfx.py`.

## Checks
- Mix levels: voice about -15 dB RMS; score in pauses about 6-10 dB under it; opening and ending never silent. Final file about -14 LUFS.
- Frame checks:
  - frame 0 shows the finished hook;
  - text never sits on top of sharp cards;
  - no label leaves the frame;
  - transitions have no muddy or flat frames.
