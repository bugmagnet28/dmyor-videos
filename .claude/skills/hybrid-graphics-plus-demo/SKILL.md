---
name: hybrid-graphics-plus-demo
description: Hybrid production style - motion graphics plus REAL dmyor screen footage. Kinetic-type hook card, then the live dmyor.com app recorded in a phone frame (guest flow, no account) with callouts, tap rings and zooms placed on spoken words, then a motion-graphics feature panel (e.g. "Full features releasing soon"), a kinetic CTA card and the dmyor brand card. Human-paced narration (free local Kokoro voice am_eric), subtitles, no music. 25-35s, 1080x1920. Use when a reel should SHOW the real product: how a vision is created, the Intent Archive, any screen a visitor can reach.
---

> **Owner rules 2026-10-24 override anything below:** no duration cap (explain completely, typically 35-55 s), logical credible examples, brand close with the value sentence, classy motion (no bounce/pop), Graphite & Sage palette (accent sage `#9DB8A3`, no orange), short gaps. Full text: `studio/quality-bar.md`.

# Hybrid: motion graphics + real app demo

**What the viewer sees**
1. Hook card on frame 0 (kinetic type, e.g. "Everyone has a dream they mean to act on *someday*.").
2. A phone frame rises in; inside it the REAL dmyor.com screens play, timed to the narration (each footage moment is pinned to a spoken anchor). Orange callout labels overlap the phone edge ("1 to 5 years", "Your vision, your words"), a tap ring marks the button being pressed, the screen zooms into the field being typed in. Subtitles of the narration sit at the top.
3. A second clip (e.g. the Intent Archive page scrolling).
4. Phone exits; a motion-graphics feature panel: headline ("Full features releasing soon"), a pill, a lock that opens on "releasing soon", and feature chips (Milestones · Actions · Daily reps · Your story) that light up.
5. CTA card ("So write *yours* today."), then the brand card (`dmyor`, tagline, `@becauseidmyor`) while the voice gives the value close (`studio/quality-bar.md` rule 3)

**Feature messaging (owner, 2026-10-24)**: new visions open a "coming soon" screen; the other features are locked for now. Never call it "the planner". Say **"Full features are releasing soon"** ("Your vision will be waiting"). Show only what a visitor can do today (create a vision, the Intent Archive) as real footage; show the coming features (milestones, actions, habits, journal) only as motion graphics, and never imply they work today.

## Footage (real app, no account)
Record from the project root; a Chrome window appears briefly (visible mode gives 2x frames, 780x1688 at ~31 fps):
```bash
HEADFUL=1 node .claude/skills/hybrid-graphics-plus-demo/scripts/capture.js create-vision     # horizon -> vision text -> tag (stops before Create)
HEADFUL=1 node .claude/skills/hybrid-graphics-plus-demo/scripts/capture.js intent-archive    # scroll of /intent-archive
```
Frames land in `app-capture/raw/<name>_frames/` with `frames.json` (timestamps). The script blocks Google Analytics and the dmyor API (recordings are not counted as visits, nothing is written), hides the cookie notice with CSS (never clicks it), and stops before "Create Vision" (a guest would be sent to login). To film another page, add a branch in `capture.js` with its own steps; keep the same safety rules. Never create accounts or type credentials on dmyor.com.

Capture timeline of `create-vision` (useful for beats): 0-2.8 s step 1 (3 years picked ~1.4 s), 2.8-8.6 s step 2 (typing ~4.7-7.2 s), 8.6-13 s step 3 (Career tag ~10.6 s, Create Vision button at screen x 0.5, y 0.815).

## Write for the ear (owner rule, 2026-10-24)

The narration is FULLER than the on-screen text. Spoken language needs more words than written language to sound complete and human; screens need fewer.
- **Say it like a person talking to one friend**: lead-ins and asides ("Seriously,", "So here's what I'd do.", "And honestly,"), connectors ("and then", "so"), contractions, first person ("I'd", "I've put"), a spoken question now and then ("And someday? It's not on there.").
- **Never end on a clipped fragment.** Not "Link in bio." but "And if you want to try it out, I've put the link in the bio." Not "Today." alone at the very end; land the point, then close warmly ("That's exactly what Dmyor is built for.").
- **Stages**: open with a short hook, explain, turn to the advice, land the point, close. Tag thoughts when needed: `[hook]`, `[turn]`, `[land]`, `[outro]` (untagged: first = hook, last two = outro, the one before = land). The voice (`say.py --stages`, on by default) changes pace, pitch and pauses per stage and ends with a natural fade.
- **Screen stays short.** On-screen text/cards/subtitles keep the punchy version; the extra spoken words are not all shown.
- Length: as long as the explanation needs (typically 35-55 s), never padded. Keep each thought one breath.

## Make a reel
1. `mkdir reels/<slug>`; copy `examples/narration.example.json` to `reels/<slug>/narration.json`; edit script and beats.
2. `python3 .claude/skills/hybrid-graphics-plus-demo/scripts/make_reel.py reels/<slug> --record` (`--package YYYY-MM-DD` for ready-to-post).
3. Check frames from the MP4 (`ffmpeg -ss <t> -i reels/<slug>/reel.mp4 -frames:v 1 x.png`): footage present in the phone at every phone moment, callouts not covering what is being shown, subtitles 1-2 lines.
4. Sanyam watches; schedule only after OK; register in `analytics/` with `--style hybrid-graphics-plus-demo`.

## narration.json
| field | meaning |
|---|---|
| `script` | narration, thoughts split by `||` (same voice rules as other styles: conversational, 6-10 thoughts, ends with the value close) |
| `hook_text`, `hook_until` | hook card text (with `*emphasis*`) and the spoken anchor where the phone takes over |
| `clips` | `[{name, beats: [[anchor, footage_seconds], ...], speed_after}]`. `"@start"` = phone entry. Footage between beats is time-stretched; after the last beat it plays at `speed_after` and holds its last frame. |
| `phone_out` | anchor where the phone leaves |
| `taps` / `callouts` / `zooms` | on-screen emphasis pinned to anchors (x, y are 0-1 of the screen) |
| `phase2` | `{from, unlock, until, title, items:[{k,t}]}` feature panel |
| `cta` | `{from, text}` kinetic card until the brand |
| `brand_anchor`, `tagline`, `handle`, `caption` | brand card and post texts |
Anchors: plain words whisper hears exactly; never the brand name; numbers as words.

## Files
`assets/hybrid.html` (engine; `__seek` waits for each footage frame to decode), `assets/fonts/`, `scripts/make_reel.py`, `scripts/capture.js`, `scripts/say.py`, `scripts/setup_tts.sh`, `examples/narration.example.json` (the "create a vision" reel, 31.9 s).
