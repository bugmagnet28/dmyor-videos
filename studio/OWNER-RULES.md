# Owner rules for Dmyor videos (authoritative)

Every decision Sanyam made about how Dmyor videos are made and posted, in one place. **Read this first, every run. Where anything else (agent file, skill docs, playbook, older notes) disagrees, this file wins; within this file, the later date wins.** Last consolidated 2026-10-25.

## 1. Accounts, platforms, posting
- **One account everywhere: @becauseidmyor.** Use it on the end card, in captions and in mentions. `@dmyor_global` is retired, so never put it on new videos.
- **Platforms:** the same 1080x1920 file goes to Instagram (@becauseidmyor), YouTube Shorts (channel "Dmyor") and X (@becauseidmyor).
- **Cadence:** 3-5 reels a day, at least 2-3 h apart. Typical IST slots: 09:30, 13:00, 16:30, 19:30, plus 22:00 for a 5th. Timing matters less than quality (2026-10-24).
- **Approval:** Sanyam approves a batch before it is scheduled. When he says "don't ask, just do it", schedule only what passes these rules, and fix or rebuild anything that doesn't (as on 2026-10-25, when two text-only reels were rebuilt).
- **Instagram safety:**
  - at most 5 scheduling flows per browser session;
  - no bulk insight scraping;
  - stop and ask on any error. The account was locked once.
- **YouTube:**
  - Phone verification is still pending, so description links are not clickable yet.
  - Title format: `<hook> #Shorts`.
  - Watch the hashtag autocomplete: end the hashtag line with a space and put the link after it.
- **Browser uploads must be under 10 MB.** Re-encode with x264 CRF ~24 and maxrate 1800k, then check a frame for banding.
- **Captions:** crisp and to the point, about what Dmyor does. No em dashes anywhere (use a colon, comma or period). "Link in bio."
- **Product claims:** most features are locked. Never call it "the planner"; say "Full features are releasing soon". Show locked features only as graphics.

## 2. Content and script
- **Usefulness test:** after watching, a stranger can *do* one specific thing differently today. Quality bar: `studio/quality-bar.md` (ship at ≥30/40, hook ≥4, usefulness ≥4).
- **Logic:** every example must convince a sceptical adult.
  - Rejected: "get fit: put your shoes by the door".
  - Right: "walk 30 min after dinner, 3 days this week".
- **The big plan is never the villain; it is a level of the breakdown.** Right: get fit → 6-day gym program → one day at a time → today is chest day. Rejected: "don't start with a 6-day program".
- **No duration cap.** Explain completely, never empty or incomplete, never padded. Typical length is 35-55 s.
- **Write for the ear.** Narration is fuller and more conversational than the screen text: lead-ins, connectors, first person, staged hook → explain → turn → land → outro. End warmly: "If you want to try it out, I've put the link in the bio."
- **Value close, always:** "That's what Dmyor is for. You archive your dream today, so you can see it tomorrow, and break it down into small steps you can actually do."
- **Hooks** (from the niche scan, `studio/analysis/2026-10-25-instagram-niche-scan.md`):
  - hard truths with a curiosity gap ("…until you understand this");
  - one line per reel that people would send to a friend;
  - relatable identity beats "7 steps" lists.
- **Voice:**
  - Kokoro `am_eric`, `say.py --stages`;
  - pauses of 0.18-0.32 s between thoughts;
  - "Dmyor" is spoken "Deem-yor" (write `Deem-yor` in the TTS text).

- Story reels (2026-10-27, Pixel Book): the story should not end abruptly on "That's what Dmyor is for". Bridge to the viewer first, then name Dmyor. Example: "Sam's story started on one page. Yours can too. Write your dreams and visions in one place, break them into small steps, and document your journey. Start yours on Dmyor."
- Story reels: say the payoff concretely, not vaguely. "He did all he wanted to" was rejected; "His own company. The house. Every dream he once wrote in that book had come true." works.
- Story reels: put a real pause after questions and dramatic beats ("But how?" then a beat). Record one clip per sentence so each pause can be placed.
- Pacing: never hold a shot after its useful part ends; no long silences (fill with narration that makes sense). Aim for about 1:20 for story reels.

## 3. Look and motion
- **Palette: Graphite & Sage.** bg `#151719`, ink `#E9E7E2`, accent `#9DB8A3`, secondary `#D8CBA8`, warning `#C98B7B`; deeper sage `#5E806A` for accent words on light backgrounds. Orange/black is rejected.
- **Real graphics in every reel.** Never a captions-only or text-only (kinetic typography) reel (2026-10-24, "just captions won't cut it"). Kinetic type may only be a hook card inside a graphic reel.
- **Classy, mature motion:**
  - ease-in-out only;
  - no bounce, wobble, cartoon sparkles or bobbing.
- **Never a frozen screen** (2026-10-25). Something is always moving: camera drift, particles, light sweeps, typing. Show visions *being written* (typewriter with a caret), not just floating.
- **Frame 0** is finished and readable (it is also the grid cover).
- **Pace for cinematic reels** (2026-10-25, latest):
  - fast, "a different thing each click", a happening reel;
  - but **not** a zoom on every beat;
  - liked: **zoom in once, then swipe across parts of the screen**, then back out;
  - no punch-ins, rotation or flash on every cut.
- **Backgrounds for cinematic reels** (2026-10-25, latest): **our own designed canvases**, mystic and galactic: drifting nebula clouds, orbit rings, aurora ribbons, a planet horizon, stars. **No background photos** for this style; flower photos are explicitly rejected.
- **If photos are ever used again:** CC0 / public domain only (Wikimedia Commons via the Openverse API; NASA Hubble public-domain images are fine, ESA/ESO CC BY are not), credited in the skill's `photos/CREDITS.md`. Never send the owner's email in a User-Agent. Unsplash and StockSnap block automation, so don't use them.

