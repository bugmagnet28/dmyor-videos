// =================== KABIR VS. KABIR #11: always from the top (practise the broken bar) ===================
function guitar(x, y, rot, s) {
  L.save(); L.translate(x, y); L.rotate(rot || 0); L.scale(s || 1, s || 1);
  rect(-3, -46, 6, 34, "#2A1F2E"); rect(-2, -46, 4, 34, "#8A5228"); rect(-4, -52, 8, 7, "#2A1F2E"); rect(-3, -51, 6, 5, "#6B4430");
  rect(-12, -14, 24, 30, "#2A1F2E"); rect(-14, -6, 28, 22, "#2A1F2E"); rect(-11, -13, 22, 28, "#E08A3A"); rect(-13, -5, 26, 20, "#E08A3A"); rect(-11, 10, 22, 4, "#C26A22");
  rect(-4, -3, 8, 8, "#2A1F2E"); for (var i = -1; i <= 1; i++) rect(i * 2, -46, 1, 56, "#FFF4E0"); L.restore();
}
function strip(u, state, y) {        // 16 bars; state(i) -> "ok" | "bad" | "todo" | "gold" | "out"
  for (var i = 0; i < 16; i++) { var r = Math.floor(i / 8), c = i % 8, x = 16 + c * 30, yy = y + r * 40, s = state(i); if (s === "out") continue;
    rect(x, yy, 28, 34, "#1A1530"); rect(x + 1, yy + 1, 26, 32, s === "bad" ? "#5A2A2E" : (s === "gold" ? "#C9902E" : "#FFF4E0"));
    for (var l = 0; l < 5; l++) rect(x + 3, yy + 8 + l * 4, 22, 1, s === "bad" ? "#8E3644" : "#B8B0C8");
    ptext(L, "" + (i + 1), x + 3, yy + 2, 1, s === "bad" ? "#FF9F94" : "#3A3560");
    if (s === "ok") { L.save(); L.translate(x + 15, yy + 24); tick(0, 0, "#28A86A"); L.restore(); } if (s === "bad") redX(x + 9, yy + 20, 10); }
}
function player(u, x, y) { chr("sit_bed", x, y); guitar(x + 30, y + 34, -1.1, .8); }
function room(u) { rect(0, 0, W, H, "#2A2245"); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, "#262040"); rect(0, 380, W, H - 380, "#3A3560"); rect(20, 352, 80, 28, "#8A5228"); }
var BASE = function (i) { return i < 11 ? "ok" : (i === 11 ? "bad" : "todo"); };
// S1: forty run-throughs from the top; bar 12 still broken (frame 0)
function sHook(u, a, b) { room(u); strip(u, BASE, 172); player(u, 34, 302); counter(150, 284, "FROM THE TOP", "40X", "#FFC145", 3); return camAt([[0, 135, 255, 1.12], [b, 135, 258, 1.15, b]], u); }
// S2: bar twelve, a crime scene
function sCrime(u, a, b) {
  room(u); strip(u, BASE, 172); player(u, 34, 302);
  if (u > LN("S2", 1)) { var x = 16 + 3 * 30, y = 212; for (var s = 0; s < 40; s++) rect(x - 10 + s, y - 6 + ((s / 4) % 2 ? 0 : 0), 1, 4, Math.floor(s / 4) % 2 ? "#FFC145" : "#1A1530"); for (var s2 = 0; s2 < 40; s2++) rect(x - 10 + s2, y + 36, 1, 4, Math.floor(s2 / 4) % 2 ? "#FFC145" : "#1A1530"); }
  return camAt([[a, 135, 255, 1.12], [LN("S2", 1), 120, 232, 2.2, .6], [b, 120, 232, 2.3, b - LN("S2", 1)]], u);
}
// S3: the maths: 40 tries at bar 12, 440 at what he already knows
function sMath(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 20, "#5A5590"); var k = eio(seg(u, LN("S3", 1), LE("S3", 1) - .4));
  rect(50, 330 - 160 * k, 60, 160 * k, "#28A86A"); rect(160, 330 - 160 * k * 40 / 440, 60, 160 * k * 40 / 440, "#E0453A");
  ptext(L, "" + Math.round(440 * k), 80 - pwidth("" + Math.round(440 * k), 2) / 2, 316 - 160 * k, 2, "#B8F5C8"); ptext(L, "" + Math.round(40 * k), 190 - pwidth("" + Math.round(40 * k), 2) / 2, 316 - 160 * k * 40 / 440, 2, "#FF9F94");
  ptext(L, "BARS 1-11", 80 - pwidth("BARS 1-11", 1) / 2, 338, 1, "#FFFFFF"); ptext(L, "BAR 12", 190 - pwidth("BAR 12", 1) / 2, 338, 1, "#FFFFFF");
  return camAt([[a, 135, 250, 1.2], [b, 135, 250, 1.25, b - a]], u);
}
// S4: the broken bar alone, slowly, ten times; then stitched back in
function sFix(u, a, b) {
  room(u); var st = LN("S4", 1), back = eio(seg(u, st, st + 1));
  strip(u, function (i) { return i === 11 ? "out" : (i < 11 ? "ok" : "todo"); }, 172);
  var reps = Math.min(10, Math.floor(seg(u, a + .5, st) * 10.99)), x = lerp(120, 16 + 3 * 30, back), y = lerp(262, 212, back);
  rect(x, y, 28, 34, "#1A1530"); rect(x + 1, y + 1, 26, 32, reps >= 10 ? "#FFF4E0" : "#5A2A2E"); ptext(L, "12", x + 3, y + 2, 1, "#3A3560"); if (reps >= 10) { L.save(); L.translate(x + 15, y + 24); tick(0, 0, "#28A86A"); L.restore(); }
  if (back < .1) { counter(160, 262, "SLOW REPS", reps + "/10", "#B8F5C8", 2); ptext(L, "60 BPM", 60, 274, 1, "#FFE066"); }
  player(u, 34, 302);
  return camAt([[a, 135, 255, 1.12], [b, 135, 258, 1.15, b - a]], u);
}
// S5: a week later, bar 12 is the best part (loops to the strip)
function sEnd(u, a, b) { room(u); strip(u, function (i) { return i === 11 ? "gold" : "ok"; }, 172); player(u, 34, 302); counter(116, 284, "BAR 12", "BEST PART", "#FFC145", 2); return camAt([[a, 135, 258, 1.15], [b, 135, 255, 1.12, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sCrime], ["S3", sMath], ["S4", sFix], ["S5", sEnd]];
var EP = {
  badge: "KABIR VS. KABIR #11", hook: "FROM THE TOP, 40X. *BAR 12: BROKEN.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S5", 2); }, endQ: "WHAT'S YOUR *BAR 12?*",
  titles: [["BAR 12: A *CRIME SCENE.*", LN("S2", 1), SCN.S2[1], 300, 9],
           ["SEND TO THE FRIEND WHO ALWAYS *STARTS FROM THE TOP.*", LN("S5", 1), LN("S5", 2), 300, 7]]
};
