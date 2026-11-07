// =================== KABIR VS. KABIR #7: "As soon as he's ready" (Reason #11: waiting to feel ready) ===================
function mic(x, y) { rect(x - 1, y + 14, 3, 18, "#2A1F2E"); rect(x - 7, y + 32, 15, 3, "#2A1F2E"); rect(x - 5, y - 1, 11, 16, "#1A1530"); rect(x - 4, y, 9, 14, "#8A8498"); for (var i = 0; i < 4; i++) rect(x - 3, y + 2 + i * 3, 7, 1, "#5A5470"); }
function camera(x, y) { rect(x - 1, y + 14, 2, 22, "#2A1F2E"); rect(x - 10, y + 34, 20, 2, "#2A1F2E"); rect(x - 14, y, 28, 16, "#1A1530"); rect(x - 13, y + 1, 26, 14, "#3A3560"); circ2(x + 2, y + 8, 5); rect(x - 10, y - 3, 8, 3, "#1A1530"); }
function circ2(cx, cy, r) { for (var y = -r; y <= r; y++) { var w = Math.round(Math.sqrt(r * r - y * y)); rect(cx - w, cy + y, w * 2 + 1, 1, y < 0 ? "#7FD4FF" : "#2A6AA0"); } }
function lamp(x, y) { rect(x - 1, y + 12, 2, 40, "#2A1F2E"); rect(x - 8, y + 50, 16, 2, "#2A1F2E"); rect(x - 10, y, 20, 13, "#1A1530"); rect(x - 9, y + 1, 18, 11, "#FFF4E0"); }
function course(x, y) { rect(x, y, 30, 20, "#1A1530"); rect(x + 1, y + 1, 28, 18, "#E0453A"); ptext(L, "LIGHT", x + 3, y + 4, 1, "#FFFFFF"); ptext(L, "101", x + 7, y + 11, 1, "#FFE066"); }
function board(x, y, vids) { x = 60; y = 168; rect(x - 2, y - 2, 154, 52, "#1A1530"); rect(x, y, 150, 48, "#FFFFFF"); rect(x, y, 150, 12, "#E0453A"); ptext(L, "MY CHANNEL", x + 75 - pwidth("MY CHANNEL", 1) / 2, y + 3, 1, "#FFFFFF"); ptext(L, "VIDEOS: " + vids, x + 75 - pwidth("VIDEOS: " + vids, 2) / 2, y + 22, 2, "#3A3560"); }
function ready(v) { bar(70, 238, 110, v, "READY"); }
function gear(u, n, dust) {
  if (n > 0) mic(170, 332); if (n > 1) camera(205, 330); if (n > 2) lamp(238, 314); if (n > 3) course(120, 360);
  if (dust) { L.fillStyle = "rgba(200,195,215,.5)"; for (var i = 0; i < 70; i++) L.fillRect(Math.round(110 + hash(i) * 150), Math.round(310 + hash(i + 3) * 70), 1, 1);
    for (var c = 0; c < 6; c++) { rect(250 - c * 3, 296 + c * 3, 3, 1, "#C8C0D8"); rect(250 + c, 296 + c * 4, 1, 3, "#C8C0D8"); } }
}
// S1: the channel board says zero; readiness is "almost" (frame 0)
function sBoard(u, a, b) { floorRoom("#3B3A6A", "#34335E"); board(130, 150, 0); ready(.12 + .1 * seg(u, 1, b)); chr(blinkAt(u, .4) ? "blink" : "stand", 30, 327); return camAt([[0, 135, 250, 1.3], [b, 135, 265, 1.3, b]], u); }
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: mic, camera, lights, a course about lights
function sGear(u, a, b) {
  floorRoom("#3B3A6A", "#34335E"); board(130, 150, 0); var t = [LN("S3", 0), LN("S3", 1), LN("S3", 1) + (LE("S3", 1) - LN("S3", 1)) * .55, LN("S3", 2)], n = 0; t.forEach(function (x) { if (u > x + .1) n++; });
  gear(u, n, false); ready([.22, .45, .62, .78, .88][n]); chr(blinkAt(u, .4) ? "blink" : "stand", 30, 327);
  return camAt([[a, 135, 265, 1.3], [b, 138, 268, 1.32, b - a]], u);
}
// S4: two years later: 99% ready, zero videos, everything dusty
function sYears(u, a, b) {
  floorRoom("#34335E", "#2E2D55"); board(130, 150, 0); gear(u, 4, true); ready(.99); chr(blinkAt(u, .3) ? "sad_blink" : "sad", 30, 327);
  if (u < LN("S4", 1)) signCard(135, 120, ["2 YEARS LATER"], "#FFFFFF", "#1A1530", 2);
  return camAt([[a, 135, 265, 1.3], [b, 135, 255, 1.4, b - a]], u);
}
// S5: the order is backwards
function chip(x, y, s, col) { var w = pwidth(s, 2) + 14; rect(x - 1, y - 1, w + 2, 24, "#1A1530"); rect(x, y, w, 22, col); ptext(L, s, x + 7, y + 4, 2, "#FFFFFF"); return w; }
function arrow(x, y) { rect(x, y + 10, 14, 2, "#FFFFFF"); rect(x + 10, y + 7, 2, 8, "#FFFFFF"); rect(x + 12, y + 8, 2, 6, "#FFFFFF"); }
function sOrder(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 25, "#5A5590"); var k = LN("S5", 1);
  var w1 = chip(50, 180, "READY", "#8A8498"); arrow(50 + w1 + 6, 180); chip(50 + w1 + 26, 180, "START", "#8A8498"); if (u > k + .3) { rect(44, 191, 210 * eout(seg(u, k + .3, k + .7)), 2, "#E0453A"); }
  if (u > k + .9) { var s = eout(seg(u, k + .9, k + 1.3)); L.save(); L.translate(135, 262); L.scale(s, s); L.translate(-135, -262);
    var w2 = chip(50, 250, "START", "#28A86A"); arrow(50 + w2 + 6, 250); chip(50 + w2 + 26, 250, "READY", "#28A86A"); L.restore(); }
  return camAt([[a, 135, 230, 1.15], [b, 135, 235, 1.2, b - a]], u);
}
// S6: one video, on a phone, in bad light
function sFilm(u, a, b) {
  rect(0, 0, W, H, "#1E1A33"); rect(0, 380, W, H - 380, "#3A2A22"); ddisc(130, 120, 50, "#FFE9A0", .18); rect(129, 0, 2, 104, "#2A1F2E"); rect(125, 104, 10, 8, "#FFE9A0");
  chr("stand", 100, 327); rect(190, 350, 34, 30, "#4C9AFF"); rect(190, 340, 34, 10, "#E0453A"); rect(204, 322, 8, 18, "#1A1530"); rect(205, 323, 6, 16, "#3A3560");
  if (Math.floor(u * 2) % 2) { rect(206, 316, 4, 4, "#E0453A"); } ptext(L, "REC", 214, 316, 1, "#E0453A");
  var bad = u > LN("S6", 1) - .1, one = u > LN("S6", 2);
  if (bad && !one) signCard(150, 236, ["AUDIO: BAD", "LIGHT: WORSE"], "#FFFFFF", "#E0453A", 1, seg(u, LN("S6", 1) - .1, LN("S6", 1) + .2));
  if (one) signCard(150, 236, ["VIDEO #1"], "#28A86A", "#FFFFFF", 2, seg(u, LN("S6", 2), LN("S6", 2) + .3));
  return camAt([[a, 150, 300, 1.6], [b, 150, 290, 1.7, b - a]], u);
}
// S7: the counter moves (loops to the board)
function sCount(u, a, b) { floorRoom("#3B3A6A", "#34335E"); board(0, 0, Math.max(1, Math.round(12 * eio(seg(u, a, a + 1.6))))); gear(u, 2, false); chr(Math.floor(u * 3) % 2 ? "jump" : "stand", 30, 327); return camAt([[a, 135, 265, 1.3], [b, 135, 250, 1.3, b - a]], u); }

var SCENES = [["S1", sBoard], ["S2", sWhy], ["S3", sGear], ["S4", sYears], ["S5", sOrder], ["S6", sFilm], ["S7", sCount]];
var EP = {
  badge: "KABIR VS. KABIR #7", hook: "ALMOST *READY.*", hookEnd: LN("S1", 1) + .4,
  endAt: function () { return LN("S7", 0); }, endQ: "WHAT ARE YOU STILL GETTING *READY* FOR?",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #11", LN("S2", 1), SCN.S2[1], 860, 14],
           ["WAITING TO FEEL *READY.*", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["READY COMES *AFTER* YOU START.", LN("S5", 1), SCN.S5[1], 300, 8]]
};
