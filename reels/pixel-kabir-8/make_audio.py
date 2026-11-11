"""Kabir vs. Kabir #8 sound (no music). tts/.venv/bin/python reels/pixel-kabir-8/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-8"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("pencil", 1.0), .08, .4)                                                               # hook: scribbling the cat
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
A(K("beep2"), SC["S3"][0] + .2, .25); A(K("reveal"), LN["S3", 1] - .3, .3); A(K("coin"), LN["S3", 1] + .4, .2)   # phone, the perfect cat, likes
A(K("swish", .4), SC["S4"][0] + .1, .25); A(K("stamp"), LN["S4", 1], .45); A(K("miss", 0), LN["S4", 1] + 1.4, .25)   # verdict
for i in range(8): A(K("tick"), SC["S5"][0] + .2 + i * .3, .1)                              # film strip rolling
A(K("pop", 1), SC["S6"][0] + .2, .25); A(K("stamp"), LN["S6", 1] - .1, .3); A(K("right", 3), LN["S6", 2], .4)
A(m.syn.bell(79, 2.5), LN["S7", 0] - .2, .2)
m.write()
