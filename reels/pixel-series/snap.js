// node snap.js t1 t2 ... -> snaps/f_<t>.png (quick frame check)
const puppeteer = require("puppeteer"); const path = require("path"); const fs = require("fs");
(async () => { const b = await puppeteer.launch({ args: ["--allow-file-access-from-files"] }); const p = await b.newPage();
  p.on("console", m => { if (m.type() === "error") console.log("PAGE:", m.text()); }); p.on("pageerror", e => console.log("ERR:", e.message));
  await p.setViewport({ width: 1080, height: 1920 }); await p.goto("file://" + path.resolve(process.env.EP, "pixel.html")); fs.mkdirSync(path.join(process.env.EP, "snaps"), { recursive: true });
  for (const t of process.argv.slice(2)) { await p.evaluate(u => window.__seek(+u), t); await p.screenshot({ path: path.join(process.env.EP, "snaps", "f_" + t + ".png") }); }
  await b.close(); })();
