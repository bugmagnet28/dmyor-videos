# Scene library

Two engines. Pick with `"engine"` at the top of `timeline.json`.

| engine | look | scenes |
|---|---|---|
| `mono` (default) | black, white, one dim grey. A pointer drives everything. | the diary / archive / system families below |
| `motion` | colour, kinetic type, camera zooms and pans. No pointer. | the motion family at the end of this file |

Do not mix them in one reel. `verify.js` skips the cursor checks on `motion` and runs
the frame-motion pass on both.


Every scene is a block in `timeline.json`. All timings are seconds against the audio.
Scenes are independent: omit any you do not need.

```json
{
  "total": 100.2,
  "brand": { "mark": "dmyor", "url": "www.dmyor.com" },
  "dreams": ["Run my own business", "..."],
  "scenes": [ { "type": "...", "note": "cue text this lands on", ... } ]
}
```

## The diary act

| type | params | what it is for |
|---|---|---|
| `diary.open` | `click`, `start`, `end` | pointer clicks the cover, book opens |
| `diary.write` | `lines:[{text,start,end}]` | pointer writes each line at the caret |
| `diary.tap` | `at:[t,t,t]` | taps a written dream, a pulse goes out and dies |
| `diary.dissolve` | `start`, `end` | the writing fades: nothing came true |
| `diary.close` | `click`, `start`, `end` | cover swings shut |
| `diary.ghost` | `in`, `out`, `strike` | the diary RETURNS and is struck out |

`diary.ghost` is the "instead of the magic diary" swap. Use it whenever the script
replaces the fantasy with the product.

## The archive act

| type | params | what it is for |
|---|---|---|
| `archive.zoom` | `start`, `end` | the closed diary opens out into the full-frame grid |
| `archive.fill` | `start`, `colDelay`, `rowDelay` | cards arrive left to right |
| `archive.counter` | `start`, `end`, `from`, `to` | "N dreams on record" climbing |
| `archive.hover` | `start`, `end`, `card:[col,row]` | pointer lifts one card |
| `archive.flip` | `at`, `card:[col,row]`, `year` | `standby` -> `real - YYYY` |
| `archive.scroll` | `start`, `speed` | continuous drift, never stops once started |
| `archive.drag` | `start`, `end` | pointer physically drags the archive |
| `archive.pullback` | `start`, `end`, `back` | grid shrinks; it extends past the frame |
| `archive.scan` | `start`, `end` | a line sweeps down: witness and verify |

A **wave** of `archive.flip` (5-6, ~0.7s apart) is the strongest single visual for any
line about dreams coming true over time. One flip alone reads as a detail; a wave
reads as an argument.

## Making the point (one scene per sentence)

These exist so a sentence never has to borrow the diary or the archive as wallpaper.

| type | params | what it is for |
|---|---|---|
| `calendar.year` | `in`,`out`,`year`,`strike:[t|null x12]`,`point`,`sweep:[a,b]`,`remain`,`remainAt` | a year burning down: months strike off one at a time, the rest keep breathing |
| `tally.compare` | `in`,`out`,`planned`,`done` | two counters: what you meant to do against what you did |
| `thoughts.float` | `in`,`out`,`items:[...]`,`dissolve`,`showNoDate` | ideas drifting untethered, no borders, then scattering into nothing |
| `progress.log` | `in`,`out`,`count`,`fillStart`,`fillEnd` | day marks filling one by one with a live count |
| `streak.bars` | `in`,`out`,`growStart`,`growEnd`,`days` | bars rising left to right: the record building |
| `stamp.trio` | `in`,`out`,`at:[t,t,t]`,`words:[...]` | three attributes stamping on, one per beat |
| `path.arc` | `in`,`out`,`start`,`end` | a dotted arc drawing from here to there |
| `orbit.trapped` | `in`,`out`,`items`,`cy`,`rx`,`ry`,`brackets`,`scramble`,`scatter` | ideas circling a point they never leave; then a date bracket that blinks and never fills; then the words decay to dashes and fly apart |
| `record.blank` | `in`,`out`,`dream`,`sub`,`fields:[{label,at}]` | a record whose fields were never filled; each empty slot hunts for a value and never finds one |
| `strike.words` | `in`,`out`,`words:[a,b]`,`at:[t,t]` | name the wrong culprits and cross them off |
| `steps.three` | `in`,`out`,`items:[...]`,`at:[t,t,t]` | a running checklist, one item per spoken step |
| `sharpen.text` | `in`,`out`,`vague`,`vagueAt`,`specific`,`at` | a vague goal types in, gets struck, resolves into a checkable one |
| `collapse.step` | `in`,`out`,`big`,`small`,`at` | the whole ambition contracting into one thing you can do tomorrow |
| `ledger.rows` | `in`,`out`,`rowStart`,`rowStep`,`entries:[{date,text,missed}]` | dated lines piling up, missed days included, with a running total |
| `feed.stream` | `in`,`out`,`speed`,`widen` | everyone's records streaming in columns, looping, never empty |
| `feed.highlight` | `at`,`out`,`labels:[a,b]` | settles the stream and attaches labels to whichever entry is nearest centre |
| `feed.real` | `at`,`year` | the annotated entry flips to real |
| `phases.bar` | `in`,`out`,`fill0`,`fill1`,`fill1Pct`,`noteAt`,`note2` | two segments: one filling and live, one dashed and coming |
| `calendar.recall` | `in`,`out`,`at:[t...]`,`items` | what you meant to do surfacing one at a time above a spent calendar |

