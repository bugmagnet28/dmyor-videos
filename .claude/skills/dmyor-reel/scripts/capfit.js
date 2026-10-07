// Place captions in whatever space the frame actually has.
// For each caption window we seek to a few sample times, measure every visible
// piece of CONTENT (decor excluded), and pick the roomiest free band inside the
// Reels safe area. Output is a y per caption, written back into the timeline.
//
//   node capfit.js <reel.html> <caps.json> <out.json>
const puppeteer = require("puppeteer");
const path = require("path"), fs = require("fs");

const TOP = 240, BOT = 1250;          // Reels safe band
const PAD = 26;                       // breathing room around existing content

(async () => {
  const [page_, capsPath, outPath] = process.argv.slice(2);
  const caps = JSON.parse(fs.readFileSync(capsPath, "utf8"));

  const browser = await puppeteer.launch({ headless: "new", args: ["--no-sandbox"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await page.goto("file://" + path.resolve(page_), { waitUntil: "load" });
  await page.waitForFunction("typeof window.__seek === 'function'");

  // occupied vertical intervals at time t, ignoring decor and the caption layer
  const occupiedAt = async (t) => page.evaluate((s) => {
    window.__seek(s);
    const vis = el => { let n = el, o = 1;
      while (n && n !== document.body) { o *= parseFloat(getComputedStyle(n).opacity); n = n.parentElement; }
      return o; };
    const out = [];
    document.querySelectorAll('#cam *').forEach(el => {
      if (el.closest('[data-decor]') || el.closest('#capTrack')) return;
      if (vis(el) < 0.14) return;
      const cs = getComputedStyle(el);
      const painted = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' ||
                      parseFloat(cs.borderTopWidth) > 0 || parseFloat(cs.borderLeftWidth) > 0;
      const isText = !el.children.length && el.textContent.trim();
      if (!isText && !painted) return;
      let b;
      if (isText) { const r = document.createRange(); r.selectNodeContents(el); b = r.getBoundingClientRect(); }
      else b = el.getBoundingClientRect();
      if (b.width < 4 || b.height < 4 || b.height >= 1900) return;
      out.push([b.top, b.bottom]);
    });
    return out;
  }, t);

  const results = [];
  for (const c of caps) {
    // sample across the caption's life so it does not collide part-way through
    const mid = (c.t + c.end) / 2;
    const samples = [c.t + 0.12, mid, Math.max(c.t + 0.12, c.end - 0.12)];
    let iv = [];
    for (const s of samples) iv = iv.concat(await occupiedAt(Math.min(s, 47.6)));

    // merge occupied intervals
    iv.sort((a, b) => a[0] - b[0]);
    const merged = [];
    for (const [a, b] of iv) {
      const last = merged[merged.length - 1];
      if (last && a - PAD <= last[1]) last[1] = Math.max(last[1], b);
      else merged.push([a - PAD, b + PAD]);
    }
    // free gaps inside the safe band
    const gaps = [];
    let cur = TOP;
    for (const [a, b] of merged) {
      if (a > cur) gaps.push([cur, Math.min(a, BOT)]);
      cur = Math.max(cur, b);
      if (cur >= BOT) break;
    }
    if (cur < BOT) gaps.push([cur, BOT]);

    const lines = Math.max(1, Math.ceil(c.text.length / 26));
    const need = lines * c.size * 1.16 + 16;
    const fits = gaps.filter(g => g[1] - g[0] >= need);
    let y;
    if (fits.length) {
      // roomiest gap, and bias to the lower one when two are similar:
      // a caption under the graphic reads as a caption, above it reads as a title
      fits.sort((a, b) => (b[1] - b[0]) - (a[1] - a[0]));
      const best = fits[0];
      y = Math.round(best[0] + (best[1] - best[0] - need) / 2);
    } else {
      // nothing fits cleanly: take the largest gap and sit centred in it
      gaps.sort((a, b) => (b[1] - b[0]) - (a[1] - a[0]));
      const g = gaps[0] || [TOP, BOT];
      y = Math.round(Math.max(TOP, Math.min(BOT - need, g[0] + (g[1] - g[0] - need) / 2)));
    }
    results.push({ ...c, y, _need: Math.round(need), _gaps: gaps.length, _fit: !!fits.length });
  }
  await browser.close();

  fs.writeFileSync(outPath, JSON.stringify(results, null, 1));
  const tight = results.filter(r => !r._fit).length;
  console.log(`placed ${results.length} captions, ${tight} with no clean gap`);
  results.forEach(r => console.log(
    `  ${String(r.t).padStart(6)}  y=${String(r.y).padStart(4)}  ${r._fit ? "  " : "!!"}  ${r.text}`));
})();
