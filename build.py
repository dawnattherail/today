"""Build Today at the Rail pages for GitHub Pages (embedded in Squarespace).
Usage: python3 build.py   (edit DAYS below; writes <out>.html)"""
import html
from collections import OrderedDict
e = html.escape
HEAD = ('<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width,initial-scale=1">'
 '<title>Today at the Rail</title><link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Source+Serif+4:wght@400;700&display=swap" rel="stylesheet">'
 '<style>html,body{margin:0;background:transparent}</style></head><body>')
CSS = """<style>
.dtr{font-family:"Source Serif Pro","Source Serif 4",Georgia,serif;color:#0F2F35;line-height:1.5;padding:8px 0}
.dtr *{box-sizing:border-box}
.dtr .date{color:#B8841A;font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:.85rem;margin:0 0 6px}
.dtr h2{font-family:"Libre Baskerville",Georgia,serif;font-weight:700;color:#154750;font-size:2.1rem;margin:0 0 6px}
.dtr .upd{font-size:.9rem;color:#3b5a60;margin:0 0 22px}
.dtr .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.dtr .card{background:#fff;border-radius:16px;box-shadow:0 4px 18px rgba(21,71,80,.12);padding:20px}
.dtr .trk{font-family:"Libre Baskerville",Georgia,serif;font-weight:700;color:#154750;font-size:1.15rem;margin:0 0 10px}
.dtr .pick{margin:0 0 10px}.dtr .pick:last-child{margin:0}
.dtr .meta{font-size:.85rem;color:#3b5a60;margin:0}
.dtr .horse{font-weight:700;font-size:1.08rem;margin:0}
.dtr .off .horse{text-decoration:line-through;color:#8a9a9d}
.dtr .ribbon{display:inline-block;background:#1F4E9E;color:#fff;font-size:.7rem;font-weight:700;letter-spacing:.06em;padding:2px 8px;border-radius:999px;margin-left:6px;vertical-align:middle;text-transform:uppercase}
.dtr .brhead{display:flex;align-items:center;gap:8px;font-family:"Libre Baskerville",Georgia,serif;font-weight:700;color:#1F4E9E;font-size:1.2rem;margin:0 0 12px}
.dtr .card.br{background:linear-gradient(160deg,#2457AD,#173E80);color:#fff;border-top:4px solid #E0A226}
.dtr .card.br .trk{color:#fff;display:flex;align-items:center;gap:8px}.dtr .card.br .meta{color:#D7E2F5}.dtr .card.br .horse{color:#fff}
.dtr .card.br .off .horse{color:#A9B9D8}
.dtr .tag{display:table;margin-top:6px!important;font-size:.72rem;font-weight:700;padding:1px 8px;border-radius:999px;margin-top:3px}
.dtr .t-ok{background:#E3EFE6;color:#1F5A33}.dtr .t-new{background:#FBEBC4;color:#7A5410}.dtr .t-off{background:#F3DEDA;color:#8A2D1F}
.dtr .scr{margin:18px 0 0;font-size:.95rem;background:#FBF6EA;border-left:4px solid #E0A226;padding:10px 14px;border-radius:8px}
.dtr .scr p{margin:0 0 4px}.dtr .scr p:last-child{margin:0}
.dtr .show{background:#154750;color:#FBF6EA}
.dtr .show p{margin:0 0 14px;font-size:1.02rem}
.dtr .btn{display:inline-block;background:#E0A226;color:#0F2F35;font-weight:700;text-decoration:none;padding:10px 20px;border-radius:999px}
@media(max-width:900px){.dtr .grid{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.dtr .grid{grid-template-columns:1fr}.dtr h2{font-size:1.7rem}}
</style>"""
ROS = ('<svg class="ros" width="18" height="22" viewBox="0 0 16 20" aria-hidden="true"><path d="M4 11 2 20 5.5 17.5 8 20 8 12Z M12 11 14 20 10.5 17.5 8 20 8 12Z" fill="#E0A226"/>'
       '<circle cx="8" cy="7" r="6.4" fill="#fff" stroke="#E0A226" stroke-width="1.6"/><circle cx="8" cy="7" r="3.4" fill="#1F4E9E"/></svg>')
