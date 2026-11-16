import json, sys, urllib.request, urllib.parse, os
UA = {"User-Agent": "DmyorReelBot/1.0 (video production)"}
out = json.load(open("cand/list.json"))
for tag, q, n in [x.split("|") for x in sys.argv[1:]]:
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "license": "cc0,pdm", "page_size": 20})
    try: r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
    except Exception as e: print("ERR", tag, e); continue
    got = 0
    for it in r.get("results", []):
        name = f"{tag}-{got}"
        try: data = urllib.request.urlopen(urllib.request.Request(it.get("thumbnail") or it["url"], headers=UA), timeout=40).read()
        except Exception as e: continue
        open(f"cand/{name}.jpg", "wb").write(data)
        out[name] = {"title": it["title"], "license": it["license"], "url": it["url"], "page": it.get("foreign_landing_url"), "source": it.get("source"), "w": it.get("width"), "h": it.get("height")}
        print(name, it["license"], it.get("source"), (it["title"] or "")[:60], it.get("width")); got += 1
        if got >= int(n): break
json.dump(out, open("cand/list.json", "w"), indent=1)
