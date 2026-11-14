// Pixel Book: every frame is a pure function of time. Worlds are drawn at 270x480 (1 art pixel = 4 screen px)
// and blitted with a nearest-neighbour "pixel camera", so zooming makes the pixels bigger, never blurry.
var W = 270, H = 480, OW = 1080, OH = 1920;
// film time u -> story time t: each narration line's slot is mapped onto the span of picture it describes (timemap.json)
var C = document.getElementById("c"), X = C.getContext("2d"); X.imageSmoothingEnabled = false;
function mk(w, h) { var c = document.createElement("canvas"); c.width = w; c.height = h; var x = c.getContext("2d"); x.imageSmoothingEnabled = false; return [c, x]; }
var LB = mk(W, H), OA = mk(OW, OH), OB = mk(OW, OH), TINY = mk(W, H);

// ---------- assets ----------
var A = {}, LIST = {
  sky: "../pixel-book/art/field/sky.png", clouds: "../pixel-book/art/field/clouds.png", far: "../pixel-book/art/field/far.png", mid: "../pixel-book/art/field/mid.png", ground: "../pixel-book/art/field/ground.png",
  shadow: "../pixel-book/art/field/shadow.png", flowers: "../pixel-book/art/field/flowers.png", tree: "../pixel-book/art/field/tree.png", reader: "../pixel-book/art/field/hero_read.png", reader_blink: "../pixel-book/art/field/hero_read_blink.png", book_ground: "../pixel-book/art/field/book_ground.png",
  house: "../pixel-book/art/scenes/house.png", hedge: "../pixel-book/art/scenes/hedge.png", car: "../pixel-book/art/scenes/car.png", wheel0: "../pixel-book/art/scenes/wheel0.png", wheel1: "../pixel-book/art/scenes/wheel1.png",
  room_night: "../pixel-book/art/scenes/room_night.png", room_dawn: "../pixel-book/art/scenes/room_dawn.png", notebook: "../pixel-book/art/scenes/notebook.png", laptop: "../pixel-book/art/scenes/laptop.png",
  alarm0: "../pixel-book/art/scenes/alarm0.png", alarm1: "../pixel-book/art/scenes/alarm1.png", phone: "../pixel-book/art/scenes/phone.png", friendcar: "../pixel-book/art/scenes/friendcar.png",
  shop: "../pixel-book/art/scenes/shop.png", sign0: "../pixel-book/art/scenes/sign0.png", sign1: "../pixel-book/art/scenes/sign1.png", office: "../pixel-book/art/scenes/office.png", library: "../pixel-book/art/scenes/library.png", bigbook: "../pixel-book/art/scenes/bigbook.png", heli: "../pixel-book/art/scenes/heli.png"
};
["stand", "blink", "shock", "walk0", "walk1", "walk2", "walk3", "owalk0", "owalk1", "owalk2", "owalk3", "ostand", "olook", "sit_write0", "sit_write1", "sit_type0", "sit_type1",
 "sit_bed", "sit_bed_blink", "sit_read", "sit_read_blink", "sit_read_happy", "bed_phone_blink", "stretch", "wave_off", "sad", "sad_blink", "shake0", "shake1", "cshake0", "cshake1", "crouch", "jump", "lookup", "bed_phone", "bed_yawn", "bed_phone_blink"].forEach(function (n) { LIST["c_" + n] = "../pixel-book/art/chars/" + n + ".png"; });
var READY = Promise.all(Object.keys(LIST).map(function (k) { return new Promise(function (res) { var i = new Image(); i.onload = function () { A[k] = i; res(); }; i.onerror = function () { console.error("missing " + LIST[k]); res(); }; i.src = LIST[k]; }); }));

// ---------- math ----------
function cl(v, a, b) { return Math.max(a, Math.min(b, v)); }
function seg(t, a, b) { return cl((t - a) / (b - a), 0, 1); }
function lerp(a, b, k) { return a + (b - a) * k; }
function eio(k) { return k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; }
function eout(k) { return 1 - Math.pow(1 - k, 3); }
function hash(i) { var x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
var BAY = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5];
function bay(x, y) { return (BAY[(x & 3) + (y & 3) * 4] + .5) / 16; }