## 4. Sound
- **Sound effects are clearly audible**, not subtle (default `"present"`).
- **Objects sound like themselves:** clock ticks, pencil scratch when crossing out, page flips, footsteps, gym plate clink, stamp, timer.
- **Feedback sounds:**
  - check marks get a "correct" chime that rises in pitch along a run;
  - things appearing get a pop;
  - one sound is never reused for everything.
- **No sound on every camera cut.** Only a soft whoosh on swipes.
- **Music:**
  - Explainer reels have no background music (owner removed it earlier).
  - Cinematic/brand films have a composed score (synthesised) with a soft pulse, and the voice ducks it (2026-10-25: "the reel I sent had narration and soundtrack, we will also have that").
  - Open question (see section 7): music for every reel at posting time.

- No risers or impacts building suspense (tried 2026-10-27, owner removed them).
- Writing on paper: soft pen strokes, never a scratchy pencil sound.
- Scene changes: a pop (picture and sound), not a page-turn effect.
- Engine and vehicle sounds (helicopter etc.) fade in and out; never a hard loop at full level.
- **Real recorded sound effects (2026-10-28):** allowed from Openverse, **CC0 only**, fetched with `python3 studio/tools/fetch_sfx.py search|get`. Never CC BY, share-alike, NC or ND. Files live in `studio/sfx-library/` with every source logged in `LICENSES.md`. Listen and match loudness before use; the synthesised `sfx.py` sounds stay the default, so reels keep one consistent sound.

- Narration voice (owner 2026-10-28): ElevenLabs **Adam** (Radio Announcer), generated manually by Sanyam from a one-take script with v3 audio tags (see `reels/pixel-book/narration-elevenlabs-v3.txt`). Fit the picture to the take with `reels/pixel-book/vo_external.py` (cuts only in real pauses, keeps the take to its natural end). Free voices tested and rejected for now: Kokoro (flat), Qwen3-TTS voice design + tone match (closest, still darker than Adam). Kokoro stays only for drafts.
- Use `tools/earshot` (MIT, local) to check a mix: `earshot measure` (loudness, bands), `earshot ab A B` (differences in words), `earshot critique film.mp4`. Never use its `llm --yes-upload`.

## 5. Styles (skills in `.claude/skills/`)
| Style | Status | Use for |
|---|---|---|
| `animated-illustration-explainer` | default, meets every rule | methods and ideas with worked examples, one scene per thought, object sound effects |
| `cinematic-motion` (`cosmos.html`) | approved 2026-10-25 (brand film "One place") | brand / flagship reels: typewriter fly-through opening, warp, dark glass card, tree of light, designed cosmic canvases, narration + score |
| `prompt-animation` (`engine.html`) | built 2026-10-26, demo "anim-dream-mountain" awaiting owner review | story animation from a prompt: full-colour illustrated universe, characters with faces walking/typing/climbing, layered worlds, ambient life. Own vivid palette (owner exception to Graphite & Sage) |
| pixel story (`reels/pixel-book/pixel.html` + `pixel-art-studio` skill) | built 2026-10-26, first film "pixel-book" awaiting owner review | 16-bit pixel art story reels: art drawn pixel by pixel with Pixel Art Studio (MIT), 270x480 worlds blitted 4x with a nearest-neighbour pixel camera, pixel-font captions, chiptune score + 8-bit/object sound effects, narration |
| `diagram-motion-graphics`, `hybrid-graphics-plus-demo` | need rework (no sound effects, older motion) | rework before using |
| `kinetic-typography` | not standalone | hook card only |

Planned (agreed plan, from the Lemo-Opuscar reference in `reference/lemo-opuscar/NOTES.md`):
1. Add their directing rules to the quality bar: an ambience bed, two near-silences, sound carrying transitions, minimum text hold time.
2. Upgrade the sound-effect kit.
3. A Dark Tech Keynote style for product reels.
4. Whiteboard / paper-notebook style. The niche scan says handwriting and paper are the faceless look that wins, so build it before Dark Keynote.

Target quality bar: @anmoldoesmotion's OpenAI piece, `studio/analysis/2026-10-25-reference-anmoldoesmotion-openai.md`.

- Reel library (2026-10-28): `studio/library/index.html` lists every reel (status, style, art style, hook type + line, topic, voice, length, links, views) with filters. Rebuilt by `studio/tools/reel_library.py` after every batch.

## 6. Build and check
- Build with the style's own script:
  - `make_reel.py` (illustrated): spoken `cue` words drive animation beats and sound events;
  - `make_film.py` (cinematic): `BEATS` drive picture, score and sound effects.
- Before showing Sanyam, look at a contact sheet of frames covering every scene. Check for:
  - text cut off or labels outside the frame;
  - overlaps;
  - empty stretches;
  - muddy transitions;
  - a finished frame 0.
- Render cost: never apply a canvas `filter` to full-frame draws every frame. Pre-blur once. A full-frame blur stalled the recorder on 2026-10-25.
- Register every scheduled post in `analytics/` (`record.py content`), update `studio/post-queue.md`, rebuild the analytics report.

## 7. Open decisions (ask Sanyam, don't assume)
- **Music for all reels at posting time.** Options given 2026-10-25:
  - mix in royalty-free tracks (Pixabay / YouTube Audio Library), which Sanyam would download into `inbox/music/`;
  - or have Sanyam add trending Instagram sounds from the phone app;
  - or check whether Meta Business Suite offers audio with scheduling.
  - Not decided yet. Explainers stay without music until then.
- **Comment-keyword funnel** ("Comment PLAN…"): proposed in the niche scan, not approved.
- **A face on camera** (founder clip): proposed, not approved.
