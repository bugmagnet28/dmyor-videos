---
name: prompt-animation
description: Prompt-to-animation. Turn a plain-language story ("she types her dream at night, then climbs a mountain of milestones at dawn") into a full-colour animated short. It is a colourful illustrated universe: characters with faces who walk, sit, type, climb and celebrate, plus props, layered worlds (rooms, skies, hills, cities, space) and ambient life (birds, clouds, stars). Sound effects are derived from the actions, with a calm score and optional narration. 1080x1920, 30 fps. Not the explainer or tree look.
---

# Prompt animation

This style is for **story animation**: people moving through colourful worlds. Do not use it for diagram explainers; that is `animated-illustration-explainer`.

**Palette exception:** the owner asked for a "coloured universe" (2026-10-26), so this style uses its own vivid palette, not Graphite & Sage. Every other owner rule in `studio/OWNER-RULES.md` still applies:
- logical story;
- the value close for Dmyor reels;
- no em dashes;
- never a frozen screen;
- objects sound like themselves.

## Workflow

Run from `~/Documents/dmyor-videos`.

1. **Turn the prompt into a script.** Write `reels/<slug>/scene.json`, keeping the prompt in a `"prompt"` field. Plan one scene per idea (3-6 s each). Make something move in every scene: an actor action, a camera push or a typewriter.
2. **Build:**
   ```
   tts/.venv/bin/python .claude/skills/prompt-animation/scripts/make_anim.py reels/<slug>
   ```
   This writes `anim.html` and `audio_mixed.mp3`.
3. **Check frames.** Look at a contact sheet before recording:
   ```
   node shots.js reels/<slug>/anim.html <outdir> 1 4 8 ...
   ```
4. **Record** by running the build again with `--record`. This writes `anim.mp4`.

Reference example: `reels/anim-dream-mountain/scene.json`, also kept in `examples/`.

## scene.json

### Top level

| Field | What it holds |
|---|---|
| `duration` | Length of the video in seconds. |
| `music` | `"calm"` or `"none"`. |
| `narration` | Optional: `{"spoken", "at", "voice"}`. |
| `scenes[]` | The scenes, described below. |
| `text[]` | On-screen lines, described below. |

### Scenes

Each scene is `{start, bg, transition, camera, props[], actors[], fx[]}`.

All times inside a scene are relative to its `start`. `transition` is one of `fade`, `dip` or `whip`.

**Backgrounds (`bg`)**
- `room-night`, `room-day`;
- `outdoor-day`, `outdoor-dawn`, `outdoor-sunset`, `outdoor-night`;
- add `-city` (for example `outdoor-night-city`) to get a skyline instead of hills;
- `space`: nebulae, a ringed planet and shooting stars.

Outdoor worlds already contain drifting clouds, birds (except at night), parallax hills and swaying grass.

**Camera**
```
{"from": {"x", "y", "z"}, "to": {...}, "dur",
 "follow": "<actor id>", "oy", "amount",
 "keys": [{"at", "dur", "x", "y", "z"}]}
```
Push in slowly. Use `follow` for climbs and walks. Use `keys` for a single reframe.

### Props

Every prop is `{type, x, y, z, in}`. `in` makes it pop in at that time.

| Type | Extra fields |
|---|---|
| `chair`, `desk`, `lamp`, `rug`, `shelf`, `plant` | none |
| `laptop` | `text`, `typeFrom`, `typeDur` (typewriter on screen) |
| `window` | `w`, `h`, `day` |
| `poster` | `text` |
| `mountain` | `w`, `h`, `ledges[{x, y, label, at, side}]` |
| `flag` | `at`, `text` |
| `dreamcard` | `text`, `tag`, `at`, `typeFrom`, `typeDur` |
| `stairs` | `n`, `sw`, `sh`, `at`, `labels[]` |
| `tree` | `s` |
| `rocket` | `at`, `dur`, `rise` |
| `sun`, `moon`, `phone`, `calendar` (`text`), `books` | as named |

**Placement:**
- The floor line in rooms and the ground outdoors is at y=1500.
- Desk, chair and laptop share the same x/y base.
- Put the laptop at `z: 2` so it draws over the actor's hands.

### Actors

An actor is:
```
{id, style: a|b|c|d, x, y, face: 1|-1, scale, z, actions[]}
```

Each entry in `actions[]` is:
```
{at, do, dur, path: [[x, y], ...], speed, seated, mood: "happy"}
```

**Character styles**

| Style | Hair | Shirt |
|---|---|---|
| `a` | bun | coral |
| `b` | short | blue |
| `c` | long | yellow |
| `d` | ginger | mint |

**Actions**
- `idle`, `walk`, `run`, `sit`, `type`, `write`;
- `wave`, `point`, `think`, `lookup`, `jump`;
- `celebrate`, `climb`, `plant`, `sleep`.

**Action rules**
- `walk`, `run` and `climb` move the actor along `path`.
- `seated: true` keeps the legs sitting during `think`, `wave` and other upper-body actions.
- `celebrate` and `wave` smile automatically.
- Poses blend over 0.3 s.
- Eyes blink by themselves.

### fx and text

**fx:**
- `{"type": "glow", x, y, at, dur, r}`
- `{"type": "sparkle", x, y, at, r}`

**Text lines:** `{at, dur, text, y, size}`
- Mark the accent word as `*word*`.
- Lines auto-shrink to fit the width.
- Keep lines short.
- Place them at y=300, or near y=1680 when the top of the frame is busy.

## Sound (automatic)

| Event | Sound |
|---|---|
| Walk, run, climb | Footsteps |
| Typing, typewriter text | Key ticks |
| Write | Pencil |
| Mountain ledge appears | Rising "right" chime |
| Flag or plant | Stamp plus chime |
| Celebrate | Chime plus chord |
| Prop with `in` | Pop |
| Scene change | Whoosh |
| Text line appears | Soft tap |

The calm score is pads plus a pluck pattern. When there is narration, the voice ducks the score.

## Prompt to script tips

- Translate abstract ideas into places and objects:
  - dream → dreamcard or poster;
  - plan → stairs or mountain ledges;
  - progress → climbing;
  - done → flag plus celebrate.
- Follow the logic rule: the big goal comes first, then it breaks into the next small step. The big plan is never the villain.