// ---------- camera ----------
function camAt(keys, t) {
  if (t <= keys[0][0]) return { x: keys[0][1], y: keys[0][2], z: keys[0][3] };
  for (var i = 1; i < keys.length; i++) {
    var k0 = keys[i - 1], k1 = keys[i], ts = k1[4] != null ? k1[0] - k1[4] : k0[0];
    if (t < k1[0]) { var k = t < ts ? 0 : eio(seg(t, ts, k1[0])); return { x: lerp(k0[1], k1[1], k), y: lerp(k0[2], k1[2], k), z: lerp(k0[3], k1[3], k) }; }
  }
  var L = keys[keys.length - 1]; return { x: L[1], y: L[2], z: L[3] };
}
function blit(cam, dx, dy, dw, dh, ctx, src) {
  src = src || LB[0]; var sw = W / cam.z, sh = H / cam.z;
  var sx = cl(cam.x - sw / 2, 0, Math.max(0, W - sw)), sy = cl(cam.y - sh / 2, 0, Math.max(0, H - sh));
  sx = Math.round(sx * cam.z * 4) / (cam.z * 4); sy = Math.round(sy * cam.z * 4) / (cam.z * 4);
  ctx.imageSmoothingEnabled = false; ctx.drawImage(src, sx, sy, sw, sh, dx, dy, dw, dh);
}

// ---------- low-res drawing helpers (L = LB context) ----------
var L = LB[1];
function img(n, x, y, flip, sx, sy) {
  var i = A[n]; if (!i) return; sx = sx == null ? 1 : sx; sy = sy == null ? sx : sy;
  L.save(); L.translate(Math.round(x), Math.round(y)); if (flip) { L.translate(Math.round(i.width * sx), 0); L.scale(-1, 1); }
  L.drawImage(i, 0, 0, Math.max(1, Math.round(i.width * sx)), Math.max(1, Math.round(i.height * sy))); L.restore();
}
function rect(x, y, w, h, c) { L.fillStyle = c; L.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h)); }
function ddisc(cx, cy, r, c, a, ctx) {           // dithered glow disc (crisp pixels, no blur)
  ctx = ctx || L; ctx.fillStyle = c; cx = Math.round(cx); cy = Math.round(cy); var R = Math.ceil(r);
  for (var y = -R; y <= R; y++) for (var x = -R; x <= R; x++) { var d = Math.sqrt(x * x + y * y) / r; if (d > 1) continue; if (bay(cx + x, cy + y) < a * (1 - d * d)) ctx.fillRect(cx + x, cy + y, 1, 1); }
}
function spark(x, y, c, big) { rect(x, y, 1, 1, c); if (big) { rect(x - 1, y, 1, 1, c); rect(x + 1, y, 1, 1, c); rect(x, y - 1, 1, 1, c); rect(x, y + 1, 1, 1, c); } }

// ---------- pixel font 5x7 ----------
var F = {":":"00000011000110000000011000110000000","#":"01010010101111101010111110101001010","\"":"01010010100000000000000000000000000",A:"01110100011000111111100011000110001",B:"11110100011000111110100011000111110",C:"01110100011000010000100001000101110",D:"11110100011000110001100011000111110",
E:"11111100001000011110100001000011111",F:"11111100001000011110100001000010000",G:"01110100011000010111100011000101111",H:"10001100011000111111100011000110001",
I:"01110001000010000100001000010001110",J:"00111000100001000010000101001001100",K:"10001100101010011000101001001010001",L:"10000100001000010000100001000011111",
M:"10001110111010110101100011000110001",N:"10001100011100110101100111000110001",O:"01110100011000110001100011000101110",P:"11110100011000111110100001000010000",
Q:"01110100011000110001101011001001101",R:"11110100011000111110101001001010001",S:"01111100001000001110000010000111110",T:"11111001000010000100001000010000100",
U:"10001100011000110001100011000101110",V:"10001100011000110001100010101000100",W:"10001100011000110101101011010101010",X:"10001100010101000100010101000110001",
Y:"10001100010101000100001000010000100",Z:"11111000010001000100010001000011111","0":"01110100011001110101110011000101110","1":"00100011000010000100001000010001110",
"2":"01110100010000100010001000100011111","3":"11110000010000101110000010000111110","4":"00010001100101010010111110001000010","5":"11111100001111000001000011000101110",
"6":"00110010001000011110100011000101110","7":"11111000010001000100010000100001000","8":"01110100011000101110100011000101110","9":"01110100011000101111000010001001100",
".":"00000000000000000000000000110001100",",":"00000000000000000000011000010001000",":":"00000011000110000000011000110000000","'":"00100001000100000000000000000000000",
"?":"01110100010000100010001000000000100","!":"00100001000010000100001000000000100","-":"00000000000000011111000000000000000","@":"01110100011011110101101111000001110",
"/":"00001000100001000100010000100010000"," ":"00000000000000000000000000000000000"};
function glyph(ctx, ch, x, y, b, c) { var g = F[ch] || F[" "]; ctx.fillStyle = c; for (var i = 0; i < 35; i++) if (g[i] === "1") ctx.fillRect(x + (i % 5) * b, y + Math.floor(i / 5) * b, b, b); }
function ptext(ctx, s, x, y, b, c) { for (var i = 0; i < s.length; i++) glyph(ctx, s[i], x + i * 6 * b, y, b, c); }
function pwidth(s, b) { return s.length * 6 * b - b; }

