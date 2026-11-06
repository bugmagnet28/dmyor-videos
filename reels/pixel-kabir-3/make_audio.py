"""Kabir vs. Kabir #3 sound: object sounds only (no music). tts/.venv/bin/python reels/pixel-kabir-3/make_audio.py (from the project root)"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-3"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("page", .32), .1, .45)                                                                 # hook: journal page
A(K("toggle"), LN["S1", 1] - .15, .3); A(K("pencil", 1.2), LN["S1", 1] + .2, .3)           # lamp on, serious writing
A(K("page", .32), LN["S1", 2] - .15, .3)
for i in range(7): A(K("pencil", .2), LN["S1", 3] + i * (LE["S1", 3] - LN["S1", 3]) / 7, .16)   # highlighter sweep
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)                                                   # REASON #3 card
for i in range(7): A(K("pen_check"), LN["S3", 1] + i * .15, .12)                           # OKAY, OKAY, OKAY...
for k in range(3): A(m.sq(60 - k * 4, .18, .5), LN["S3", 2] + k * .7, .06)                 # habits fade out
A(K("pop", 1), LN["S4", 1], .25); A(K("pop", 3), LN["S4", 1] + 1.1, .25)                   # bubbles
A(K("pencil", .6), LN["S5", 0] + 1.0, .3)                                                  # strike-through
A(K("pencil", .9), LN["S5", 1] - .2, .25); A(m.syn.bell(81, 1.6), LN["S5", 1] + .7, .14)   # the new question
for i in range(3): A(K("pencil", .5), SC["S6"][0] + .2 + i * .55, .22)                     # honest answers
for i in range(3): A(K("pop", i), LN["S6", 1] + .3 + i * .5, .2)                           # they light up
A(K("typing", 1.0), SC["S7"][0] + .2, .3); A(K("beep2"), LN["S7", 1] - .2, .3); A(K("swish", .4), LN["S7", 1], .25); A(K("right", 3), LN["S7", 1] + .4, .4)  # email sent
A(K("page", .32), SC["S8"][0] + .05, .3)
A(m.syn.bell(79, 2.5), LN["S8", 2] - .2, .2)
m.write()
