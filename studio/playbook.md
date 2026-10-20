# Playbook (video)

Rules learned from evidence. Each cites its source. Revise when data disagrees.

- **Visual style (owner decision, 2026-10-20): calm, small, aesthetic type.** Sanyam found the full-frame heavy text too big. The punch engine now defaults to `style: "calm"`: the whole text layer renders at 0.62x, semibold weights, softer palette, content nudged toward the visual centre. Write timeline sizes as before (the px rules below are design units before the 0.62 shrink). Never set `"style":"loud"` or a `typeScale` above 0.7 unless Sanyam asks. Keep one idea per screen with lots of empty space; fewer words per beat beats bigger words. Source: Sanyam's 2026-10-20 review.
- (starter) Frame 0 must be readable (calm style: readable, not loud). Source: diagnosis 2026-10-08 (3 of 4 old reels opened on an empty frame).
- (starter) Watch your own frames before packaging. Source: setup.
- (starter) Every video tests a named experiment with a written expectation. Source: setup.
- Use the `punch` engine (`"engine":"punch"`) for no-VO reels: heavy type on flat bright panes, frame 0 drawn finished. Put the full hook at `at: 0`. Source: diagnosis 2026-10-08 + frame check of twelve-weeks-one-thing. Revisit once V-EXP-09 has numbers.
- Put hand-placed sound on frame 0 (`"sfx":[{"t":0,"v":"thud"}]`), otherwise the first second is silent: the timeline rules only fire on entrances after 0. Source: twelve-weeks-one-thing dry run.
- Date-bound hooks ("12 weeks left") must state their valid posting window in post.md and post-queue. Source: twelve-weeks-one-thing.
- Fill the safe band: body/answer text 124px+ (never 60px list rows), blocks start y 300-360 and end near y 1150-1250. Source: Sanyam's 2026-10-08 review note + next-step-not-motivation frame check.
- Run probe.js on any block that safearea flags: a silent wrap (two lines' cy ~200px apart instead of ~145) is the usual cause; reword to <= 10 chars per line at 140-150px rather than shrinking below 124px. Source: three-questions-before-a-goal build (2026-10-10), next-step-not-motivation (2026-10-09).
- Make evergreen (not date-bound) reels while more than 2 videos sit unposted in the queue. Source: twelve-weeks-one-thing reached its last valid day unposted (2026-10-11).
- All-caps and quoted words in the punch engine: budget ~7 caps chars at 165px; run overflow.js after any caps line. Source: someday-is-not-a-day build (2026-10-12), overflow at 190px.
- Before packaging, ffprobe the mp4: duration must equal timeline `total` and the file must have a video stream. Record with `caffeinate -dims` and never end a run while record.js is still running. Source: 2026-10-13 run lost its render; 2026-10-14 first record of plan-the-bad-day died at 2.5s.
- In a stack, use gap >= 0 under any line with descenders (g, p, y, j, q) below 190px; audits do not catch overlap inside one scene, only the frame check does. Source: plan-the-bad-day "Open the / book." (2026-10-14).
- At run start, ffprobe the newest ready-to-post video.mp4 (exists, duration == timeline total); recover a missing render before building anything new. Recording uses record.js with Chrome auto-relaunch (2026-10-16); still never end a run with a record in flight. Source: 10-13 and 10-15 runs ended with no video; learnings 2026-10-14, 2026-10-16.
- Loop endings: add a small lead-in line plus an exact copy of the frame-0 stack (same y, sizes, colours) entering about 1s before the end. Check with probe.js that positions at t=total-0.1 match t=0. Budget ~8 chars at 195px for 2-line hooks. Source: too-many-goals build (2026-10-19); audience effect still untested (V-EXP-14/20).
- A beat that is the moment of tension (countdown digit, the number of a reveal) must be the biggest thing on screen at that moment (180px+); use per-swap `size` rather than keeping the title size. Source: which-one-is-a-plan v1 frame check (2026-10-20).
