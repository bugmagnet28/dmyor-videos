# make a choice

hook pattern: Direct statement
target: ~52s (147 words)
voice: ElevenLabs, **v3 model required** (see note at the bottom)
engine: motion, narrated

> First reel on the new positioning: the product is the daily choice, not the archive.
> Say **"deemyor"**, put **dmyor.com** on screen.
>
> Tone: level and certain, not hyped. The emotion sits under the line, never on top of it.
> The only lift is at "you will not be stuck", and it is quiet confidence, not triumph.

---

## VO script, tagged for ElevenLabs v3

```
[thoughtful] Everything that happens to you next is the result of choices you make today.

[matter-of-fact] Not the big ones. Those are rare.

The small ones. The one you make on a Tuesday, at nine in the morning, about what you
actually do with the next hour.

[serious] And here is the problem... most days, you don't make one at all. The day just
happens to you.

[confident] So that is what deemyor does.

Every morning it gives you three things you could do today that move your goal forward.
Real ones, pulled from your own plan.

[warm] You pick one. That's it. Ten seconds.

[sincere] It will not promise you the outcome. Nobody can promise you that.

[confident] What it promises is this. Make a choice every day... and in two months you
will be somewhere.

[quiet] You will not be stuck.

[warm] Deemyor dot com. Make today's choice.
```

---

## Clean version (no tags)

Paste this one if you are on Multilingual v2 or Flash, which read brackets aloud.

```
Everything that happens to you next is the result of choices you make today.

Not the big ones. Those are rare.

The small ones. The one you make on a Tuesday, at nine in the morning, about what you
actually do with the next hour.

And here is the problem... most days, you don't make one at all. The day just happens
to you.

So that is what deemyor does.

Every morning it gives you three things you could do today that move your goal forward.
Real ones, pulled from your own plan.

You pick one. That's it. Ten seconds.

It will not promise you the outcome. Nobody can promise you that.

What it promises is this. Make a choice every day... and in two months you will be
somewhere.

You will not be stuck.

Deemyor dot com. Make today's choice.
```

---

## ElevenLabs settings

| Setting | Use | Why |
|---|---|---|
| **Model** | **Eleven v3** | Audio tags only work here. v2 and Flash will either speak the brackets or drop them. |
| **Stability** | **Natural** | Creative over-acts the tags on a script this plain. Robust mostly ignores them. |
| Similarity | 75 to 85 | |
| Speed | 0.95 to 1.0 | The ellipses already carry the pauses. |

**Tags used, and why each one is there**

| Tag | Line | Doing what |
|---|---|---|
| `[thoughtful]` | opener | lands it as an observation, not a slogan |
| `[matter-of-fact]` | "Not the big ones" | keeps the correction from sounding clever |
| `[serious]` | "here is the problem" | the only dark beat in the script |
| `[confident]` | "that is what deemyor does" | the turn into the product |
| `[warm]` | "You pick one" | the product should feel small and easy here |
| `[sincere]` | "will not promise" | the concession has to sound meant |
| `[quiet]` | "You will not be stuck" | the payoff line, under-played on purpose |

Eight tags in 147 words. Resist adding more: ElevenLabs degrades when tags are dense, and
this voice should sound like a person stating something, not performing it.

**The ellipses are doing real work.** Three of them, all before a turn. If you need a
longer gap, `<break time="0.7s" />` works, but ellipses sound more human.

---

## Notes on the script

**The claim is honest, and that is the point.** "It will not promise you the outcome.
Nobody can promise you that." This is the same concession that carried the earlier
reels, and it is why the final line is believable. The product genuinely cannot deliver
a million people. It can deliver not-stuck.

**"Tuesday, at nine in the morning" is the only concrete detail**, and it is doing more
than it looks. The whole argument is that the small choices decide it, so the script has
to name a small moment rather than describe one.

**No statistics.** No "most people fail at X percent". There is no data for that and an
invented number would undercut the one real claim.

**Sendable line:** "Not the big ones. Those are rare. The small ones."

---

## Beat map (for the build)

| line | scene intent |
|---|---|
| everything that happens next | a branching path, one node today, many ends |
| not the big ones, those are rare | the big branch points dim out, leaving the small ones |
| Tuesday, nine in the morning | zoom to one ordinary node, timestamped |
| most days you don't make one at all | the node greys, the path stalls, no branch taken |
| the day just happens to you | the path drifts without a decision marker |
| that is what deemyor does | three live options appear off one node |
| three things you could do today | each labelled, specific, pulled from a goal above |
| you pick one | one lights, the other two fade, the path advances |
| ten seconds | a short timer, under-stated |
| it will not promise you the outcome | the far end of the path stays deliberately unresolved |
| make a choice every day | sixty nodes accumulate, a visible line of taken choices |
| you will not be stuck | the line has clearly travelled, destination still unnamed |
| dmyor.com | brand card |

**The visual argument:** a path made of daily nodes. Not taking a choice is a grey gap.
Taking one advances the line. Sixty of them is a visible distance covered, which is
exactly the promise the script makes and the only one it makes.
