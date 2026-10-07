# stair to space

hook pattern: Impossible object
target: ~48s (130 words at 2.68 w/s)
engine: motion, new `stair.build` + `giant.step` scenes

> **The maths, done properly.** Space (Kármán line) is 100,000 m. From 1 Jan to 11 Sep
> 2026 is 254 days. 100,000 / 254 = **393.7 m per step**, call it 394 m.
>
> That is taller than the Eiffel Tower (330 m), every day, for 254 days. So the literal
> premise does not motivate anybody: it says the task is impossible.
>
> **So the absurd number becomes the hook, not the lesson.** We open on 394 m, let it be
> ridiculous for six seconds, then invert to the number that is actually true: a normal
> 17 cm step, 254 days, puts you 43 m up. The reel earns its turn instead of asserting it.

---

## Every figure on screen, verified

| figure | value | source |
|---|---|---|
| days, 1 Jan to 11 Sep 2026 | 254 | inclusive count |
| step needed to reach space today | 393.7 m | 100,000 / 254 |
| Eiffel Tower | 330 m | for scale |
| a normal stair riser | 17 cm | ~7 inch building standard |
| 254 normal steps | 43.2 m | ~14 storeys |
| a full year of them | 62.1 m | 365 x 0.17 |
| five years | 310.4 m | 310 m, NOT the tower: 330 m needs 1,941 days |
| days to reach the Eiffel Tower | 1,941 | 330 / 0.17, about 5 years 4 months |
| space at 17 cm/day | 1,611 years | 100,000 / 0.17 / 365.25 |

No invented figures anywhere. If a number is on screen it is checkable.

---

## VO script (record this exactly)

To be standing in space right now, you would have needed to build one step a day since
January. Each step three hundred and ninety four metres tall.

Taller than the Eiffel Tower. Every single day.

Obviously not.

So here is the real number. A normal step is seventeen centimetres. Two hundred and
fifty four of them, one a day since January, puts you forty three metres up. Fourteen
storeys. Higher than anything on your street.

Sixty two metres by New Year. One thousand nine hundred and forty one days and you
are level with the Eiffel Tower.

You are not getting to space. That was never the offer.

The offer is that the stair exists at all, and that you can see exactly how high you got.

Most people's stair has no steps on it. Not because they did not climb. Because nobody
ever wrote down when they started.

---

## Beat map (one visual per line)

| line | camera | visual |
|---|---|---|
| to be standing in space right now | slow crane up a vertical axis, 100 km at the top | a single line rising out of frame |
| each step three hundred and ninety four metres | hard cut to a wide, low angle | **one** colossal riser, Eiffel Tower drawn beside it for scale |
| taller than the Eiffel Tower, every day | push in on the tower, then whip up the riser | the tower is dwarfed |
| obviously not | camera settles, everything stops | the riser dims and is struck through |
| a normal step is seventeen centimetres | snap to an extreme close-up | one small step, drawn as two lines, measured |
| two hundred and fifty four of them | dolly back steadily as steps accrue | the staircase draws itself, step by step, left to right |
| forty three metres up, fourteen storeys | keep pulling back, roll the horizon slightly | a 43 m marker arrives beside the stair top |
| higher than anything on your street | wide | a street silhouette line passes below the stair |
| sixty two metres by New Year | continue back and up | the stair extends, a 62 m marker lands |
| 1,941 days, level with the tower | long pull back, tower rises into frame | the stair meets the tower's top exactly |
| you are not getting to space | hard pull back to the full axis | 100 km sits far above, unreachable, and that is fine |
| that was never the offer | hold | the space marker dims out |
| the offer is that the stair exists | push back in to the stair | every step visible, dated |
| you can see exactly how high you got | slow track up the stair | step numbers running 001 to 254 |
| most people's stair has no steps | cut to an empty axis | nothing drawn on it |
| because nobody wrote down when they started | settle | one dated step appears at the bottom |

**Sendable line:** "You are not getting to space. That was never the offer."

**Camera is the point of this one.** The user asked for movement: crane, whip, snap
cut, dolly back, roll. The stair is a static object; the camera does the acting.

---

## New scenes needed

**`stair.build`** - a line-drawn staircase in world coordinates that accrues one step at
a time, with an altitude axis and markers (43 m, 62 m, 330 m, 100 km) that arrive as the
stair passes them. Camera auto-frames the drawn portion, with `rot` on the keyframes so
the horizon can cant for a shot that feels handheld.

**`giant.step`** - one colossal riser with the Eiffel Tower drawn beside it to scale,
struck through on "obviously not".

**Do not recycle:** `receipt.print` (yesterday), `axis.travel` / `dream.stack` /
`rows.verdict` (`letter-to-future`), `year.grid` (`days-gone`).

---

## Layout

Everything inside the Reels safe band **y 240..1250**. A tall vertical subject fights
that band, so the axis has to be framed, not drawn full-height. Audit with `safearea.js`.

---

## Open question

Ending: pure comment CTA, or `dmyor.com`. Three reels have now gone out brand-free with
no performance logged for any of them, so the no-brand test still proves nothing.
