// Grab still frames from a timeline page at given seconds, for visual checking.
//   node shots.js <page.html> <outdir> <t1> <t2> ...
const puppeteer = require("puppeteer");
const path = require("path");
const fs = require("fs");

(async () => {
  const [page_, outdir, ...times] = process.argv.slice(2);
  const PAGE = path.resolve(page_);
  fs.mkdirSync(outdir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--force-device-scale-factor=1", "--hide-scrollbars",
           "--disable-lcd-text", "--font-render-hinting=none"]
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });

  const errs = [];
  page.on("pageerror", e => errs.push(String(e)));
  page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });

  await page.goto("file://" + PAGE, { waitUntil: "load" });
  await page.waitForFunction("typeof window.__seek === 'function'");
  await page.evaluate(() => { const b = document.getElementById("playBtn"); if (b) b.style.display = "none"; });

  for (const t of times) {
    await page.evaluate((s) => window.__seek(s), Number(t));
    await page.screenshot({ path: path.join(outdir, `t${t}.png`) });
  }
  await browser.close();
  console.log(errs.length ? "PAGE ERRORS:\n" + errs.join("\n") : "no page errors");
})();
