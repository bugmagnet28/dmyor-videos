---
name: idea-film
description: Calm "big idea" film in the style of "Bend reality" (reels/bend-reality) - a thought experiment told by a calm narrator, built mostly from canvas animation (diagrams, branching lines, illustrated metaphors) with short real-footage inserts, a strong animated hook, captions, real sound effects on every movement and no music (Sanyam adds Instagram audio). 1080x1920, 30 fps, 45-65 s. Use when Sanyam brings his own script or an idea about choices, reality, the future, habits or identity, and for any comment-keyword reel ("Comment REALITY").
---

# Idea film

The reference build is `reels/bend-reality/` (`film.html`, `make_audio.py`, `extract.sh`, `lines.json`, `sfx/`). Copy it to start a new film; the engine pieces you need are already in `film.html`: frame-sequence footage with async `__seek`, `cover()` plus `zin()` zoom, `caption()`, `border()`, `diverge()` diagrams, the tree of choices, typed glass cards, the comment CTA.

Everything below is Sanyam's feedback on that film (2026-11-15 to 11-17). It overrides older style rules where they conflict.

## 0. Latest (owner 2026-11-19): fully animated, no real footage
"Bend reality" was rebuilt with **zero real video**:
- every clip was replaced by line-art animation: black ink on off-white (`#F4F3EF`), sage-dark accent `#3F6B55`, white-filled shapes with thick black outlines;
- something is always moving.
The owner liked the hook (a line-drawn city whose street folds up into the sky) and asked for "these kind of animated interesting pieces in the whole video".
- **Default from now on:** fully animated line art, no footage.
- **Reference scenes (`reels/bend-reality/film.html`):**
  - `hook()` (3D wire city with a quarter-pipe fold);
  - `forkScene()` (top-down street map, a car takes one branch);
  - `drawPhone()` (feed scrolling in a hand);
  - `drawDesk()` (lamp, book with a plane sketch, page flip, steam);
  - `bedScene()` (moon window, phone glow, lights out);
  - `wingScene()` (airfoil, airflow, LIFT, plane crossing);
  - `vShop` / `vFamily` / `vSummit` (future vignettes);
  - the tree in black ink.
- **Cards and chips are light:** white fill, black outline, black text. Captions stay as the dark pill.

## 1. The direction: more animation, less real video (owner 2026-11-17)
- **At least 60% of screen time is designed canvas animation**: diagrams, branching lines, illustrated metaphors, typed cards, the tree, the CTA. Real footage is the minority, used only where a real image makes the line land, such as a person scrolling in bed or a wing above clouds.
- Keep footage inserts to **2-4 s**, and never two footage shots in a row without an animated beat between them.
- **Every line of the script gets its own visual idea.** Before building, write a visual map: a table of `line -> what we see -> what moves -> what sound`. If a row says "footage of X", ask whether a drawing would explain the idea better, and usually it does.
- **Concept lines get a diagram, not footage.** This is the owner's own example: "Did this simple choice alter reality?" became NOW → a fork → two branches (phone / plane); "reality diverged" became the scroll branch fading to grey dashes with YOU ARE HERE travelling the other branch. Find these moments everywhere: a comparison, a cause and effect, time passing, a choice, a future state.

## 2. Hooks and visuals need to be much better (owner 2026-11-17)
**The hook (first 3 s)** decides the reel.
- **Frame 0 is finished and readable on mute:** the hook text, 6-8 words, plus a visual that demands an explanation.
- **Layer two mechanisms:** a strange or impossible visual, plus a curiosity question in the text. "Could you bend reality with your will?" worked because the picture itself bent; make the visual *do* the hook.
- The visual moves from frame 0, never a still title card. Ideas:
  - the screen warps, folds or tears;
  - a line splits in two;
  - a clock runs backwards;
  - the viewer's own phone screen is shown and then changes;
  - two versions of the same person side by side.
- Never open with a greeting, the logo, a slow fade-in or backstory.
- **Re-hook** about every 8-10 s with a new visual turn: a split, a reveal, a diagram, a jump in scale.
- Write 3 hook options (text + visual) in the visual map and pick the strongest. Show Sanyam the options when he hasn't written the hook himself.

**Visual quality bar:**
- **Something is always moving:** every footage shot zooms, every diagram draws itself, and labels appear on their spoken word.
- The visual must **land on the word** it illustrates, using timings from the voice take.
- **Clean and simple wins.** Sanyam rejected decoration that doesn't explain anything.

