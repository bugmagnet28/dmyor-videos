# Content Kit v2 (adopted 2026-10-28)

How every new reel is scripted, from the owner's "Content Kit v2" PDF (October 2026), adapted to `OWNER-RULES.md`. Where the PDF and OWNER-RULES disagree, the decisions in section 0 apply. Posting, scheduling, approval and analytics are unchanged. Applies to new batches only: do not retrofit old reels.

**Why:** reels earn views from strangers (98.7% non-followers, 30 days to 2026-10-28) but 0 follows. V1 designed only the first 1.5 seconds. V2 designs the three moments a viewer decides to stay: about 1.5 s, 10 s and 25 s, and gives the outro a real reason to follow.

## 0. Decisions on the PDF (Claude, delegated by Sanyam 2026-10-28: "do whats best")

| PDF says | Decision | Why |
|---|---|---|
| No generic "pop"; object sounds only | **Keep the owner's pop on scene changes** (2026-10-27 rule). Inside a scene, anything that is an object makes its own sound; a pop is only for abstract items (labels, cards) | Owner chose the pop explicitly; the PDF's point (objects sound like themselves) is kept |
| One payoff sound per reel | **Check marks keep their rising "right" chime** (feedback). Add exactly **one distinct payoff sound** at the reveal (stamp, book closing or chord), different from the chimes | Feedback and payoff are different jobs |
| Hook templates with numbers / "most people" / "I did X" | **Owner 2026-10-29: allowed.** Number hooks may be rhetorical ("Half of those blocks will never happen"). Still never attribute a number to a study, survey or research, never fake Dmyor user numbers or testimonials, and the method inside the reel must be real | Owner decision; keeps hooks strong without fake "research" |
| Sources: Pexels, Pixabay, Unsplash, Openverse, Commons | **CC0 only** (Openverse filter `license=cc0`). Unsplash is banned (blocks automation). Pexels/Pixabay need a new owner decision | Owner said CC0 on 2026-10-28 |
| Real photo/video preferred for stakes and proof beats | **Not yet.** Our engines are drawn canvases with no video layer. A real-footage hybrid style is the next style to build (it also gives the missing 2nd daily style). Until then the shot list uses the fallback ladder steps 3-4 (illustration, designed canvas) | Pipeline cannot play footage today |

## 1. Pick the story structure first

Write at the top of `script.meta.json` (`"frame"`): structure, want, obstacle, cost in numbers.

- **A. Method with stakes** (default): hard truth -> a named situation where it matters -> method in 2-3 steps -> the moment it nearly fails -> concrete payoff -> sendable line.
- **B. Want, obstacle, choice, payoff** (character story): a character wants a specific outcome by a specific time -> obstacle -> they choose the method at a visible cost -> payoff shown, not described -> bridge to the viewer before naming Dmyor.
- **C. Mistake, cost, fix** (best for saves/shares): show the mistake -> count its cost in numbers -> the one change -> corrected version side by side -> end on a rule or checklist worth a screenshot.

Rules: one want, one obstacle per reel. "You" can be the character if the situation is specific. Costs are numbers (minutes, rupees, days, reps), never "it wastes time". The payoff is shown as a finished thing (filled page, completed week, before/after).

## 2. Hooks: write three, keep one

Lead with a hard truth (our only hook signal: 2.8x, now 4.1x; question hooks 0.4-0.5x). Never open with a question, greeting, title card or logo.

