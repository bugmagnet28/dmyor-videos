"""Straight Answer #2 sound (no music). tts/.venv/bin/python reels/pixel-straight-2/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-straight-2"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(m.syn.whoosh(.7, 400, 2500), .05, .25); A(K("pop", 0), .15, .3)                          # hook: clouds drift in
for i in range(3): A(K("miss", i), LN["S1", 1] + i * .3, .2)                               # crossed out
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
A(m.syn.whoosh(1.0, 200, 1200), SC["S3"][0] + .1, .15); A(K("pop", 1), LN["S3", 1], .25); A(K("miss", 0), LN["S3", 2] + .5, .25)
A(K("pop", 0), SC["S4"][0] + .2, .25); t0, t1 = LN["S4", 1] + .3, LE["S4", 1] - .4
for i in range(4): A(K("pop", i + 1), t0 + (t1 - t0) * i / 4, .25)                          # ladder steps
A(K("right", 3), t1 + .1, .4)
A(K("miss", 1), SC["S5"][0] + 1.2, .25); A(K("right", 2), SC["S5"][0] + 1.9, .35)         # hands test
A(K("pen_check"), SC["S6"][0] + .6, .3)
A(m.syn.bell(79, 2.5), LN["S6", 1] - .2, .2)
m.write()
