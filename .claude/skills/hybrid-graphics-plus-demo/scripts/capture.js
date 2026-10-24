// Records real dmyor.com screens as a guest (no account), phone-sized, for hybrid reels.
//   HEADFUL=1 node .claude/skills/hybrid-graphics-plus-demo/scripts/capture.js create-vision|intent-archive   (from project root; HEADFUL gives 2x frames)
// - blocks analytics + the dmyor API so recordings are not counted as visits and nothing is written
// - hides the cookie notice with CSS (does not click/accept it)
// - stops before the final confirm (which would send a guest to login)
// Output: app-capture/raw/<name>.webm (real time), then frames are extracted by extract.sh.
const puppeteer = require("puppeteer");
const path = require("path"), fs = require("fs");
const name = process.argv[2] || "create-vision";
const OUT = path.join(process.cwd(), "app-capture", "raw"); fs.mkdirSync(OUT, { recursive: true });  // run from project root
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const HIDE = `.cookie-banner{display:none!important}`;
(async () => {
  const browser = await puppeteer.launch({ headless: process.env.HEADFUL ? false : "new", args: ["--hide-scrollbars", "--window-size=420,900"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
  await page.setRequestInterception(true);
  page.on("request", (r) => {
    const u = r.url();
    if (/google-analytics|googletagmanager|doubleclick|prod\.dmyor\.com/.test(u)) return r.abort();
    r.continue();
  });
  const url = name === "intent-archive" ? "https://www.dmyor.com/intent-archive" : "https://www.dmyor.com/dashboard/planning/new";
  await page.goto(url, { waitUntil: "networkidle2", timeout: 60000 });
  await page.addStyleTag({ content: HIDE });
  await sleep(1200);
  // raw CDP screencast at device pixels (3x), every frame saved with its timestamp
  const FR = path.join(OUT, name + "_frames"); fs.rmSync(FR, { recursive: true, force: true }); fs.mkdirSync(FR);
  const client = await page.createCDPSession(); const frames = []; let t0 = null;
  client.on("Page.screencastFrame", async (f) => {
    const ts = f.metadata.timestamp; if (t0 === null) t0 = ts;
    const file = path.join(FR, String(frames.length).padStart(5, "0") + ".jpg");
    fs.writeFileSync(file, Buffer.from(f.data, "base64")); frames.push({ file, t: ts - t0 });
    await client.send("Page.screencastFrameAck", { sessionId: f.sessionId }).catch(() => {});
  });
  await client.send("Page.startScreencast", { format: "jpeg", quality: 92, maxWidth: 1170, maxHeight: 2532, everyNthFrame: 1 });
  const rec = { stop: async () => { await client.send("Page.stopScreencast"); fs.writeFileSync(path.join(FR, "frames.json"), JSON.stringify(frames)); } };
  await sleep(1400);
  if (name === "create-vision") {
    const pills = await page.$$(".vsf-year-pill");
    await pills[2].click(); await sleep(1300);                       // 3 years
    await page.click(".vsf-cta"); await sleep(1500);                 // Continue -> step 2
    await page.focus(".vsf-textarea"); await sleep(500);
    await page.type(".vsf-textarea", "I'm going to earn $2,000 a month freelancing.", { delay: 55 });
    await sleep(1300);
    await page.click(".vsf-cta"); await sleep(1600);                 // Continue -> step 3
    const picked = await page.evaluate(() => {
      const bs = [...document.querySelectorAll(".vsf-stage button")];
      const b = bs.find((x) => /career|work|money|finance|business/i.test(x.innerText)) || bs[0];
      b.scrollIntoView({ block: "center" }); return b.getBoundingClientRect().toJSON ? b.innerText : b.innerText;
    });
    await sleep(500);
    await page.evaluate(() => {
      const bs = [...document.querySelectorAll(".vsf-stage button")];
      const b = bs.find((x) => /career|work|money|finance|business/i.test(x.innerText)) || bs[0]; b.click();
    });
    await sleep(2200);                                               // stop before "Confirm"
    console.log("category:", picked);
  } else {
    for (let i = 0; i < 90; i++) { await page.evaluate(() => window.scrollBy(0, 14)); await sleep(80); }
    await sleep(800);
  }
  await rec.stop();
  await browser.close();
  console.log("saved", path.join(OUT, `${name}.webm`));
})();
