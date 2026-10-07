# 2026, itemised

hook pattern: Receipt (first use)
target: ~31s, NO VOICEOVER
engine: motion, new `receipt.print` scene

> No voice. On-screen text carries it and the sound design is the whole soundtrack:
> a thermal printer chattering out one line at a time, a bell on the total, a stamp
> at the end. Built with `sfx.py --no-vo`.
>
> **The joke only works if the numbers are real.** 36 Mondays, 254 days used, 111 days
> left are all true for 11 September 2026. The invented counts are obviously rhetorical
> (they are about the viewer, not about dmyor) and must stay that way: never put a
> fake dmyor statistic on screen.
>
> Deadpan. No exclamation marks, no emoji, no winking. The comedy is in the accounting.

---

## On-screen copy (there is no other text)

**Header**
```
          2026
   YOUR YEAR, ITEMISED
```

**Items** (print one line at a time, dot leaders, right-aligned figures)
```
plans announced out loud ............. 14
plans given an actual date ............ 0
Mondays identified as "the" Monday ... 36
notes titled "goals" .................. 6
of those, still readable .............. 1
times you said "next year" ........... 22
```

**Totals** (after a rule)
```
DAYS USED ........................... 254
DAYS LEFT ........................... 111
```

**Stamp**
```
        STILL ENOUGH
```

**Close**
```
   what is on your receipt?
```

---

## Beat map

| t | on screen | sound |
|---|---|---|
| 0.0 | receipt slides up into frame, blank | paper feed |
| 0.6 | `2026` lands | thud |
| 1.4 | `YOUR YEAR, ITEMISED` | soft clack |
| 2.6 | item 1 prints, figure snaps in last | printer chatter, tick on the figure |
| 4.4 | item 2 prints. **The 0 lands in coral** | chatter, then a flat low tone |
| 6.4 | item 3 prints | chatter |
| 8.4 | item 4 prints | chatter |
| 10.2 | item 5 prints, `1` lands small and sad | chatter, single tick |
| 12.2 | item 6 prints | chatter |
| 14.4 | rule draws left to right | zip |
| 15.2 | `DAYS USED 254` | roll up to 254, bell |
| 17.6 | `DAYS LEFT 111` in amber, larger | roll down to 111, deeper bell |
| 20.4 | receipt holds, everything visible | room tone |
| 21.6 | `STILL ENOUGH` stamps on at an angle, green | stamp thud + paper |
| 24.4 | receipt slides down, close card wipes in | paper out |
| 25.2 | `what is on your receipt?` | chime |
| 31.0 | end | |

**The turn is at 17.6.** Everything before it is the joke at your expense; `111` is the
line that makes it not a joke. It gets the biggest type and the only warm colour.

**Sendable line:** "DAYS LEFT 111. STILL ENOUGH."

---

## Why the items are in this order

1. `14` sets the deadpan register.
2. `0` is the punchline of the whole reel and it arrives second, not last, so the rest
   plays under it.
3. `36` is the one that stings, because it is true and checkable.
4. `6` then `1` is a two-line joke: the setup and the payoff are separate rows.
5. `22` closes the run on the phrase this whole product exists to kill.

---

## New scene needed

`receipt.print`: a cream receipt on a dark pane. Rows print top to bottom with dot
leaders that stretch to fill, figures snapping in after their label. Needs a rule, two
total rows, and an angled rubber stamp.

Visually this is a deliberate break from the last three reels, which were all outlined
chips on dark panes. A light paper object reads as a *thing*, not a slide.

**Do not recycle:** `axis.travel`, `dream.stack`, `rows.verdict` (`letter-to-future`),
`year.grid` (`days-gone`).

---

## Layout

Receipt centred in the Reels safe band **y 240..1250**, bottom third left clear.
Audit with `safearea.js` before recording.

---

## Open question

Ending: `what is on your receipt?` as a pure comment CTA, or add `dmyor.com` under it.
Two reels have now gone out brand-free as a test and **no performance has been logged
for either**, so the test currently proves nothing either way.
