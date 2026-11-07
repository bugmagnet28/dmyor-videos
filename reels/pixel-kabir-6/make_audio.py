"""Kabir vs. Kabir #6 sound (no music). tts/.venv/bin/python reels/pixel-kabir-6/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-6"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("pen_check"), .08, .35); A(K("reveal"), .2, .2)                                        # hook: the list, confetti
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
a, b = SC["S3"][0] + .1, LE["S3", 0]
for i in range(7): A(K("pop", i % 5), a + (b - a) * i / 7, .22)                             # seven balls in the air
A(K("miss", 0), LN["S3", 1] + .3, .3); A(K("plate"), LN["S3", 1] + .6, .15)                 # one drops
for i in range(6): A(K("plate"), LN["S3", 2] + .5 + i * .07, .14)                           # all of them
for i in range(7): A(m.sq(62 - i * 2, .08, .5), SC["S4"][0] + .2 + i * (LE["S4", 1] - SC["S4"][0]) / 7, .06)   # tank drains
A(K("buzz", .6), LE["S4", 1] - .3, .2)
for i in range(4): A(K("tap"), SC["S5"][0] + .3 + i * .62, .15)                             # one ball, steady
A(K("right", 3), LN["S5", 1] + 1.2, .4)
for i in range(6): A(K("pop", i % 5), SC["S6"][0] + .2 + i * (LE["S6", 0] + .2 - SC["S6"][0]) / 6, .2)
A(m.syn.bell(79, 2.5), LN["S6", 2] - .2, .2)
m.write()
