---
name: kinetic-typography
description: Motion-graphics style where the words are the animation. Each spoken thought is a full-screen card of bold type on a crisp dark canvas; every word pops in exactly when it is spoken, marked words turn accent orange and punch, others get struck through or muted; the hook card is fully drawn on frame 0. Human-paced narration (free local Kokoro voice am_eric) or silent at reading pace; no music; dmyor brand card. 10-20s, 1080x1920. Use for one-liners, hard truths, reframes, hooks and short punchy reels where the message is a sentence, not a structure.
---

# Kinetic typography

**What the viewer sees**
1. Frame 0: the hook card, fully drawn (e.g. "**Someday** isn't a day." with "Someday" in orange). Never empty, never mid-animation.
2. Each following thought replaces the card (old card lifts and fades, new one rises in). Words appear one by one on their spoken time with a small rise and settle.
3. `*emphasis*` words land in orange with a quick punch; `~strike~` words get a red line drawn through them right after they are spoken and dim; `{muted}` words are grey asides.
4. A thin orange progress bar runs along the bottom edge.
5. Brand card: `dmyor`, tagline, `@becauseidmyor` pill, while the voice says "That's Dmyor. Link's in the bio."

Same visual system as `diagram-motion-graphics` (dark `#0B0C10`, faint dot grid, Inter Tight, accent `#FF7A1A`), so the account looks consistent. Text auto-sizes per card to the largest size that fits (max 150 px, min 56 px).

## Make a reel
From the project root (`~/Documents/dmyor-videos`). One-time voice setup: `bash .claude/skills/kinetic-typography/scripts/setup_tts.sh`.
1. `mkdir reels/<slug>`; copy `examples/narration.example.json` to `reels/<slug>/narration.json`; write the script.
2. `python3 .claude/skills/kinetic-typography/scripts/make_reel.py reels/<slug> --record` (add `--package YYYY-MM-DD` to create `ready-to-post/<date>-<slug>/`).
3. Check, show Sanyam, schedule only after his OK, then register the post in `analytics/` (`record.py content --style kinetic-typography ...`).

## Write for the ear (owner rule, 2026-10-24)

The narration is FULLER than the on-screen text. Spoken language needs more words than written language to sound complete and human; screens need fewer.
- **Say it like a person talking to one friend**: lead-ins and asides ("Seriously,", "So here's what I'd do.", "And honestly,"), connectors ("and then", "so"), contractions, first person ("I'd", "I've put"), a spoken question now and then ("And someday? It's not on there.").
- **Never end on a clipped fragment.** Not "Link in bio." but "And if you want to try it out, I've put the link in the bio." Not "Today." alone at the very end; land the point, then close warmly ("That's exactly what Dmyor is built for.").
- **Stages**: open with a short hook, explain, turn to the advice, land the point, close. Tag thoughts when needed: `[hook]`, `[turn]`, `[land]`, `[outro]` (untagged: first = hook, last two = outro, the one before = land). The voice (`say.py --stages`, on by default) changes pace, pitch and pauses per stage and ends with a natural fade.
- **Screen stays short.** On-screen text/cards/subtitles keep the punchy version; the extra spoken words are not all shown.
- Length: fuller narration runs ~20-30 s for a 6-8 thought script. Keep each thought one breath.

## Script rules
- 4-6 cards (`||`), 30-55 words total → 10-18 s. One idea per card, max ~12 words on a card.
- Card 1 is the hook and is read on frame 0: 2-6 words, a hard truth or sharp question. Best so far: "Someday isn't a day." (hard truths beat quizzes and step lists on our account).
- Mark 1 word per card at most with `*...*`; use `~...~` for the belief being killed ("~Someday~ isn't on it"). Markup is per WORD: `~a fresh start~` does not work (stray marks were spoken as "tilda" before 2026-10-24; now stripped from the voice, but the strike still fails). Strike one word.
- Write it to be said: contractions, natural phrasing; the voice speaks each card as one thought, so a card should be one breath.
- End with `|| That's Dmyor. || Link's in the bio.` (`brand_anchor` = "That's Dmyor"; everything from that card on becomes the brand card).
- Silent version: set `"voice": null` → reading-pace timing (hook held 1.6 s, 0.32 s per word, 0.7 s between cards).

## narration.json
| field | meaning |
|---|---|
| `voice` / `speed` / `gap_min` / `gap_max` | `am_eric`, 1.0, 0.30-0.55 s pauses between cards (same voice rules as the diagram skill) |
| `script` | what is SHOWN: short card text with markup (above), one card per `||`. |
| `spoken` | what is SAID: the fuller conversational version, **same number of `||` thoughts** as cards, optional `[stage]` tags. Each shown word pops when its matching spoken word is said. Write "Dmyor"; it is spoken "Deem-yor". Omit to speak the card text as-is. |
| `brand_anchor` | text of the card where the brand card takes over |
| `tagline`, `handle` | brand card |
| `max_font` | cap for the auto-fit size (150) |
| `caption` | `instagram`, `hashtags`, `x`, `youtube_title` for `--package` |

## Check
- Build line: 2.6-3.2 words/sec, total 10-20 s; "whisper heard" matches the script.
- Frames: `node shots.js reels/<slug>/reel.html /tmp/k 0 <mid of each card> <brand>`: frame 0 shows the whole hook; no card overflows; emphasis/strike land on the right words.
- Sanyam listens before anything is scheduled.

## Files
`assets/kinetic.html` (engine), `assets/fonts/`, `scripts/make_reel.py`, `scripts/say.py` (thought-level Kokoro voice with varied pauses and room tone), `scripts/setup_tts.sh`, `examples/narration.example.json` ("Someday isn't a day", 16.1 s).
