"""Small Stories #1 sound (no music). tts/.venv/bin/python reels/pixel-story-1/make_audio.py"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-story-1"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("toggle"), .08, .35); A(K("toggle"), .3, .3)                                           # hook: two lamps click on
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)
A(K("typing", 1.6), LN["S3", 0] + .2, .25); A(K("timer", 1.4), LN["S3", 0] + .3, .12)      # twenty minutes
A(K("pencil", .4), LN["S3", 1] + .1, .25)                                                  # writes "tomorrow"
A(K("tap"), SC["S4"][0] + .05, .25); A(K("tap"), LN["S4", 1] + .05, .25)
A(K("ratchet", .6), SC["S5"][0] + .2, .2); A(m.syn.impact(.4), SC["S5"][0] + 1.0, .15)       # the scale tips
A(m.syn.whoosh(1.2, 200, 1500), SC["S6"][0], .2); A(K("reveal"), LN["S6", 1] - .1, .35)     # a year; the finished thing
for i in range(6): A(K("pencil", .15), LN["S6", 2] + .05 + i * .12, .12)                   # notes pile up
A(m.syn.bell(79, 2.5), LN["S7", 2] - .2, .2)
m.write()
