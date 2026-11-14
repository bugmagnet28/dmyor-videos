"""Habit Roast #4 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/roast-pizza-run"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("footsteps", 4.0), .02, .3); A(K("plate"), .15, .25)                                   # hook: running, pizza lands
A(K("miss", 0), LN["S1", 1] + .3, .3)
A(K("chop", .6), LN["S2", 0] + .4, .25); A(K("pop", 2), LN["S2", 1], .25)                   # slices cut away
A(K("stamp"), SC["S3"][0] + .1, .35); A(K("pop", 1), LN["S3", 1], .25); A(K("pop", 3), LN["S3", 1] + 1.4, .25)
A(m.syn.bell(79, 2.0), LN["S4", 0] - .1, .2)
m.write()
