"""
Render deliverable markdown docs as properly designed standalone HTML pages
(same visual identity as the case-study presentation) for GitHub Pages.

Outputs to repo:  /levels-design/index.html, /balance-notes/index.html, /monetization/index.html
"""
import re
from pathlib import Path
import markdown

HERE = Path(__file__).parent
REPO = HERE.parent.parent
SITE = "https://elenarumiru.github.io/word-tangle"

DOCS = [
    ("ux-concept",     REPO/"deliverables/levels/ux-concept.md",           "UX и управление · концепт"),
    ("levels-design",  REPO/"deliverables/levels/levels-design.md",        "Дизайн уровней · обоснование кривой"),
    ("balance-notes",  REPO/"deliverables/balance/balance-notes.md",       "Баланс · формула и веса"),
    ("monetization",   REPO/"deliverables/monetization/scroll-puzzle-hybrid.md", "Монетизация · полный план a→d"),
]

CSS = """
  :root{
    --paper:#F1EBDD; --card:#FBF8F1; --ink:#1B2430; --ink-2:#2A3541; --soft:#55606B;
    --faint:#8A8574; --line:#DcD2BF; --teal:#1F6E63; --teal-d:#17544c; --amber:#E2853F;
    --display:"Helvetica Neue",Arial,"Segoe UI",system-ui,sans-serif;
    --body:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
    --mono:"SF Mono","Cascadia Code",Consolas,ui-monospace,monospace;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);line-height:1.65;
    -webkit-font-smoothing:antialiased}
  .topbar{position:sticky;top:0;z-index:10;background:rgba(241,235,221,.92);backdrop-filter:blur(8px);
    border-bottom:1px solid var(--line);padding:11px 22px;display:flex;align-items:center;gap:14px}
  .topbar a.back{font-family:var(--mono);font-size:12.5px;font-weight:700;color:var(--teal-d);
    text-decoration:none;display:inline-flex;gap:6px;align-items:center}
  .topbar a.back:hover{color:var(--teal)}
  .topbar .lbl{font-family:var(--mono);font-size:11px;letter-spacing:.09em;text-transform:uppercase;
    color:var(--soft);margin-left:auto}
  .hero{max-width:800px;margin:0 auto;padding:44px 24px 6px}
  .hero .eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;
    color:var(--teal);font-weight:600}
  .hero h1{font-family:var(--display);font-weight:800;font-size:clamp(28px,4.6vw,42px);
    letter-spacing:-.02em;margin:12px 0 0;text-wrap:balance;line-height:1.05}
  .article{max-width:760px;margin:0 auto;padding:22px 24px 90px}
  .article>*:first-child{margin-top:0}
  .article h2{font-family:var(--display);font-weight:800;font-size:25px;margin:40px 0 12px;
    padding-top:18px;border-top:1px solid var(--line);letter-spacing:-.01em}
  .article h3{font-family:var(--display);font-weight:700;font-size:19px;margin:26px 0 8px}
  .article h4{font-family:var(--display);font-weight:700;font-size:16px;margin:20px 0 6px;color:var(--teal-d)}
  .article p{margin:0 0 14px}
  .article ul,.article ol{margin:0 0 15px;padding-left:22px}
  .article li{margin:5px 0}
  .article li>ul,.article li>ol{margin:6px 0}
  .article a{color:var(--teal-d);text-underline-offset:3px}
  .article strong{color:var(--ink);font-weight:700}
  .article code{font-family:var(--mono);font-size:.88em;background:#ece2cd;padding:1px 6px;
    border-radius:5px;color:#8a5a24;word-break:break-word}
  .article pre{background:var(--ink);color:#EFE7D6;padding:16px 18px;border-radius:12px;
    overflow-x:auto;font-family:var(--mono);font-size:13px;line-height:1.55;margin:0 0 16px}
  .article pre code{background:none;padding:0;color:inherit;font-size:inherit}
  .article blockquote{border-left:3px solid var(--teal);background:var(--card);margin:0 0 15px;
    padding:12px 16px;border-radius:0 10px 10px 0;color:var(--ink-2)}
  .article blockquote p:last-child{margin:0}
  .article hr{border:none;border-top:1px solid var(--line);margin:30px 0}
  /* custom tables — same un-generic style as the deck */
  .tblwrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--card);margin:0 0 18px}
  table.tbl{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;min-width:520px}
  table.tbl thead th{background:var(--ink);color:#EFE7D6;font-family:var(--mono);font-size:11px;
    font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:11px 14px;text-align:left;white-space:nowrap}
  table.tbl tbody td{padding:10px 14px;border-top:1px solid var(--line);font-size:13.5px;color:var(--ink-2);vertical-align:top}
  table.tbl tbody tr:nth-child(even){background:rgba(31,110,99,.045)}
  table.tbl tbody td code{background:#e4dcc8}
  .docfoot{max-width:760px;margin:0 auto;padding:22px 24px 60px;border-top:1px solid var(--line);
    color:var(--faint);font-size:13px}
  .docfoot a{color:var(--teal-d)}
  @media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

MD_EXT = ["tables", "fenced_code", "sane_lists", "attr_list", "nl2br"]


def render(md_text: str):
    html = markdown.markdown(md_text, extensions=MD_EXT)
    # pull first <h1> out as the page title, drop it from the body
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else "Документ"
    if m:
        html = html[:m.start()] + html[m.end():]
    # wrap tables for horizontal scroll + apply the custom class
    html = html.replace("<table>", '<div class="tblwrap"><table class="tbl">').replace("</table>", "</table></div>")
    return title, html


PAGE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Word Tangle</title>
<style>{css}</style>
</head>
<body>
<div class="topbar">
  <a class="back" href="{site}/">← Word Tangle · case study</a>
  <span class="lbl">{eyebrow}</span>
</div>
<header class="hero">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{title}</h1>
</header>
<main class="article">
{content}
</main>
<footer class="docfoot">
  Документ проекта Word Tangle. <a href="{site}/">← вернуться к презентации</a>
</footer>
</body>
</html>
"""


def main():
    for slug, path, eyebrow in DOCS:
        title, content = render(path.read_text(encoding="utf-8"))
        out_dir = REPO / slug
        out_dir.mkdir(exist_ok=True)
        page = PAGE.format(title=title, css=CSS, site=SITE, eyebrow=eyebrow, content=content)
        (out_dir / "index.html").write_text(page, encoding="utf-8")
        print(f"  /{slug}/  <- {path.name}  ({len(page)//1024} KB)")


if __name__ == "__main__":
    main()
