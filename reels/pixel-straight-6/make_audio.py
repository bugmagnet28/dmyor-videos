"""Straight Answer #6 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-straight-6"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("beep2"), .08, .4); A(K("miss", 0), LN["S1", 1] + .3, .3)                               # hook: scale beeps
A(K("pencil", 1.6), LN["S2", 1], .2); A(K("pop", 2), LN["S2", 1] + 2, .25)
A(K("ratchet", 1.2), SC["S3"][0] + .3, .15); A(K("ratchet", .8), LN["S3", 0] + 2.6, .15)
A(K("pencil", 2.0), LN["S4", 1], .2); A(K("right", 3), LN["S4", 2], .35)
A(K("beep2"), SC["S5"][0] + .1, .3); A(m.syn.bell(79, 2.0), LN["S5", 1] - .1, .2)
m.write()
