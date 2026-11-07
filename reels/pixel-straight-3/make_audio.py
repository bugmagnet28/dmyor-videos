"""Straight Answer #3 sound (no music). tts/.venv/bin/python reels/pixel-straight-3/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-straight-3"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("footsteps", 3.5), .05, .3); A(K("pen_check"), .15, .25)                                # hook: walking, the plan
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
t1, e1 = LN["S3", 1], LE["S3", 1]
A(K("footsteps", 2.0), SC["S3"][0], .25); A(m.syn.impact(.6), t1 + .3, .3); A(K("plate"), t1 + .32, .2)   # the rock lands
A(m.syn.whoosh(1.2, 300, 3000), t1 + (e1 - t1) * .45, .2)                                   # rain
A(K("alarm", .9), t1 + (e1 - t1) * .75, .2)                                                # phone rings
A(K("miss", 0), LN["S3", 2] + .3, .3); A(K("pencil", .4), LN["S3", 2] + .35, .2)            # plan crossed out
A(K("buzz", .5), SC["S4"][0] + .3, .15); A(K("pop", 1), SC["S4"][0] + .2, .2); A(K("pop", 3), LN["S4", 1], .2)
A(K("pop", 0), LN["S5", 1], .25); t = LN["S5", 2]; e = LE["S5", 2]
A(K("stamp"), t, .35); A(K("stamp"), t + (e - t) * .5, .35); A(K("stamp"), e, .35)          # if-then cards
for i in range(3): A(K("swish", .4), SC["S6"][0] + .2 + (LN["S6", 2] - .5 - SC["S6"][0]) * (i + .5) / 3.4, .25)   # hops the obstacles
A(K("right", 3), LN["S6", 2] - .3, .4)
A(m.syn.bell(79, 2.5), LN["S6", 2] - .1, .2)
m.write()
