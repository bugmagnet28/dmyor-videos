// =================== STRAIGHT ANSWER #4: "That's just not me" (Reason #12: it doesn't feel like you, yet) ===================
var TAGS = [["NOT A MORNING PERSON", 0], ["NOT A READER", 1], ["BAD WITH MONEY", 2]];
function tag(x, y, s, k, col) { if (k <= 0) return; var w = pwidth(s, 1) + 10, sc = eout(k); L.save(); L.translate(x, y); L.scale(sc, sc); L.rotate(-.04); rect(-w / 2 - 1, -7, w + 2, 15, "#1A1530"); rect(-w / 2, -6, w, 13, col || "#FFFFFF"); rect(-w / 2, -6, 4, 13, "#E0453A"); ptext(L, s, -w / 2 + 7, -3, 1, "#1A1530"); L.restore(); }
function bookIn(x, y) { rect(x, y, 12, 9, "#1A1530"); rect(x + 1, y + 1, 5, 7, "#4C9AFF"); rect(x + 6, y + 1, 5, 7, "#3A7AE0"); }
function plain(u) { rect(0, 0, W, H, "#2A2245"); for (var i = 0; i < 14; i++) rect(i * 20, 0, 1, 380, "#262040"); rect(0, 380, W, H - 380, "#3A3560"); }
// S1: three labels he wears (frame 0)
function sTags(u, a, b) {
  plain(u); chr(blinkAt(u, .3) ? "blink" : "stand", 111, 327);
  tag(135, 214, TAGS[0][0], 1); tag(135, 244, TAGS[1][0], u < .01 ? 1 : seg(u, LN("S1", 1) - .1, LN("S1", 1) + .2) || 1, null); tag(135, 274, TAGS[2][0], 1);
  return camAt([[0, 135, 262, 1.6], [b, 135, 268, 1.65, b]], u);
}
function sWhy(u, a, b) { return whyScene(u, a, b); }
// S3: the habit doesn't match the label, so the book goes down
function sDrop(u, a, b) {
  plain(u); var d = LN("S3", 1) + .4, k = seg(u, d, d + .5);
  chr(u > d ? (blinkAt(u, .2) ? "sad_blink" : "sad") : "stand", 111, 327);
  if (u < d) bookIn(142, 352); else bookIn(142 + 14 * k, 352 + 20 * k * k);
  tag(135, 244, "NOT A READER", 1, u > LN("S3", 1) ? "#FFE066" : "#FFFFFF");
  if (u > d + .5) { ptext(L, "CONSISTENT", 135 - pwidth("CONSISTENT", 2) / 2, 170, 2, "#E0453A"); ptext(L, "WITH THE OLD YOU.", 135 - pwidth("WITH THE OLD YOU.", 1) / 2, 194, 1, "#FF9F94"); }
  return camAt([[a, 135, 280, 1.5], [b, 135, 270, 1.6, b - a]], u);
}
// S4/S5: identity is evidence: votes into a box
function ballotBox(x, y, n) { rect(x - 62, y, 124, 76, "#1A1530"); rect(x - 60, y + 2, 120, 72, "#C8C0E8"); rect(x - 60, y + 2, 120, 10, "#9A92C0"); rect(x - 20, y + 5, 40, 3, "#1A1530"); ptext(L, "I'M SOMEONE", x - pwidth("I'M SOMEONE", 1) / 2, y + 22, 1, "#3A3560"); ptext(L, "WHO READS", x - pwidth("WHO READS", 1) / 2, y + 32, 1, "#3A3560");
  var lab = "VOTES: " + n; ptext(L, lab, x - pwidth(lab, 2) / 2, y + 48, 2, n > 0 ? "#28A86A" : "#8A8498"); }
function slip(x, y) { rect(x - 7, y - 4, 14, 9, "#1A1530"); rect(x - 6, y - 3, 12, 7, "#FFFFFF"); rect(x - 3, y, 2, 2, "#28A86A"); rect(x - 1, y + 1, 2, 2, "#28A86A"); rect(x + 1, y - 1, 2, 2, "#28A86A"); }
var DOS = ["1 PAGE", "2 PAGES, BADLY", "1 PAGE", "5 PAGES", "1 PAGE", "10 PAGES"];
function sEvidence(u, a, b) {
  plain(u); ballotBox(135, 250, 0);
  if (u > LN("S4", 1)) { signCard(135, 150, ["IT'S EVIDENCE."], "#FFE066", "#1A1530", 2, seg(u, LN("S4", 1), LN("S4", 1) + .3)); }
  return camAt([[a, 135, 250, 1.4], [b, 135, 255, 1.45, b - a]], u);
}
function sVotes(u, a, b) {
  plain(u); var per = (LE("S5", 0) - a) / 6, n = Math.min(6, Math.floor((u - a) / per)), t = ((u - a) % per) / per;
  ballotBox(135, 250, n);
  if (n < 6) { var lab = "DAY " + (n + 1) + ": " + DOS[n]; ptext(L, lab, 135 - pwidth(lab, 1) / 2, 200, 1, "#FFFFFF"); slip(135, lerp(214, 255, eio(t))); }
  if (u > LN("S5", 1)) signCard(135, 150, ["I'M SOMEONE WHO READS."], "#28A86A", "#FFFFFF", 1, seg(u, LN("S5", 1), LN("S5", 1) + .3));
  return camAt([[a, 135, 250, 1.4], [b, 135, 250, 1.45, b - a]], u);
}
// S6: you don't need a majority; you need the first vote (Dmyor close)
function sFirst(u, a, b) {
  plain(u); ballotBox(135, 250, 1); slip(135, 240 - 4 * Math.sin(u * 3));
  tag(135, 352, "NOT A READER", 1, "#8A8498"); if (u > LN("S6", 1)) rect(70, 352, 130 * eout(seg(u, LN("S6", 1), LN("S6", 1) + .4)), 2, "#E0453A");
  return camAt([[a, 135, 270, 1.4], [b, 135, 270, 1.45, b - a]], u);
}

var SCENES = [["S1", sTags], ["S2", sWhy], ["S3", sDrop], ["S4", sEvidence], ["S5", sVotes], ["S6", sFirst]];
var EP = {
  badge: "STRAIGHT ANSWER #4", badgeBg: STRAIGHT.badgeBg, badgeFg: STRAIGHT.badgeFg, hook: "\"THAT'S JUST *NOT ME.\"*", hookEnd: LN("S1", 1) + .4,
  endAt: function () { return LN("S6", 3); }, endQ: "WHAT'S YOUR *FIRST VOTE* TODAY?",
  titles: [["WHY DO WE STOP DOING THINGS WE KNOW ARE *GOOD* FOR US?", LN("S2", 0), SCN.S2[1], 470, 8],
           ["REASON #12", LN("S2", 1), SCN.S2[1], 860, 14],
           ["IT DOESN'T FEEL LIKE *YOU.* YET.", LN("S2", 1) + .5, SCN.S2[1], 1060, 7],
           ["EVERY TIME YOU DO IT, THAT'S *ONE VOTE.*", LN("S5", 0), LN("S5", 1), 300, 7],
           ["YOU NEED THE *FIRST* VOTE.", LN("S6", 1), LN("S6", 3), 300, 8]]
};
