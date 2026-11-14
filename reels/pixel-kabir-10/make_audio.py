"""Kabir vs. Kabir #10 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-10"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("typing", 1.0), .05, .3); A(K("page", .3), .4, .25)                                      # hook: clicking through slides
A(K("right", 2), LN["S1", 1] + 1.5, .3)
A(m.syn.whoosh(.6, 300, 1500), SC["S2"][0], .2); A(K("miss", 0), LN["S2", 0] + 1.6, .35)     # freezes
A(K("ratchet", .8), SC["S3"][0] + .2, .15); A(K("buzz", .4), SC["S3"][0] + 1.4, .2)
for i in range(3): A(K("tick"), SC["S4"][0] + .3 + i * (LE["S4", 0] - SC["S4"][0] - .3) / 3, .25)
A(K("pop", 2), LN["S4", 1], .25)
A(K("reveal"), SC["S5"][0] + .1, .3); A(m.syn.bell(79, 2.0), LN["S5", 1] - .1, .2)
m.write()
