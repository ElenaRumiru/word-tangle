"""Inject base64 assets into template.html -> index.html (self-contained fragment for Artifact)."""
import json, re
from pathlib import Path

HERE = Path(__file__).parent
tpl = (HERE / "template.html").read_text(encoding="utf-8")
assets = json.loads((HERE / "_assets.json").read_text(encoding="utf-8"))

missing = set(re.findall(r"\{\{(\w+)\}\}", tpl)) - set(assets)
if missing:
    raise SystemExit(f"Missing assets referenced by template: {sorted(missing)}")

for key, uri in assets.items():
    tpl = tpl.replace("{{" + key + "}}", uri)

out = HERE / "index.html"
out.write_text(tpl, encoding="utf-8")
print(f"Built {out.name}: {out.stat().st_size/1024:.0f} KB, {len(assets)} assets embedded")
