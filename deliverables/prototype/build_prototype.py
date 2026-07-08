"""
build_prototype.py — assemble the self-contained prototype.

Reads:
  jumble-mobile.template.html   (game code with __LEVELS_JSON__ / __IMAGES_JSON__ markers)
  ../levels/levels.json          (the 10 levels)
  ../art/level-01..10.png        (cartoons; optional — placeholders shown if absent)

Writes:
  jumble-mobile.html             (single offline file: levels + base64 images inlined)

Re-run any time levels or art change. Images are re-encoded to JPEG q72 to keep the
file small enough to open instantly and to publish as an Artifact (no external requests).
"""
import base64, io, json, re
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE / "jumble-mobile.template.html"
OUT = HERE / "jumble-mobile.html"
LEVELS = HERE.parent / "levels" / "levels.json"
ART = HERE.parent / "art"

try:
    from PIL import Image
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False


def encode_image(png: Path) -> str:
    raw = png.read_bytes()
    if HAVE_PIL:
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        # cap the long side so 10 images stay light
        maxside = 900
        if max(im.size) > maxside:
            r = maxside / max(im.size)
            im = im.resize((int(im.size[0] * r), int(im.size[1] * r)))
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=72, optimize=True)
        b = buf.getvalue()
        return "data:image/jpeg;base64," + base64.b64encode(b).decode()
    return "data:image/png;base64," + base64.b64encode(raw).decode()


def main():
    tpl = TEMPLATE.read_text(encoding="utf-8")
    levels_json = LEVELS.read_text(encoding="utf-8")

    images = {}
    if ART.exists():
        for lvl in json.loads(levels_json)["levels"]:
            f = ART / f"level-{lvl['id']:02d}.png"
            if f.exists():
                images[str(lvl["id"])] = encode_image(f)

    html = tpl.replace("__LEVELS_JSON__", levels_json)
    html = html.replace("__IMAGES_JSON__", json.dumps(images))
    OUT.write_text(html, encoding="utf-8")

    kb = OUT.stat().st_size / 1024
    print(f"Built {OUT.name}: {len(images)}/10 images embedded, {kb:.0f} KB"
          + ("" if images else "  (placeholders — run again after art is ready)"))


if __name__ == "__main__":
    main()
