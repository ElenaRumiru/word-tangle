"""
Build the STANDALONE full-document presentation for GitHub Pages.
Injects base64 assets into template.html (fragment) and wraps it in a proper
<!doctype html> document with <meta charset=utf-8>. Writes to the repo root as index.html.
Also copies the self-contained prototype to /prototype/index.html.
"""
import json, re, shutil
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parent.parent                       # Testing Assignment/
tpl = (HERE / "template.html").read_text(encoding="utf-8")
assets = json.loads((HERE / "_assets.json").read_text(encoding="utf-8"))

for key, uri in assets.items():
    tpl = tpl.replace("{{" + key + "}}", uri)

title = re.search(r"<title>.*?</title>", tpl, re.S).group(0)
style = re.search(r"<style>.*?</style>", tpl, re.S).group(0)
body = tpl.split("</style>", 1)[1]              # everything after the style block

doc = (
    "<!DOCTYPE html>\n<html lang=\"ru\">\n<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    f"{title}\n{style}\n</head>\n<body>\n{body}\n</body>\n</html>\n"
)
(REPO / "index.html").write_text(doc, encoding="utf-8")

# prototype as a clean Pages path: /prototype/index.html
proto_dir = REPO / "prototype"
proto_dir.mkdir(exist_ok=True)
shutil.copy(REPO / "deliverables" / "prototype" / "jumble-mobile.html", proto_dir / "index.html")

print(f"Wrote {REPO/'index.html'} ({(REPO/'index.html').stat().st_size//1024} KB)")
print(f"Wrote {proto_dir/'index.html'} ({(proto_dir/'index.html').stat().st_size//1024} KB)")
