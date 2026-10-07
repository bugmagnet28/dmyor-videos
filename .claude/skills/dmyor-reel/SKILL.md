---
name: dmyor-reel
description: End-to-end pipeline for dmyor social videos - write a script from a hint, log the audio settings, sync a pointer-driven animation to recorded narration, record the MP4, then track Instagram/YouTube performance and learn what improves reach. Use when the user asks for a dmyor reel, video, script, or wants to log/analyse reel performance.
---

# dmyor reel pipeline

Makes the vertical (1080x1920) pointer-driven explainers for dmyor, and gets better at
it over time by keeping every script, audio setting, post time and performance number
in `reels/`.

## The loop

```
1 SCRIPT   hint -> draft -> user edits -> final          (script.md)
2 AUDIO    user records elsewhere, drops the file        (audio.mp3 + audio.meta.json)
3 ALIGN    whisper word timings -> cue sheet             (cues.json)
4 TIMELINE map script beats onto scenes at real cues     (timeline.json)   <- your judgment
5 BUILD    timeline + engine -> playable page            (reel.html)
6 RECORD   frame-accurate capture + audio mux            (reel.mp4)
7 PUBLISH  log platform, time, caption                   (publish.json)
8 LEARN    enter metrics, read the report                (performance.json)
```

Steps 1-2 are a conversation. 3, 5, 6 are scripts. 4 is the part that needs you.
7-8 is how the next reel gets better.

## 1. Script from a hint

The user gives a hint ("phase two launch", "why standby matters", "founder story").
Read `references/script-craft.md` FIRST - it has the dmyor voice, the hook patterns
that have worked, and the structural rules. Then:

```bash
python3 .claude/skills/dmyor-reel/scripts/reel.py new "<slug>" --hint "<the hint>"
```

Draft 2-3 openings, not one. Show the user word count and the projected runtime at
their usual pace (`reel.py rate` prints the measured words/sec from past reels;
default 2.5). Iterate until they say it is final, then save to `reels/<slug>/script.md`.

Never invent product claims. If the hint implies a feature you cannot verify, ask.

## 2. Audio

The user records the VO themselves and drops it in the project. Ask for the file, then:

```bash
python3 .claude/skills/dmyor-reel/scripts/reel.py audio "<slug>" --file <path> \
  --voice "George" --provider elevenlabs --model eleven_multilingual_v2 \
  --stability 50 --similarity 75 --style 32 --speed 95
```

Those settings matter - `report.py` correlates them with retention. If the user does
not know a value, omit the flag rather than guessing.

## 3. Align (never estimate timings)

```bash
python3 .claude/skills/dmyor-reel/scripts/align.py reels/<slug>
```

Runs whisper with word timestamps and writes `cues.json`: every word with start/end,
plus a `phrases` map you can query. **Estimated timings are the single biggest cause
of a bad reel** - a previous cut was 3-5s out on every beat because the timings were
guessed. Always align against the real audio.

To find where a specific line lands:

```bash
python3 .claude/skills/dmyor-reel/scripts/align.py reels/<slug> --find "no magic diary"
```

## 4. Timeline (your judgment)

Read `references/animation-cookbook.md` for the scene library and what each scene is
*for*. Then write `reels/<slug>/timeline.json` mapping script beats to scenes at cue
times from `cues.json`.

Rules that came from things going wrong:
- **Every scene anchors to a spoken cue.** Put the cue text in the `note` field.
- **No dead air.** Any gap over ~4s with nothing new appearing reads as broken.
  Check with `reel.py gaps <slug>` after writing the timeline.
- **Cursor waypoints arrive then hold.** A sparse path interpolates into a slow
  drift; a dense path with holds looks deliberate.
- **Pin waypoints to the caret at typing-window edges**, or the pointer snaps
  hundreds of pixels when the override hands back.

## 5b. Sound effects (optional)

```bash
python3 .claude/skills/dmyor-reel/scripts/sfx.py reels/<slug> --dry   # list the cues
python3 .claude/skills/dmyor-reel/scripts/sfx.py reels/<slug>         # -> audio_mixed.mp3
```

Every hit is synthesised with ffmpeg, so there is no sample library to license and
nothing to download. **Cues are read from `timeline.json`, not placed by ear** - a
kinetic title gets a swish, a dismissal gets a strike, a collapse gets a downward
chirp, an arrival gets a chime. That means the sound lands on the animation by
construction, and it stays correct if you retime a scene and rebuild.

Then record against the mixed file:

```bash
node record.js --page reels/<slug>/reel.html --out reels/<slug>/reel.mp4 \
     --audio reels/<slug>/audio_mixed.mp3
```

`--gain` sets the bed under the voice. Default 0.32 puts it about 9dB below a -26dB
narration, which reads on a phone speaker. Check with:

```bash
ffmpeg -hide_banner -nostats -i <file> -af volumedetect -f null /dev/null 2>&1 | grep volume
```

The voice is never processed - only the bed is attenuated, then a limiter catches peaks.

## 5-6. Build and record

