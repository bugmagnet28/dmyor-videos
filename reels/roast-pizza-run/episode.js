// =================== HABIT ROAST #4: running to earn the pizza (you can't out-run your fork) ===================
function street(u) { rect(0, 0, W, H, "#2A2245"); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, "#262040"); rect(0, 380, W, H - 380, "#3A3560"); }
function pizza(cx, cy, r, eaten, hi) {          // 8 slices; eaten = slices gone (can be fractional); hi = highlight remaining
  rect(cx - r - 4, cy - r - 4, 2 * r + 8, 2 * r + 8, "rgba(0,0,0,0)");
  for (var i = 0; i < 8; i++) { var a0 = -Math.PI / 2 + i * Math.PI / 4, a1 = a0 + Math.PI / 4, gone = Math.max(0, Math.min(1, eaten - i));
    if (gone >= 1) continue; L.beginPath(); L.moveTo(cx, cy); L.arc(cx, cy, r, a0 + (a1 - a0) * gone, a1); L.closePath(); L.fillStyle = "#E8A040"; L.fill(); L.beginPath(); L.moveTo(cx, cy); L.arc(cx, cy, r - 4, a0 + (a1 - a0) * gone, a1); L.closePath(); L.fillStyle = hi ? "#F25C3A" : "#E0453A"; L.fill();
    for (var p = 0; p < 2; p++) { var aa = a0 + (a1 - a0) * (.3 + p * .4), rr = r * (.45 + p * .2); if ((aa - a0) / (a1 - a0) > gone) { rect(cx + Math.cos(aa) * rr - 2, cy + Math.sin(aa) * rr - 2, 5, 5, "#FFF4E0"); rect(cx + Math.cos(aa) * rr, cy + Math.sin(aa) * rr, 2, 2, "#3A7A3A"); } } }
  for (var j = 0; j < 8; j++) { var a = -Math.PI / 2 + j * Math.PI / 4; for (var s = 0; s < r; s += 1) rect(cx + Math.cos(a) * s, cy + Math.sin(a) * s, 1, 1, "#B8702A"); }
}
function chip(x, y, s, bg) { var w = pwidth(s, 1) + 10; rect(x - 1, y - 1, w + 2, 16, "#1A1530"); rect(x, y, w, 14, bg); ptext(L, s, x + 5, y + 4, 1, "#FFFFFF"); return w; }
// S1: ran 5 km for the pizza; the run is worth about a slice and a half (frame 0)
function sHook(u, a, b) {
  street(u); pizza(170, 230, 62, 0, false); chr("walk" + (Math.floor(u * 8) % 4), 30, 327);
  chip(20, 150, "5 KM RUN", "#28A86A"); chip(166, 150, "LARGE PIZZA", "#E0453A");
  return camAt([[0, 135, 250, 1.12], [b, 135, 252, 1.15, b]], u);
}
// S2: the run "eats" 1.5 slices; 6.5 left
function sMath(u, a, b) {
  street(u); var e = 1.5 * eio(seg(u, LN("S2", 0) + .4, LE("S2", 0))); pizza(150, 230, 62, e, u > LN("S2", 1)); chr("stand", 20, 327);
  chip(20, 150, "5 KM RUN: ABOUT 1.5 SLICES", "#28A86A"); if (u > LN("S2", 1)) chip(150, 310, "6.5 SLICES LEFT", "#E0453A");
  return camAt([[a, 135, 250, 1.15], [b, 140, 255, 1.22, b - a]], u);
}
// S3: what running is for, what the plate is for
function sFix(u, a, b) {
  street(u); var k1 = seg(u, LN("S3", 1), LN("S3", 1) + .3), k2 = seg(u, LN("S3", 1) + 1.4, LN("S3", 1) + 1.7);
  if (k1 > 0) { rect(20, 170, 110, 110, "#1A1530"); rect(22, 172, 106, 106, "#2E5A3E"); ptext(L, "RUN FOR", 50, 182, 1, "#B8F5C8"); ["HEART", "HEAD", "MOOD"].forEach(function (s, i) { ptext(L, s, 40, 204 + i * 20, 2, "#FFFFFF"); }); }
  if (k2 > 0) { rect(140, 170, 110, 110, "#1A1530"); rect(142, 172, 106, 106, "#5A2A2E"); ptext(L, "PLATE FOR", 166, 182, 1, "#FF9F94"); ptext(L, "WEIGHT", 160, 214, 2, "#FFFFFF"); plateIcon(195, 252); }
  chr("walk" + (Math.floor(u * 7) % 4), 110, 327);
  return camAt([[a, 135, 250, 1.12], [b, 135, 252, 1.15, b - a]], u);
}
function sEnd(u, a, b) { street(u); pizza(170, 230, 62, 6, false); chr("walk" + (Math.floor(u * 8) % 4), 30, 327); chip(20, 150, "5 KM RUN", "#28A86A"); chip(166, 150, "2 SLICES", "#28A86A"); return camAt([[a, 135, 252, 1.15], [b, 135, 250, 1.12, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sMath], ["S3", sFix], ["S4", sEnd]];
var EP = {
  badge: "HABIT ROAST #4", badgeBg: ROAST.badgeBg, badgeFg: ROAST.badgeFg, hook: "RAN 5 KM FOR THE PIZZA. *PIZZA WON.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S4", 0); }, endQ: "WHAT'S YOUR *EARNED* TREAT?",
  titles: [["YOU CAN'T OUT-RUN YOUR *FORK.*", LN("S3", 0), LN("S3", 2), 300, 9],
           ["SEND TO YOUR *LARGE-PIZZA* RUNNING BUDDY.", LN("S3", 2), SCN.S3[1], 300, 8]]
};
