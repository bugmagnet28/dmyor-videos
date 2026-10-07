// Sample the cursor every frame and report teleports, slow crawls, and dead time.
//   node analyze.js <page.html> [fps]
const puppeteer = require("puppeteer");
const path = require("path");

(async () => {
  const PAGE = path.resolve(process.argv[2] || "deemyor-explainer.html");
  const FPS = Number(process.argv[3] || 30);

  const browser = await puppeteer.launch({ headless: "new", args: ["--no-sandbox"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  const errs = [];
  page.on("pageerror", e => errs.push(String(e)));
  await page.goto("file://" + PAGE, { waitUntil: "load" });
  await page.waitForFunction("typeof window.__seek === 'function'");

  const dur = await page.evaluate(() => window.__duration);
  const n = Math.round(dur * FPS);

  const pts = [];
  for (let f = 0; f < n; f++) {
    const t = f / FPS;
    const p = await page.evaluate((s) => {
      window.__seek(s);
      const c = document.getElementById("cursor");
      return [parseFloat(c.style.left) || 0, parseFloat(c.style.top) || 0];
    }, t);
    pts.push({ t, x: p[0], y: p[1] });
  }
  await browser.close();

  // per-frame speed
  const sp = [];
  for (let i = 1; i < pts.length; i++) {
    const dx = pts[i].x - pts[i-1].x, dy = pts[i].y - pts[i-1].y;
    sp.push({ t: pts[i].t, v: Math.hypot(dx, dy) });
  }

  const TELEPORT = 55;   // px in one frame
  const CRAWL_LO = 0.4, CRAWL_HI = 6;   // px/frame that reads as sluggish drift
  const CRAWL_MIN = 1.0; // seconds of sustained crawl worth flagging

  const jumps = sp.filter(s => s.v > TELEPORT);
  console.log(`duration ${dur}s, ${n} frames`);
  console.log(`page errors: ${errs.length ? errs.join(" | ") : "none"}`);

  // anything near the origin is the old 0,0 bug
  const origin = pts.filter(p => p.x < 40 && p.y < 40);
  console.log(`frames near origin (0,0): ${origin.length}` +
    (origin.length ? `  first at t=${origin[0].t.toFixed(2)}` : ""));

  console.log(`fast frames (>${TELEPORT}px/frame): ${jumps.length}`);

  // A real discontinuity is an isolated spike: fast frame with near-still neighbours.
  // A run of fast frames is just a quick, smooth move.
  const spikes = [];
  for (let i = 1; i < sp.length - 1; i++) {
    if (sp[i].v > TELEPORT && sp[i-1].v < 18 && sp[i+1].v < 18) spikes.push(sp[i]);
  }
  console.log(`SNAPS (isolated discontinuities): ${spikes.length}`);
  spikes.forEach(s => console.log(`   t=${s.t.toFixed(2)}  ${s.v.toFixed(0)}px in one frame`));
  console.log(`peak speed: ${Math.max(...sp.map(s=>s.v)).toFixed(0)}px/frame`);

  // sustained slow drift
  const runs = [];
  let cur = null;
  for (const s of sp) {
    const slow = s.v > CRAWL_LO && s.v < CRAWL_HI;
    if (slow) { if (!cur) cur = { s: s.t, e: s.t }; else cur.e = s.t; }
    else { if (cur && cur.e - cur.s >= CRAWL_MIN) runs.push(cur); cur = null; }
  }
  if (cur && cur.e - cur.s >= CRAWL_MIN) runs.push(cur);
  console.log(`slow drifts (>=${CRAWL_MIN}s at ${CRAWL_LO}-${CRAWL_HI}px/frame): ${runs.length}`);
  runs.forEach(r => console.log(`   t=${r.s.toFixed(1)}s -> ${r.e.toFixed(1)}s  (${(r.e-r.s).toFixed(1)}s)`));

  const moving = sp.filter(s => s.v > CRAWL_LO).length;
  console.log(`moving ${(100*moving/sp.length).toFixed(0)}% of frames, still ${(100-100*moving/sp.length).toFixed(0)}%`);
})();
