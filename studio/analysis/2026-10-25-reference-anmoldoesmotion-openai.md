# Target reference: @anmoldoesmotion, "a personal motion project for OpenAI" (shared by Sanyam 2026-10-25)

https://www.instagram.com/p/Dcn6EINyzaa/ · 31 s · 1280x720 (16:9) · 11.1K likes · August 2026. Owner: "that's the kind of animation and effects we are trying to reach."

## Beat sheet (studied frame by frame, muted)

| t (s) | What happens | Technique |
|---|---|---|
| 0-1 | Black, two hairline crosshair lines, tiny glyphs drifting, "100 signals" in blue + white | hairline grid, two-tone kinetic type |
| 2 | "too many thoughts": white type over a cloud of code snippets at different depths, far ones blurred | 3D z-depth layers + depth-of-field blur, parallax |
| 3 | Everything collapses into one glowing blue point; a sine wave runs into it | bloom/glow light point, line that "carries signal" |
| 4-7 | The point splits into ~10 thin white fibres that curve out to labelled nodes: "12 new messages", "research_final_v4", "meeting at 5pm", "app.py", "tomorrow" | bezier fibres drawn on, icon + label + small meta line, staggered |
| 8-9 | Fibres collapse into a blue ring; the ring zooms (concentric tunnel) and the scene flips from dark to light | morph transition, tunnel zoom, dark → light colour turn |
| 10 | "OpenAI" assembles letter by letter on a light construction grid (circles, guides) | wordmark build on a design grid |
| 12 | Calm beach photo, "What will we build?" + a frosted-glass prompt box typing a request | photo plate + glass UI (blur, soft shadow) |
| 14-15 | Dozens of designed posters burst outward radially; "Seconds" resolves in blue | radial burst, motion blur, word morph |
| 16-21 | Code editor window on a misty forest photo; lines get green ticks one by one, one red line flashes red (colour grade flips red), then a voxel cube builds next to the code and recolours | glass window on photo, tick cascade, colour-grade flash, particle/voxel object |
| 22-26 | Warm paper texture; scattered dots with labels (Clients, Feedback, Files, Reports…) and small counters ("48 ↑") rise, then a hand-painted brown **tree grows**, branches reaching each dot, leaves and blossoms open | organic growth animation, data labels on branches, paper grain |
| 28-31 | Flowers against blue sky, "One place to Imagine", then the logo | photo outro, two-tone tagline, logo lockup |

## Why it feels premium (vs our current reels)

1. **One continuous camera.** Every scene *becomes* the next (point → fibres → ring → tunnel → grid). No crossfades and no hard cuts.
2. **Depth and light.** Blur by depth, bloom on light sources, glass panels, soft shadows. Ours are flat 2D vector.
3. **Mixed media.** Vector lines + real photography + realistic UI windows + a 3D-ish voxel object + a painted tree on paper texture.
4. **A story in the visuals, no narration.** Chaos ("too many thoughts") → one signal → connections → clarity → calm → brand.
5. **Colour as emotion.** Dark/chaotic → bright/calm; one red flash for the problem; one blue accent throughout.
6. **Restraint in type.** 2-3 words on screen at a time, two-tone (accent + white), lots of empty space.

## Why it fits Dmyor almost exactly

Its arc is Dmyor's pitch:
- scattered thoughts and dreams → one place → connected → a **tree that grows** with labelled branches → "One place to …".

The tree scene is literally our vision → milestones → steps metaphor, just painted and organic instead of a diagram.

## What it takes in our pipeline (HTML page as a function of time → frames)

- **Feasible:**
  - canvas 2D/WebGL with additive blending for glow, CSS/canvas blur for depth of field;
  - one world → screen camera function for continuous push-ins and morphs;
  - bezier fibres;
  - glass panels (backdrop blur);
  - procedural tree growth (L-system or hand-authored branch paths with stroke reveal plus a bark texture);
  - particles and voxels (three.js);
  - photo plates. The photos must be licensed, e.g. Unsplash/Pexels licence or our own.
- **Format change:**
  - re-compose for 9:16 (vertical fibres, the tree grows bottom-up);
  - render at 30 fps;
  - sound: whooshes on morphs, a soft hum on the light point, ticks on checks, a riser into the logo. (We said no music; this reference likely has music. Ask Sanyam whether a subtle score is wanted for the flagship.)
- **Closest saved style prompts:** `reference/lemo-opuscar/styles/dark-keynote` (dark stage, light sweeps, UI as hero) and `TECHNIQUE.md` sections 2 and 9 (camera, 3D).
