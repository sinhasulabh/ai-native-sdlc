#!/usr/bin/env python3
"""Generate index.html from data.json. Usage: python3 build.py"""
import json, html
from pathlib import Path

root = Path(__file__).parent
d = json.loads((root / "data.json").read_text())
e = html.escape

RATINGS = {
    "same": ("Same", "r-same"),
    "similar": ("Similar", "r-similar"),
    "different-path": ("Different path, same outcome", "r-path"),
    "different": ("Completely different", "r-diff"),
}

def links(ls):
    return " ".join(
        f'<a href="{e(l["url"])}" target="_blank" rel="noopener">{e(l["label"])}&nbsp;&#8599;</a>'
        for l in ls
    )

def cell(c, vid, baseline, assessment):
    cls = ["cell"]
    badge = ""
    if vid == baseline:
        cls.append("r-base")
        if not assessment:
            badge = '<span class="badge">Baseline</span>'
    elif c.get("rating"):
        label, rc = RATINGS[c["rating"]]
        cls.append(rc)
        badge = f'<span class="badge">{e(label)}</span>'
    body = ""
    if "bullets" in c:
        body = "<ul>" + "".join(f"<li>{e(b)}</li>" for b in c["bullets"]) + "</ul>"
    else:
        body = f'<p>{e(c["text"])}</p>'
    lk = f'<div class="links">{links(c["links"])}</div>' if c.get("links") else ""
    return f'<td class="{" ".join(cls)}">{badge}{body}{lk}</td>'

vendors = d["vendors"]
head = "".join(
    f'<th scope="col"><div class="vname">{e(v["name"])}</div>'
    f'<div class="vfw">{e(v["framework"])}</div></th>'
    for v in vendors
)

rows = []
for r in d["rows"]:
    cls = "assess" if r.get("assessment") else ""
    tds = "".join(cell(r["cells"][v["id"]], v["id"], d["baseline"], r.get("assessment")) for v in vendors)
    rows.append(f'<tr class="{cls}"><th scope="row">{e(r["topic"])}</th>{tds}</tr>')

legend = "".join(
    f'<li class="{rc}"><span class="swatch"></span><strong>{e(lbl)}</strong></li>'
    for lbl, rc in RATINGS.values()
)

src_items = "".join(
    f'<li><strong>{e(v["name"])}</strong>: {links(v["sources"])}</li>' for v in vendors
)
tp_items = "".join(f'<li>{links([t])}</li>' for t in d.get("third_party", []))
pending = ", ".join(e(x) for x in d.get("pending", []))

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(d["title"])}</title>
<meta name="description" content="Side-by-side comparison of vendor frameworks for an AI-native software development lifecycle, using Anthropic's playbook as the baseline.">
<style>
:root {{
  --bg:#fbfaf7; --fg:#1d1d1b; --muted:#5f5e5a; --line:#dcd9d0; --card:#ffffff;
  --accent:#8a3b12;
  --same:#e3f1e5;     --same-b:#2f7d3a;
  --similar:#eef5df;  --similar-b:#6a8f22;
  --path:#fff1d6;     --path-b:#b9770e;
  --diff:#fbe3e0;     --diff-b:#b23a2e;
  --base:#eef0f5;     --base-b:#4a5a85;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg:#161614; --fg:#ecebe6; --muted:#a3a198; --line:#34332f; --card:#1e1e1c;
    --accent:#e08a5a;
    --same:#1d3322;    --same-b:#6cc07a;
    --similar:#2a3216; --similar-b:#a7c95a;
    --path:#3a2c10;    --path-b:#e6a23c;
    --diff:#3d1f1b;    --diff-b:#ec7a6c;
    --base:#232738;    --base-b:#8fa0d6;
  }}
}}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
.wrap {{ max-width:1200px; margin:0 auto; padding:32px 16px 64px; }}
h1 {{ font:700 clamp(1.6rem,4vw,2.3rem)/1.15 Georgia,"Times New Roman",serif; margin:0 0 8px; letter-spacing:-.01em; }}
.sub {{ color:var(--muted); margin:0 0 24px; max-width:70ch; }}
.meta {{ font-size:.85rem; color:var(--muted); margin-bottom:24px; }}
.note {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent);
  padding:12px 16px; border-radius:6px; margin:0 0 24px; font-size:.92rem; }}
