"""Kabir vs. Kabir #2 sound: object sounds only (no music). tts/.venv/bin/python reels/pixel-kabir-2/make_audio.py (from the project root)"""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-kabir-2"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("coin"), .1, .45)                                                                      # hook: the card shines (cha-ching)
A(K("stamp"), LN["S1", 1] + .2, .3)                                                        # paid in full
A(K("reveal"), LN["S1", 2] + .05, .35); [A(K("pop", i), LN["S1", 2] + .15 + i * .12, .18) for i in range(4)]   # confetti
A(m.syn.bell(76, 2.0), LN["S2", 1], .25)                                                   # REASON #2 card
A(K("footsteps", 1.2), LN["S3", 0], .35); A(K("door"), LN["S3", 1] - .35, .3)              # day 1: running in
A(K("footsteps", 1.0), LN["S3", 1], .28); A(K("door"), LN["S3", 2] - .35, .25)             # day 2
A(K("footsteps", 1.4), LN["S3", 2] + .2, .2)                                               # day 3: dragging
for d in range(3): A(m.sq(64 - d * 5, .1, .5), LN["S3", d] + .1, .06)                      # chart point drops
A(K("miss", 0), LN["S4", 0] + .3, .3)
A(K("pop", 1), LN["S4", 2], .25)                                                           # question bubble
A(K("plate"), LN["S4", 3] + .25, .2)                                                       # flops onto the sofa
A(K("swish", .5), SC["S5"][0] + .2, .15); A(K("tick"), LN["S5", 0], .2)                    # dust settles, counter
A(K("pen_check"), LN["S6", 0] + .6, .3)                                                    # question crossed out
for j in range(3): A(K("pop", j + 2), LN["S6", 1] + .9 + j * .45, .3)                      # three slots booked
A(K("miss", 1), LN["S6", 2] + .05, .25); A(K("swish", .3), LN["S6", 2] + 1.0, .3); A(K("right", 2), LN["S6", 2] + 1.6, .35)   # missed, moved
A(K("footsteps", 2.5), SC["S7"][0] + .3, .25)                                              # rainy Wednesday walk
A(m.syn.whoosh(.8, 300, 1500), SC["S7"][0], .08)
for i in range(6): A(K("tick"), SC["S8"][0] + .2 + i * .23, .14)                           # visits counter climbs
A(K("right", 4), SC["S8"][0] + 1.6, .35)
A(m.syn.bell(79, 2.5), LN["S8", 1] - .2, .2)
m.write()
