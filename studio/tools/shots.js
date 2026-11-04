// Scene check before recording: node studio/tools/shots.js <reel.html> <outdir> <t1> [t2 ...]  -> PNG per time (1080x1920)
const puppeteer = require("puppeteer"); const path = require("path"); const fs = require("fs");
(async () => {
  const [page_, out, ...ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await puppeteer.launch({ headless: "new", args: ["--allow-file-access-from-files"] }); const p = await b.newPage();
  await p.setViewport({ width: 1080, height: 1920 }); await p.goto("file://" + path.resolve(page_)); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => { const s = document.getElementById("stage"); s.style.transform = "none"; const v = document.getElementById("viewport"); v.style.alignItems = "flex-start"; v.style.justifyContent = "flex-start"; const pb = document.getElementById("playBtn"); if (pb) pb.style.display = "none"; });
  for (const t of ts) { await p.evaluate((t) => window.__seek(t), Number(t)); const f = path.join(out, "t" + t + ".png"); await p.screenshot({ path: f, clip: { x: 0, y: 0, width: 1080, height: 1920 } }); console.log(f); }
  await b.close();
})();
