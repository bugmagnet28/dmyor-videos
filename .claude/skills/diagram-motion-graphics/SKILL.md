---
name: diagram-motion-graphics
description: Motion-graphics style. Crisp dark-mode diagram animation (nodes, straight right-angle connectors, progress lighting up) drawn in sync with a human-paced narration (free local Kokoro voice am_eric), subtitles, no music, dmyor brand card. Current layout - the goal tree (vision -> 3 milestones -> 3 actions -> one TODAY action ticked -> progress back to the vision); 20-28s, 1080x1920. Use for any reel that explains a structure or process (how a goal becomes a plan, how the pieces of dmyor fit). New layouts (timeline, flow, before/after map) are added here, not as new skills.
---

# Diagram motion graphics (layout: goal tree)

A production style, end to end: script -> voice -> word timings -> diagram animation on spoken cues -> subtitles -> MP4 -> ready-to-post folder.

**What the viewer sees (in order)**
1. Frame 0: a bold hook on a near-black canvas with a faint dot grid (finished on frame 0, never mid-animation).
2. VISION node (orange outline) appears on the word that names it.
3. A connector drops from the vision; three MILESTONE nodes appear one by one, each on its spoken phrase, joined by straight right-angle lines (org-chart / planning-diagram style).
4. From the centre milestone, three ACTION nodes (with checkboxes) appear on their phrases.
5. Focus: everything dims except one action, which grows slightly and gets an orange TODAY tag.
6. On "today"/"that's it" the checkbox ticks green.
7. An orange line runs from that action up through its milestone to the vision; the milestone and vision progress bars fill (one small action moves the whole plan).
8. Brand card: `dmyor` wordmark, tagline, `@becauseidmyor` pill; narration ends "... Link's in the bio."
Spoken phrases appear as subtitles at the top (the script's exact words), because most people watch muted.

**Look (owner decisions, 2026-10-22)**: modern, crisp, "clarity". No scenery, no illustration, no fairy tale. Dark `#0B0C10` canvas, Inter Tight, white text, one accent orange `#FF7A1A`, green `#3DDC97` only for "done". Do not add music: the owner removed it.

## Requirements (one time)

From the project root (`~/Documents/dmyor-videos`, the folder with `record.js`):
```bash
bash .claude/skills/diagram-motion-graphics/scripts/setup_tts.sh   # Kokoro venv + models (~340 MB) in ./tts
```
Also needed and already present on this Mac: `ffmpeg`, the `whisper` CLI (word timestamps), node + puppeteer (`record.js`), and the `dmyor-reel` skill (its `align.py` is reused for timings).

## Make a reel

1. `mkdir reels/<slug>` and copy `examples/narration.example.json` to `reels/<slug>/narration.json`.
2. Write the content, script and anchors (rules below). Show Sanyam the script before rendering if it is a new angle.
3. Build and record:
```bash
python3 .claude/skills/diagram-motion-graphics/scripts/make_reel.py reels/<slug> --record
# or also package to ready-to-post/<date>-<slug>/ with post.md:
python3 .claude/skills/diagram-motion-graphics/scripts/make_reel.py reels/<slug> --package 2026-10-23
```
4. Check (below), then let Sanyam watch/listen. Never schedule without his OK.

### narration.json fields
| field | meaning |
|---|---|
| `voice`, `speed` | `am_eric` at `1.0` (owner's pick, "kinda retro"). At 1.1+ Eric swallows short phrases. Samples of other voices: `tts/samples/`. |
| `gap_min`, `gap_max` | pause range between thoughts (0.30-0.55 s). Varied on purpose. |
| `tail` | seconds kept after the last word (1.2) so the brand card holds. |
| `content.hook` | `[big line, sub line]` on frame 0. Big line <= ~12 chars ("Too big?", "Someday"). |
| `content.vision` | one line with a date or number ("Earn $2,000 a month freelancing"). <= ~40 chars. |
| `content.milestones` | exactly 3, <= ~22 chars each. |
| `content.actions` | exactly 3, <= ~20 chars each, start with a verb. |
| `content.actionParent` | milestone index the actions hang from (keep `1`, centre). |
| `content.todayIdx` | which action gets TODAY + the tick (0-2). |
| `content.tagline`, `content.handle` | brand card lines (`\n` allowed). |
| `script` | the narration (rules below). Write "Dmyor"; it is spoken "Deem-yor" automatically. |
| `anchors` | where each visual beat lands (rules below). |
| `caption` | `instagram`, `hashtags`, `x` (<= 280 chars, link counts 23), `youtube_title` for `--package`. |

## Writing the script (this is what makes it sound human)

The voice is generated per THOUGHT, so how you write is how it sounds.
- Split the script into 6-8 thoughts with `||`. Each thought is spoken in one breath with natural intonation; pauses happen only between thoughts.
- Write like talking: contractions, connectors ("so", "then", "now", "and then"), flowing lists ("like sending five proposals, posting one project, following up").
- Avoid strings of one- or two-word sentences ("Post one project. Follow up. Today.") as separate thoughts: each restarts the intonation and sounds choppy. Keep short punches for the hook, the "today" beat and the ending.
- 60-80 words -> 22-27 s. Over ~80 words the reel drags.
- Always end with `|| That's Dmyor. || Link's in the bio.` (or `|| Dmyor turns your someday into a plan. || Link's in the bio.`).
- Never invent product features. The tree, milestones, actions, today list, habits/streaks and progress are real dmyor features.

Template that works:
```
<hook question or hard truth> || <reframe>. <vision with a date>. || Then <three milestones>. ||
Now take one of them, and break it into small actions. Like <a1>, <a2>, <a3>. ||
You don't need motivation for that. You just need one thing, done today. ||
And then you watch it grow. || That's Dmyor. || Link's in the bio.
```

## Anchors (where the animation lands)

`anchors` maps each beat to a phrase as it will be *heard*. They are searched in order through whisper's transcript.
```
hookOut     first words after the hook (hook text fades)          "So shrink it"
vision      vision node appears                                   "the vision"
trunk       first connector drops                                  "give it a date"
milestones  [3 phrases] one per milestone node                     ["three milestones","that show","getting there"]
actions     [3 phrases] one per action node                        ["sending five proposals","posting one project","following up"]
focus       everything dims, TODAY tag on the chosen action        "one thing"
done        checkbox ticks                                         "today"
grow        progress line lights up to the vision                  "watch it grow"
brand       brand card                                              "That's"
```
Rules:
- Use 2-3 plain words whisper will transcribe exactly. Avoid homophones: "Write down the vision" was heard as "right down the vision", so anchor on "the vision".
- Numbers: write them as words in the script ("five proposals"); the finder tries digits too.
- Never anchor on the brand name (whisper hears "Deem-yor" as "demure", "deem your", "D-Mure").
- If the build stops with "anchor not found", read the printed "whisper heard:" line and pick words from it.

## Check before showing Sanyam
- Build output: 2.5-3.2 words/sec overall, 22-28 s total, every anchor found.
- `whisper heard:` line ends with the brand + "Link's in the bio".
- Frames: `node shots.js reels/<slug>/reel.html /tmp/f 0 <milestones> <actions> <focus> <brand>` then look at them: frame 0 readable, nodes not clipped, subtitles 1-2 lines, TODAY tag on the right node.
- Pauses: `ffmpeg -i reels/<slug>/audio.mp3 -af silencedetect=noise=-45dB:d=0.2 -f null - 2>&1 | grep silence_duration` -> one pause per `||`, varied 0.25-0.6 s.
- He listens. Things he has rejected: background music, continuous run-on voice, a pause after every couple of words, fairy-tale scenery, "Dee-MY-er" pronunciation.

## Posting notes
- Instagram via browser: one scheduling flow per reel, nothing else in the same session (the account was locked once after heavy automation). Crop 9:16, cover = frame 0, sound on.
- X: link goes in the post (clickable card). YouTube Shorts: title from `caption.youtube_title`, description = caption with "Plan yours: https://www.dmyor.com" instead of "Link in bio".

## Files
- `assets/diagram.html` - the template (pure function of time: `window.__seek(t)`, `window.__duration`), fonts in `assets/fonts/`.
- `scripts/make_reel.py` - the whole pipeline.
- `scripts/say.py` - Kokoro voice, thought-level generation, varied pauses, room tone.
- `scripts/setup_tts.sh` - one-time voice setup.
- `examples/narration.example.json` - the 2026-10-23 "Too big? Shrink it." reel.

## Results so far
After scheduling, register each platform post in `analytics/` (`record.py content --style diagram-motion-graphics --narrated yes --voice am_eric ...`) and measure at 24h/48h/7d (see `analytics/README.md`). First two of this type were scheduled 2026-10-23 (diagram-howto-vo 09:30, diagram-someday-vo 19:30 IST) as V-EXP-23. Update this section with what the numbers say.
