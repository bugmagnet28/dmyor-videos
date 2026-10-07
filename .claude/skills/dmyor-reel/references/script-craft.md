# Writing a dmyor script

## What dmyor is
A public, dated archive of what people intend to do. You write a dream; it sits at
`standby`; when it happens the record shows it became real. Phase one (live now) is
writing it down. Phase two is the tooling to actually get there. The pitch is
*permanence and verification*, not motivation.

## Voice
- Plain, unhurried, slightly dry. No hype words, no "unlock", no "journey".
- Second person. The viewer is the one with the dream.
- Concrete over abstract: "buy my parents a house" beats "achieve your goals".
- Admit the obvious. The first reel worked partly because it said *"we all know there
  is no magic diary"* - conceding the objection buys credibility for the real claim.
- Never promise outcomes. dmyor records intent; it does not grant wishes.

## Structure that has worked
1. **Hook (0-5s)** - a hypothetical or a question the viewer answers in their head.
2. **Turn (5-15s)** - undercut the hook. The fantasy fails.
3. **The real thing (15-40s)** - the archive. Dated, public, permanent.
4. **Stakes (40-55s)** - why permanence matters; the five-year frame.
5. **What to do (55-85s)** - phase one, concretely, with the actual UI.
6. **CTA (85-end)** - phase two teaser + the URL.

Not every reel needs all six. A 30s reel is usually 1-3-6.

## Hook patterns
| Pattern | Example | Use for |
|---|---|---|
| Impossible object | "If you had a diary where every dream came true..." | cold audience |
| Dated callback | "In 2031 someone will check if you did this." | permanence angle |
| Direct challenge | "Name the thing you keep not starting." | engagement bait |
| Receipt | "12,480 dreams are on record. None of them are yours." | scale/FOMO |
| Countdown | "There are four months left in 2026." | seasonal / deadline pressure |

Log which pattern each reel used in `script.meta.json` - `report.py` correlates
pattern against reach.

## Length
Pace measured from real recordings is ~2.4-2.6 words/sec. Run `reel.py rate` for the
current number from actual audio files rather than assuming.

| Target | Words | Notes |
|---|---|---|
| 30s | ~75 | one idea, hard CTA |
| 60s | ~150 | hook + turn + archive + CTA |
| 100s | ~240 | the full six-beat structure |

Longer is not worse if retention holds, but check the report: watch-through % falls
off a cliff past the point where a reel stops introducing new information.

## The brand is spelled two ways, on purpose
The written mark is **dmyor**. Voices mispronounce that, so the VO script spells it
**deemyor** (and `www.deemyor.com`). Keep them split: `script.md` says deemyor because
it is read aloud; `timeline.json` `brand` says dmyor because it is read on screen.
Record both in `script.meta.json` as `brand_spoken` / `brand_written`. Do not
"correct" one to match the other.

## Rules
- Write for the ear. Read it aloud; if you stumble, rewrite.
- One idea per sentence. The animation needs a cue per beat.
- Put the concrete noun early in a sentence so the visual can land on it.
- End on the URL, spoken slowly - the animation types it in sync.
- No em dashes in copy. Use a colon, a period, or a comma.
