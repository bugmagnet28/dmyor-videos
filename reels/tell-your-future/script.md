# tell your future

hook pattern: Direct question
target: ~54s (136 words at 2.52 w/s)
engine: motion, narrated

> **Brand ON.** Say **"deemyor"**, put **dmyor.com** on screen.
>
> Delivery: plain and level. The question at the top is a real question, not a tease.
> Ask it, answer it, describe what the thing does, stop.

---

## VO script (record this exactly)

Is there a way to tell your future self what your dreams and plans actually were?

Because most of it gets forgotten. Not the big ones. The specifics. What you wanted,
when you wanted it by, and why it mattered at the time.

That is what deemyor is for.

You write down what you intend to do. It gets today's date. It goes into a public
archive. It stays there.

Phase one is live now. That is the writing it down part.

It will not remind you. It will not track your progress. That is phase two, and it is
not built yet.

What phase one gives you is one thing. In five years there is a dated record of what you
said, in your own words, that you can go back and check.

Deemyor dot com. Write one down today.

---

## Structure

**Question, then answer, then scope.** No build-up, no reveal, no guessing at the
viewer's inner life. The hook is a question they can answer yes or no to in their head,
and the rest of the reel is the answer.

| section | t | what it does |
|---|---|---|
| the question | 0 to 6 | asks it plainly |
| the reason | 6 to 17 | what actually gets lost: the specifics, not the ambition |
| the answer | 17 to 32 | four factual statements about what the product does |
| the scope | 32 to 42 | what it does **not** do, and that phase two is not built |
| the one claim | 42 to 50 | a dated record you can check |
| CTA | 50 to end | dmyor.com |

**"Most of it gets forgotten" is the only general claim in the script**, and it is stated
without a number. I have no data on how often people forget their goals, so inventing a
statistic would undercut the whole point of a factual script.

**The limitation stays in.** "It will not remind you. It will not track your progress."
Saying it out loud costs nothing and makes the single real claim credible.

**The specifics line is the strongest idea in it:** what disappears is not the ambition,
it is *what you wanted, by when, and why it mattered*. That is exactly what a dated
record preserves, so the problem and the product line up without any persuasion.

---

## Beat map (one visual per line)

| line | scene intent |
|---|---|
| is there a way to tell your future self | today's date on the left, a date five years out on the right, nothing in between |
| what your dreams and plans actually were | one card appears at today's end |
| because most of it gets forgotten | the card's contents drop away, leaving the outline |
| not the big ones, the specifics | three labelled fields: **what**, **by when**, **why** |
| what you wanted | field one empties |
| when you wanted it by | field two empties |
| why it mattered at the time | field three empties, the card is now blank |
| that is what deemyor is for | the blank card fills back in, all three fields |
| it gets today's date | the date stamp lands, 16 SEP 2026 |
| it goes into a public archive | it joins other dated rows |
| it stays there | nothing moves |
| phase one is live now | phase one lit |
| it will not remind you, will not track you | phase two shown explicitly dim and empty |
| in five years there is a dated record you can check | the span from the opening returns, now with a record at each end |
| deemyor dot com | dmyor.com |

**Sendable line:** "Not the big ones. The specifics. What you wanted, when you wanted it
by, and why it mattered at the time."

**The three fields are the spine.** `what / by when / why` empty out one at a time in the
problem half, and fill back in one at a time in the solution half. Same diagram, run
backwards then forwards. The viewer does not need to be told what changed.

**Bookend the span.** The five-year line opens the reel empty and closes it with a dated
record at both ends. That is the argument, drawn.

---

## New scene needed

`fields.empty` - a card with three labelled fields (`what`, `by when`, `why`) whose
values drain away one at a time, then refill. The labels stay put the whole time; only
the values move. Reused in both halves, run in opposite directions.

**Do not recycle:** `card.pressure` (`not-storage`). `stair.build` and `receipt.print`
were rejected. `phase.marks` and `archive.scroll` fit and are already built.
`ambient.field` stays, tuned quiet: this reel is an explanation, not a mood piece.

---

## Layout

Captions top, graphic below, everything inside the Reels safe band **y 240..1250**.
Audit with `safearea.js` before recording.
