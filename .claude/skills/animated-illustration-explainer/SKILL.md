---
name: animated-illustration-explainer
description: Motion-graphics explainer where every spoken thought gets its own refined line-art scene (gauges, calendars, books, week trackers, timers, charts, an archived-dream card branching into steps) that animates in sync with the narration, with a short headline above it. Mature, classy motion (ease-in-out, small moves, thin strokes, no bounce or cartoon effects), Graphite & Sage palette, human-paced Kokoro voice am_eric with stage-aware delivery, no music, value close and dmyor brand card. 1080x1920, no duration cap (typically 35-55 s). Use for explaining an idea or method with worked examples, where each step deserves a picture.
---

# Animated illustration explainer

> Owner rules 2026-10-24 apply in full (`studio/quality-bar.md`): no duration cap, logical credible examples, value close, classy motion, Graphite & Sage, short gaps.

**What the viewer sees**
1. Frame 0: the hook scene already finished plus its headline (e.g. "Not motivation. A *size* problem." over a full motivation gauge next to a towering goal block).
2. One scene per spoken thought. Scenes crossfade (ease-in-out, 36 px drift); inside a scene, elements draw on (stroke-dash), count up, or slide a short distance. Nothing bounces, wobbles or sparkles.
3. Headline above each scene: short, 1-2 lines, one `<b>` word in sage. The voice says more than the headline (write for the ear).
4. The value sentence gets its own visual (`dream-to-steps`: "ARCHIVED TODAY" card branching into three ticked steps).
5. Brand card (`dmyor`, tagline, `@becauseidmyor`) only for the final "I've put the link in the bio".

## Make a reel
From `~/Documents/dmyor-videos` (voice setup once: `bash .claude/skills/animated-illustration-explainer/scripts/setup_tts.sh`).
1. `mkdir reels/<slug>`; copy `examples/narration.example.json` to `reels/<slug>/narration.json`; write `spoken` and `scenes`.
2. `python3 .claude/skills/animated-illustration-explainer/scripts/make_reel.py reels/<slug> --record` (`--package YYYY-MM-DD` creates `ready-to-post/<date>-<slug>/`).
3. Contact-sheet the frames (one per scene midpoint, plus frame 0 and the brand card), fix overlaps or empty stretches, show Sanyam, schedule only after his OK, register in `analytics/`.

## narration.json
| field | meaning |
|---|---|
| `spoken` | thoughts split by `||`, optional `[hook]/[turn]/[land]/[outro]` tags. Fuller, conversational. Write "Dmyor" (spoken DEEM-yor). |
| `scenes` | one per thought: `{type, params, head}` or `null` to keep the previous scene through that thought |
| `brand_from` | index of the first thought shown on the brand card (normally the last one, "link in the bio") |
| `gap_min` / `gap_max` | pauses between thoughts, default 0.18-0.32 s |
| `tagline`, `handle`, `caption` | brand card and `--package` captions |
| `palette` (optional) | override any of `bg ink mute acc acc2 warn ok panel line onAcc` |

## Sound design (`scripts/sfx.py`, `assets/events.json`)
Owner rule (2026-10-24): **objects sound like themselves**, at a clearly audible level (default `"present"`). Synthesized in code, no samples, no music.
- Object sounds: `clock` (tick-tock while a clock is on screen), `timer` (fast ticking while a timer runs), `beep2` (timer passes the limit), `pencil` (crossing out, writing; give a duration), `page` (calendar or page flip), `riffle` (pages counting up), `footsteps` (a person walking), `plate` (gym weight clink), `stamp` (archiving).
- Feedback sounds: `right` (every check mark / done: a soft two-note "correct" chime that steps up in pitch along a run of checks in the same scene) and `pop` (anything appearing: cards, chips, rows; pitch varies per item). Never reuse one sound for everything: checks = right, appearing = pop, objects = their own sound.
- Interface sounds, only where nothing above fits: `swish` (scene change), `ratchet` (abstract counter), `tone` (warm swell under the value close), `chord` (brand card).
- `events.json`: per scene type, `[seconds after scene start, sound, duration or "end"]`, mirroring the animation timings in `illustrated.html`: **change both together**, and give every new scene its object sounds.
- Hook scene is silent (finished on frame 0). One-shots closer than 0.28 s are dropped; beds (clock, timer, footsteps, riffle) may overlap. The voice ducks effects lightly. `"sfx"`: `"present"` (default), `"subtle"` (-6 dB), `"off"`. Outputs `audio_voice.mp3`, `audio_fx.wav` (effects alone, for checking), `audio_mixed.mp3`.

