# Copy timemap.json + captions.json into pixel.html (MAP, DUR, FCAPS).
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open("timemap.json")); C = json.load(open("captions.json")); s = open("pixel.html").read()
s = re.sub(r"var MAP = .*?, DUR = [0-9.]+;", lambda m: "var MAP = " + json.dumps(M["segs"]) + ", DUR = " + str(M["end_u"]) + ";", s, flags=re.S)
s = re.sub(r"var FCAPS = .*?;\n", lambda m: "var FCAPS = " + json.dumps(C) + ";\n", s, flags=re.S)
if os.path.exists("subs.json"): s = re.sub(r"var SUBS = .*?;\n", lambda m: "var SUBS = " + json.dumps(json.load(open("subs.json"))) + ";\n", s, count=1, flags=re.S)
open("pixel.html", "w").write(s); print("synced", M["end_u"])
