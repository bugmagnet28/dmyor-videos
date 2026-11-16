// node reels/stick-get-up/snap.js t1 t2 ... -> reels/stick-get-up/snaps/t.png
const puppeteer = require("puppeteer"), path = require("path"), fs = require("fs");
(async () => {
  const b = await puppeteer.launch({ headless: "new", args: ["--no-sandbox"] });
  const p = await b.newPage(); await p.setViewport({ width: 1080, height: 1920 });
  p.on("pageerror", e => console.log("ERR", e.message));
  await p.goto("file://" + path.resolve(__dirname, "film.html")); await p.waitForFunction("typeof window.__seek==='function'");
  await p.evaluate(() => document.getElementById("playBtn").style.display = "none");
  fs.mkdirSync(path.join(__dirname, "snaps"), { recursive: true });
  for (const t of process.argv.slice(2)) { await p.evaluate(t => window.__seek(+t), t); await p.screenshot({ path: path.join(__dirname, "snaps", t + ".png") }); }
  await b.close();
})();
