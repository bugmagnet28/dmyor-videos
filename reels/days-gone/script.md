# days gone

hook pattern: Countdown
target: 43s, no narration
engine: motion (`year.grid`)

> NO VO. The sound design is the whole soundtrack: 107 synthesised cues driven off the
> same reveal and fill curves the animation uses, so every tick lands on a real day.
> Built with `sfx.py --no-vo`, which runs the effects bed at full level instead of
> ducking it under a voice. The closing captions carry sound too: `sfxWords` puts a
> tick on every word, `sfxChime` opens the final card. 107 cues total.

---

## The idea

Captions sit at the top and the graphic below them, so nothing lands under the
Instagram UI. One continuous pull-back through five scales. A single box becomes a week, becomes a
month, becomes the year. Days that have already happened fill in solid. The days still
ahead stay empty, and there are fewer of them than you think.

Dated 8 September 2026: **251 days gone, 114 left.**

The 114 is deliberate. It is the same four months the previous reel was about.

---

## On-screen copy (there is no other text)

| t | on screen |
|---|---|
| 0.7 | Visualising how many days you wasted in 2026 |
| 4.2 | one box is one day |
| 7.6 | one month |
| 13.4 | then another |
| 18.6 | 2026 so far |
| 25.4 | **251** / days gone |
| 29.4 | **114** / days left |
| 33.4 | You don't have to wait another **four months** to start again. |
| 38.6 | Check out **dmyor.com** and make a move, **today.** |

---

## Beat map

| t | scale | what happens |
|---|---|---|
| 0.3 | one cell, 300px | a box appears and fills |
| 4.4 | a week, 122px cells | six more arrive, the row fills left to right |
| 7.4 | a month, 100px cells | four rows drop in, January fills day by day |
| 12.4 | two months | February lands beside it |
| 14.8 | four months | the pace picks up, the fill front becomes visible |
| 17.4 | eight months | months arriving faster than they can be counted |
| 20.6 | nine months | September stops eight days in |
| 23.4 | the year | Oct/Nov/Dec revealed and left empty, month labels fade up |
| 25.4 | hold | 251 gone |
| 29.4 | hold | 114 left, in amber |

**The point of the pull-back:** each step has to zoom out *further* than the last. That
is only possible because the year grid is 2 columns wide and grows downward. At 3
columns the grid maxes out its width after three months and every later zoom stalls,
which is the whole effect dead. See the note in `animation-cookbook.md`.

**Camera leads the reveal.** A cell must never appear outside the frame that is about to
contain it. Every widen keyframe sits ~1s before the reveal batch it holds.
