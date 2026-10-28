"""Promote a downloaded CC0 candidate to the sound kit: python3 studio/sfx-library/use.py <candidate-name> <kit-key>
e.g. use.py typing-1 typing  ->  studio/sfx-library/real/typing.wav (+ licence row copied into LICENSES.md).
sfx.py loads studio/sfx-library/real/<kit-key>.wav in place of the synthesised sound (owner 2026-10-28: real CC0 recordings, not synth)."""
import os, shutil, sys
LIB = os.path.join(os.getcwd(), "studio", "sfx-library"); cand, key = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(LIB, "real"), exist_ok=True)
shutil.copy(os.path.join(LIB, "candidates", cand + ".wav"), os.path.join(LIB, "real", key + ".wav"))
rows = [l for l in open(os.path.join(LIB, "candidates", "LICENSES.md")) if l.startswith(f"| {cand}.wav")]
main = os.path.join(LIB, "LICENSES.md")
if not os.path.exists(main): open(main, "w").write("# Sound library licences\n\nEvery file here is CC0 (no credit required). Source kept for the record.\n\n| file | title | author | licence | source |\n|---|---|---|---|---|\n")
txt = open(main).read()
for r in rows:
    r = r.replace(f"| {cand}.wav", f"| real/{key}.wav", 1)
    if r.split("|")[1] not in txt: open(main, "a").write(r)
print("real/%s.wav <- %s" % (key, cand))
