#!/usr/bin/env node
/* Motion audit. Must report 0 snaps and 0 origin frames before recording:
   a cursor teleport is invisible in stills but obvious in the video. */
const puppeteer = require(require('path').join(process.cwd(),'node_modules','puppeteer'));
const path = require('path');
(async () => {
  const dir = process.argv[2] || '.';
  const page_ = path.resolve(dir.endsWith('.html') ? dir : path.join(dir, 'reel.html'));
  const FPS = 30;
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto('file://' + page_, { waitUntil: 'load' });
  await page.waitForFunction("typeof window.__seek === 'function'");
  const dur = await page.evaluate(() => window.__duration);
  const n = Math.round(dur * FPS), pts = [];
  for (let f = 0; f < n; f++) {
    pts.push(await page.evaluate(s => { window.__seek(s);
      const c = document.getElementById('cursor');   // motion engine has no cursor
      return c ? [parseFloat(c.style.left) || 0, parseFloat(c.style.top) || 0] : null; }, f / FPS));
  }
  // frame-motion pass: the cursor can be moving while the FRAME sits still.
  // This is what catches a scene that looks like a photograph.
  await page.setViewport({ width: 540, height: 960, deviceScaleFactor: 1 });
  const STEP = 0.4; let prevBuf = null; const motion = [];
  for (let t = 0; t < dur; t += STEP) {
    await page.evaluate(s => window.__seek(s), t);
    const buf = await page.screenshot({ type: 'jpeg', quality: 45 });
    if (prevBuf) { const m = Math.min(prevBuf.length, buf.length); let d = 0;
      for (let i = 0; i < m; i += 7) if (prevBuf[i] !== buf[i]) d++;
      motion.push({ t: +t.toFixed(1), d: d / (m / 7) }); }
    prevBuf = buf;
  }
  const frozen = []; let run = [];
  motion.forEach(r => { if (r.d < 0.04) run.push(r.t);
    else { if (run.length >= 3) frozen.push([run[0], run[run.length-1] + STEP]); run = []; } });
  if (run.length >= 3) frozen.push([run[0], run[run.length-1] + STEP]);

  await browser.close();
  const hasCursor = pts[0] !== null;
  const sp = [];
  if (hasCursor) for (let i = 1; i < pts.length; i++)
    sp.push({ t: i / FPS, v: Math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1]) });
  const origin = hasCursor ? pts.filter(p => p[0] < 40 && p[1] < 40).length : 0;
  const snaps = hasCursor ? sp.filter((s,i) => i>0 && i<sp.length-1 && s.v>55 && sp[i-1].v<18 && sp[i+1].v<18) : [];
  const peak = sp.length ? Math.max(...sp.map(s => s.v)) : 0;
  const still = sp.length ? sp.filter(s => s.v <= 0.4).length / sp.length * 100 : 0;
  console.log(`duration ${dur}s, ${n} frames`);
  console.log(`page errors      : ${errs.length ? errs.join(' | ') : 'none'}`);
  if (hasCursor) {
    console.log(`origin frames    : ${origin}${origin ? '   <-- FIX: unresolved waypoint' : ''}`);
    console.log(`SNAPS            : ${snaps.length}${snaps.length ? '   <-- FIX: ' + snaps.map(s=>s.t.toFixed(2)).join(', ') : ''}`);
    console.log(`peak speed       : ${peak.toFixed(0)} px/frame${peak > 120 ? '   <-- whippy, start that move earlier' : ''}`);
    console.log(`cursor still     : ${still.toFixed(0)}% of frames`);
  } else {
    console.log(`cursor           : none (motion engine)`);
  }
  console.log(`frozen frames    : ${frozen.length ? frozen.map(f=>f[0].toFixed(1)+'-'+f[1].toFixed(1)+'s').join(', ') : 'none - frame always moving'}`);
  const bad = errs.length || origin || snaps.length;
  console.log(bad ? '\nNOT READY' : '\nready to record');
  process.exit(bad ? 1 : 0);
})();
