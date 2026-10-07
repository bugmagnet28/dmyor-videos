# Why the first 12 reels underperformed (diagnosis, 2026-10-08)

Status: **hypotheses from a craft review**, not yet confirmed by numbers. No performance data was logged for any reel (`reel.py report` = empty). Confirm or reject each point once metrics land in `inbox/metrics/`.

Method: watched frames at 0.3s, 1s, 2s, 3s and 10s of four reels (tell-your-future, four-months-left, the-resistance, year-itemised), read all scripts and meta, measured every duration.

## The numbers we do have

| Reel | Length | Hook pattern |
|---|---|---|
| phase-one-launch | 100s | Impossible object |
| four-months-forward | 83s | Forward count |
| the-resistance | 75s | The question |
| not-storage | 61s | Direct challenge |
| documented-odds | 59s | No start date |
| four-months-left | 53s | Countdown |
| letter-to-future | 47s | Impossible object |
| tell-your-future | 47s | Direct question |
| days-gone | 43s | Countdown |
| stair-to-space | 42s | Impossible object |
| year-itemised | 31s | Receipt |

Median length about 53s. Account size: 0 followers.

## Likely causes, most important first

1. **Nothing is on screen at the moment people decide to scroll.** In 3 of 4 reels checked, the frame at 0.3s is empty or a grey placeholder: black screen and cursor (four-months-left), blurred gradient (the-resistance), grey box (year-itemised). Text types in word by word, so the hook is only readable at 1 to 3s. On Reels and Shorts the scroll decision happens in under a second, and the first frame is also the cover in the grid.
2. **Too long for a new account.** 42 to 100s. With no followers, distribution is driven by completion and rewatch rate, and long explainers bleed viewers every second. New accounts usually get traction in the 7 to 25s range.
3. **Too small and too dark to read on a phone.** Key elements (timeline dates, the month grid, form fields) sit in the middle third at small sizes, thin weights, low contrast on navy/black. Large parts of the frame are empty. It reads as "premium website", not "stop scrolling".
4. **Mostly silent without sound.** Captions are off by default and the voice carries the message, but most people watch muted. Muted, several reels are a few small words on a dark screen.
5. **About the product, not about the viewer.** Several scripts spend a third of their time on "phase one is live, phase two is not built yet". Viewers don't share or save a product status update. What gets shared: a sharp truth about their own life, a useful tool, or a number that stings.
6. **Slow pacing.** A new visual every 3 to 5s; the strongest reels change something every 1 to 1.5s.
7. **No reason to rewatch or save.** No loop, no list, no "save this for January".
8. **Weak brand recognition.** Narration says "deemyor" while the screen says "dmyor", and the brand card comes at the end. A new account needs a consistent look people recognise at a glance.

What was good and should be kept: honest scripts with no fake claims, a recognisable art direction, frame-accurate rendering, and quality checks (no dead air, no snaps, safe areas).

## Experiments to run (one change at a time where possible)

| ID | Change | Measure | Success |
|---|---|---|---|
| V-EXP-01 | Frame 0 = full-screen bold statement (90 to 120px type, high contrast), readable at 0.0s | 3-second hold rate, avg watch % | Hold rate up vs. previous reels |
| V-EXP-02 | Length 12 to 25s | avg watch %, completion | Over 50% watched |
| V-EXP-03 | Large burned-in captions always on | avg watch, views | Up vs. captions off |
| V-EXP-04 | Viewer-first topics (a specific pain, a number, a "you" moment); product only in the last 2 to 3s | shares + saves per view | Above 1% |
| V-EXP-05 | A new visual every 1 to 1.5s | avg watch % | Up |
| V-EXP-06 | Show the real dmyor canvas (actual UI) vs. abstract shapes | profile visits, follows per view | Higher follows |
| V-EXP-07 | Saveable formats ("3 questions to plan 2027", checklists) with "save this" at the end | saves per view | Highest saves |
| V-EXP-08 | Brighter, fuller-frame palette vs. the current dark navy | 3-second hold | Up |

## What the video agent will do with this

- Treat these as open hypotheses in its experiments list; confirm or kill each as numbers come in.
- Never repeat a pattern that has data saying it loses.
- Re-analyze old reels once their real numbers are in `inbox/metrics/`, and update this file's status.
