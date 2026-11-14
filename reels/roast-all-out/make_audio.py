"""Habit Roast #2 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/roast-all-out"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("footsteps", 3.0), .02, .35); A(K("timer", 1.0), .3, .12)                              # hook: sprinting, stopwatch
A(K("miss", 0), LN["S1", 1] + .4, .3)
A(m.syn.whoosh(.5, 300, 2000), SC["S2"][0], .2); A(K("ratchet", 1.0), LN["S2", 1], .15); A(K("pop", 2), LN["S2", 1] + .9, .25)
for i in range(5): A(K("pop", i), SC["S3"][0] + .2 + i * .25, .22)
for i in range(5): A(K("tick"), LN["S3", 1] + i * (LE["S3", 1] - LN["S3", 1]) / 5, .15)
A(K("right", 3), LE["S3", 1], .35)
A(m.syn.bell(79, 2.0), LN["S4", 0] - .1, .2)
m.write()
