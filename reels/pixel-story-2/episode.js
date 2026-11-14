// =================== SMALL STORIES #2: Sam rereads, Dev tests himself (retrieval practice) ===================
function half(x0, wall, wall2) { rect(x0, 0, 134, 380, wall); for (var i = 0; i < 7; i++) rect(x0 + i * 20, 0, 1, 380, wall2); rect(x0, 380, 134, 100, "#6B4430"); rect(x0, 392, 134, 1, "#5A3826"); }
function desk(x0) { rect(x0 + 52, 336, 74, 6, "#8A5228"); rect(x0 + 56, 342, 4, 38, "#6B4430"); rect(x0 + 118, 342, 4, 38, "#6B4430"); rect(x0 + 112, 316, 2, 20, "#2A1F2E"); rect(x0 + 106, 310, 14, 7, "#FFC145"); }
function book(x, y, open) { if (open) { rect(x - 1, y - 1, 34, 14, "#1A1530"); rect(x, y, 16, 12, "#FFF4E0"); rect(x + 16, y, 16, 12, "#F2E6CC"); for (var i = 0; i < 3; i++) { rect(x + 2, y + 3 + i * 3, 11, 1, "#8A8498"); rect(x + 18, y + 3 + i * 3, 11, 1, "#8A8498"); } } else { rect(x - 1, y - 1, 26, 12, "#1A1530"); rect(x, y, 24, 10, "#4C9AFF"); ptext(L, "CH5", x + 4, y + 2, 1, "#FFFFFF"); } }
function paper(x, y, n, wrong) { rect(x - 1, y - 1, 30, 20, "#1A1530"); rect(x, y, 28, 18, "#FFFFFF"); for (var i = 0; i < n; i++) { rect(x + 3, y + 3 + i * 3, 14 + (i * 5) % 8, 1, "#3A3560"); if (wrong && i % 2) rect(x + 21, y + 2 + i * 3, 3, 3, "#E0453A"); } }
function base(u) { half(0, "#3B4A7A", "#35436E"); half(136, "#3B4A7A", "#35436E"); rect(134, 0, 2, H, "#1A1530"); desk(0); desk(136); ptext(L, "SAM", 48, 196, 2, "#FFFFFF"); ptext(L, "DEV", 184, 196, 2, "#FFFFFF"); }
function people(u, sam, dev) { chr(sam || "stand", 30, 327); chr(dev || (blinkAt(u, .7) ? "olook" : "ostand"), 166, 327, true); }
function meter(x0, label, v, col) { ptext(L, label, x0 + 18, 228, 1, "#FFFFFF"); rect(x0 + 18, 238, 96, 10, "#1A1530"); rect(x0 + 19, 239, 94 * v, 8, col); }
// S1: same chapter, same three hours (frame 0)
function sSame(u, a, b) { base(u); people(u); book(80, 324, false); book(216, 324, false); dayTag("3 HRS", 24, 226, "#FFFFFF", "#1A1530"); dayTag("3 HRS", 156, 226, "#FFFFFF", "#1A1530"); return camAt([[0, 135, 280, 1.12], [b, 135, 282, 1.15, b]], u); }
// S2: Sam rereads 3x; Dev reads once, closes the book, writes what he remembers
function sMethod(u, a, b) {
  base(u); people(u); var r = Math.min(3, 1 + Math.floor(seg(u, LN("S2", 0), LE("S2", 0)) * 2.99)); book(76, 324, true); ptext(L, "READ " + r + "X", 30, 232, 2, "#B8F5C8");
  if (u > LN("S2", 1)) { book(222, 326, false); var n = Math.min(5, Math.floor(seg(u, LN("S2", 1) + 1, LE("S2", 1)) * 5.99)); paper(186, 316, n, true); ptext(L, "FROM MEMORY", 168, 236, 1, "#FFE066"); }
  return camAt([[a, 135, 280, 1.12], [b, 135, 282, 1.15, b - a]], u);
}
// S3: it feels awful; Sam feels ready, Dev feels behind
function sFeel(u, a, b) { base(u); people(u, "stand", "sad"); book(76, 324, true); paper(186, 316, 5, true);
  if (u > LN("S3", 1)) { meter(0, "FEELS READY", .9, "#28A86A"); meter(136, "FEELS BEHIND", .3, "#E0453A"); }
  return camAt([[a, 135, 280, 1.12], [b, 135, 282, 1.15, b - a]], u); }
// S4: one week later, the test: Dev remembers more
function sTest(u, a, b) {
  base(u); var k = seg(u, LN("S4", 1), LN("S4", 1) + 1); dayTag("1 WEEK LATER", 135 - pwidth("1 WEEK LATER", 3) / 2 - 5, 140, "#FFFFFF", "#1A1530");
  people(u, k > .5 ? "sad" : "stand", k > .5 ? "jump" : "ostand");
  rect(20, 260, 96, 10, "#1A1530"); rect(21, 261, 94 * .35 * k, 8, "#E0453A"); rect(156, 260, 96, 10, "#1A1530"); rect(157, 261, 94 * .8 * k, 8, "#28A86A"); ptext(L, "REMEMBERED", 34, 248, 1, "#FFFFFF"); ptext(L, "REMEMBERED", 170, 248, 1, "#FFFFFF");
  return camAt([[a, 135, 270, 1.12], [b, 135, 272, 1.15, b - a]], u);
}
// S5: pulling it back out makes it stay (loops to the desks)
function sEnd(u, a, b) { base(u); people(u, "stand", "ostand"); book(80, 324, false); paper(186, 316, 5, false); return camAt([[a, 135, 282, 1.15], [b, 135, 280, 1.12, b - a]], u); }

var SCENES = [["S1", sSame], ["S2", sMethod], ["S3", sFeel], ["S4", sTest], ["S5", sEnd]];
var EP = {
  badge: "SMALL STORIES #2", badgeBg: STORY.badgeBg, badgeFg: STORY.badgeFg, hook: "SAME CHAPTER. SAME 3 HOURS. *ONE FORGETS.*", hookEnd: LN("S1", 0) + 1.5,
  endAt: function () { return LN("S5", 2); }, endQ: "ARE YOU A *SAM* OR A *DEV?*",
  titles: [["FAMILIAR ISN'T *REMEMBERED.*", LN("S5", 0), LN("S5", 2), 300, 9]]
};
