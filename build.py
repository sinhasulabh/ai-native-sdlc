#!/usr/bin/env python3
"""Generate comparison.html from data.json. Usage: python3 build.py"""
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
    "not-covered": ("Not covered in sources", "r-none"),
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
nextup = f" &middot; Coming next: {pending}" if pending else ""


# ---- summary section (computed counts + written patterns) ----
sm = d.get("summary", {})
content_rows = [r for r in d["rows"] if not r.get("assessment")]
order = ["same", "similar", "different-path", "different", "not-covered"]
bars = []
for v in vendors:
    if v["id"] == d["baseline"]:
        continue
    counts = {k: 0 for k in order}
    for r in content_rows:
        counts[r["cells"][v["id"]]["rating"]] += 1
    n = len(content_rows)
    segs = "".join(
        f'<span class="seg {RATINGS[k][1]}" style="flex:{counts[k]}" title="{e(RATINGS[k][0])}: {counts[k]}">{counts[k]}</span>'
        for k in order if counts[k]
    )
    close = counts["same"] + counts["similar"]
    bars.append(
        f'<div class="bar"><div class="bname">{e(v["name"])}</div>'
        f'<div class="track" role="img" aria-label="{e(v["name"])}: '
        + ", ".join(f"{counts[k]} {RATINGS[k][0].lower()}" for k in order if counts[k])
        + f'">{segs}</div><div class="bnote">{close} of {n} close to baseline</div></div>'
    )

def cards(items, with_who):
    out = []
    for it in items:
        who = f'<span class="who">{e(it["who"])}</span>' if with_who else ""
        out.append(f'<li><div class="ct">{e(it["title"])}{who}</div><p>{e(it["detail"])}</p></li>')
    return "".join(out)

summary_html = ""
if sm:
    summary_html = (
        '<section class="summary" aria-labelledby="sum-h">'
        '<h2 id="sum-h">The short version</h2>'
        '<div class="cols">'
        f'<div><h3>Where they agree</h3><ul class="cards">{cards(sm["common"], True)}</ul></div>'
        f'<div><h3>Where they differ</h3><ul class="cards">{cards(sm["differences"], False)}</ul></div>'
        '</div>'
        '<div class="take"><h3>Our read (assessment)</h3><ul>'
        + "".join(f"<li>{e(t)}</li>" for t in sm["takeaway"]) +
        '</ul></div>'
        '<h3>How closely each vendor matches Anthropic, topic by topic</h3>'
        f'<div class="bars">{"".join(bars)}</div>'
        '<p class="bars-note">"Close to baseline" means rated Same or Similar. Counts are table rows per rating, out of '
        f'{len(content_rows)}. Computed from the table below.</p>'
        '</section>'
    )

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
  --none:#f0efec;     --none-b:#6b6a66;
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
    --none:#262624;    --none-b:#a3a198;
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
.legend .r-none .swatch {{ background:var(--none); border-color:var(--none-b); border-style:dashed; }}
.scroll {{ overflow-x:auto; border:1px solid var(--line); border-radius:8px; background:var(--card); }}
table {{ border-collapse:separate; border-spacing:0; width:100%; min-width:{170 + 300*len(vendors)}px; table-layout:fixed; }}
thead th {{ position:sticky; top:0; z-index:2; background:var(--card); text-align:left;
  padding:14px 14px; border-bottom:2px solid var(--line); vertical-align:bottom; }}
.vname {{ font-weight:700; font-size:1.1rem; }}
.vfw {{ font-weight:400; font-size:.8rem; color:var(--muted); margin-top:2px; }}
thead th:first-child {{ width:170px; }}
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
td.r-none {{ background:var(--none); }}  td.r-none .badge {{ color:var(--none-b); border-style:dashed; }}
tr.assess td {{ background:transparent; }}
tr.assess th[scope=row] {{ color:var(--accent); }}
h2 {{ font:700 1.2rem/1.3 Georgia,serif; margin:40px 0 10px; }}
.summary {{ margin:0 0 32px; }}
.summary h2 {{ margin-top:0; }}
.summary h3 {{ font:700 .95rem/1.3 system-ui,sans-serif; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); margin:18px 0 8px; }}
.cols {{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
@media (max-width:820px) {{ .cols {{ grid-template-columns:1fr; }} }}
.cards {{ list-style:none; margin:0; padding:0; display:grid; gap:10px; }}
.cards li {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px 14px; }}
.cards p {{ margin:4px 0 0; font-size:.9rem; }}
.ct {{ font-weight:700; font-size:.95rem; display:flex; justify-content:space-between; gap:10px; align-items:baseline; }}
.who {{ font-size:.72rem; font-weight:700; text-transform:uppercase; letter-spacing:.03em; color:var(--same-b); border:1.5px solid currentColor; border-radius:99px; padding:1px 8px; white-space:nowrap; }}
.take {{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--accent); border-radius:6px; padding:4px 16px 8px; margin-top:20px; }}
.take ul {{ margin:0; padding-left:18px; }} .take li {{ margin-bottom:6px; }}
.bars {{ display:grid; gap:8px; }}
.bar {{ display:grid; grid-template-columns:90px 1fr 190px; gap:10px; align-items:center; font-size:.85rem; }}
@media (max-width:640px) {{ .bar {{ grid-template-columns:70px 1fr; }} .bnote {{ grid-column:1 / -1; }} }}
.bname {{ font-weight:600; }}
.track {{ display:flex; height:26px; border-radius:5px; overflow:hidden; border:1px solid var(--line); }}
.seg {{ display:flex; align-items:center; justify-content:center; font-weight:700; font-size:.78rem; min-width:22px; }}
.seg.r-same {{ background:var(--same); color:var(--same-b); }}
.seg.r-similar {{ background:var(--similar); color:var(--similar-b); }}
.seg.r-path {{ background:var(--path); color:var(--path-b); }}
.seg.r-diff {{ background:var(--diff); color:var(--diff-b); }}
.seg.r-none {{ background:var(--none); color:var(--none-b); }}
.bnote {{ color:var(--muted); }} .bars-note {{ color:var(--muted); font-size:.8rem; margin:8px 0 0; }}

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
  <div class="note"><strong>Companion page:</strong> <a href="index.html">AI-Native SDLC: Target Flow Design</a>, a first-principles target flow with six human gates.</div>
  <p class="meta">Last updated {e(d["updated"])} &middot; Vendors reviewed: {", ".join(e(v["name"]) for v in vendors)}{nextup}</p>
  <div class="note"><strong>How to read this.</strong> Rows marked "our assessment" are the author's judgement, not vendor claims. Colour shows how a vendor's approach relates to the baseline; the label in each cell says the same in words. Each cell links to the section it is based on.</div>
  {summary_html}
  <h2 id="table-h" style="margin-top:8px">The full comparison</h2>
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
(root / "comparison.html").write_text(page)
print("wrote comparison.html", len(page), "bytes")