`record.blank` also takes `fillAt` and `value` per field: the same empty slots from the
opening get answered later in the reel. Re-using a motif *within* one reel is good;
re-using last reel's scenes is not.

`diary.write` also takes `stamp:{text,at}` - a date types itself under the line as it is
written. Use it whenever the script says anything about being dated.

## The system act

| type | params | what it is for |
|---|---|---|
| `timeline.draw` | `in`,`start`,`end`,`out`,`from`,`to` | pointer drags a year rule |
| `phase.tabs` | `in`, `out`, `labels:[a,b]` | the system UI appears |
| `phase.select` | `at`, `index`, `title`, `body` | pointer clicks a tab, panel switches |
| `phase.steps` | `at:[t,t,t]`, `steps:[...]` | numbered steps, one per spoken line |
| `compose.open` | `addAt`, `clickAt` | pointer clicks "+ Post a dream" |
| `compose.type` | `start`, `end`, `text` | types into the focused field |
| `compose.post` | `clickAt`, `flyStart`, `flyEnd` | POST, card flies into the archive |
| `prompt.turn` | `in`, `out`, `clickAt` | empty slot, blinking caret: your turn |
| `end.card` | `in`, `urlStart`, `urlEnd` | brand card; URL types in sync with the VO |

## Direct it: what is the line actually saying?

Pick the visual from the *meaning* of the sentence, not from what is already on screen.
The scenes above exist because a line demanded something and nothing fit.

| the line is doing | give it |
|---|---|
| asking a question | something searching - items surfacing, a sweep, a count that hunts |
| conceding a point | the thing intact and warm before you take it away |
| describing being stuck | a closed loop: orbiting, returning, never landing |
| naming an absence | the slot for the missing thing, empty and blinking |
| dismissing something | let it lose its form - text decaying, scattering |
| stating a fact | a stamp, a counter, a hard number |
| promising a change | a path, an arc, a bar rising |

## Diagram before kinetic type

Animated text is not an explanation. It is the same sentence the narrator already said,
moving. If a line carries a **relationship** - a comparison, a sequence, a rule, a
trajectory - draw the relationship. Reserve kinetic type for lines with no structure to
draw: the ask, the closing line, the sendable phrase.

The test: *cover the audio. Does the frame still teach anything?* If not, it is decoration.

