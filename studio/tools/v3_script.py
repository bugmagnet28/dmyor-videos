#!/usr/bin/env python3
"""Turn an illustrated reel's narration.json into a one-take ElevenLabs v3 script (Adam, owner rule 2026-10-28).
   python3 studio/tools/v3_script.py reels/<slug>   -> reels/<slug>/narration-elevenlabs-v3.txt
Stage tags become v3 audio tags; each thought is its own paragraph so the take has real pauses to cut in."""
import json, re, sys, os
TAGS = {"hook": "[confident]", "turn": "[short pause] [thoughtful]", "land": "[warm, encouraging]", "outro": "[warm]", None: ""}
d = sys.argv[1].rstrip("/"); n = json.load(open(os.path.join(d, "narration.json")))
out, seen_outro = [], False
for th in [t.strip() for t in n["spoken"].split("||") if t.strip()]:
    m = re.match(r"\[(hook|body|turn|land|outro)\]\s*", th); st = m.group(1) if m else None; th = re.sub(r"\[(?:hook|body|turn|land|outro)\]\s*", "", th)
    th = re.sub(r"\bDmyor\b", "Deem-yor", th)
    th = re.sub(r"(\?)\s+", r"\1 [pause] ", th)                     # owner: a real pause after questions
    tag = TAGS.get(st, "")
    if st == "outro" and seen_outro: tag = "[smiling]"
    seen_outro |= st == "outro"
    out.append((tag + " " + th).strip())
open(os.path.join(d, "narration-elevenlabs-v3.txt"), "w").write("\n\n".join(out) + "\n")
print(os.path.join(d, "narration-elevenlabs-v3.txt"))
