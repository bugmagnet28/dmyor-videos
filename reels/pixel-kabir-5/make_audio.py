"""Kabir vs. Kabir #5 sound (no music). tts/.venv/bin/python reels/pixel-kabir-5/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-5"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("door"), .06, .4)                                                                      # hook: closet door creaks open
for i in range(3): A(K("plate"), LN["S1", 1] + 1.4 + i * .3, .18)                           # three boxes
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
t0 = SC["S3"][0] + .2; st = (LE["S3", 0] - t0) / 6
for i in range(6): A(K("tap"), t0 + i * st, .28)                                            # six steps
A(K("beep2"), LN["S3", 1] + .05, .3)                                                       # phone unlock
A(K("typing", 1.0), SC["S4"][0] + .3, .12); [A(K("tick"), SC["S4"][0] + i * (SC["S4"][1] - SC["S4"][0]) / 5, .2) for i in range(5)]   # hours tick
for i in range(6): A(K("step"), SC["S5"][0] + .2 + i * .17, .2)
A(K("right", 2), LN["S5", 1] + .05, .3)
A(K("swish", .5), SC["S6"][0] + .4, .3); A(K("plate"), SC["S6"][0] + 1.6, .2)              # guitar onto the stand
A(K("beep2"), LN["S6", 1] + .1, .15)                                                       # phone charging
for i, mn in enumerate([0, 4, 7, 12]): A(m.syn.pluck(60 + mn, 1.2), SC["S7"][0] + .2 + i * .28, .25)   # he plays
A(m.syn.bell(79, 2.5), LN["S7", 1] - .2, .2)
m.write()