**Triple hook in the first 1.5 s:** picture shows the problem or payoff (finished on frame 0, something moving), on-screen truth in 6 words or fewer, the first spoken line is the truth itself, and **one object sound in the first second** (sfx.py does this automatically from the hook scene's first object sound; pick a hook scene that has one).

**Hook score, all five must pass:** hard truth not a topic; a specific curiosity gap; works muted; at least one sendable line in the reel; payoff promised concretely.

**Hook bank** (fill the brackets):
- The thing nobody admits: "You don't stop [habit] because you're lazy. You stop because [real reason]."
- The expensive mistake: "This one [mistake] costs you [amount/time from the reel's own example] every [week]."
- The 2-minute version: "You don't need [big system]. You need [small action] for two minutes."
- The backwards rule: "[Common advice] works, but only if you do it backwards."
- The day it breaks: "Day [n] is where [the plan] breaks. Here's why."
- Stop doing this first: "Before you [method], stop [habit]. It cancels everything."
- The check you can do now: "Open [app/calendar]. If you see [signal], this is already happening to you."
- The honest trade-off: "[Method] works. Here's what it actually costs you."
- The friend line: "Send this to the friend who [behaviour]."
- The before picture: "This is [your desk/budget/week] before. Wait for after."
- The rule of one: "One [page/rule]. That's the whole system."
- The hidden step: "Every tutorial skips step [n]. It's the only one that makes the rest work."
- The uncomfortable comparison: "Same [time/income]. One [outcome A], one [outcome B]. The difference is boring."
- The thing you already own: "You already own everything you need for [result]. It's in [place]."
- The screenshot moment: "Screenshot this [checklist]. You'll need it on [day]."
- The restart: "If I had to start [goal] from zero, I wouldn't start with [obvious step]."
- The last line first: "The answer is [payoff]. Here's why it works."
- The number that changes it: "[Number]% of [result] comes from [one overlooked step]. Here's the step."
- Also allowed (owner 2026-10-29): "[n]% of [result] comes from [one step]", "[n] of those blocks will never happen", "The first ten minutes decide the day. Most people waste nine of them", "I removed [one thing] for a week...", "The 7-day test: day four is where almost everyone quits". Never add "studies show" or name a source that does not exist.

## 3. Beat map (fill before animating)

| Time | Beat | Must include |
|---|---|---|
| 0-1.5 s | Triple hook | problem/payoff in frame, truth text, object sound |
| 1.5-5 s | Promise | concrete payoff stated, the crucial piece withheld (open loop) |
| 5-10 s | Stakes | a specific situation, a number, a person or "you" |
| ~10 s | Re-hook 1 | cost of doing nothing, or "step two is where it breaks" |
| 10-25 s | Method part 1 | steps 1-2 done, new visual every 1.5-3 s, one pattern interrupt |
| ~25 s | Re-hook 2 | a beat question (questions are fine here), visual escalation, **near-silence 1** just before |
| 25-42 s | Payoff | the withheld piece shown as a finished thing; **near-silence 2** before the payoff line; the one payoff sound |
| ~42 s | Save moment | rule/checklist full screen, held 2 s+ |
| end | Close | value close (owner, unchanged) -> one concrete follow reason -> "link in bio" |

Write it into `script.meta.json` as `"beats"`: hard_truth, open_loop (promised / withheld), stakes, rehook_10, interrupt, rehook_25, save_moment, share_line, follow_reason. Put the two near-silence times into the reel config as `"silences": [t1, t2]` after timing to the voice.

**Ending order** (fixes the 0-follows gap without dropping the owner's value close): share line inside the payoff section -> "That's what Dmyor is for. You archive your dream today..." -> follow reason naming the next concrete thing ("Follow, tomorrow's reel is the bad-day version of this plan") -> "If you want to try it out, I've put the link in the bio." The follow reason must be true: name a reel that is actually scheduled next, or the next part of a series.

## 4. Sound: five layers

1. **Voice** carries the story; nothing masks a word.
2. **Object sounds** sound like the object. Real CC0 recordings from `studio/sfx-library/real/` replace the synth automatically (`studio/sfx-library/use.py`). Level raised +4 dB from 2026-10-28 (about 10 dB under the voice), under test on the next batch.
3. **Ambience bed**: a quiet CC0 room tone under the whole reel (~27 dB under), from `studio/sfx-library/real/ambience-room.wav` (or config `"ambience"`). Not music; the explainer music question stays open (section 7 of OWNER-RULES), to be settled by an A/B pair.
4. **Transitions**: pop on scene changes (owner), soft whoosh only on real swipes.
5. **Payoff and silence**: one payoff sound at the reveal; two ~0.5 s near-silences (config `"silences"`), where bed and effects drop out.

Audio QA (phone speaker once, headphones once): every object makes its sound; one payoff sound; two silences in place; no effect on top of a key word; first second has the hook sound; last line clean.

## 5. Voice direction

Mark the ElevenLabs v3 script with the tags we already use, and keep a clean copy (no tags) for captions and post text:
- `[pause]` / `[short pause]` after the hard truth, before the re-hook question and before the payoff line,
- delivery tags for each beat: `[confident]` for the hard truth, `[curious]` for the open loop and the 25 s question, `[softly]` or `[thoughtful]` for the honest trade-off, `[warm]` / `[smiling]` for the close,
- stress: put the stressed word last in its sentence rather than inventing marks the engine does not read.
Kokoro drafts ignore the marks; that is fine, the final voice is Adam.

## 6. Shot list (during scripting)

For each beat note the scene and medium. Fallback ladder until the hybrid style exists: existing drawn scene type -> new scene type in the illustrated engine -> designed Graphite & Sage card. Any external asset needs a CC0 licence-log row (`studio/sfx-library/LICENSES.md` for sounds; images would get `assets/LICENCE-LOG.md`).

## 7. Batch rules and the 2-week test

- Per day: 2+ story structures, no hook formula twice in a row, all beat maps written before any animation, sound pass as its own step.
- 2+ visual styles per day stays the rule but cannot be met until a second style passes OWNER-RULES (rework diagram, or build the hybrid style). Note it in the run journal; do not ship a failing style to meet it.
- Test: next 2 weeks of batches in V2. At 48 h compare saves, shares, follows and replays against the last V1 batches (Oct 25-30), by structure and hook formula. Day 11-14: keep winners, retire losers, lock mix levels, decide explainer music. Record outcomes in `studio/experiments.md` (V-EXP-32).
