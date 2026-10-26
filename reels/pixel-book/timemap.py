# Story time (t, what the scenes are written in) <-> film time (u, after cutting dead spans / fast-forwarding wordless ones).
import json, os
M = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "timemap.json"))); SEGS = M["segs"]; TEMPO = M["tempo"]
def t2u(t): return t - sum(max(0, min(b, t) - a) * (1 - f) for a, b, f in SEGS)
def in_cut(t): return any(a < t < b and f == 0 for a, b, f in SEGS)
def U(a, b): return max(.05, t2u(b) - t2u(a))      # film-time length of a story span
TOTAL = round(t2u(M["end"]), 3)
