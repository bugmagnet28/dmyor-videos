"""Straight Answer #4 sound (no music). tts/.venv/bin/python reels/pixel-straight-4/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-straight-4"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
for i in range(3): A(K("stamp"), .06 + i * .22, .25)                                       # hook: three labels slap on
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
A(K("page", .32), SC["S3"][0] + .2, .2); A(K("plate"), LN["S3", 1] + .9, .25)               # the book drops
A(m.syn.whoosh(.6, 300, 1500), SC["S4"][0] + .1, .12); A(K("stamp"), LN["S4", 1], .35)
per = (LE["S5", 0] - SC["S5"][0]) / 6
for i in range(6): A(K("page", .2), SC["S5"][0] + i * per + per * .8, .25); A(K("tick"), SC["S5"][0] + i * per + per * .95, .15)   # votes drop in
A(K("right", 3), LN["S5", 1], .35)
A(K("pencil", .5), LN["S6", 1], .25)
A(m.syn.bell(79, 2.5), LN["S6", 3] - .2, .2)
m.write()
