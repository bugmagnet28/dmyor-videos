// =================== KABIR VS. KABIR #8: "Day 1 vs. year 10" (Reason #13: comparing your first page to someone's best page) ===================
function ell(cx, cy, rx, ry, c, outline, jit) {      // filled or outlined pixel ellipse; jit adds wobble
  for (var a = 0; a < Math.PI * 2; a += .03) { var j = jit ? (hash(Math.floor(a * 20) + cx) - .5) * jit : 0, x = cx + Math.cos(a) * (rx + j), y = cy + Math.sin(a) * (ry + j);
    if (outline) rect(x, y, 1, 1, c); else rect(cx, y, x - cx, 1, c); }
}
function cat(x, y, q, s) {                            // q: 0 = day-1 scribble, .5 = day-30, 1 = year-10
  L.save(); L.translate(x, y); L.scale(s || 1, s || 1);
  if (q < .3) {
    var ink = "#3A3560"; ell(0, 14, 16, 11, ink, true, 5); ell(-2, -6, 11, 9, ink, true, 4);
    for (var i = 0; i < 6; i++) { rect(-11 + i, -14 - i * 1.5, 1, 1, ink); rect(4 + i * .8, -15 + i * .3, 1, 1, ink); }
    rect(-6, -8, 2, 2, ink); rect(1, -6, 2, 2, ink); rect(-3, -2, 4, 1, ink);
    for (var w = 0; w < 7; w++) { rect(-14 + w, -3 + w * .4, 1, 1, ink); rect(6 + w, -4 - w * .3, 1, 1, ink); }
    for (var t = 0; t < 14; t++) rect(16 + t, 14 - t * 1.2 + Math.sin(t) * 2, 1, 1, ink);
  } else {
    var body = q > .8 ? "#F08A3A" : "#F2E6CC", dark = q > .8 ? "#C2601E" : "#3A3560";
    ell(0, 14, 16, 11, body, false); ell(0, -6, 11, 9, body, false);
    for (var e = 0; e < 7; e++) { rect(-10 + e * .7, -12 - e, 7 - e, 1, body); rect(4 + e * .3, -12 - e, 7 - e, 1, body); }
    ell(0, 14, 16, 11, dark, true); ell(0, -6, 11, 9, dark, true);
    if (q > .8) { for (var st = 0; st < 3; st++) rect(-8 + st * 6, 6, 3, 10, dark); ell(0, 18, 8, 5, "#FFF4E0", false); rect(-5, -8, 3, 3, "#28A86A"); rect(2, -8, 3, 3, "#28A86A"); rect(-4, -7, 1, 1, "#1A1530"); rect(3, -7, 1, 1, "#1A1530"); rect(-1, -3, 2, 1, "#FF9FC2"); }
    else { rect(-5, -8, 2, 2, "#3A3560"); rect(3, -8, 2, 2, "#3A3560"); rect(-1, -3, 2, 1, "#3A3560"); }
    for (var w2 = 0; w2 < 8; w2++) { rect(-16 + w2, -3, 1, 1, q > .8 ? "#FFFFFF" : dark); rect(9 + w2, -3, 1, 1, q > .8 ? "#FFFFFF" : dark); }
    for (var t2 = 0; t2 < 14; t2++) rect(15 + t2, 18 - t2 * 1.4, 3, 2, q > .8 ? body : dark);
  }
  L.restore();
}
function paper(x, y, w, h, label, col) { rect(x - 1, y - 1, w + 2, h + 2, "#1A1530"); rect(x, y, w, h, "#FFF4E0"); for (var i = 0; i < 6; i++) rect(x + 4, y + 10 + i * 12, w - 8, 1, "#ECE0C4"); if (label) { var lw = pwidth(label, 1) + 8; rect(x + w / 2 - lw / 2, y - 12, lw, 11, col || "#3A3560"); ptext(L, label, x + w / 2 - lw / 2 + 4, y - 10, 1, "#FFFFFF"); } }
function heart(x, y, c) { rect(x, y + 1, 2, 2, c); rect(x + 3, y + 1, 2, 2, c); rect(x + 1, y + 2, 3, 2, c); rect(x + 2, y + 4, 1, 1, c); }
// S1: day one, a cat, probably (frame 0)
function sCat(u, a, b) {
  floorRoom("#3B3A6A", "#34335E"); paper(70, 170, 130, 110); cat(135, 228, 0, 1.4);
  if (u > LN("S1", 1)) chr(blinkAt(u, .3) ? "blink" : "stand", 20, 327);
  rect(180, 270, 26, 3, "#FFC145"); rect(204, 270, 3, 3, "#FF9FC2");
  return camAt([[0, 135, 228, 1.8], [LN("S1", 1) + .3, 135, 228, 1.8], [b, 120, 260, 1.3, b - LN("S1", 1) - .3]], u);
}
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: he opens his phone: year ten, flawless
function phoneFrame(x, y) { rect(x - 3, y - 3, 126, 214, "#1A1530"); rect(x, y, 120, 208, "#F4F0FF"); rect(x, y, 120, 14, "#FFFFFF"); ptext(L, "@ARTIST.YR10", x + 6, y + 4, 1, "#3A3560"); }
function sPhone(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); phoneFrame(75, 120);
  var k = seg(u, LN("S3", 1) - .3, LN("S3", 1) + .2); if (k > 0) { rect(80, 140, 110, 120, "#4A6FA5"); ell(135, 240, 60, 14, "#3A5A8A", false); cat(135, 205, 1, 1.8); }
  if (u > LN("S3", 1) + .4) { heart(82, 270, "#E0453A"); ptext(L, "12.4K", 92, 271, 1, "#3A3560"); ptext(L, "YEAR 10. FLAWLESS.", 82, 286, 1, "#3A3560"); }
  return camAt([[a, 135, 225, 1.3], [b, 135, 220, 1.45, b - a]], u);
}
// S4: day one Kabir vs. year ten stranger; verdict
function sVs(u, a, b) {
  rect(0, 0, W, H, "#2A2245"); paper(14, 140, 116, 110, "DAY 1 KABIR", "#E0453A"); cat(72, 196, 0, 1.2); paper(140, 140, 116, 110, "YEAR 10 STRANGER", "#28A86A"); rect(141, 141, 114, 108, "#4A6FA5"); cat(198, 196, 1, 1.2);
  ptext(L, "VS", 135 - pwidth("VS", 3) / 2, 180, 3, "#FFC145");
  var v = LN("S4", 1); if (u > v) { signCard(135, 268, ["VERDICT:", "NO TALENT."], "#E0453A", "#FFFFFF", 2, seg(u, v, v + .3)); }
  if (u > v + 1.4) chr(blinkAt(u, .1) ? "sad_blink" : "sad", 111, 327);
  return camAt([[a, 135, 230, 1.05], [b, 135, 240, 1.08, b - a]], u);
}
// S5: page one vs. their best page: a highlight reel
function sReel(u, a, b) {
  rect(0, 0, W, H, "#1A1530"); stars(u, 20, "#5A5590");
  var off = (u * 20) % 40; rect(0, 150, W, 70, "#2A1F2E"); for (var i = -1; i < 8; i++) { var x = i * 40 - off; rect(x + 2, 152, 6, 4, "#5A5470"); rect(x + 2, 214, 6, 4, "#5A5470"); rect(x + 4, 158, 32, 54, "#4A6FA5"); cat(x + 20, 187, 1, .6); }
  ptext(L, "THEIR BEST PAGES", 135 - pwidth("THEIR BEST PAGES", 1) / 2, 228, 1, "#B8F5C8");
  paper(95, 260, 80, 66, "HIS PAGE 1", "#E0453A"); cat(135, 296, 0, .8);
  if (u > LN("S5", 1)) ptext(L, "NOT A FAIR FIGHT.", 135 - pwidth("NOT A FAIR FIGHT.", 1) / 2, 346, 1, "#FF9F94");
  return camAt([[a, 135, 250, 1.15], [b, 135, 250, 1.2, b - a]], u);
}
// S6: new opponent: day 30 Kabir vs. day 1 Kabir
function sRematch(u, a, b) {
  rect(0, 0, W, H, "#2A2245"); var r = LN("S6", 1) - .2;
  if (u < r) { chr(blinkAt(u, .2) ? "blink" : "stand", 111, 327); ptext(L, "NEW OPPONENT...", 135 - pwidth("NEW OPPONENT...", 2) / 2, 220, 2, "#FFC145"); return camAt([[a, 135, 280, 1.4], [r, 135, 280, 1.45, r - a]], u); }
  paper(14, 140, 116, 110, "DAY 1 KABIR", "#8A8498"); cat(72, 196, 0, 1.2); paper(140, 140, 116, 110, "DAY 30 KABIR", "#28A86A"); cat(198, 196, .5, 1.2);
  ptext(L, "VS", 135 - pwidth("VS", 3) / 2, 180, 3, "#FFC145");
  var w = LN("S6", 2); if (u > w) { signCard(198, 262, ["WINNER"], "#28A86A", "#FFFFFF", 2, seg(u, w, w + .3)); chr(Math.floor(u * 3) % 2 ? "jump" : "stand", 40, 327); }
  return camAt([[r, 135, 230, 1.05], [b, 135, 240, 1.08, b - r]], u);
}
// S7: close on the day-30 page (end card)
function sClose(u, a, b) { floorRoom("#3B3A6A", "#34335E"); paper(70, 170, 130, 110, "DAY 30", "#28A86A"); cat(135, 228, .5, 1.4); chr("stand", 20, 327); return camAt([[a, 120, 260, 1.3], [b, 135, 228, 1.8, b - a]], u); }

var SCENES = [["S1", sCat], ["S2", sWhy], ["S3", sPhone], ["S4", sVs], ["S5", sReel], ["S6", sRematch], ["S7", sClose]];
var EP = {
  badge: "KABIR VS. KABIR #8", hook: "DAY 1: A CAT. *PROBABLY.*", hookEnd: LN("S1", 1) + .4,
  endAt: function () { return LN("S7", 0); }, endQ: "WHO ARE YOU *COMPARING* YOURSELF TO?",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #13", LN("S2", 1), SCN.S2[1], 860, 14],
           ["YOUR PAGE 1 VS. THEIR *BEST* PAGE.", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["THAT'S A *HIGHLIGHT REEL.*", LN("S5", 1), SCN.S5[1], 300, 8]]
};
