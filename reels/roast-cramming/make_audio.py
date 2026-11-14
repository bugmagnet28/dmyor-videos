"""Habit Roast #3 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/roast-cramming"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("pencil", 1.2), .05, .35); A(K("clock", 2.0), .1, .1)                                  # hook: writing at 2 AM, clock
A(K("miss", 0), LN["S1", 1] + .3, .3)
A(m.syn.whoosh(.6, 300, 1500), LN["S2", 0] + .8, .15); A(K("pop", 2), LN["S2", 1], .3); A(K("right", 2), LN["S2", 1] + .5, .3)
for i in range(6): A(K("pen_check"), SC["S3"][0] + .2 + i * (LE["S3", 0] - SC["S3"][0] - .2) / 6, .2)
A(K("reveal"), LN["S3", 1], .3)
A(m.syn.bell(79, 2.0), LN["S4", 0] - .1, .2)
m.write()
