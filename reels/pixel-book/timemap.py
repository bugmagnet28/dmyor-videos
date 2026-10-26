# Story time t (what scenes are written in) -> film time u, via timemap.json segments [u0, u1, t0, t1].
import json, os
M = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "timemap.json"))); SEGS = M["segs"]; TOTAL = M["end_u"]
def t2u(t):
    for u0, u1, t0, t1 in SEGS:
        if t0 <= t < t1: return u0 + (t - t0) / (t1 - t0) * (u1 - u0)
    return None
def in_cut(t): return t2u(t) is None
def U(a, b):
    ua, ub = t2u(a), t2u(b - 1e-3)
    return max(.05, (ub if ub is not None else ua + 1) - (ua if ua is not None else 0))