// screen-level caption: *word* = accent. Letters type on, shadowed, pixel blocks of 8 px (= 2 art px).
function caption(t, s, a, b, opt) {
  opt = opt || {}; if (t < a || t > b) return; var B = opt.b || 8, y0 = opt.y || 230, maxc = Math.floor((OW - 96) / (6 * B));
  var words = [], acc = false; s.split(" ").forEach(function (w) { var st = w[0] === "*", en = w[w.length - 1] === "*" || w.slice(-2) === "*." || w.slice(-2) === "*?"; if (st) acc = true; words.push([w.replace(/\*/g, ""), acc]); if (en) acc = false; });
  var lines = [[]], len = 0; words.forEach(function (w) { if (len + w[0].length > maxc && len) { lines.push([]); len = 0; } lines[lines.length - 1].push(w); len += w[0].length + 1; });
  var shown = Math.floor((t - a) * 45), n = 0;
  lines.forEach(function (ln, li) {
    var str = ln.map(function (w) { return w[0]; }).join(" "), x = Math.round((OW - pwidth(str, B)) / 2), y = y0 + li * 11 * B;
    ln.forEach(function (w) {
      for (var i = 0; i < w[0].length; i++) { if (n++ >= shown) return; [[B, B], [B, 0], [-B, 0], [0, B], [0, -B], [B, -B], [-B, B], [-B, -B]].forEach(function (o) { glyph(X, w[0][i], x + o[0], y + o[1], B, "#1A1530"); }); glyph(X, w[0][i], x, y, B, w[1] ? (opt.accent || "#FFC145") : "#FFFFFF"); x += 6 * B; }
      n++; x += 6 * B;
    });
  });
}

// ---------- in-world choice sign ----------
function sign(label, cx, y, t, tPop, tPick, picked, tOut) {
  if (t < tPop || (tOut && t > tOut)) return; var k = eout(seg(t, tPop, tPop + .25)), w = label.length * 6 + 7, x = Math.round(cx - w / 2), yy = Math.round(y - (1 - k) * 10);
  var done = t >= tPick, col = done ? (picked ? "#28A86A" : "#6B6F80") : "#C98A4E", edge = done ? (picked ? "#1C7A4C" : "#4A4D5C") : "#8A5228";
  if (done && picked) { var p0 = eout(seg(t, tPick, tPick + .25)); ddisc(cx, yy + 6, 18 * p0, "#FFE9A0", .35 * (1 - seg(t, tPick + .3, tPick + .9))); }
  rect(x + w / 2 - 1, yy + 12, 2, 10, "#6B4430");
  rect(x - 1, yy - 1, w + 2, 14, "#2A1F2E"); rect(x, yy, w, 12, col); rect(x, yy + 10, w, 2, edge);
  ptext(L, label, x + 4, yy + 2, 1, done && !picked ? "#A8ABB8" : "#FFFFFF");
  if (done && picked) { var p = eout(seg(t, tPick, tPick + .25)); if (p > 0) { rect(x + w + 2, yy + 4, 2, 2, "#FFFFFF"); rect(x + w + 4, yy + 6, 2, 2, "#FFFFFF"); rect(x + w + 6, yy + 2, 2, 4, "#FFFFFF"); } }
  if (done && !picked) { rect(x, yy + 5, w, 1, "#4A4D5C"); }
}
function chr(n, x, y, flip) { img("c_" + n, x, y, flip); }      // character sprite 48x56, feet at y+53
var GY = 53;