.legend {{ list-style:none; display:flex; flex-wrap:wrap; gap:10px 18px; padding:0; margin:0 0 20px; }}
.legend li {{ display:flex; align-items:center; gap:8px; font-size:.88rem; }}
.swatch {{ width:16px; height:16px; border-radius:4px; border:2px solid; }}
.legend .r-same .swatch {{ background:var(--same); border-color:var(--same-b); }}
.legend .r-similar .swatch {{ background:var(--similar); border-color:var(--similar-b); }}
.legend .r-path .swatch {{ background:var(--path); border-color:var(--path-b); }}
.legend .r-diff .swatch {{ background:var(--diff); border-color:var(--diff-b); }}
.scroll {{ overflow-x:auto; border:1px solid var(--line); border-radius:8px; background:var(--card); }}
table {{ border-collapse:separate; border-spacing:0; width:100%; min-width:760px; }}
thead th {{ position:sticky; top:0; z-index:2; background:var(--card); text-align:left;
  padding:14px 14px; border-bottom:2px solid var(--line); vertical-align:bottom; }}
.vname {{ font-weight:700; font-size:1.1rem; }}
.vfw {{ font-weight:400; font-size:.8rem; color:var(--muted); margin-top:2px; }}
tbody th[scope=row] {{ text-align:left; width:170px; padding:14px; vertical-align:top;
  font-weight:600; font-size:.92rem; border-bottom:1px solid var(--line);
  background:var(--card); position:sticky; left:0; z-index:1; }}
td {{ padding:12px 14px; vertical-align:top; border-bottom:1px solid var(--line);
  border-left:1px solid var(--line); font-size:.9rem; }}
td p {{ margin:0 0 8px; }}
td ul {{ margin:0; padding-left:18px; }}
td li {{ margin-bottom:5px; }}
.badge {{ display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.03em;
  text-transform:uppercase; padding:2px 8px; border-radius:99px; margin-bottom:8px;
  border:1.5px solid currentColor; }}
.links {{ display:flex; flex-wrap:wrap; gap:4px 12px; font-size:.8rem; }}
a {{ color:var(--accent); text-underline-offset:2px; }}
a:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; border-radius:2px; }}
td.r-base {{ background:var(--base); }}  td.r-base .badge {{ color:var(--base-b); }}
td.r-same {{ background:var(--same); }}  td.r-same .badge {{ color:var(--same-b); }}
td.r-similar {{ background:var(--similar); }} td.r-similar .badge {{ color:var(--similar-b); }}
td.r-path {{ background:var(--path); }}  td.r-path .badge {{ color:var(--path-b); }}
td.r-diff {{ background:var(--diff); }}  td.r-diff .badge {{ color:var(--diff-b); }}
tr.assess td {{ background:transparent; }}
tr.assess th[scope=row] {{ color:var(--accent); }}
h2 {{ font:700 1.2rem/1.3 Georgia,serif; margin:40px 0 10px; }}
.src {{ padding-left:18px; }} .src li {{ margin-bottom:6px; }}
.pending {{ color:var(--muted); font-size:.92rem; }}
footer {{ margin-top:40px; color:var(--muted); font-size:.82rem; border-top:1px solid var(--line); padding-top:16px; }}
@media (max-width:640px) {{ tbody th[scope=row] {{ width:120px; font-size:.82rem; }} }}
@media print {{ thead th, tbody th[scope=row] {{ position:static; }} }}
</style>
</head>
<body>
<main class="wrap">
  <h1>{e(d["title"])}</h1>
  <p class="sub">What each vendor recommends for an AI-native software development lifecycle, and where they agree or differ. Anthropic's playbook is used as the baseline; every other vendor is rated against it.</p>
  <p class="meta">Last updated {e(d["updated"])} &middot; Vendors reviewed: {", ".join(e(v["name"]) for v in vendors)} &middot; Coming next: {pending}</p>
  <div class="note"><strong>How to read this.</strong> Rows marked "our assessment" are the author's judgement, not vendor claims. Colour shows how a vendor's approach relates to the baseline; the label in each cell says the same in words. Each cell links to the section it is based on.</div>
  <ul class="legend" aria-label="Colour legend">{legend}</ul>
  <div class="scroll">
  <table>
    <thead><tr><th scope="col">Topic</th>{head}</tr></thead>
    <tbody>
{chr(10).join(rows)}
    </tbody>
  </table>
  </div>
  <h2>Grounding sources</h2>
  <ul class="src">{src_items}</ul>
  <h2>Independent commentary</h2>
  <ul class="src">{tp_items}</ul>
  <footer>Based on public vendor pages only. Vendor figures are vendor-reported and not independently verified. Personal project; views are the author's own and do not represent any employer or client.</footer>
</main>
</body>
</html>
"""
(root / "index.html").write_text(page)
print("wrote index.html", len(page), "bytes")