| the line carries | draw it as | scene |
|---|---|---|
| two possible futures | one origin, two curves, both ends named | `split.paths` |
| a rule with a pass and fail case | two rows side by side, same pattern, one broken | `miss.rule` |
| a process with ordered steps | nodes joined by connectors, drawn in order | `method.flow` |
| something compounding over time | a curve with the milestones marked *on the line* | `captions.track` | `in`,`out`,`items:[{t,end,text,y,size,accent,color,drift,grow}]` | phrase captions cut to the word. Each enters with a scale-up and settle, drifts a few px while held, and clears before the next one starts. `accent` words take the colour |
| `fields.empty` | `windows`/`in`,`out`,`y`,`color`,`stamp`,`stampColor`,`stampAt`,`items:[{label,value,at,emptyAt,fillAt}]` | a card of labelled fields whose **values** drain and refill while the **labels** never move. Run it in both directions across a reel and the viewer reads the change without being told |
| `span.bookend` | `windows`/`in`,`out`,`y`,`color`,`drawAt`,`leftLabel`,`rightLabel`,`recordLeft`/`recordRight:{text,date,color,at}` | a dated span with a tick at each end. Opens empty, closes with a record on both ends. Axis labels hand over to the records so the date is never printed twice |
| `ambient.field` | `in`,`out`,`count`,`rings:[{r}]`,`phases:[{t,c,density,amp,drift}]`,`bursts:[{t,power,dur}]`,`flashes:[{t,power,dur,c}]` | a deterministic drifting field of dots, bars and slow rings behind everything. `phases` retint and thicken it with the story; `bursts` shove it outward from centre; `flashes` bloom on a beat |
| `card.pressure` | `windows`/`in`,`out`,`y`,`text`,`date`,`color`,`weights:[{label,at,color}]`,`dimAt`,`dimEnd`,`dimTo`,`driftAt`,`snapAt` | one dated card with an arc: sure, buried under named weights, dimmed, drifted off centre and stripped of its date, then snapped back at `snapAt`. The weights clear themselves once `driftAt` has passed |
| `archive.scroll` | `in`,`out`,`y`,`rows:[{date,text,mine}]`,`scroll:{at,end,from,to}` | a dated list scrolling past the frame, the viewer's own row highlighted. Masked at the bottom so it fades into any background |
| `holder.leak` | `windows`/`in`,`out`,`y`,`rightAt`,`left:{label,color}`,`right:{label,color}`,`items:[{text,color,at,leakAt,moveAt,stampAt,date}]` | two labelled containers: a dashed one that does not hold (items drift, `leakAt` drops one out for good) and a solid one that does (`moveAt` carries an item across, `stampAt` gives it a date) |
| `phase.marks` | `in`,`out`,`y`,`items:[{name,text,live,color,at}]`,`caption`,`capAt` | phase cards side by side, the live one lit and the rest dimmed |
| `stair.build` | `windows`/`in`,`out`,`pxPerM`,`stepRise`,`stepRun`,`steps`,`color`,`weight`,`anchorY`,`fitW`,`fitH`,`maxScale`,`tower:{h,x,label,color,at}`,`draw:[{t,n}]`,`markers:[{h,label,at,color,labelUntil}]`,`strikeAt`,`cam:[{t,focus,fit,rot,tower}]`,`captions` | a line-drawn staircase in metres. `focus` is `steps:N`; `rot` cants the horizon. Multiple instances allowed |
| `receipt.print` | `in`,`out`,`y`,`title`,`sub`,`titleAt`,`subAt`,`ruleAt`,`slideIn`,`slideOut`,`items:[{label,fig,at,figColor,figSfx}]`,`totals:[{label,fig,from,at,rollFor,color,big}]`,`stamp`,`stampColor`,`stampAt` | a cream monospace receipt that prints line by line: dot leaders stretch to fill, the figure snaps in after its label, totals count from `from` to `fig`, and a rubber stamp lands at the end |
| `axis.travel` | `windows`/`in`,`out`,`y`,`color`,`years:[...]`,`drawAt`,`drawEnd`,`tickAt`,`tickStep`,`cardAt`,`cardTop`,`cardDate`,`cardText`,`travelAt`,`travelEnd`,`fromTick`,`toTick` | a year axis with a dated card riding it from one year to another. The card is clamped inside the frame so it never leaves at the far tick |
| `dream.stack` | `in`,`out`,`y`,`items:[{text,color,at,outAt}]`,`dimAt`,`dimEnd`,`caption`,`capAt` | colour-coded chips, bright on arrival, desaturating together at `dimAt`; an item with `outAt` goes out on its own |
| `rows.verdict` | `windows`/`in`,`out`,`y`,`items:[{date,text,verdict,at,verdictAt}]`,`caption`,`capAt` | dated rows whose badges resolve one at a time. `verdict` is `done` (green), `close` (amber) or `open` (coral) |
| `year.grid` | `in`,`out`,`year`,`elapsed`,`maxScale`,`anchorY`,`labelsAt`,`zoom:[{t,focus,fit}]`,`reveal:[{t,n}]`,`fill:[{t,n}]`,`captions`,`stats` | a calendar year of day cells. `focus` names a target (`cells:a-b`, `month:m`, `months:a-b`, `year`) and the engine frames it automatically; `fit` (0-1) shrinks the target box to control how far each pull-back goes. `reveal`/`fill` are eased fronts over cell index |
| `arc.curve` |
| a threshold being crossed | the quantity moving against a fixed reference | `floor.bar` |
| accumulation | units filling a grid | `daygrid.fill` |

**Label both ends of a diagram.** A fork with unnamed endpoints is decoration. `split.paths`
was unreadable until the origin said "today" and the ends said "january / you did it" and
"same as today". A viewer must be able to read the axes without the voiceover.

**Anchor marks to the geometry, not to a guessed coordinate.** `arc.curve` first placed
its 30/60/120 labels at a linear x, so they floated below a curve they did not touch.
Using `getPointAtLength` to put a dot on the actual curve and drop a tick to the label
turned three captions into a diagram.

**Check that a label is on screen long enough to read.** `split.paths` faded its win label
in at `winEnd` while the scene ended 0.2s later, so the payoff of the whole diagram was
never visible. Any label appearing within ~1s of a scene's `out` is a bug.

**A continuous pull-back needs a grid that grows downward.** `year.grid` lays 12 months
in **2 columns**, not 3. With 3 columns the grid reaches full frame width after three
months, and from then on every "zoom out" is width-bound and the scale stops changing:
rows keep appearing but the camera visibly stalls, which kills the entire effect. Two
columns keeps the growth vertical so each step really does pull back further. Verify it
numerically before animating: print the scale at every focus step and confirm it
decreases monotonically.

