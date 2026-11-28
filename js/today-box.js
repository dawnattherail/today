/* Dawn at the Rail: draws the Today at the Rail box from data/today.json.
   Used by the Squarespace embed:  <div id="dar-today"></div><script src="https://dawnattherail.github.io/today/js/today-box.js"></script>
   Rules (Chris, Nov 27): one same-size box per Blue Ribbon Selection, even from the same track;
   the Play the episode box is one grid cell, same size; scratched selections leave the grid and appear in the Scratches line. */
(function () {
  var BASE = "https://dawnattherail.github.io/today/";
  var el = document.getElementById("dar-today");
  if (!el) return;
  var ROS = '<svg class="ros" width="18" height="22" viewBox="0 0 16 20" aria-hidden="true"><path d="M4 11 2 20 5.5 17.5 8 20 8 12Z M12 11 14 20 10.5 17.5 8 20 8 12Z" fill="#E0A226"/><circle cx="8" cy="7" r="6.4" fill="#fff" stroke="#E0A226" stroke-width="1.6"/><circle cx="8" cy="7" r="3.4" fill="#1F4E9E"/></svg>';
  var TAG = {ok: ["t-ok", "Still running after scratches"], new: ["t-new", "Became a Blue Ribbon Selection after scratches"], pre: ["", ""],
             won: ["t-ok", "Won"], lost: ["t-off", "Did not win"]};
  var CSS = '.dtr{font-family:"Source Serif Pro","Source Serif 4",Georgia,serif;color:#0F2F35;line-height:1.5;padding:8px 0}.dtr *{box-sizing:border-box}' +
    '.dtr .date{color:#B8841A;font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:.85rem;margin:0 0 6px}' +
    '.dtr h2{font-family:"Libre Baskerville",Georgia,serif;font-weight:700;color:#154750;font-size:2.1rem;margin:0 0 6px}' +
    '.dtr .upd{font-size:.9rem;color:#3b5a60;margin:0 0 22px}' +
    '.dtr .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,max(240px,calc((100% - 36px)/3))),1fr));grid-auto-rows:1fr;gap:18px}' +
    '.dtr .card{border-radius:16px;box-shadow:0 4px 18px rgba(21,71,80,.12);padding:20px}' +
    '.dtr .trk{font-family:"Libre Baskerville",Georgia,serif;font-weight:700;font-size:1.15rem;margin:0 0 10px;display:flex;align-items:center;gap:8px}' +
    '.dtr .meta{font-size:.85rem;margin:0}.dtr .horse{font-weight:700;font-size:1.08rem;margin:0}' +
    '.dtr .brhead{display:flex;align-items:center;gap:8px;font-family:"Libre Baskerville",Georgia,serif;font-weight:700;color:#1F4E9E;font-size:1.2rem;margin:0 0 12px}' +
    '.dtr .card.br{background:linear-gradient(160deg,#2457AD,#173E80);color:#fff;border-top:4px solid #E0A226}.dtr .card.br .meta{color:#D7E2F5}' +
    '.dtr .tag{display:table;margin-top:6px;font-size:.72rem;font-weight:700;padding:1px 8px;border-radius:999px}' +
    '.dtr .t-ok{background:#E3EFE6;color:#1F5A33}.dtr .t-new{background:#FBEBC4;color:#7A5410}.dtr .t-off{background:#F3DEDA;color:#8A2D1F}' +
    '.dtr .show{background:#154750;color:#FBF6EA}.dtr .show p{margin:0 0 14px;font-size:1.02rem}' +
    '.dtr .btn{display:inline-block;background:#E0A226;color:#0F2F35;font-weight:700;text-decoration:none;padding:10px 20px;border-radius:999px}' +
    '.dtr .tot{margin:18px 0 0;font-size:.95rem;color:#154750}' +
    '.dtr .scr{margin:18px 0 0;font-size:.95rem;background:#FBF6EA;border-left:4px solid #E0A226;padding:10px 14px;border-radius:8px}.dtr .scr p{margin:0 0 4px}.dtr .scr p:last-child{margin:0}' +
    '.dtr .sample{background:#FBEBC4;color:#7A5410;padding:6px 10px;border-radius:8px;font-size:.85rem;margin:0 0 14px}' +
    '@media(max-width:560px){.dtr h2{font-size:1.7rem}}';
  function esc(s) { return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function render(d) {
    var sel = d.selections || [];
    var cards = sel.map(function (p) {
      var t = TAG[p.status] || TAG.pre;
      return '<div class="card br"><p class="trk">' + ROS + esc(p.track) + '</p><p class="meta">Race ' + esc(p.race) + ' &middot; ' + esc(p.post) +
        '</p><p class="horse">' + esc(p.horse) + '</p>' + (t[0] ? '<span class="tag ' + t[0] + '">' + t[1] + '</span>' : '') + '</div>';
    });
    cards.push('<div class="card show"><p>Watch Birdie break down today\'s card in about 90 seconds.</p><a class="btn" href="' + esc(d.show_url || "#") + '" target="_blank" rel="noopener">Play the episode</a></div>');
    var scr = (d.scratch_notes && d.scratch_notes.length) ? d.scratch_notes.map(function (s) { return "<p>" + s + "</p>"; }).join("")
      : "<p>Morning scratches are checked about an hour before each track's first post.</p>";
    el.innerHTML = '<style>' + CSS + '</style><div class="dtr">' +
      (d.sample ? '<p class="sample">' + esc(d.status_line) + '</p>' : '') +
      '<p class="date">' + esc(d.date_label) + '</p><h2>Today at the Rail</h2>' +
      '<p class="upd">' + (d.phase === "night" ? "Posted the night before &middot; Scratches not checked yet" : "Scratches checked &middot; Updated " + esc(d.updated)) + '</p>' +
      '<p class="brhead">' + ROS + 'Blue Ribbon Selections &middot; ' + sel.length + ' today</p>' +
      (sel.length ? '<div class="grid">' + cards.join("") + '</div>' : '<p>No Blue Ribbon Selections today. We only bet when the numbers say so.</p>') +
      '<p class="tot">' + (d.totals_line || "") + '<a href="/full-card">See every race on Today\'s Full Cards &rarr;</a></p>' +
      '<div class="scr"><p><b>Scratches</b> (Blue Ribbon Selections only)</p>' + scr + '</div></div>';
  }
  if (!document.getElementById("dar-fonts")) {
    var l = document.createElement("link"); l.id = "dar-fonts"; l.rel = "stylesheet";
    l.href = "https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Source+Serif+4:wght@400;700&display=swap";
    document.head.appendChild(l);
  }
  fetch(BASE + "data/today.json?t=" + Date.now(), {cache: "no-store"})
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(render)
    .catch(function () { el.innerHTML = '<p style="font-family:Georgia,serif">Today\'s picks are loading slowly. Please refresh in a minute.</p>'; });
})();
