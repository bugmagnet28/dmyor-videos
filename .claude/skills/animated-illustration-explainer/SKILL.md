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
2. `python3 .claude/skills/animated-illustration-explainer/scripts/make_reel.py reels/<slug> --record` (`--skip-voice` reuses audio.mp3 + cues.json after picture fixes) (`--package YYYY-MM-DD` creates `ready-to-post/<date>-<slug>/`).
   **Final voice (owner 2026-10-28): ElevenLabs Adam.** Kokoro builds are drafts. Write the one-take script with `python3 studio/tools/v3_script.py reels/<slug>` (v3 audio tags, Dmyor → Deem-yor, a pause after questions), Sanyam generates the take, then `make_reel.py reels/<slug> --vo <take.mp3> --record`: the take is trimmed, aligned with whisper, and every cue/scene/sound re-times to it (the Kokoro audio is kept as audio-kokoro.mp3).
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
- `pencil` is a soft pen (band-limited strokes, owner 2026-10-27: never a scratchy pencil).
- Object sounds: `clock` (tick-tock while a clock is on screen), `timer` (fast ticking while a timer runs), `beep2` (timer passes the limit), `pencil` (crossing out, writing; give a duration), `page` (calendar or page flip), `riffle` (pages counting up), `footsteps` (a person walking), `plate` (gym weight clink), `stamp` (archiving), `coin` (money landing), `typing` (keyboard, bed), `buzz` (phone vibrating), `door` (door closing), `toggle` (switch on).
- Feedback sounds: `right` (every check mark / done: a soft two-note "correct" chime that steps up in pitch along a run of checks in the same scene) and `pop` (anything appearing: cards, chips, rows; pitch varies per item). Never reuse one sound for everything: checks = right, appearing = pop, objects = their own sound.
- New 2026-10-29: `alarm` (bedside alarm), `sizzle` (pan, fades), `chop` (knife on board), `reveal` (the ONE payoff sound per reel, Content Kit v2; `before-after` and `sketch-progress:final` use it).
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
| `fit-breakdown` | goal → program → 5-6 day chips (centred; `stage: draw` swaps the plate clink for pen sounds) → today (Chest) highlighted → today's exercises tick off | `goal`, `program`, `days[[day,name]]`, `today[3]` |
| `fifteen-test` | timer runs past the limit (red, "too big"), the step splits into 3, timer resets green ("start now") | `minutes`, `over`, `small`, `step`, `parts[3]` |
| `weather-week` | week of sunny days ticked, one cloudy day crossed, the rest fade (hook) | `bad`, `days` |
| `energy-dip` | energy line dips; checks stop at the bad day, the rest of the week fades | cue: plans / bad / falls apart |
| `habit-split` | one habit branches into "Full version" (sun) and "Bad-day version" (cloud) | `habit`, `full`, `small`; cue x3 |
| `two-versions` | title, FULL card vs BAD DAY card, bad-day card gets the check | `title`, `full`, `small`; cue x4 |
| `chain-switch` | "Skip" chain breaks, "Switch" chain holds with one thin link | cue: skip / switch |
| `skip-vs-switch` | two weeks: switch (small check, week survives) vs skip (bad week) | cue x2 |
| `goal-tree` | vision → 3 milestones → 3 actions + TODAY; `stage`: all (hook), vision (+ two people talking), milestones, actions, path (today lit up to the vision) | `vision`, `tag`, `milestones`, `actions`, `m`, `today`, `say1/2` |
| `math-split` | total counts up, "÷ per day", grid of days fills, "= N days" | `total`, `per`, `unit`, `milestone`, optional `prefix` ($), `cells`, `cols`, `cellLabels`, `perText`, `resText`; cue x4 |
| `flashcards` | big vague goal struck through, flashcard stack flips through N cards, "about 15 min" | `big`, `n`, `words`, `time`; cue x4 |
| `progress-bars` | three labelled bars fill (count, milestone %, vision %) | `rows`; cue x3 |
| `date-chase` | START note jumps Monday → 1st → January, each date crossed out; `stage`: hook / chase | `dates`, `note`; cue x4 |
| `same-you` | Today vs Monday: same goal, same doubts, Monday's time bar shorter | `a`, `b`; cue x4 |
| `cv-step` | 15-min timer, goal card, a document with one section highlighted and written in | `goal`, `doc`, `sections`, `hi`, `minutes`; cue x4 |
| `day-streak` | tonight / day 2-4 steps ticked, Monday card "Not day one" | `days`, `label`; cue x3 |
| `date-vs-step` | calendar date fades, "First step: done, today" card gets the check | `day`, `num`, `step`, `when`; cue x4 |
| `proof-to-motivation` | ticked tiles stack up a rising curve, label turns proof into motivation | `a`, `b` |
| `night-list` | "TOMORROW" note card (moon), 3 items written on with a pencil reveal, the goal item moves to the top with a FIRST tag and a time; `stage`: hook (finished) / write (+ optional `timer` chip) / first (pre-written, reorders) / all | `items[3]`, `first`, `when`, `title`, `timer`; cue: write x2 / first x2 / all x3 |
| `morning-drift` | 7-10 AM rows; distraction tiles (Emails, Phone, Messages) take the slots and push the goal card down to "later..." | `goal`, `tiles[3]`, `hours`; cue x3 |
| `ready-desk` | laptop draws on, a document opens with a blinking cursor, sticky note "7:00 start here" | `doc`, `time`, `note`; cue x3 |
| `day-done` | day schedule cards; the first (goal) block is ticked, busy blocks pile in and dim, label "done before the day gets busy" | `rows[[time,label]]`, `label`; cue x2 |
| `outcome-line` | "morning weigh-in" display + a jagged 14-day line the dot follows, digits change; red "nothing's working" cross; `stage`: hook (finished) | `values`, `unit`, `label`, `days`, `quit`; cue x3 |
| `outcome-vs-input` | OUTCOME card (can't control, dims) vs INPUT card (you control, sage + check) | `outcome[2]`, `input[2]`; cue x3 |
| `input-week` | M-S grid rows of input ticks with live counters ("5 / 5") | `rows[[label,[day idx]]]`; cue per row |
| `goal-date` | goal card "Get fit" with an empty date slot (blinking caret); `stage`: hook (finished) / rewrite (pencil strike, new goal typed, date chip stamped) / done (+ THIS WEEK card ticked) | `old`, `neu`, `date`, `week`, `label`; cue rewrite x3 / done x2 |
| `week-countdown` | "N weeks" counts up, week columns W1..WN with the end date, W1 lit, THIS WEEK panel with 3 ticked rows | `weeks`, `end`, `rows[3]`; cue x3 |
| `month-leftover` | payday balance line drops through expense chips to $0 by day 30, "Saved this month $0"; `stage`: hook | `items[[label, amount, x 0-1]]`, `save`; cue x4 |
| `pay-order` | "Spend → Save what's left" struck out, "Save first → Spend what's left" ticked | `a`; cue x3 |
| `auto-transfer` | Checking (Payday) → Savings, a $ coin travels every 1.7 s and the savings balance grows, "Every month" toggle switches on | `amount`, `when`; cue x4 |
| `bank-form` | phone with a recurring-transfer form: rows appear, amount typed, repeat row, Confirm fills + check, 5-min timer | `amount`, `repeat`, `title`, `minutes`; cue x4 |
| `course-vs-talk` | hook: dimmed COURSE card vs FIRST: 3 conversations card (heads breathing) | `course`, `months` |
| `course-cost` | course card "Month 1 of 6" bar fills, "+ fees" chip, "What's a normal Tuesday like?" bubble, still unknown | `course`, `months`, `q`; cue x3 |
| `three-people` | YOU + three people doing the job, dashed links, "3 of 3 this week" | `roles[3]`, `label`; cue x2 |
| `people-search` | search bar typed, 3 result rows (one "friend of a friend"), ticked | `query`, `results[[role, source]]`; cue x3 |
| `message-send` | phone chat: message typed line by line, sent, Delivered, counter 1/3 → 3/3 | `lines[3]`, `to`; cue [start, -, send] |
| `question-list` | notepad, 3 questions written with a pencil reveal, each ticked | `items[3]`, `title`; cue x3 |
| `phone-desk` | laptop with a blinking cursor, phone buzzing on the desk, "1 second" arc; `stage`: hook | `label`; cue x2 |
| `phone-room` | the phone goes into another room, the door closes, laptop timer counts down from 25:00 | `room`, `minutes`; cue [phone, timer, door] |
| `phone-walk` | footsteps from the desk to the closed door, "the pause", work line keeps growing + check | `room`, `label`; cue x3 |
| `two-blocks` | two task cards (task, amount, "phone: kitchen") with 25-min rings filling and ticks | `rows[[task, amount, phone]]`; cue x2 |
| `break-timer` | focus ring runs out, beep, 5-min BREAK ring, "Go again" back to 25:00 | `label`; cue x3 |
| `room-pick` | three room doors, one picked + check, note "Tomorrow, first block: phone goes to the kitchen" | `rooms[3]`, `pick`, `note`; cue x3 |
| `when-question` | TODAY'S WORKOUT card with a blinking "When?" slot, DAY 1 → DAY 4 counter, excitement bar drains; a "maybe tomorrow" chip fills the slot | `what`, `mood`, `bar`; cue x3 |
| `meeting-card` | calendar NEW EVENT card: title typed with caret, time + repeat rows, reminder toggle on, "Saved, like a meeting" | `title`, `rows[2]`, `remind`; cue x2 |
| `gym-calendar` | MON-SUN columns with 7:00 session blocks; `stage`: add (blocks pop in), decide (`hi` days light up, `rest` labels, note), move (`move`:[block, to day], missed X then slides), ticks (each block ticked, "3 of 3 this week") | `blocks[[day,time,label]]`, `note`; cue per beat |
| `shelf-year` | "10 pages × 365 nights = 3,650 pages ÷ 300" and 12 book spines appearing on a shelf, "= 12 books a year" (hook) | `a`, `b`, `c`, `label`, `books` |
| `pillow-book` | bed line art, book drops onto the pillow, page counter 0 → 10 / 10, phone on the side "later", order chips "1. Ten pages / 2. Then the phone", optional `note` card | `note`; cue [book, pages, phone, note] |
| `page-log` | PAGES READ log rows ticked, Book 1 progress bar, "12 books: far away" dims vs "Tonight: 10 pages" ticked | `rows[[day,n]]`, `goal`; cue x3 |
| `vague-list` | TO DO notepad, vague items written on with "?" each, phone slides in "picks this" and the list dims (hook-safe) | `items[3]`, `phone`; cue x4 |
| `rewrite-task` | vague task struck out, the next action written in with the verb in sage + "verb" tag, "Done = ..." card ticked | `old`, `neu`, `done`; cue x3 |
| `list-rewrite` | three cards: vague item struck, next action written, ticked | `rows[[old,new]]`; cue x3 |
| `done-test` | "Work on website" + dashed "done = ?" frame crossed vs "Write the headline" + a page with a headline drawn, ticked; note "Can't picture done? Split it again." | `vague`, `clear`, `note`; cue x3 |
| `budget-vs-cap` | dim 20-row budget sheet vs one "Food delivery $40 a week" cap card with a ring (hook) | `rows`, `left`, `cap`, `amt`, `per` |
| `budget-sheet` | spreadsheet rows typed in with amounts, then the sheet greys and "Last opened: 9 days ago" | `rows[[label,amt]]`, `title`, `chip`; cue [start, stop] |
| `bank-scroll` | phone transaction list scrolls, one category highlighted in sage, counter adds it up | `hl`, `total`; cue [open, scroll, add] |
| `cap-math` | Last month $240 → weekly cap $40 → 4 weeks $160 → Kept $80, coin drops into a jar | `month`, `cap`, `weeks`; cue x4 |
| `week-cap` | SUNDAY CHECK: week bars against a dashed cap line, WIN under the cap, overflow in clay, next week "starts at $0" | `cap`, `max`, `w1`, `w2`; cue [w1, win, w2, zero] |
| `leak-pick` | 4 spending chips, one picked ("JUST ONE" + check), others dim | `items[4]`, `pick`; cue [items, one] |
| `resume-vs-line` | dim resume page vs ONE SENTENCE card written in (hook) | `line`, `left` |
| `ramble-bubble` | two people, speech bubble: job title, then rambling lines, "Forgotten by lunch" | `title`, `lines[3]`, `note`; cue x3 |
| `pitch-template` | WHO / WHAT / PROOF rows; blank dashed slots, or filled with `who`/`what`/`proof` written in on cue | `who`, `what`, `proof`; cue x3 |
| `pitch-places` | the sentence typed into a profile headline, resume top and a message | `line`; cue x3 |
| `say-back` | long pitch (word count) → friend garbles it → struck, short version, friend repeats it, check | `long`, `short`, `n0`, `n1`, `garble`, `back`; cue x3 |
| `practice-bars` | TIMES PLAYED bars per song section, hard section in clay; `stage` hook (finished) / replay (playhead restarts at the hard part, counts grow) | `sections[[name,count,hard]]`; cue x3 |
| `loop-zoom` | 8 bars of notation, 4 bracketed with a loop arrow, the rest dim, "Practise only this" | `from`, `to`, `start`, `label`; cue x2 |
| `tempo-loop` | swinging metronome (bpm), 10 clean-rep checks, bpm nudges up, "10 minutes, then the whole song" | `bpm[2]`, `n`, `timer`; cue x4 |
| `voice-record` | vocab lesson chip struck, phone records 1:00 with a live waveform, M-S ticks | `drop`, `prompt`; cue x3 |
| `easy-hard` | two effort gauges: "Feels easy = rehearsing" (dim) vs "Feels hard = improving" (sage + check) | `a`, `ar`, `b`, `br`; cue x2 |
| `recipe-saved` | phone "Saved 214" grid of recipe tiles scrolling + COOKED 0 card; `stage` hook / tuesday (clock 7:00 → 7:20 PM, "Toast. Again." card) | `count`, `names`, `day`, `result`; cue [scroll, twenty, toast] |
| `cost-tally` | (structure C) notepad rows [label, amount] pencilled in, sum line, total counts up in clay, optional note card | `rows`, `total`, `unit`, `title`, `totalLabel`, `note`; cue [rows, total, note] |
| `pick-three` | 3x3 grid of options, three light up with checks, others dim, tag chip | `items[9]`, `pick[3]`, `tag`; cue [items, pick, tag] |
| `before-after` | (payoff) BEFORE column (mute) → arrow → AFTER column (sage) with 3 rows; plays the reel's one `reveal` payoff sound | `rows[[label,before,after]]`, `a`, `b`; cue [before, after] |
| `rule-card` | (save moment) "SCREENSHOT THIS" card, title, 3 numbered lines with checks | `title`, `items[3]` (≤ 20 chars), `tag`; cue x3 |
| `struck-card` | "BEDTIME 11:00 PM" card struck out, dashed "?" card (open loop) | `a`, `aBig`, `b`; cue [?, strike] |
| `sketch-progress` | paper portrait drawn in pencil; `stage` blank (+ `chips`), muddy (clay hatching, "Muddy", then redone neat + `fix` chip), final (time-lapse, frame, `count` chip, reveal) | cue: blank x2 / muddy [shading, quit, again] / final [frame, count] |
| `sketch-session` | alarm clock rings (6:40 AM), 20:00 timer, sketchbook circles drawn, cost chip | `time`, `label`, `cost`; cue [timer, draw, cost] |
| `wake-chart` | wake-up time per day M-S; `stage` hook (jagged + alarm + "+3 h"), jagged (points, bracket, chip), flat (morph to 7:30), weekend (+1 h band, "not 10") | `jag`, `chip`, `chipRed`; cue per beat |
| `curtain-light` | curtains open, sun rises, light on the floor, coffee mug, "Daylight within 10 minutes" chip | `chip`; cue [curtains, coffee] |
| `follow-next` | (follow reason) "NEXT ON @BECAUSEIDMYOR" card: next reel title + when, Follow button turns "Following" | `title`, `when`; cue [null, follow] |
| `dream-to-steps` | "ARCHIVED TODAY" dream card branching into three ticked steps (use for the value close) | `tag`, `dream`, `date`, `steps[3]` |

**Cues**: `params.cue` lists the spoken word that triggers each animation beat (null = default); `make_reel.py` resolves them to `params.at`, and `events.json` can time sounds as `"@i"` / `"@i+0.3"`, so picture and sound land on the voice. Prefer cues over fixed times for any new scene.

Each scene is `function(group, params) -> render(k, t)` (`t` = seconds since the scene started). New scenes follow the same rules: thin strokes (3-6 px), panels `PANEL`/`LINE`, accent `ACC` only for the point, `RED` (warm clay) only for "wrong/too big", `eio`/`eout` easing only, and keep something resolving for the whole thought (no scene that finishes in 2 s and then sits empty for 4).

## Script rules
- Hook, explain why, worked example, the method, a second example from another life area, a test or rule they can apply, land the point, value close, link line.
- Every example must pass the logic check (would a sceptical adult agree this helps?). The big plan is never the villain: show it as a level of the breakdown (get fit → 6-day gym program → today: chest day).
- Headlines: max ~8 words, no em dashes.

## Files
`assets/illustrated.html` (engine + scenes), `assets/fonts/`, `scripts/make_reel.py`, `scripts/say.py`, `scripts/sfx.py`, `assets/events.json`, `scripts/setup_tts.sh`, `examples/narration.example.json` ("You don't have a motivation problem", 56.7 s).
