"""Kabir vs. Kabir #9 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-9"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
for i in range(4): A(K("plate"), .05 + i * .33, .3)                                         # hook: barbell clanks
A(K("stamp"), LN["S1", 1] + .2, .25)
for i in range(3): A(m.sq(60 - i * 4, .12, .5), SC["S2"][0] + .2 + i * .7, .06)
A(K("pop", 4), LN["S2", 1] + 1.4, .3); A(K("miss", 1), LN["S2", 1] + 1.6, .25)              # the eighth day
A(m.syn.impact(.4), LN["S3", 1] + .3, .2); A(K("reveal"), LN["S3", 1] + (LE["S3", 1] - LN["S3", 1]) * .5, .3)
for i in range(7): A(K("pen_check"), SC["S4"][0] + .2 + i * .25, .14)
A(K("plate"), SC["S4"][0] + .1, .15)
for i in range(6): A(K("tick"), SC["S5"][0] + i * .25, .15)
A(K("right", 3), SC["S5"][0] + 1.6, .35); A(m.syn.bell(79, 2.0), LN["S5", 2] - .1, .2)
m.write()
