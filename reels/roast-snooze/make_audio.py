"""Habit Roast #5 sound: alarms, snooze taps, curtain, footsteps. Music arc comedy -> resolve."""
import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), "reels/pixel-series"))
from sfxmix import Mix
m = Mix("reels/roast-snooze"); A, K, LN, LE, SC = m.A, m.K, m.LN, m.LE, m.SC
A(K("alarm", .8), .1, .22); A(K("tap"), 1.1, .3); A(K("alarm", .6), 1.6, .18); A(K("tap"), 2.4, .3)   # hook: alarm, snooze, alarm
A(K("miss", 0), LN["S1", 1] + 2.6, .3)                                                                  # more tired
A(m.syn.whoosh(.5, 300, 2000), SC["S2"][0], .2)
for i in range(6): A(K("pop", i), LN["S2", 1] + .6 * i + .3, .22)                                      # six naps cut
A(K("stamp"), LN["S2", 1] + 4.4, .3)
A(K("alarm", .9), SC["S3"][0] + .1, .16); A(K("footsteps", 1.8), SC["S3"][0] + .6, .2); A(K("toggle"), SC["S3"][0] + 2.5, .3)
A(K("swish", .6), LN["S3", 1], .3); A(K("right", 3), LE["S3", 1] - .2, .3)
A(m.syn.bell(79, 2.0), LN["S4", 0] - .1, .2)
m.write(music=[("comedy", 0), ("resolve", SC["S3"][0])])