**The camera must lead the reveal.** Never let an element appear outside the frame that
is about to contain it. In `days-gone` February revealed at 10.8 while the camera still
framed January until 12.9, so a column of cells sat off the right edge for two seconds.
Every widen keyframe now sits ~1s ahead of the reveal batch it holds. `overflow.js`
catches this, but only because it checks painted boxes on both axes.

**`accentWords` must match after punctuation is stripped.** The engine compares a bare
word against the list, so an entry written as `"today."` or `"it,"` silently never
matches and the accent colour just does not appear. Nothing errors. Three accents across
two shipped reels were dead this way. The engine now strips both sides, but write the
bare word anyway. Check it with `probe.js <reel.html> <t>`, which prints the computed
colour of every run.

**Keep `stagger` above 0.09 on any title using `sfxWords`.** `sfx.py` drops a repeat of
the same voice within 0.09s to stop identical samples flamming. A 0.075 stagger silently
lost every second tick: 11 words, 6 sounds, no warning. Count the emitted cues with
`sfx.py <dir> --dry` rather than assuming they all landed.

## The Reels safe area

The canvas is 1080x1920 but Instagram covers a lot of it: the status bar and header eat
the top strip, and the caption, handle, audio ticker and action rail cover the bottom
third. **Design inside y 240..1250.** The bottom 670px is not yours.

That inverts the usual layout: **captions go at the top, the graphic sits below them.**
A caption at `bottom: 200px` is under the username in the feed and might as well not
exist. `year.grid` takes `fitW`/`fitH` so the framing box is the safe band rather than
the whole frame, and `anchorY` centres the graphic within it.

Audit it with `safearea.js <reel.html>`, which flags anything outside the band. It
ignores full-bleed layers (width >= 1080), which bleed on purpose.

**Re-check the layout maths when the band changes.** `days-gone` was laid out in 2
columns to keep the pull-back going. Against a 700px-tall band that produced a 17px
cell, unreadable. Three columns gives 26px and a squarer block that suits a short wide
band. The column count is a function of the space you actually have.

**A scene can appear twice without duplicating its DOM.** Give it `windows:
[[in,out],[in,out]]` and the engine takes the union for opacity; per-element times stay
absolute. `letter-to-future` uses one `axis.travel` for both the opening span and the
travel to 2031, and one `rows.verdict` for the list and its verdicts eight seconds
later. This is the fix for the `S()` returns-first-only trap: reach for `windows` before
you reach for a second instance.

**Every consecutive pair of scenes is a collision until proven otherwise.** Fades run
~0.42s past `out`, so an outgoing scene whose `out` equals the next scene's `in` overlaps
for that whole fade. Six of them showed up at once here. Set each `out` about 0.5s before
the next `in` and let `collide.js` confirm it.

## Captions: measure the space, do not guess it

`capfit.js` places every caption by **measuring the frame**, not by picking a default.
For each caption it seeks to three times across that caption's life, collects the
bounding box of every visible piece of content (skipping `[data-decor]` and the caption
layer itself), merges them into occupied bands, and drops the caption into the roomiest
free gap inside y 240..1250. Sampling three times, not one, stops a caption from being
legal on arrival and colliding halfway through.

The result moves with the reel on its own: captions sit at y≈1050 while the card owns the
middle, ride up to y≈900 as the archive shortens, and jump to y≈706 when the phase cards
take the centre. Nothing is hand-placed.

**Phrases, not words.** Word-by-word karaoke is noise. Chunk on units of meaning
(`"and why it mattered"`, `"The specifics."`) and let size carry emphasis: 50px for a
qualifier, 78px for the line that matters.

**Match the ASR, display the brand.** Whisper hears "deemyor" as "demia", so a caption
phrase carries an optional match string: the timing comes from what was heard, the text
shown is `dmyor`.

**Delete a caption that repeats the graphic.** The end card already reads `dmyor.com`, so
the captions for those two lines were cut, and `phase.marks` lost its own caption once
the spoken one covered it. Two elements saying the same words at the same moment reads as
a bug, not emphasis.

## Run one diagram backwards, then forwards

The strongest structure in `tell-your-future` is a single card of three labelled fields
(`what` / `by when` / `why`). In the problem half the **values** drain away one at a time
while the **labels** stay exactly where they are. In the solution half the same values
refill, in the same order, into the same slots.

Nothing has to explain what changed. The labels are the constant that makes the
difference legible, and the viewer does the reading themselves.

The same trick bookends the reel: `span.bookend` opens on an empty five-year span and
closes on the same span with a dated record at each end. First frame and last frame are
the argument.

