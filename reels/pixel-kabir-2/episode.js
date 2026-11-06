// =================== KABIR VS. KABIR #2: "The gym membership" (Reason #2: it turns into a daily decision, and your mood makes it) ===================
// Stage: dark room, spotlight, pedestal with the gym card. Street: the shop art (awning y ~160-180, door x 160-230, street from y ~378) turned into a gym.

function cone(cx, top, bot, w0, w1, col, al) {   // dithered spotlight cone
  L.fillStyle = col; for (var y = top; y < bot; y++) { var k = (y - top) / (bot - top), hw = lerp(w0, w1, k) / 2; for (var x = Math.round(cx - hw); x < cx + hw; x++) if (bay(x, y) < al) L.fillRect(x, y, 1, 1); }
}
function stage(u) { rect(0, 0, W, H, "#1A1530"); cone(135, 0, 380, 30, 150, "#FFE9A0", .18); rect(0, 380, W, H - 380, "#2A2245"); ddisc(135, 384, 70, "#FFE9A0", .25); }
function pedestal() { rect(91, 288, 88, 8, "#2A1F2E"); rect(92, 289, 86, 6, "#E9E4FF"); rect(110, 296, 50, 84, "#2A1F2E"); rect(111, 296, 48, 84, "#C8C0E8"); rect(111, 296, 8, 84, "#FFFFFF"); rect(150, 296, 9, 84, "#9A92C0"); }
function gymCard(u, x, y, wear, dust) {        // wear 0..1 (scuffs, bent corner), dust 0..1 (grey film, cobweb)
  rect(x - 1, y - 1, 82, 40, "#1A1530"); rect(x, y, 80, 38, "#3A6FD8"); rect(x, y + 8, 80, 6, "#FFC145"); rect(x + 6, y + 20, 10, 8, "#FFE066"); rect(x + 7, y + 22, 8, 1, "#C99A2E"); rect(x + 7, y + 25, 8, 1, "#C99A2E");
  ptext(L, "GYM PASS", x + 4, y + 1, 1, "#FFFFFF"); ptext(L, "12 MONTHS", x + 21, y + 20, 1, "#FFFFFF"); ptext(L, "PAID", x + 21, y + 29, 1, "#B8F5C8");
  if (!wear && !dust) { var s = ((u * .5) % 1.6) * 110 - 20; for (var i = 0; i < 38; i++) { var sx = Math.round(x + s - i * .5); if (sx > x && sx < x + 78) rect(sx, y + i, 3, 1, "rgba(255,255,255,.55)"); } }
  if (dust) { L.fillStyle = "rgba(170,165,190," + (.75 * dust) + ")"; for (var yy = 0; yy < 38; yy++) for (var xx = 0; xx < 80; xx++) if (bay(xx + x, yy + y) < .45) L.fillRect(x + xx, y + yy, 1, 1);
    for (var c = 0; c < 6; c++) { rect(x + 80 - c * 3, y - 18 + c * 3, 3, 1, "#D8D4E8"); rect(x + 80 + c, y - 18 + c * 4, 1, 3, "#D8D4E8"); } }
  if (wear) { for (var j = 0; j < 7; j++) rect(x + 4 + hash(j) * 70, y + 4 + hash(j + 9) * 30, 4 + hash(j + 3) * 8, 1, "#24479A"); rect(x + 72, y, 8, 8, "#1A1530"); rect(x + 72, y, 7, 7, "#7FA4F0"); rect(x + 72, y + 7, 8, 1, "#24479A"); }
}
function confetti(u, t0, cx, cy) { if (u < t0) return; var k = u - t0; for (var i = 0; i < 40; i++) { var vx = (hash(i) - .5) * 120, vy = -60 - hash(i + 7) * 70, x = cx + vx * k, y = cy + vy * k + 90 * k * k; if (y < H) rect(x, y, 2, 2, BC[i % BC.length]); } }
var BC = ["#FF7A59", "#FFC145", "#6CC7A3", "#4C9AFF", "#B07CFF", "#FF9FC2"];
function gymFront(u, rain) {
  img("shop", 0, 0); rect(70, 136, 130, 26, "#2A1F2E"); rect(71, 137, 128, 24, "#E0453A"); ptext(L, "GYM", 135 - pwidth("GYM", 3) / 2, 140, 3, "#FFFFFF");
  rect(40, 250, 100, 70, "#3A4570");                                     // window: a rack of dumbbells instead of boxes
  for (var i = 0; i < 4; i++) { var dx = 50 + i * 22; rect(dx, 290, 14, 3, "#C8C0E8"); rect(dx - 2, 286, 4, 11, "#2A1F2E"); rect(dx + 12, 286, 4, 11, "#2A1F2E"); }
  rect(44, 300, 92, 3, "#8A5228");
  if (rain) { L.fillStyle = "rgba(20,15,46,.35)"; L.fillRect(0, 0, W, H); for (var r = 0; r < 70; r++) { var x = (hash(r) * 300 + u * 120) % 300 - 15, y = (hash(r + 50) * 520 + u * 360) % 520 - 20; rect(x, y, 1, 6, "#9FB4E8"); } }
}
function walker(u, t0, t1, x0, x1, mode) {     // Kabir crossing the street to the gym door; disappears inside
  if (u < t0 || u > t1 + .1) return; var k = seg(u, t0, t1), x = lerp(x0, x1, mode === "run" ? eout(k) : k);
  var n = mode === "run" ? (Math.floor(u * 6) % 2 ? "jump" : "walk1") : mode === "drag" ? (blinkAt(u, .1) ? "sad_blink" : "sad") : "walk" + (Math.floor(u * (mode === "slow" ? 5 : 8)) % 4);
  var y = 325 + (mode === "drag" ? 2 : 0); if (mode === "run") ddisc(x + 24, y + 30, 22, "#FFE9A0", .35); chr(n, x, y); if (mode === "drag") rect(x + 34, y + 40, 6, 3, "#E0453A");
}
function chart(u, pts, n) {                    // "EXCITEMENT" line chart, n points shown
  rect(150, 86, 110, 48, "#2A1F2E"); rect(151, 87, 108, 46, "#FFF4E0"); ptext(L, "EXCITEMENT", 156, 89, 1, "#3A3560"); rect(158, 99, 1, 26, "#3A3560"); rect(158, 125, 96, 1, "#3A3560");
  var px = function (i) { return 166 + i * 26; }, py = function (v) { return 123 - v * 22; };
  for (var i = 0; i < n; i++) { if (i > 0) for (var s = 0; s <= 1; s += .05) rect(lerp(px(i - 1), px(i), s), lerp(py(pts[i - 1]), py(pts[i]), s), 2, 2, "#E0453A"); rect(px(i) - 1, py(pts[i]) - 1, 4, 4, "#1A1530"); ptext(L, "" + (i + 1), px(i) - 2, 127, 1, "#3A3560"); }
}
var EXC = [.95, .7, .35, .08];

