// =================== HABIT ROAST #6: the all-yellow textbook (familiar is not remembered) ===================
function desk(u) { rect(0, 0, W, H, "#2A2245"); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, "#262040"); rect(0, 380, W, H - 380, "#6B4430"); rect(0, 380, W, 3, "#8A5A3A"); }
// open book: two pages of text lines; yel = fraction of lines highlighted (0..1)
function book(x, y, yel, cover) {
  rect(x - 2, y - 2, 224, 134, "#1A1530"); rect(x, y, 108, 130, "#FFF4E0"); rect(x + 112, y, 108, 130, "#FFF4E0"); rect(x + 108, y, 4, 130, "#CFC6B4");
  var n = 0; for (var p = 0; p < 2; p++) for (var r = 0; r < 12; r++) { var lx = x + 8 + p * 112, ly = y + 10 + r * 10, lw = 88 - (r % 4 === 3 ? 30 : 0);
    if (n++ < yel * 24) rect(lx - 2, ly - 2, lw + 4, 6, "#FFE066"); rect(lx, ly, lw, 2, "#8A86A8"); }
  if (cover) { rect(x + 112, y, 108 * cover, 130, "#4C9AFF"); }
}
function hl(x, y) { rect(x, y, 6, 20, "#FFE066"); rect(x, y + 20, 6, 4, "#3A3560"); }
// S1 (frame 0): 24 pages, all yellow; recall meter at 0
function sHook(u, a, b) {
  desk(u); book(25, 150, 1); hl(200 + 4 * Math.sin(u * 6), 260);
  counter(24, 300, "PAGES HIGHLIGHTED", "24", "#FFE066", 3); chr(blinkAt(u, .4) ? "sit_read_blink" : "sit_read", 170, 327);
  if (u > LN("S1", 1) + .2) { rect(130, 296, 116, 16, "#1A1530"); ptext(L, "REMEMBERED: YELLOW", 136, 301, 1, "#E0453A"); }
  return camAt([[0, 135, 250, 1.12], [b, 135, 255, 1.16, b]], u);
}
// S2: two bars: "feels known" (tall, yellow) vs "can answer" (short, red); then the exam card hides the page
function sTrap(u, a, b) {
  desk(u); var m = LN("S2", 1), k1 = eio(seg(u, m, m + 1)), k2 = eio(seg(u, m + 1.6, m + 2.4)), ex = seg(u, m + 4.6, m + 5.2);
  rect(28, 140, 214, 150, "#1A1530"); rect(30, 142, 210, 146, "#FFF4E0");
  rect(64, 270 - 110 * k1, 50, 110 * k1, "#FFE066"); ptext(L, "FEELS", 72, 274 + 0, 1, "#3A3560"); ptext(L, "KNOWN", 72, 282, 1, "#3A3560");
  rect(156, 270 - 26 * k2, 50, 26 * k2, "#E0453A"); ptext(L, "CAN", 172, 274, 1, "#3A3560"); ptext(L, "ANSWER", 164, 282, 1, "#3A3560");
  if (ex > 0) signCard(135, 300, ["EXAM: NO PAGE.", "JUST QUESTIONS."], "#E0453A", "#FFFFFF", 1, ex);
  chr(u > m + 4.6 ? "shock" : "sit_read", 110, 327);
  return camAt([[a, 135, 240, 1.18], [b, 135, 250, 1.24, b - a]], u);
}
// S3: heading -> question, cover the page, answer out loud; misses get a red flag
function sFix(u, a, b) {
  desk(u); var cv = eio(seg(u, LN("S3", 0) + 1.8, LN("S3", 0) + 2.6)); book(25, 150, .25, cv);
  rect(30, 128, 200, 16, "#1A1530"); ptext(L, "HEADING", 36, 133, 1, "#9A92C0"); if (u > LN("S3", 0) + .8) ptext(L, "-> WHY DOES IT HAPPEN?", 84, 133, 1, "#6CC7A3");
  if (u > LN("S3", 0) + 3) { bubble(150, 286, 92, 18, 190); ptext(L, "BECAUSE...", 160, 292, 1, "#1A1530"); }
  if (u > LN("S3", 1)) { tick(60, 300); tick(80, 300); redX(100, 298, 9); ptext(L, "STUDY THIS", 90, 312, 1, "#E0453A"); }
  chr(Math.floor(u * 3) % 2 ? "sit_write0" : "sit_write1", 170, 327);
  return camAt([[a, 135, 250, 1.12], [b, 135, 252, 1.16, b - a]], u);
}
function sEnd(u, a, b) { desk(u); book(25, 150, .25); counter(24, 300, "PAGES HIGHLIGHTED", "24", "#FFE066", 3); rect(130, 296, 116, 16, "#1A1530"); ptext(L, "ANSWERED: 9 OF 10", 136, 301, 1, "#28A86A"); chr("sit_read_happy", 170, 327); return camAt([[a, 135, 255, 1.16], [b, 135, 250, 1.12, b - a]], u); }

var SCENES = [["S1", sHook], ["S2", sTrap], ["S3", sFix], ["S4", sEnd]];
var EP = {
  badge: "HABIT ROAST #6", badgeBg: ROAST.badgeBg, badgeFg: ROAST.badgeFg, hook: "24 PAGES. ALL *YELLOW.*", hookEnd: LN("S1", 1) + .5,
  endAt: function () { return LN("S4", 0); }, endQ: "WHAT COLOUR IS *YOUR* HIGHLIGHTER?",
  titles: [["FAMILIAR IS NOT *REMEMBERED.*", LN("S2", 1), SCN.S2[1], 300, 9],
           ["SEND TO YOUR *NEON YELLOW* FRIEND.", LN("S3", 2), SCN.S3[1], 300, 8]]
};
