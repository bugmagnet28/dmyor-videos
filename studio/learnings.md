# Learnings (video)

Newest at the bottom. `- YYYY-MM-DD [topic] lesson. Evidence: ... Confidence: low/med/high`

- 2026-10-08 [baseline] 12 old reels, 0 followers, no metrics logged. Craft review points to empty first frames, long runtimes (median ~53s), small dark text, product-first scripts. Evidence: frame review of 4 reels + all scripts. Confidence: med (no numbers yet)
- 2026-10-08 [craft] Old engines cannot produce a readable frame 0: kinetic.title words always enter with a 0.42s fade, so t=0 is empty by design. Built a "punch" engine where any cue at t<=0 is drawn finished. Evidence: engine-motion.js render(), own frame check of twelve-weeks-one-thing (frames 0/0.5/1/2 all show the full hook). Confidence: high (mechanical)
- 2026-10-08 [tooling] build.py used a string replacement in re.sub, so any "\n" inside timeline text became a raw newline and the page silently failed to load (all audits timed out on __seek). Fixed with a lambda. Evidence: brand line "Turn a big goal\ninto a daily plan." broke the build. Confidence: high
- 2026-10-08 [craft] With the Reels safe band (y 240..1250) the permanent camera drift (+/-14px, 1.4% scale) eats ~20px each side; a full-height hook block must be <= ~950px tall. Evidence: safearea.js flagged the hook at 1255 and 239 before resizing "12" 420->380px. Confidence: high
- 2026-10-08 [audience] No numbers yet for any reel. twelve-weeks-one-thing is the first new-format bet (V-EXP-09). Do not draw conclusions until 48h insights exist for 3+ new-format reels. Confidence: n/a
