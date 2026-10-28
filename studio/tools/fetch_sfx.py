"""Fetch CC0 sound effects from Openverse into the studio sound library.

    python3 studio/tools/fetch_sfx.py search "pen writing"              # list CC0 matches, no download
    python3 studio/tools/fetch_sfx.py get "pen writing" --name pen-write # download the first usable match
    python3 studio/tools/fetch_sfx.py get "page turn" --name page --pick 2 --max-sec 3

Only CC0 is accepted (owner rule 2026-10-28; add --allow-pdm for public-domain marks). Each download is
converted to 44.1 kHz mono wav, trimmed of leading/trailing silence, peak-normalised, and logged in
studio/sfx-library/LICENSES.md with title, author, licence and source URL. Reads no accounts or keys:
Openverse allows light anonymous use. Run from ~/Documents/dmyor-videos.
"""
import argparse, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

ROOT = os.getcwd()
LIB = os.path.join(ROOT, "studio", "sfx-library")
API = "https://api.openverse.org/v1/audio/"
UA = {"User-Agent": "dmyor-videos-sfx/1.0 (becauseidmyor)"}


def get(url, tries=6, timeout=40, binary=False):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                data = r.read()
            return data if binary else json.loads(data)
        except Exception as e:  # Openverse audio search is sometimes slow or 5xx; back off and retry
            last = e
            time.sleep(2 + 3 * i)
    sys.exit(f"Openverse not reachable after {tries} tries: {last}")


def search(q, allow_pdm, max_sec, page_size=20):
    lic = "cc0,pdm" if allow_pdm else "cc0"
    params = {"q": q, "license": lic, "page_size": page_size}  # no category filter: CC0 + sound_effect returned 0 hits (2026-10-28)
    res = get(API + "?" + urllib.parse.urlencode(params)).get("results", [])
    ok = {"cc0", "pdm"} if allow_pdm else {"cc0"}
    out = []
    for r in res:
        if (r.get("license") or "").lower() not in ok or not r.get("url"):
            continue  # trust the record, not the filter: skip anything that is not CC0
        sec = (r.get("duration") or 0) / 1000
        if max_sec and sec and sec > max_sec:
            continue
        out.append(r)
    return out


def show(rs):
    for i, r in enumerate(rs, 1):
        print(f"{i:>2}. {r.get('title','?')[:50]:<50} {((r.get('duration') or 0)/1000):5.1f}s  {r.get('license')}  by {r.get('creator') or 'unknown'}  {r.get('foreign_landing_url','')}")


def fetch(r, name):
    os.makedirs(LIB, exist_ok=True)
    raw = os.path.join(LIB, f".raw-{name}.{(r.get('filetype') or 'mp3').lower()}")
    with open(raw, "wb") as f:
        f.write(get(r["url"], binary=True, timeout=90))
    out = os.path.join(LIB, f"{name}.wav")
    af = ("silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
          "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
          "loudnorm=I=-20:TP=-2:LRA=7")
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-ac", "1", "-ar", "44100", "-af", af, out])
    os.remove(raw)
    if p.returncode:
        sys.exit("ffmpeg failed on " + name)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                               capture_output=True, text=True).stdout or 0)
    log = os.path.join(LIB, "LICENSES.md")
    if not os.path.exists(log):
        open(log, "w").write("# Sound library licences\n\nEvery file here is CC0 (no credit required). Source kept for the record.\n\n"
                              "| file | title | author | licence | source |\n|---|---|---|---|---|\n")
    row = "| {} | {} | {} | {} | {} |\n".format(
        name + ".wav", re.sub(r"[|\n]", " ", r.get("title", "")), re.sub(r"[|\n]", " ", r.get("creator") or "unknown"),
        (r.get("license") or "").upper(), r.get("foreign_landing_url") or r.get("url"))
    open(log, "a").write(row)
    print(f"saved studio/sfx-library/{name}.wav ({dur:.2f}s)  <- {r.get('title')}  [{r.get('license')}]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["search", "get"])
    ap.add_argument("query")
    ap.add_argument("--name")
    ap.add_argument("--pick", type=int, default=1, help="which listed match to download (1 = first)")
    ap.add_argument("--max-sec", type=float, default=8, help="skip clips longer than this (0 = any)")
    ap.add_argument("--allow-pdm", action="store_true")
    a = ap.parse_args()
    rs = search(a.query, a.allow_pdm, a.max_sec)
    if not rs:
        sys.exit("no CC0 sound effects matched; try other words")
    if a.cmd == "search":
        return show(rs)
    if not a.name:
        sys.exit("--name is required for get")
    if not 1 <= a.pick <= len(rs):
        sys.exit(f"--pick must be 1..{len(rs)}")
    fetch(rs[a.pick - 1], re.sub(r"[^a-z0-9-]", "-", a.name.lower()))


if __name__ == "__main__":
    main()