// S1: the card in the spotlight; Kabir and confetti on "Discipline, purchased"
function sCard(u, a, b) {
  stage(u); pedestal(); gymCard(u, 95, 248 - 2 * Math.sin(u * 2), 0, 0);
  var t2 = LN("S1", 2); if (u > LN("S1", 0) + .3) { var proud = u > t2; chr(proud ? (Math.floor(u * 4) % 2 ? "jump" : "stand") : (blinkAt(u, .4) ? "blink" : "stand"), 180, 327); }
  confetti(u, t2 + .1, 135, 250);
  return camAt([[0, 135, 280, 1.8], [LN("S1", 0) + 1.2, 135, 280, 1.8], [LN("S1", 1) + .5, 150, 290, 1.45, 1.2], [b, 150, 290, 1.5]], u);
}
// S2: the series question
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: day one, two, three at the gym door, excitement falling
function sDays(u, a, b) {
  gymFront(u); var d = u < LN("S3", 1) ? 0 : (u < LN("S3", 2) ? 1 : 2), t0 = LN("S3", d) - .1, t1 = d < 2 ? LN("S3", d + 1) - .3 : b;
  walker(u, t0, t1, -40, 172, ["run", "walk", "drag"][d]); dayTag("DAY " + (d + 1), 36, 92); chart(u, EXC, d + 1);
  return { x: 135, y: 240, z: 1.3 };
}
// S4: day four: shoes on at the door, a question, the sofa wins
function sofa() { rect(16, 326, 100, 54, "#2A1F2E"); rect(18, 328, 96, 26, "#C2566A"); rect(18, 352, 96, 18, "#A8434F"); rect(16, 340, 12, 40, "#8E3644"); rect(104, 340, 12, 40, "#8E3644"); rect(22, 370, 4, 10, "#2A1F2E"); rect(106, 370, 4, 10, "#2A1F2E"); }
function livingRoom(u) {
  rect(0, 0, W, H, "#3B3A6A"); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, "#34335E"); rect(0, 380, W, H - 380, "#6B4430"); for (var j = 0; j < 6; j++) rect(0, 392 + j * 14, W, 1, "#5A3826");
  rect(196, 264, 52, 116, "#2A1F2E"); rect(198, 266, 48, 114, "#8A5228"); rect(204, 274, 36, 40, "#7A4620"); rect(204, 322, 36, 50, "#7A4620"); rect(238, 324, 4, 4, "#FFC145");
  rect(40, 220, 50, 34, "#2A1F2E"); rect(42, 222, 46, 30, "#FFF4E0"); ptext(L, "DAY 4", 51, 232, 1, "#E0453A"); sofa();
}
function sDayFour(u, a, b) {
  livingRoom(u); dayTag("DAY 4", 14, 84, "#E0453A", "#FFFFFF");
  var q = LN("S4", 2), s = LN("S4", 3) + .2;
  if (u < s) chr(blinkAt(u, .3) ? "blink" : "stand", 150, 327); else chr(blinkAt(u, .3) ? "sit_bed_blink" : "sit_bed", 44, 300);
  if (u > q && u < s + .1) { bubble(78, 236, 128, 16, 172); ptext(L, "WHEN DO I GO TODAY?", 82, 241, 1, "#1A1530"); }
  if (u > s + .3) { var k = eout(seg(u, s + .3, s + .6)); bubble(84, 270, 44 * k, 16, 90); if (k > .9) ptext(L, "MEH.", 92, 275, 1, "#1A1530"); }
  return camAt([[a, 160, 300, 1.7], [q, 150, 300, 1.6, 1], [s, 110, 310, 1.7, .6], [b, 100, 310, 1.8, b - s]], u);
}
// S5: the card gathers dust; 3 / 365
function sDust(u, a, b) {
  stage(u); pedestal(); gymCard(u, 95, 248, 0, eio(seg(u, a, a + 1.4)));
  for (var i = 0; i < 18; i++) rect(80 + hash(i) * 110, (200 + hash(i + 4) * 180 - u * 6 * (1 + hash(i))) % 200 + 180, 1, 1, "#D8D4E8");
  var lab = "VISITS: 3 / 365", w = pwidth(lab, 1); rect(135 - w / 2 - 4, 206, w + 8, 15, "#2A1F2E"); ptext(L, lab, 135 - w / 2, 210, 1, "#FFFFFF");
  return camAt([[a, 135, 260, 1.6], [b, 135, 252, 2.0, b - a]], u);
}
// S6: stop asking: three booked slots, a missed one moves instead of disappearing
var DN = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"];
function planner(u, a, b) {
  rect(0, 0, W, H, "#2A2245"); rect(10, 150, 250, 220, "#1A1530"); rect(12, 152, 246, 216, "#FFF4E0");
  for (var i = 0; i < 7; i++) { var x = 16 + i * 34; rect(x, 158, 32, 12, "#3A3560"); ptext(L, DN[i], x + 7, 161, 1, "#FFFFFF"); rect(x, 170, 32, 192, i % 2 ? "#F2E6CC" : "#FBF1DD"); }
  for (var r = 0; r < 6; r++) rect(16, 202 + r * 30, 238, 1, "#E4D6B8");
  var books = [0, 2, 4], t1 = LN("S6", 1), m0 = LN("S6", 2);
  books.forEach(function (d, j) {
    var k = eout(seg(u, t1 + .9 + j * .45, t1 + 1.2 + j * .45)); if (k <= 0) return; var dd = d;
    if (d === 2 && u > m0) dd = lerp(2, 3, eio(seg(u, m0 + 1.0, m0 + 1.6)));
    var x = 16 + dd * 34, y = 206, missed = d === 2 && u > m0 && u < m0 + 1.0;
    L.save(); L.translate(x + 16, y + 14); L.scale(k, k); L.translate(-16, -14);
    rect(0, 0, 32, 28, "#2A1F2E"); rect(1, 1, 30, 26, missed ? "#E0453A" : "#4C9AFF"); ptext(L, "GYM", 7, 5, 1, "#FFFFFF"); ptext(L, "7:00", 4, 16, 1, "#FFFFFF"); L.restore();
  });
  if (u > m0 + 1.6) { ptext(L, "MOVED,", 16 + 3 * 34 - 1, 240, 1, "#28A86A"); ptext(L, "NOT", 16 + 3 * 34 + 7, 250, 1, "#28A86A"); ptext(L, "GONE", 16 + 3 * 34 + 4, 260, 1, "#28A86A"); }
  var qk = seg(u, a + .2, a + .5), cross = u > LN("S6", 0) + .6;
  if (u < t1 + .9) { bubble(70, 116, 130, 16, 0); ptext(L, "WHEN DO I GO TODAY?", 74, 121, 1, "#1A1530"); if (cross) rect(66, 123, 138 * eout(seg(u, LN("S6", 0) + .6, LN("S6", 0) + .9)), 2, "#E0453A"); }
}
function sBook(u, a, b) { planner(u, a, b); return camAt([[a, 135, 236, 1.08], [b, 135, 240, 1.12, b - a]], u); }
// S7: rainy Wednesday, 7:00, not glowing, just there
function sRain(u, a, b) {
  gymFront(u, true); walker(u, a + .2, b - .6, -40, 172, "slow"); dayTag("WED 7:00", 44, 206, "#4C9AFF", "#FFFFFF");
  return camAt([[a, 135, 240, 1.3], [b, 140, 250, 1.4, b - a]], u);
}
// S8: the same card, worn from use (loops to frame 0)
function sWorn(u, a, b) {
  stage(u); pedestal(); gymCard(u, 95, 248 - 2 * Math.sin(u * 2), 1, 0);
  var n = Math.round(lerp(3, 96, eio(seg(u, a + .2, a + 1.6)))), lab = "VISITS: " + n, w = pwidth(lab, 1); rect(135 - w / 2 - 4, 206, w + 8, 15, "#2A1F2E"); ptext(L, lab, 135 - w / 2, 210, 1, "#B8F5C8");
  return camAt([[a, 135, 262, 1.6], [b, 135, 280, 1.8, b - a]], u);
}

var SCENES = [["S1", sCard], ["S2", sWhy], ["S3", sDays], ["S4", sDayFour], ["S5", sDust], ["S6", sBook], ["S7", sRain], ["S8", sWorn]];
var EP = {
  badge: "KABIR VS. KABIR #2", hook: "HE BOUGHT *DISCIPLINE.*", hookEnd: LN("S1", 2) + .4,
  endAt: function () { return LN("S8", 1); }, endQ: "WHAT'S YOUR *DAY FOUR?*",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #2", LN("S2", 1), SCN.S2[1], 860, 14],
           ["IT BECOMES A *DAILY DECISION.*", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["DAY 4 IS WHERE IT *DIES.*", LN("S4", 0), LN("S4", 2), 300, 9],
           ["YOUR *MOOD* DECIDES.", LN("S4", 3), SCN.S4[1], 300, 9],
           ["STOP *ASKING.*", LN("S6", 0), LN("S6", 1), 300, 9],
           ["DECIDED ON *SUNDAY.*", LN("S7", 1), SCN.S7[1], 300, 9]]
};