```bash
python3 .claude/skills/dmyor-reel/scripts/build.py reels/<slug>     # -> reel.html
node .claude/skills/dmyor-reel/scripts/verify.js reels/<slug>       # motion audit
node .claude/skills/dmyor-reel/scripts/overflow.js reels/<slug>/reel.html   # glyphs past frame edge
node .claude/skills/dmyor-reel/scripts/collide.js reels/<slug>/reel.html    # scenes overlapping
node .claude/skills/dmyor-reel/scripts/safearea.js reels/<slug>/reel.html   # under the Reels UI
node .claude/skills/dmyor-reel/scripts/capfit.js reels/<slug>/reel.html \\
     caps.json caps_placed.json                                           # auto-place captions
node record.js --page reels/<slug>/reel.html --out reels/<slug>/reel.mp4 \
     --audio reels/<slug>/audio.mp3
```

All three audits must come back clean before you record: `verify.js` **0 snaps, 0 origin
frames, no frozen frames**; `overflow.js` **no glyph overflow**; `collide.js` **no
scene-layer collisions**. Run the last two again after *any* font-size or copy edit:
enlarging type wraps lines and grows blocks into whatever scene shares the screen.

For a reel with no narration, skip alignment entirely: set `total` in `timeline.json`
by hand and build the soundtrack from the timeline with
`sfx.py reels/<slug> --no-vo`, which runs the effects bed at full level instead of
ducking it under a voice and pads it to `total`.

`probe.js reels/<slug>/reel.html <t>` dumps the computed size, weight and colour of
every visible text run at time `t`. Use it whenever something looks dim or missing:
it catches text painting black through inherited colour, which contrast maths on the
palette will never reveal.

`verify.js` runs two passes:

- *cursor* - catches teleports and origin jumps that stills will not show. Peak speed
  over ~120px/frame reads as a whip; widen the hop by starting the move earlier.
- *frame motion* - screenshots every 0.4s and diffs pixels. **This is the one that
  catches a scene looking like a photograph.** A cursor can travel across a frame that
  is otherwise dead, so `cursor still` being high is fine; `frozen frames` being
  non-empty is not.

Every frozen stretch is fixable: give the resting element a slow breathe, overlap the
neighbouring scenes by half a second, or add a second small thing to the beat.

Spot-check frames from the encoded file, not just the page:

```bash
node shots.js reels/<slug>/reel.html <outdir> 6.5 20 45 70 92
```

## 7-8. Publish and learn

```bash
python3 .claude/skills/dmyor-reel/scripts/reel.py publish "<slug>" \
  --platform instagram --at "2026-09-02 19:30" --caption "..." --hashtags "..."

python3 .claude/skills/dmyor-reel/scripts/reel.py perf "<slug>" \
  --platform instagram --views 12400 --reach 9800 --likes 340 --comments 22 \
  --shares 88 --saves 140 --avg-watch 11.2 --follows 31
```

Metrics accepted per platform are listed in `references/performance-playbook.md`,
along with which ones actually predict reach (shares and saves per reach, and the
3-second hold rate - not likes).

Then:

```bash
python3 .claude/skills/dmyor-reel/scripts/reel.py report
```

Read the report before writing the next script, and say out loud which past result
you are acting on. That is the whole point of the history.

## Conventions

- 1080x1920, 30fps, H.264 + AAC, exact duration = audio duration.
- Two looks, set by `"engine"` in `timeline.json`: `mono` (black and white, pointer
  driven) or `motion` (colour, kinetic type, camera zooms). Ask which one the reel
  wants before writing the timeline; they share no scenes.
- `mono` palette: bg `#0A0A0A`, text `#F5F5F0`, dim `#8C8C86`, meta `#6B6B6B`. Nothing else.
- `motion` palette: deep `#070812`, ink `#F7F7FB`, plus blue/cyan/green/coral/amber/violet
  used semantically, never decoratively.
- One system font stack. No icons, no emoji, no gradients.
- On-screen captions are OFF by default (the VO carries it); `?text=1` turns them on
  for a silent-autoplay cut. The closing brand card always shows.
- Brand name on screen: check with the user - the narrator says "deemyor" but the
  written mark has been `dmyor`.

## Worked examples

Read a `timeline.json` before writing a new one. Every scene in both carries the spoken
phrase it lands on in its `note`.

- **`reels/phase-one-launch/`** - 100s, the full six-beat structure. Reference for the
  diary act and the archive act.
- **`reels/four-months-left/`** - 53s, seasonal hook. Reference for **one visual per
  sentence**: the calendar, the planned/done tally, the drifting thoughts that scatter,
  the streak bars, the stamping trio, the arc. Built after a note that the previous cut
  was "just like a photo" in places; 93% active runtime, no gaps over 4s.

## What good looks like

| check | target |
|---|---|
| `reel.py gaps` | no dead air over 4s; 85%+ active runtime |
| `verify.js` snaps / origin | 0 / 0 |
| `verify.js` frozen frames | none |
| `verify.js` peak speed | under ~120 px/frame |
| `overflow.js` | no glyph overflow |
| `collide.js` | no scene-layer collisions |
| `safearea.js` | all content within y 240..1250 |

All three layout audits ignore anything clipped away by an `overflow:hidden` ancestor,
so a scrolling list does not report its off-screen rows as overflow.
| smallest on-screen type | 26px, body copy 40px+ |
| lightest supporting weight | 300, never 200 |
| duration | exactly the audio duration |