// =================== pixel-series helpers (TL from timeline.js is loaded first) ===================
var DUR = TL.total, SCN = TL.scenes;
function LN(k, i) { for (var j = 0; j < TL.lines.length; j++) { var l = TL.lines[j]; if (l[0] === k && l[1] === i) return l[2]; } return 0; }
function LE(k, i) { for (var j = 0; j < TL.lines.length; j++) { var l = TL.lines[j]; if (l[0] === k && l[1] === i) return l[3]; } return 0; }
function blinkAt(t, off) { return ((t + off) % 3.3) < .12; }
function stars(t, n, col) { for (var i = 0; i < n; i++) if ((t * 1.3 + hash(i + 5)) % 1 > .25) rect(hash(i) * W, hash(i + 300) * H, 1, hash(i + 9) > .9 ? 2 : 1, col || (i % 4 ? "#FFFFFF" : "#8C8FC8")); }
function bar(x, y, w, v, label) {         // motivation-style meter
  rect(x - 1, y - 1, w + 2, 10, "#2A1F2E"); rect(x, y, w, 8, "#3A3560"); var c = v > .6 ? "#28A86A" : (v > .3 ? "#FFC145" : "#E0453A"); rect(x, y, Math.round(w * cl(v, 0, 1)), 8, c); rect(x, y, Math.round(w * cl(v, 0, 1)), 2, "#FFFFFF");
  if (label) ptext(L, label, x, y - 9, 1, "#FFFFFF"); var pct = Math.round(v * 100) + "%"; ptext(L, pct, x + w + 4, y + 1, 1, c);
}
function calendarGrid(x, y, cols, rows, cw, ch, cellFn) {   // wall calendar: cellFn(i, cx, cy) draws marks
  rect(x - 2, y - 12, cols * cw + 4, rows * ch + 16, "#2A1F2E"); rect(x - 1, y - 11, cols * cw + 2, 9, "#E0453A"); rect(x - 1, y - 2, cols * cw + 2, rows * ch + 4, "#FFF4E0");
  for (var r = 0; r < rows; r++) for (var c = 0; c < cols; c++) { var cx = x + c * cw, cy = y + r * ch; rect(cx, cy, cw - 1, ch - 1, "#F2E6CC"); cellFn && cellFn(r * cols + c, cx, cy, c, r); }
}
function redX(cx, cy, s) { for (var i = 0; i < s; i++) { rect(cx + i, cy + i, 2, 1, "#E0453A"); rect(cx + s - i - 1, cy + i, 2, 1, "#E0453A"); } }
function tick(cx, cy, col) { col = col || "#28A86A"; rect(cx, cy + 3, 2, 2, col); rect(cx + 2, cy + 5, 2, 2, col); rect(cx + 4, cy + 3, 2, 2, col); rect(cx + 6, cy + 1, 2, 2, col); rect(cx + 8, cy - 1, 2, 2, col); }
// series-question scene (Reason card sits on top as EP.titles): night sky, Kabir looking up, a floating "?"
function whyScene(u, a, b) {
  rect(0, 0, W, H, "#140F2E"); stars(u, 70);
  var k = eout(seg(u, a + .1, a + .6)); img(blinkAt(u, .2) ? "c_blink" : "c_lookup", 87, 298 + (1 - k) * 8, false, 2);
  if (u > a + .3) ptext(L, "?", 178, 282 - 3 * Math.sin(u * 3), 4, "#FFC145");
  return { x: 135, y: 240, z: 1 + .04 * seg(u, a, b) };
}
function dayTag(lab, x, y, bg, fg) { var bw = pwidth(lab, 3) + 10; rect(x, y, bw, 32, "#2A1F2E"); rect(x + 1, y + 1, bw - 2, 30, bg || "#FFC145"); ptext(L, lab, x + 5, y + 6, 3, fg || "#1A1530"); }
function bubble(x, y, w, h, tail) { rect(x - 1, y - 1, w + 2, h + 2, "#2A1F2E"); rect(x, y, w, h, "#FFFFFF"); if (tail) { rect(tail - 2, y + h, 5, 2, "#FFFFFF"); rect(tail - 1, y + h + 2, 3, 2, "#FFFFFF"); rect(tail, y + h + 4, 1, 2, "#FFFFFF"); } }
// month grid: cells[i] = "tick" | "x" | "grey" | "now" | null; letters on the red header
function monthGrid(x, y, cells, rows, k) {
  rows = rows || 5; k = k == null ? 1 : k; var n = Math.floor(cells.length * k + .0001);
  calendarGrid(x, y, 7, rows, 14, 12, function (i, cx, cy) { if (i >= n) return; var s = cells[i];
    if (s === "tick") tick(cx + 1, cy + 4); else if (s === "x") redX(cx + 3, cy + 2, 7); else if (s === "grey") { rect(cx, cy, 13, 11, "#CFC6B4"); rect(cx + 3, cy + 5, 7, 1, "#A89F8C"); }
    else if (s === "now") { rect(cx, cy, 13, 11, "#FFE066"); rect(cx, cy, 13, 1, "#E0453A"); } });
  "MTWTFSS".split("").forEach(function (d, j) { ptext(L, d, x + j * 14 + 4, y - 10, 1, "#FFFFFF"); });
}
// line chart: series = [{pts: [0..1], col, k (0..1 drawn)}]
function lineChart(x, y, w, h, series, title) {
  rect(x - 1, y - 1, w + 2, h + 2, "#2A1F2E"); rect(x, y, w, h, "#FFF4E0"); if (title) ptext(L, title, x + 5, y + 4, 1, "#3A3560");
  var gx = x + 8, gy = y + h - 8, gw = w - 16, gh = h - (title ? 22 : 14); rect(gx, gy - gh, 1, gh, "#3A3560"); rect(gx, gy, gw, 1, "#3A3560");
  series.forEach(function (s) { var p = s.pts, m = p.length - 1, kk = s.k == null ? 1 : s.k;
    for (var t = 0; t <= kk; t += .004) { var f = t * m, i = Math.min(m - 1, Math.floor(f)), r = f - i, v = lerp(p[i], p[i + 1], r); rect(gx + t * gw, gy - 2 - v * (gh - 4), 2, 2, s.col); } });
  return { gx: gx, gy: gy, gw: gw, gh: gh };
}
// in-world sign card with 1-3 centred lines
function signCard(cx, y, lines, bg, fg, b, k) {
  b = b || 2; k = k == null ? 1 : eout(k); if (k <= 0) return; var w = 0; lines.forEach(function (l) { w = Math.max(w, pwidth(l, b)); }); w += 12 * b / 2 + 8; var h = lines.length * 10 * b + 8;
  L.save(); L.translate(cx, y + h / 2); L.scale(k, k); L.translate(-w / 2, -h / 2);
  L.fillStyle = "#1A1530"; L.fillRect(-1, -1, w + 2, h + 3); L.fillStyle = bg || "#FFC145"; L.fillRect(0, 0, w, h);
  lines.forEach(function (l, i) { ptext(L, l, Math.round((w - pwidth(l, b)) / 2), 5 + i * 10 * b, b, fg || "#1A1530"); }); L.restore();
}
function floorRoom(wall, wall2, floor) { rect(0, 0, W, H, wall); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, wall2); rect(0, 380, W, H - 380, floor || "#6B4430"); for (var j = 0; j < 6; j++) rect(0, 392 + j * 14, W, 1, "#5A3826"); }
function sofaAt(x) { rect(x - 2, 326, 100, 54, "#2A1F2E"); rect(x, 328, 96, 26, "#C2566A"); rect(x, 352, 96, 18, "#A8434F"); rect(x - 2, 340, 12, 40, "#8E3644"); rect(x + 86, 340, 12, 40, "#8E3644"); }
var STRAIGHT = { badgeBg: "#6CC7A3", badgeFg: "#1A1530" }, STORY = { badgeBg: "#B07CFF", badgeFg: "#FFFFFF" };
var ROAST = { badgeBg: "#E0453A", badgeFg: "#FFFFFF" };
// big counter readout: label + number (b px blocks) inside a dark chip
function counter(x, y, label, num, col, b) { b = b || 3; var w = Math.max(pwidth(num, b), pwidth(label, 1)) + 12; rect(x - 1, y - 1, w + 2, 12 + 8 * b + 2, "#1A1530"); rect(x, y, w, 12 + 8 * b, "#2A2245"); ptext(L, label, x + 6, y + 3, 1, "#B8B0D8"); ptext(L, num, x + 6, y + 11, b, col || "#FFFFFF"); return w; }
function mat(x, y, w) { rect(x, y, w, 5, "#2A1F2E"); rect(x + 1, y, w - 2, 3, "#4C9AFF"); }
function plateIcon(x, y) { ell2(x, y, 9, "#FFFFFF"); ell2(x, y, 6, "#E9E4D0"); rect(x - 3, y - 2, 6, 4, "#6CC7A3"); rect(x - 12, y - 6, 1, 12, "#C8C0E8"); rect(x + 12, y - 6, 1, 12, "#C8C0E8"); }
function ell2(cx, cy, r, c) { for (var y = -r; y <= r; y++) { var w = Math.round(Math.sqrt(r * r - y * y)); rect(cx - w, cy + y, w * 2 + 1, 1, c); } }
