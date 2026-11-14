"""Kabir vs. Kabir #11 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-11"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
for i, mn in enumerate([0, 4, 7, 12, 7, 4]): A(m.syn.pluck(60 + mn, .8), .05 + i * .2, .25)   # hook: strumming bars 1-11
A(m.syn.pluck(61, .6), 1.4, .25); A(m.syn.pluck(66, .6), 1.5, .25)                              # bar 12: a wrong note
A(K("miss", 0), LN["S2", 1], .3); A(K("stamp"), LN["S2", 1] + .2, .25)
A(K("ratchet", 1.2), LN["S3", 1], .15)
st = LN["S4", 1]
for i in range(10): A(K("tick"), SC["S4"][0] + .5 + i * (st - SC["S4"][0] - .5) / 10, .18)  # metronome slow reps
A(K("swish", .4), st, .25); A(K("right", 3), st + 1.0, .4)
for i, mn in enumerate([0, 4, 7, 12, 16]): A(m.syn.pluck(60 + mn, .9), SC["S5"][0] + .1 + i * .2, .25)
A(m.syn.bell(79, 2.0), LN["S5", 2] - .1, .2)
m.write()