**When two elements would print the same string, make one hand over to the other.** The
record cards carry their own dates, so the axis labels beneath them fade out as the
records land instead of repeating them.

## Give the frame an atmosphere, not just a subject

A single element on a flat pane is restraint, not art, and in a 1080x1920 frame it leaves
two thirds of the picture dead. `ambient.field` runs the whole reel behind everything:
~150 dots and bars at three parallax depths plus four slow counter-rotating rings, all
**deterministic** (position is a pure function of `t` via a hashed per-particle seed), so
frame-stepped recording reproduces it exactly.

The point is that it is **driven by the script**, not decoration: `phases` retint and
thicken it beat by beat (blue and sparse for the memory, dense coral for "work, money,
tiredness", thinned to almost nothing on "they just lose track of them", flooding green
on "not a chance"), `bursts` shove everything outward from centre on an impact, and
`flashes` bloom a radial glow.

**Let the subject take damage.** In `card.pressure` each weight now cracks the card with a
jagged path in that weight's own colour, and the cracks retract on `snapAt` while a halo
blooms. The object earns its arc instead of just changing opacity.

**Mark atmosphere `data-decor="1"`.** A full-bleed field is meant to run off every edge,
so all three layout audits skip `[data-decor]` subtrees. Audits check content, not
atmosphere, otherwise every particle reports as an overflow.

## One object with an arc beats four scenes

`not-storage` carries a single dated card through the whole first half: certain, then
buried under **named** weights (work, money, tiredness), then dimmed to 15%, then drifted
off centre with its date stripped, then snapped back to full on "not a chance". Same
object, five states, one continuous read. It is stronger than cutting between five
different diagrams because the viewer never has to re-learn what they are looking at.

**Name the weights.** "Work. Money. Tiredness you cannot explain." lands because each one
is a separate hit the viewer recognises. "Life gets in the way" is one vague chip.

**Never let the dream leave the frame.** It fades to 15% and drifts, but it is always
there, because the script says *nobody forgets their dreams, they just lose track of them*.
If it had faded to zero the visual would contradict the line.

**Clear a prop the moment it has spoken.** The weights lingered at full opacity long past
their beat and collided with the next scene's text. Anything that lands has to be given
an exit.

## Backgrounds: wipe down, not up

A pane wiping `up` exposes the outgoing colour along the **top** edge for the whole wipe,
and in a Reel the top is prime visible area, so a dark seam reads as a broken letterbox.
Wipe `down` (or sideways) and the seam lands in the bottom third the UI covers anyway.

## Scenes that zoom a long way

`stair.build` frames a single 17 cm step and, later, a 330 m tower: a **1941:1** range.
Three things break at that span and all of them are silent:

**Minimum sizes in the framing box block zooming in.** A floor of 200x150 on the focus
box meant one step could never fill the frame; it rendered half a pixel. Let the box be
the true extents and let `maxScale` be the only limit.

**Stroke width scales with the camera.** A 5px line at 368x is a 1800px slab that fills
the screen. `vector-effect:non-scaling-stroke` does not help when the transform is CSS
on an ancestor, so set `stroke-width = base / scale` every frame. Dash patterns need the
same division.

**HTML labels inside the transformed layer scale too.** Keep them in the untransformed
wrapper and project their world point by hand:
`x = tx + (wx·cos - wy·sin)·s`, `y = ty + (wx·sin + wy·cos)·s`.
Then **clamp x into the frame**: a label pinned to a world coordinate flies off-screen
the moment the camera pulls back, and `overflow.js` will catch it as a horizontal
overflow with a negative left.

**Labels converge as you pull back.** 43 m and 62 m are 19 m apart, which is 29 screen px
once the whole tower is in frame, so the labels overlap. Give each a `labelUntil` and let
it step aside when the next arrives; keep its rule for context.

**SVG needs no viewBox here.** Give it `width=1 height=1`, `overflow:visible`, and no
viewBox, so SVG user units equal world px and share an origin with the HTML labels in the
same layer. A viewBox silently offsets the geometry by thousands of pixels.

## Comedy, if a reel is going for it

`year-itemised` is the deadpan one: 2026 as an itemised receipt. What made it work:

**The real numbers have to be real.** 36 Mondays, 254 days used, 111 left are all true
for the date it was cut. A checkable figure is funnier than an invented one, and it
keeps the piece honest. The rhetorical counts (14 plans announced, 22 "next year"s) are
obviously about the viewer. **Never put an invented dmyor statistic on screen** just
because it would land.

**Put the punchline second, not last.** `plans given an actual date ... 0` is the joke
the whole reel rests on, so it arrives early and everything after plays underneath it.

**Give the audience somewhere to land.** Twenty seconds of jokes at the viewer's expense
needs a turn: `111` gets the biggest type and the only warm colour, and the reel resolves
on `STILL ENOUGH`, not on the mockery.

