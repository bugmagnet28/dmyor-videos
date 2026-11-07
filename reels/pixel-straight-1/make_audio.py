"""Straight Answer #1 sound (no music). tts/.venv/bin/python reels/pixel-straight-1/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-straight-1"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("chop", .5), .08, .3); A(m.syn.whoosh(.6, 200, 900), .1, .12)                          # hook: soil, roots creaking
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
A(K("pencil", 1.2), SC["S3"][0] + .2, .22); A(K("pencil", .8), LN["S3", 1], .18)            # lines drawn
for i in range(3): A(K("tap"), LN["S4", i] + .05, .3)                                       # week tags
A(m.syn.whoosh(1.2, 200, 800), LN["S4", 3], .2); A(K("ratchet", 1.0), LN["S4", 3] + .2, .12)   # roots spread
A(K("miss", 0), SC["S5"][0] + .9, .25)
n = 28; a, b = LN["S6", 1], LE["S6", 1] + .4
for i in range(0, n, 2): A(K("pencil", .12), a + (b - a) * i / n, .16)                      # tally marks
A(K("reveal"), SC["S7"][0] + .4, .3); A(K("right", 3), LE["S7", 1] - .3, .35)              # sprout breaks through
A(m.syn.bell(79, 2.5), LN["S7", 3] - .2, .2)
m.write()
