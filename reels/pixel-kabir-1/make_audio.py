"""Kabir vs. Kabir #1 sound: object sounds only (no music). tts/.venv/bin/python reels/pixel-kabir-1/make_audio.py (from the project root)"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
import numpy as np
from sfxmix import Mix
m = Mix("reels/pixel-kabir-1"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("pencil", .35), .12, .4); A(K("pencil", .3), .55, .3)                                   # hook: marker crossing out a Monday
A(K("pop", 0), LN["S1", 0] + .45, .3)                                                      # sticky note slaps on the wall
for i in range(4): A(K("pencil", .2), LN["S1", 1] + .3 + i * .45, .2)                      # 41 crossed Mondays
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)                                                   # REASON #1 card
for i in range(3): A(K("pencil", .3), SC["S3"][0] + .3 + i * .5, .22)                      # writing the plan
for i in range(10): A(m.sq(64 + i * 2, .06, .25), LN["S3", 1] + i * .15, .06)              # bar fills
A(K("right", 2), LN["S3", 1] + 1.6, .35)
s0, e0 = LN["S4", 0], LE["S4", 0]
for d in range(3): A(m.sq(60 - d * 4, .14, .5), s0 + d * (e0 - s0) / 3, .08)              # bar drops a notch each day
A(K("miss", 0), LN["S4", 1] + 1.2, .3)
A(K("alarm", 1.5), SC["S5"][0] + .05, .35)                                                 # Monday alarm
A(K("swish", .3), LN["S5", 1] + .1, .3)                                                    # waves it off
A(K("stamp"), LN["S5", 1] + 1.5, .45)                                                      # another red X
A(m.syn.whoosh(.55, 400, 3000), SC["S6"][0], .35)                                          # rewind
for i in range(12): A(K("tick"), LN["S6", 2] + i * (LE["S6", 2] - LN["S6", 2] - .3) / 12, .12)   # two-minute timer
A(K("page", .32), LN["S6", 2] + .2, .2); A(K("right", 3), LE["S6", 2] - .3, .45)
n = 33; a, b = SC["S7"][0] + .3, SC["S7"][1] - .3
for i in range(0, n, 2): A(K("pen_check"), a + (b - a) * (i / n) ** (1 / 1) , .14)       # ticks fill the month
A(K("right", 4), b, .35)
A(K("page", .32), LN["S8", 1] + .5, .18)
A(m.syn.bell(79, 2.5), LN["S8", 2] - .2, .2)
m.write()