## Scene library (`assets/illustrated.html`, `SCENES`)
| type | shows | params |
|---|---|---|
| `gauge-vs-goal` | motivation gauge fills to 100% while a goal block grows far taller than the person | `left`, `right` |
| `postpone-calendar` | day after day, "start tomorrow" struck through and pushed on | `days`, `note` |
| `book-vs-evening` | 300-page stack counts up next to a clock on a weeknight | `pages`, `when` |
| `book-breakdown` | big item shrinks aside, sub-steps tick off, a daily-amount counter | `book`, `items[3]`, `per`, `unit` |
| `week-tracker` | 7-day grid, chosen days ticked, a person walks the line | `on` (day indexes), `what` |
| `fit-breakdown` | goal → program → 6 day chips → today (Chest) highlighted → today's exercises tick off | `goal`, `program`, `days[[day,name]]`, `today[3]` |
| `fifteen-test` | timer runs past the limit (red, "too big"), the step splits into 3, timer resets green ("start now") | `minutes`, `over`, `small`, `step`, `parts[3]` |
| `weather-week` | week of sunny days ticked, one cloudy day crossed, the rest fade (hook) | `bad`, `days` |
| `energy-dip` | energy line dips; checks stop at the bad day, the rest of the week fades | cue: plans / bad / falls apart |
| `habit-split` | one habit branches into "Full version" (sun) and "Bad-day version" (cloud) | `habit`, `full`, `small`; cue x3 |
| `two-versions` | title, FULL card vs BAD DAY card, bad-day card gets the check | `title`, `full`, `small`; cue x4 |
| `chain-switch` | "Skip" chain breaks, "Switch" chain holds with one thin link | cue: skip / switch |
| `skip-vs-switch` | two weeks: switch (small check, week survives) vs skip (bad week) | cue x2 |
| `goal-tree` | vision → 3 milestones → 3 actions + TODAY; `stage`: all (hook), vision (+ two people talking), milestones, actions, path (today lit up to the vision) | `vision`, `tag`, `milestones`, `actions`, `m`, `today`, `say1/2` |
| `math-split` | total counts up, "÷ per day", grid of days fills, "= N days" | `total`, `per`, `unit`, `milestone`; cue x4 |
| `flashcards` | big vague goal struck through, flashcard stack flips through N cards, "about 15 min" | `big`, `n`, `words`, `time`; cue x4 |
| `progress-bars` | three labelled bars fill (count, milestone %, vision %) | `rows`; cue x3 |
| `date-chase` | START note jumps Monday → 1st → January, each date crossed out; `stage`: hook / chase | `dates`, `note`; cue x4 |
| `same-you` | Today vs Monday: same goal, same doubts, Monday's time bar shorter | `a`, `b`; cue x4 |
| `cv-step` | 15-min timer, goal card, a document with one section highlighted and written in | `goal`, `doc`, `sections`, `hi`, `minutes`; cue x4 |
| `day-streak` | tonight / day 2-4 steps ticked, Monday card "Not day one" | `days`, `label`; cue x3 |
| `date-vs-step` | calendar date fades, "First step: done, today" card gets the check | `day`, `num`, `step`, `when`; cue x4 |
| `proof-to-motivation` | ticked tiles stack up a rising curve, label turns proof into motivation | `a`, `b` |
| `dream-to-steps` | "ARCHIVED TODAY" dream card branching into three ticked steps (use for the value close) | `tag`, `dream`, `date`, `steps[3]` |

**Cues**: `params.cue` lists the spoken word that triggers each animation beat (null = default); `make_reel.py` resolves them to `params.at`, and `events.json` can time sounds as `"@i"` / `"@i+0.3"`, so picture and sound land on the voice. Prefer cues over fixed times for any new scene.

Each scene is `function(group, params) -> render(k, t)` (`t` = seconds since the scene started). New scenes follow the same rules: thin strokes (3-6 px), panels `PANEL`/`LINE`, accent `ACC` only for the point, `RED` (warm clay) only for "wrong/too big", `eio`/`eout` easing only, and keep something resolving for the whole thought (no scene that finishes in 2 s and then sits empty for 4).

## Script rules
- Hook, explain why, worked example, the method, a second example from another life area, a test or rule they can apply, land the point, value close, link line.
- Every example must pass the logic check (would a sceptical adult agree this helps?). The big plan is never the villain: show it as a level of the breakdown (get fit → 6-day gym program → today: chest day).
- Headlines: max ~8 words, no em dashes.

## Files
`assets/illustrated.html` (engine + scenes), `assets/fonts/`, `scripts/make_reel.py`, `scripts/say.py`, `scripts/sfx.py`, `assets/events.json`, `scripts/setup_tts.sh`, `examples/narration.example.json` ("You don't have a motivation problem", 56.7 s).
