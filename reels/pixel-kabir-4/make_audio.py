"""Kabir vs. Kabir #4 sound (no music). tts/.venv/bin/python reels/pixel-kabir-4/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-4"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
for i in range(4): A(K("pen_check"), .08 + i * .18, .3)                                    # hook: ticks on the calendar
A(K("right", 2), LN["S1", 1] + .3, .3)
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
A(K("pop", 0), SC["S3"][0] + .3, .2); A(K("pop", 2), SC["S3"][0] + .6, .2)                 # party
A(K("miss", 0), LN["S3", 1] + .4, .35); A(m.syn.impact(.5), LN["S3", 1] + .42, .2)          # streak 0
A(K("plate"), SC["S4"][0] + .2, .2)                                                        # flops on sofa
for i in range(9): A(m.sq(55 - i, .08, .5), LN["S4", 1] + i * (LE["S4", 1] - LN["S4", 1]) / 9, .05)   # grey days
A(K("pencil", 1.2), SC["S5"][0] + .2, .2); A(K("miss", 1), LN["S5", 1] + .9, .3)
A(K("stamp"), LN["S6", 1], .4); A(K("right", 3), LN["S6", 2] + .1, .35)
for i in range(6): A(K("pen_check"), SC["S7"][0] + i * .25, .15)
A(m.syn.bell(79, 2.5), LN["S7", 2] - .2, .2)
m.write()
