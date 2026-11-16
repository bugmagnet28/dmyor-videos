# search Wikimedia Commons for CC0 / public-domain files; writes cand/<tag>-N.<ext> thumbs + cand/list.json
import json, sys, urllib.request, urllib.parse, os, re
UA = {"User-Agent": "DmyorReelBot/1.0 (video production; contact via dmyor.com)"}
def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
OK = re.compile(r"^(cc0|public domain|pd|pdm)", re.I)
out = json.load(open("cand/list.json")) if os.path.exists("cand/list.json") else {}
for tag, q, kind, n in [x.split("|") for x in sys.argv[1:]]:
    r = api({"action": "query", "format": "json", "generator": "search", "gsrsearch": q + (" filetype:video" if kind == "video" else " filetype:bitmap"), "gsrnamespace": 6, "gsrlimit": 40,
             "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 1080})
    got = 0
    for p in sorted(r.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)):
        ii = p["imageinfo"][0]; lic = ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "")
        if not OK.match(lic): continue
        if kind != "video" and ii.get("width", 0) < 1600: continue
        name = f"{tag}-{got}"; thumb = ii.get("thumburl")
        try:
            data = urllib.request.urlopen(urllib.request.Request(thumb, headers=UA), timeout=60).read()
            open(f"cand/{name}.jpg", "wb").write(data)
        except Exception as e: print("skip", e); continue
        out[name] = {"title": p["title"], "license": lic, "url": ii["url"], "page": ii.get("descriptionurl"), "mime": ii.get("mime"), "w": ii.get("width"), "h": ii.get("height"), "dur": ii.get("duration")}
        print(name, lic, p["title"][:80]); got += 1
        if got >= int(n): break
json.dump(out, open("cand/list.json", "w"), indent=1)
