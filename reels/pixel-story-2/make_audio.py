"""Small Stories #2 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-story-2"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("page", .32), .05, .35); A(K("page", .32), .3, .3)                                       # hook: two books open
for i in range(3): A(K("riffle", .6), LN["S2", 0] + i * (LE["S2", 0] - LN["S2", 0]) / 3, .2)   # Sam rereads
A(K("page", .32), LN["S2", 1], .25); A(K("pencil", 2.0), LN["S2", 1] + 1, .25)               # Dev closes the book, writes
A(K("miss", 0), SC["S3"][0] + .3, .2); A(K("pop", 1), LN["S3", 1], .2); A(K("pop", 3), LN["S3", 1] + .2, .2)
A(K("page", .32), SC["S4"][0] + .1, .25); A(K("ratchet", 1.0), LN["S4", 1], .15); A(K("right", 3), LN["S4", 1] + 1, .4)
A(m.syn.bell(79, 2.0), LN["S5", 2] - .1, .2)
m.write()