**A tall object eats the safe band.** The receipt is ~920px of a 1010px band, so the
feed-in travel had to drop to 34px and the camera zoom to 1.03 before `safearea.js` went
quiet. Budget the object first, then the motion.

**Watch what the stamp lands on.** The first cut put `STILL ENOUGH` straight over the
`111`. A stamp needs its own line in the layout, not just a spare corner.

**One scene cannot carry three sentences.** In the four-months reel a single drifting
cloud spanned "it stayed in your head", "nothing has a date on it" and "it is a mood" -
ten seconds, one picture, and it went flat. The fix was one system with three phases:
orbit, then a blinking empty date bracket, then decay and scatter. Same elements, three
distinct frames, each landing on its own line.

## Rules learned the hard way

**Never let a colour inherit.** Every element that renders text must declare its own
`color`. An element with no `color` anywhere up its ancestor chain falls back to the
browser default, black, and on a dark pane it renders invisible. This shipped once:
`.th .thn`, `.tok`, `#bignumV` and `.rollg .rs` were all black-on-navy and nobody
caught it, because WCAG contrast maths on the *palette* passes fine while the actual
DOM is painting black. Set `color` on `#stage` as a backstop and explicitly on every
leaf. Audit with `node probe.js <reel.html> <t>`, which prints the computed colour of
every visible run.

**Minimum type size is 26px, body copy is 40px+.** The canvas is 1080x1920 but it is
watched on a phone at roughly a third of that. Anything under ~26px is unreadable in
the feed, and 30px thin-weight grey is worse than the ratio suggests: contrast maths
does not model stroke weight, so a 200-weight face at small size reads far dimmer than
its number. Supporting copy sits at 300 weight minimum, never 200.

**Type changes are layout changes.** Enlarging a font wraps lines, grows blocks, and
pushes them into whatever scene overlaps in time. After any size edit, re-run all three
audits: `overflow.js` (glyph ink past the frame edge, measured with a Range so
full-width centred blocks do not false-positive), `collide.js` (two visible scene
layers occupying the same box), and `verify.js` (frozen frames). Bumping steps to 44px
silently wrapped them into the "bad day floor" panel and only `collide.js` caught it.

**Anchor everything.** Each scene's `note` is the spoken phrase it lands on. If you
cannot name the phrase, the scene does not belong.

**One example, followed all the way through.** If the VO names a domain, every example
in the reel lives in that domain. A record card reading "publish my first novel" while
the next scene sharpens "get healthy" into "walk thirty minutes" reads as two unrelated
stories: the viewer has to re-orient at every cut. Pick the goal from whatever the
narration locks you into, then use it in the record card, the collapse, the ledger
entries and the highlighted feed row. The surrounding archive can be varied - that is
other people - but the one being followed never changes.

**Late scenes get cluttered, not sparse.** Density that reads fine at 40s becomes noise
by 50s once panels start stacking on it. Two rules: a background stream drops to ~0.2
the moment a panel takes the frame, and anything being annotated goes to full while
everything else drops to ~0.3. Fewer, larger elements beat more, smaller ones on a
phone - this reel went from three dense columns to two roomy ones and read better.

**Put annotations where there is room.** Labels anchored to the right of a right-hand
column fall off the frame. Anchor the highlight to the left column, or flip the label
side based on available space.

**Do not re-run the last reel.** Two videos sharing a scene library start to look like
the same video. Each reel should introduce its own visual family: reel 2 was the
calendar and the streak, reel 3 was the record card, the ledger and the feed. Reach for
an existing scene only when the *meaning* genuinely matches.

**A looping stream needs three sets, not one.** Anything that scrolls forever must
repeat its content and modulo on the measured set height, or it runs dry and leaves the
frame empty halfway through. Same bug as the archive grid, learned twice.

**Anchor a highlight to what is actually on screen.** Pinning labels to a fixed row
index breaks the moment the thing scrolls: pick the element nearest centre at the
moment the annotation starts, lock it, and settle the motion while the labels are up.

**One sentence, one visual.** If two consecutive sentences share a scene, the second
one has nothing to show. Reaching for the diary or the archive a third time is the
tell. Build a new scene instead - the library above grew entirely from that pressure.

**Kill dead air.** More than ~4s with nothing new appearing reads as a frozen video.
`reel.py gaps <slug>` lists them. Fill with: a flip wave, a counter tick, a scan, a
pullback, or a pointer visiting something.

**Small blinking things do not count as motion.** A blinking bracket or a caret is too
few pixels for the frame-motion pass, and it looks static to a viewer too. Big panels
get a slow float (`floaty()` in the engine, sine on translateY) so the frame is never a
photograph. That single change took one reel from four frozen stretches to none.

