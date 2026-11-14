"""Straight Answer #5 sound (no music)."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/pixel-straight-5"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("typing", 2.0), .02, .35); A(K("buzz", .3), .6, .2); A(K("buzz", .3), 1.4, .2)           # hook: fast sloppy typing, error buzzes
for i in range(12): A(K("pop", i % 5), SC["S2"][0] + .2 + i * (LE["S2", 0] - SC["S2"][0] - .2) / 12, .12)
A(K("stamp"), LN["S2", 1] + 1, .35)
for i in range(10): A(K("tick"), LN["S3", 1] + i * (LE["S3", 1] - LN["S3", 1]) / 10, .14)
for i in range(6): A(m.sq(64 + i * 2, .08, .5), LN["S3", 2] + i * (LE["S3", 2] - LN["S3", 2]) / 6, .06)
A(K("typing", 1.5), SC["S4"][0] + .1, .25); A(K("right", 3), SC["S4"][0] + .4, .35)
A(m.syn.bell(79, 2.0), LN["S4", 2] - .1, .2)
m.write()
