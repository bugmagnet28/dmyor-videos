# Lemo-Opuscar: what we took and why

Source: https://github.com/lemomo-ai/lemo-opuscar (MIT, by Lemomo), commit 413a6bd, copied 2026-10-25.
Gallery: https://lemomo-ai.github.io/lemo-opuscar/ . Licence in `LICENSE`; keep it with anything we port, and credit "Lemo-Opuscar (MIT)" in code we adapt.

Only the parts useful to Dmyor reels are copied here: the directing and technique guides, the audio code (sfx, pluck, sampler), the text read-time checker, the style index, and 8 style prompts. The plugin itself is NOT installed (it is built for 16:9 scored films, 30-60 min each; we make 9:16 reels, no music, 3-5 a day).

## Same pipeline as ours
Page as a pure function of time, rendered frame by frame; Kokoro TTS + Whisper check; procedural foley driven by on-screen events (`window.EV`). Anything here drops into our skills.

## Plan (agreed with Sanyam 2026-10-25, in this order)
1. **Directing rules into `studio/quality-bar.md`** (from `DIRECTOR.md` sections 6, 7, 10, 11):
   - ambience bed under each scene, not only action foley; match the material (paper, wood, metal, glass)
   - at least two near-silences: before the turn and before the value close; the first sound after is an important one
   - sound as transition at least twice (J-cut / L-cut)
   - text hold time: after text animates in, hold about (letters / 15 + 1.5) s; subtitles at least 1.8 s; `core/render/readcheck.mjs` checks it
   - vary the pace: one acceleration or deceleration, one held breath
   - failure list: subject too small, colour on same colour, text over subject, gag too fast, blank transition frames
2. **Upgrade our sound kit** (`animated-illustration-explainer/scripts/sfx.py`) with the techniques in `core/audio/sfx.py`: scipy butterworth band/low/high-pass, compress + limit, pan; sounds click, clack, whoosh, thump, ding, pop, step, creak, brown-noise beds.
3. **New style skill: Dark Tech Keynote** (`styles/dark-keynote/STYLE.md`) adapted to 9:16 + Graphite & Sage, for Dmyor product/feature reels; replaces the weak hybrid demo style. Remake hybrid-create-vision with it.
4. **Then Whiteboard Explainer** (`styles/whiteboard/`) as a second explainer look, so the feed is not one style every day.
5. Later candidates: Pictogram Motion (list reels), Data Storytelling (number reels), Swiss Motion, Isometric Infographic, Living Screencast (app walkthrough with a mascot), One-line Drawing.

## Their pipeline for reference
- Render at our size with `--size 1080x1920` and lay out from innerWidth/innerHeight (`TECHNIQUE.md` 2).
- Mix: compress the voice first, then balance by RMS (voice about 10 dB over music); final file about -14 LUFS, check with ebur128 + blackdetect + Whisper (`TECHNIQUE.md` 6, 8).
- Make-your-own-style process: `MY-STYLES.md`.
