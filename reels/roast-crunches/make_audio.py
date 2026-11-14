"""Habit Roast #1 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/roast-crunches"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
for i in range(6): A(K("tick"), .05 + i * .17, .25)                                         # hook: crunch counter ticking
A(K("miss", 0), LN["S1", 1] + .3, .3)                                                      # belly: unchanged
A(m.syn.whoosh(.5, 300, 2000), SC["S2"][0], .2); A(K("pop", 1), LN["S2", 1] + .3, .25); A(K("stamp"), LN["S2", 1] + 1.6, .35)
A(K("ratchet", .8), SC["S3"][0] + .1, .15); A(K("footsteps", 2.0), SC["S3"][0] + .4, .2); A(K("right", 3), LE["S3", 0] - .2, .35)
A(m.syn.bell(79, 2.0), LN["S4", 0] - .1, .2)
m.write()