TAGS = {"ok": ("t-ok", "Still running after scratches"), "new": ("t-new", "Became a Blue Ribbon Selection after scratches"),
        "off": ("t-off", "Scratched. No Blue Ribbon bet in this race")}

def build(date, updated, picks, scratches, banner=""):
    tracks = OrderedDict()
    for p in picks: tracks.setdefault(p[0], []).append(p[1:])
    cards = []
    for t, ps in tracks.items():
        rows = []
        for r, post, num, h, st in ps:
            meta = f"Race {r}" + (f" &middot; {e(post)} ET" if post else "")
            tag = f'<span class="tag {TAGS[st][0]}">{TAGS[st][1]}</span>' if st else ""
            rib = ""
            rows.append(f'<div class="pick{" off" if st=="off" else ""}"><p class="meta">{meta}</p><p class="horse">#{e(num)} {e(h)}{rib}</p>{tag}</div>')
        cards.append(f'  <div class="card br"><p class="trk">{ROS}{e(t)}</p>{"".join(rows)}</div>')
    cards.append('  <div class="card show"><p>Watch Birdie break down today\'s card in about 90 seconds.</p>'
                 '<a class="btn" href="#" target="_blank">Play the episode</a></div>')
    scr = "".join(f"<p>{s}</p>" for s in scratches)
    return (HEAD + banner + CSS + f'<div class="dtr">\n <p class="date">{e(date)}</p>\n <h2>Today at the Rail</h2>\n'
            f' <p class="upd">{e(updated)}</p>\n <p class="brhead">{ROS}Blue Ribbon Selections</p>\n <div class="grid">\n' + "\n".join(cards) +
            f'\n </div>\n <div class="scr"><p><b>Scratches</b> (Blue Ribbon Selections only)</p>{scr}</div>\n</div>\n</body></html>\n')

# Live daily pages are built outside this repo until launch (Dec 11).
# ---- Sample using the real Nov 26 morning scratches (Churchill, checked 10:31 AM ET) ----
note = ('<p style="font:600 14px Georgia,serif;background:#154750;color:#FBF6EA;padding:8px 12px;border-radius:8px;margin:0 0 12px">'
        'SAMPLE: real Nov 26 morning scratches, to show the layout. Not live.</p>')
P26 = [("Churchill Downs", 8, "", "3", "Bravojuliet", "new")]
open("sample-scratches.html", "w").write(build("Thursday, November 26, 2026",
    "Last updated 10:31 AM ET · Scratches checked", P26,
    ["<b>Churchill Downs</b>, checked 10:31 AM ET. Race 8: #1 Great Grenzen, #7 Mariamakesmelaugh, #13 Modifly and #16 Waawaatesi scratched. "
     "With those four out, #3 Bravojuliet became a Blue Ribbon Selection."], note))
# layout sample showing all three states (made-up combination of Nov 27 picks; clearly labeled)
note2 = note.replace("real Nov 26 morning scratches, to show the layout", "made-up horses and scratches, to show all three cases")
P27s = [("Sample Park", 7, "2:38 PM", "3", "Morning Line", "ok"), ("Example Downs", 4, "5:04 PM", "4", "Stopwatch Sally", "off"),
        ("Example Downs", 9, "7:35 PM", "6", "Coffee At Dawn", "ok")]
open("sample-states.html", "w").write(build("Sample day", "Last updated 11:40 AM ET · Scratches checked", P27s,
    ["<b>Sample Park</b>, checked 11:40 AM ET. Race 7: no scratches. Our pick runs.",
     "<b>Example Downs</b>, checked 2:05 PM ET. Race 4: #4 Stopwatch Sally scratched, so no Blue Ribbon bet in that race. Race 9: #2 scratched. Our pick runs."], note2))

import shutil; shutil.copy("sample-states.html","index.html")