**The pointer cannot be in two places at once.** Two scenes wanting it within ~0.3s
force an impossible sprint. The engine now drops the earlier of two conflicting
targets, and drops a "park at rest" hop entirely if the next beat is within 1.5s.
Caret pins at typing-window edges are exempt - dropping those is what causes snaps.

**A moving cursor is not a moving frame.** `verify.js` runs a frame-motion pass that
screenshots every 0.4s and diffs pixels. It has caught scenes that were visually frozen
while the cursor happily travelled - a calendar sitting after its reveal, a seam between
two scenes, a typing beat too small to register. Trust `frozen frames`, not `cursor
still`. Fixes that work:
- give the resting element a slow breathe (opacity + a hair of scale)
- overlap the outgoing and incoming scene by half a second instead of butting them
- add a second, smaller thing to the beat (the date stamping on under a written line)

**Opaque panels.** Anything with text over the archive needs `background:#0A0A0A`.
Transparent panels let card text bleed through and everything turns to mush.

**The archive is the subject.** Keep the grid at full brightness while it is being
introduced. Only dim it (to ~0.3) when a panel or the timeline sits on top.

**Cursor:** short deliberate hops, then hold. Never let two waypoints sit far apart in
time - the interpolation becomes a crawl. Pin waypoints to the exact caret position at
the edges of any typing window.

**Card slots are reserved.** A card the pointer will "post" into must not be left
empty for 20s waiting - either fill it normally and have the flying card dissolve into
it, or the grid shows a hole.


# Motion engine scenes (`"engine": "motion"`)

Type: **Helvetica Neue at Light (250-300)**, large, with open line-height and a little
positive tracking. At 80px+ the elegance comes from the letterforms and the space
around them, not from weight. Light rather than Thin so it still survives a phone
screen at speed. `"font": "serif"` switches the frame to Didot for an editorial reel.

Emphasis is **colour, not weight**: an `accentWords` word shifts one step (250 -> 300)
and takes the accent hue. Jumping to 500 against a 250 line snaps the eye and kills the
slim feel. `"demi": true` marks the two or three lines the reel is really about: a small
weight step, tighter tracking, and `sfx.py` gives them a swell.

Colour lives in CSS variables: `blue cyan green coral amber violet` plus `ink` and
`dim`. Scenes take a colour by name. Background is a slow drifting wash of blurred
blobs plus a fine grain, so the frame is never flat.

| type | params | what it is for |
|---|---|---|
| `kinetic.title` | `in`,`out`,`y`,`size`,`stagger`,`text`,`accentWords`,`sub` | words arrive one at a time with a slight overshoot; `accentWords` colour individual words |
| `split.paths` | `in`,`out`,`start`,`winEnd`,`loseEnd`,`winColor`,`loseColor`,`originLabel`,`goalLabel`,`winLabel`,`loseLabel` | two routes from one origin: one reaches the marker, one stops short. Always set the four labels |
| `method.flow` | `in`,`out`,`y`,`caption`,`capAt`,`items:[{text,color,at}]` | ordered nodes joined by connectors that draw in between them |
| `miss.rule` | `in`,`out`,`y`,`rowA`/`rowB:{label,color,at,step,pattern,breakAt,breakFrom}`,`verdict`,`verdictAt` | two day-rows from the same pattern (`#` marked, `.` missed); the row that misses twice goes dead from `breakFrom` |
| `arc.curve` | `in`,`out`,`y`,`color`,`drawAt`,`drawEnd`,`capAt`,`caption`,`items:[{n,label,at,at01}]` | a compounding curve; each item gets a dot on the line at `at01` (0-1 along it) and a tick down to its label |
| `cards.dismiss` | `in`,`out`,`y`,`items:[{text,color,at,dismiss}]` | candidate answers appear and get struck off, one per spoken guess |
| `field.expand` | `in`,`out`,`start`,`end`,`count`,`collapse`,`collapseEnd` | a field of coloured points expanding into abundance, then collapsing to a line |
| `plan.empty` | `in`,`out`,`y`,`title`,`stampAt` | a plan with empty rows and a stamp that says there is none |
| `chips.reorder` | `in`,`out`,`items`,`orderAt`,`liveAt`,`metaText` | scattered dreams that snap into an ordered archive and go on the record |
| `slot.waiting` | `in`,`out`,`y`,`typeAt`,`text` | a dashed slot that types your entry with a caret |
| `stage.two` | `in`,`out`,`y`,`items:[{no,title,body,color,at,fillAt,fillPct}]` | two stages, one filled and one partly engaged |
| `end.card` | `in`,`y`,`urlStart`,`urlEnd` | brand mark with the URL typing in step with the voice |
| `date.roll` | `in`,`out`,`from`,`to`,`roll`,`tail` | odometer digits spinning to a target date |
| `tokens.land` | `in`,`out`,`items:[{text,color,at}]` | small tokens slamming in, one per phrase |
| `count.up` | `in`,`out`,`start`,`end`,`to`,`label` | one huge number counting |
| `daygrid.fill` | `in`,`out`,`count`,`fillStart`,`fillEnd`,`miss:[i]`,`dead:[i]`,`label` | a wall of days filling; `miss` outlines a skipped day, `dead` marks a broken streak |
| `thresholds` | `in`,`out`,`items:[{n,label,at}]` | milestone numbers arriving one at a time |
| `floor.bar` | `in`,`out`,`fillAt`,`floorAt`,`floorPct`,`dropAt`,`caption` | a full bar with a floor line: the bad-day minimum that still counts |
| `collapse.step`, `sharpen.text`, `steps.three` | see mono | ported to motion with colour styling |