## 3. Look (owner rules from the "Bend reality" rounds)
- **Footage is full screen** with a **plain thin white border** (inset 30 px, radius 26, about 55% white).
- **Rejected:** coloured stage backgrounds, giant background words, cards, polaroids, airplane-window frames.
- **Every footage shot zooms in visibly:** `zin(t0, t1, t, .35-.4)`, a sine-eased push-in of 35-40% over the shot. 16% was invisible. Extract frames at **1440x2560** so the zoom stays sharp.
- **No light-blue or sage glow lines, gradient seams or circle wipes.** A split is a plain thin white line.
- **Emphasis moments are plain:** a white band with black lines at its top and bottom edges and the word in bold black (the "YES." band). Diagrams are an off-white canvas (`#F4F3EF`) with black lines, black icons and black text.
- **Type:** Inter Tight, uppercase captions in a dark pill near the bottom (y about 1495), hook text two-tone white / sage.
- **Grade:** footage darkened slightly with a soft-light sage tint, plus a vignette. Apply the vignette before diagrams so white canvases stay clean.

## 4. Script and voice
- **Keep Sanyam's own words.** Fix grammar only. Keep his connectors and framing ("Think of it this way", "Let's say, right now", "The answer is yes", "Now let's say I imagine..."). He said these make it make sense to people. Diff your lines against his text before voicing.
- Point out a confusing phrase (for example "in an ideal world" for the default outcome), but don't change it without his OK.
- **Voice:**
  - Draft with Kokoro `am_eric`, slowed: `TEMPO 0.98`, `--speed 0.94`. Use the reel's own `build_audio.py`. **Delete `vo/` whenever lines change**, because clips are cached by key.
  - Sanyam may drop an **ElevenLabs take** in the reel's `ready-to-post/` folder. Use it: `python3 .claude/skills/idea-film/scripts/align_take.py reels/<slug> <take.mp3>` (local whisper, word timestamps) rewrites `timeline.js` and `audio.wav`, and the picture follows the new times.
- **CTA:** comment-keyword endings ("Comment REALITY") need a reply plan. Write it in `post.md` (reply with www.dmyor.com and the value line).

## 5. Sound
- **No music in the file.** Sanyam adds Instagram audio in the app. He rejected our library music on this film.
- **Real recorded effects only**, from Pixabay (see `scripts/browser_grab.md`). No synthesized effects: he called the synth swishes "too loud and bad".
- **A sound on every movement:**
  - a whoosh on every scene change;
  - a soft pop when any label, chip or text appears;
  - a riser when a line draws or an arrow climbs;
  - typing when text types;
  - a send click or ping on buttons;
  - an object's own sound when it acts: clock ticking, light switch, wind, paper drop;
  - quiet ambience under real-life footage: cafe, kids giggling, mountain wind.
- **Levels:** each effect is RMS-normalised, then set to 0.10-0.30 of the voice RMS (`make_audio.py` `snd()` / `put()`). Ambience 0.10-0.12, pops 0.15, whooshes 0.18-0.22, signature moments (chime, warp) 0.25-0.30. Never louder than the voice.
- Keep the file around -16 dB mean and -1.5 dB peak.

## 6. Build and render
1. `reels/<slug>/`: `lines.json` (owner wording), a visual map in `notes.md`, footage in `pex/` (gitignored), frames via `extract.sh`.
2. Voice (Kokoro draft or owner take), then the timeline. Picture times come from `TL` (`L(key, i)`). If you re-time to a new take, keep one anchor map (`ANCH`) shared by `film.html` and `make_audio.py`.
3. Snapshot before every render: `node reels/<slug>/snap.js <times...>`, then a contact sheet. Check:
   - frame 0;
   - every diagram;
   - labels inside the frame;
   - the zoom (compare the start and end of a shot);
   - no text sitting on the border.
4. Render: `node record.js --page reels/<slug>/film.html --out reels/<slug>/film.mp4 --audio reels/<slug>/audio_mixed.mp3 --fps 30`, then an H.264 CRF 21 copy to `ready-to-post/<slug>/video.mp4`.
   - Take the render lock `/tmp/dmyor-pixel-render.lock`.
   - **Never render while a website deploy is running.** Check `pgrep -f "react-snap|deploy.sh"` first. The Mac's swap is nearly full and two Chromiums crashed a deploy on 2026-11-17.
   - Audio-only change: remux, no re-render.
5. Package `post.md`:
   - the caption in Sanyam's wording;
   - the comment-reply plan;
   - the key moments (for lining up Instagram music);
   - footage and sound credits.
   Commit sources (frames, `pex/`, mp4 and wav are gitignored). Not scheduled until Sanyam says so; evening slot (19:30-20:30 IST).

## Rejected in this film (don't repeat)
| Tried | Owner said |
|---|---|
| Library music (mystery → resolve) | remove, he adds Instagram music |
| Tightened script (cut "Think of it this way" etc.) | keep his connectors |
| Synth swishes on every cut | too loud and bad, use real effects |
| Thin border plus glint, coloured stage backgrounds, cards, polaroids, window frame | remove, keep normal footage plus a plain border |
| Light-blue glow seam, gradient "YES" with shadow | plain: white band, black lines, black text |
| 16% zoom | not visible, zoom every shot clearly |
| Mostly footage | next films: more animated, less real video |
