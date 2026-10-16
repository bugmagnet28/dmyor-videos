// Frame-accurate recorder for dmyor-launch.html
//
// The page renders purely as a function of time via window.__seek(seconds), so we
// step it frame by frame rather than screen-recording in real time. Output is
// therefore independent of machine speed and never drops or duplicates a frame.
//
//   node record.js [--fps 30] [--out dmyor-launch.mp4] [--scale 1] [--start 0] [--end 45]

const puppeteer = require("puppeteer");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

function arg(name, fallback) {
  const i = process.argv.indexOf("--" + name);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const FPS = Number(arg("fps", 30));
const SCALE = Number(arg("scale", 1));
const OUT = path.resolve(arg("out", "dmyor-launch.mp4"));
const AUDIO = arg("audio", null);   // muxed in after capture
const PAGE = path.resolve(arg("page", "dmyor-launch.html"));
const W = 1080, H = 1920;

(async () => {
  if (!fs.existsSync(PAGE)) {
    console.error("Page not found: " + PAGE);
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    headless: "new",
    protocolTimeout: 900000,           // machine stalls killed records at the 180s default (2026-10-14)
    args: [
      "--no-sandbox",
      "--force-device-scale-factor=1",
      "--hide-scrollbars",
      "--disable-lcd-text",              // greyscale AA, avoids colour fringing in video
      "--font-render-hinting=none",
      "--disable-features=DefaultPassthroughCommandDecoder"
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: SCALE });
  await page.goto("file://" + PAGE, { waitUntil: "load" });

  // The stage scales itself to the viewport; at 1080x1920 that is exactly 1:1.
  await page.waitForFunction("typeof window.__seek === 'function'");
  await page.evaluate(() => {
    const btn = document.getElementById("playBtn");
    if (btn) btn.style.display = "none";
  });

  const duration = Number(arg("end", await page.evaluate(() => window.__duration)));
  const startAt = Number(arg("start", 0));
  const total = Math.round((duration - startAt) * FPS);

  const ff = spawn("ffmpeg", [
    "-y",
    "-f", "image2pipe",
    "-c:v", "png",
    "-r", String(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "17",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    "-r", String(FPS),
    OUT
  ], { stdio: ["pipe", "inherit", "inherit"] });

  const ffDone = new Promise((res, rej) => {
    ff.on("close", (code) => (code === 0 ? res() : rej(new Error("ffmpeg exited " + code))));
    ff.on("error", rej);
  });

  // Backpressure: if ffmpeg's buffer is full, wait for drain before the next frame.
  const write = (buf) =>
    ff.stdin.write(buf) ? Promise.resolve() : new Promise((r) => ff.stdin.once("drain", r));

  console.log(`Recording ${total} frames @ ${FPS}fps -> ${path.basename(OUT)}`);
  for (let f = 0; f < total; f++) {
    const t = startAt + f / FPS;
    await page.evaluate((sec) => window.__seek(sec), t);
    const shot = await page.screenshot({ type: "png", optimizeForSpeed: true });
    await write(shot);
    if (f % (FPS * 5) === 0) {
      process.stdout.write(`  ${(t).toFixed(1)}s / ${duration.toFixed(1)}s\n`);
    }
  }

  ff.stdin.end();
  await ffDone;
  await browser.close();

  if (AUDIO && fs.existsSync(AUDIO)) {
    // capture is silent; mux the narration on afterwards so video stays frame-exact
    const tmp = OUT.replace(/\.mp4$/, ".silent.mp4");
    fs.renameSync(OUT, tmp);
    await new Promise((res, rej) => {
      const m = spawn("ffmpeg", ["-v", "error", "-y", "-i", tmp, "-i", path.resolve(AUDIO),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
        "-movflags", "+faststart", OUT], { stdio: "inherit" });
      m.on("close", c => (c === 0 ? res() : rej(new Error("ffmpeg mux exited " + c))));
    });
    fs.unlinkSync(tmp);
    console.log("muxed audio: " + path.basename(AUDIO));
  }
  console.log("Done: " + OUT);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