## Background

`"bg": [ {t, c, dur, dir}, ... ]` - flat colour panes that wipe in (`up`/`down`/`left`/
`right`) and stay until the next covers them. A thin rule sweeps the frame on each
change. **Flat colour, no gradients**: the blurred-blob wash was tried and dropped, it
reads as generic. Solid panes that change on the beat carry far more energy.

## Camera

`"camera": [ {t, s, x, y}, ... ]` moves the whole frame. `s` is scale, `x`/`y` pan in
stage pixels. Interpolated with the same ease as everything else.

Push in a little on a claim (`s: 1.10`), pull back on scale or abundance (`s: 0.90`),
return to 1.0 between. Keep it under about 1.15 or the edges of scenes show. A move per
sentence is plenty; more than that reads as seasickness rather than energy.

## Rules

**Colour carries meaning or it is noise.** green = reached, coral = stopped, blue =
the product, amber and violet = candidates being dismissed. Do not colour something
just to brighten it.

**Kinetic type needs the line, not the paragraph.** Six to eight words maximum per
`kinetic.title`. Anything longer stops reading as motion and starts reading as a wall.

**Every engine needs a permanent drift.** On top of the camera keyframes there is a
constant slow move (`sin(t*0.62)*17px`, scale +/-1%). Between two keyframes the frame
would otherwise be perfectly still. Amplitude and *rate* both matter: a 9px drift at
0.2Hz is sub-pixel across a 0.4s sample and still reports as frozen. Grain sits on top.

**`S()` returns the FIRST scene of a type.** If a reel uses two of something - two day
grids, two of anything - the engine must build them with `ALL()`. A second instance
silently never renders, and it shows up as a frozen stretch rather than an error. This
cost a debugging pass; check it whenever a scene type appears twice in a timeline.

**Scenes are per-engine.** `collapse.step`, `sharpen.text` and `steps.three` existed only
in mono. Putting them in a motion timeline produced no error and no visual, just dead
frames. If a scene is missing from an engine, port it rather than substituting.


# Sound

`sfx.py` derives its cues from the timeline, so the palette below is really a mapping
from *what a scene means* to *what it should sound like*.

| voice | character | fires on |
|---|---|---|
| `swish` | short filtered noise | kinetic titles, dismissals, camera pushes over 1.10 |
| `mark` | soft mallet, one clean partial | a line begins to be written |
| `bell` | two clean partials, long tail | a line resolving |
| `paper` | soft brown noise, no transient | a page or panel arriving |
| `clack` | dry wooden relay | a tap, a candidate appearing, a stamp |
| `swell` | reverse riser | builds INTO a statement or a reveal, placed ~1s before it |
| `shimmer` | high partials, slow decay | something going live |
| `whoosh` | longer pink-noise sweep | a scene arriving, a book opening, paths starting |
| `tick` | tiny high click | a tap, a month striking off |
| `pop` | soft two-tone blip | a card appearing, a post, a stage engaging |
| `thud` | low sine hit | stopping short, a stamp landing |
| `chime` | three decaying partials | arriving, going live, flipping to real |
| `riser` | upward chirp | expansion, a zoom in, a bar filling |
| `drop` | downward chirp plus sub | a collapse, a deflation |
| `sub` | low sustained tone | the pivot line, the end card |

Two hits of the same voice inside 90ms are thinned to one: stacked identical hits just
sound like a smear.

**Do not synthesise a mechanism.** A typewriter was tried and cut: ffmpeg noise bursts
can suggest a texture but they cannot fake a physical action, and the near-miss is worse
than not doing it. Typing beats now get a soft `mark` where the line starts and a
`shimmer` or `bell` where it resolves. Sound the *event*, not the machinery.

**Build into the big lines, punctuate the small ones.** A `swell` placed about a second
*before* a statement makes it land; a `swish` *on* it just marks it. Reserve swells for
the two or three lines the reel is actually about.

**Do not sound every scene.** Roughly one hit per spoken beat. The bed should read as
punctuation, not as a drum track competing with the narration.
