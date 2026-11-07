"""Kabir vs. Kabir #7 sound (no music). tts/.venv/bin/python reels/pixel-kabir-7/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-7"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("pencil", .5), .08, .35); A(K("tick"), .6, .2)                                         # hook: marker on the board
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
t = [LN["S3", 0], LN["S3", 1], LN["S3", 1] + (LE["S3", 1] - LN["S3", 1]) * .55, LN["S3", 2]]
for i, x in enumerate(t): A(K("coin"), x + .1, .25); A(m.sq(64 + i * 3, .1, .5), x + .25, .06)   # purchases, bar up
A(m.syn.whoosh(1.0, 200, 900), SC["S4"][0], .2); A(K("miss", 0), LN["S4", 1] + 1.5, .3)
A(K("pop", 0), SC["S5"][0] + .2, .2); A(K("pencil", .4), LN["S5", 1] + .3, .25); A(K("right", 2), LN["S5", 1] + .9, .35)
A(K("beep2"), SC["S6"][0] + .3, .3); A(K("miss", 1), LN["S6", 1] - .1, .25); A(K("right", 4), LN["S6", 2], .4)
for i in range(6): A(K("tick"), SC["S7"][0] + i * .27, .18)
A(m.syn.bell(79, 2.5), LN["S7", 0] - .2, .2)
m.write()
