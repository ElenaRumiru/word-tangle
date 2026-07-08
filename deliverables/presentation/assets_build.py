"""
Build all embedded assets for the case-study presentation:
  - two matplotlib charts (difficulty curve, ARPDAU before/after) styled to the deck palette
  - downscaled JPEG data-URIs for screenshots and cartoons
Writes _assets.json  { key: "data:...base64,..." }  consumed by build_presentation.py
"""
import base64, io, json, csv
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
OUT = HERE / "_assets.json"

# ---- palette (must match the HTML) ----
PAPER   = "#F1EBDD"
CARD    = "#FBF8F1"
INK     = "#1B2430"
INKSOFT = "#55606B"
TEAL    = "#1F6E63"
AMBER   = "#E2853F"
GOLD    = "#C29A2E"
GREEN   = "#2E8B57"
LINE    = "#D8CEBB"

assets = {}


def png_to_datauri(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor="none", transparent=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def img_to_datauri(path: Path, maxw: int, q: int = 72):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.size[0] > maxw:
        r = maxw / im.size[0]
        im = im.resize((maxw, int(im.size[1] * r)))
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ============================================================== charts
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": INKSOFT, "ytick.color": INKSOFT,
    "axes.edgecolor": LINE, "axes.linewidth": 1.0,
})

# ---- Chart 1: difficulty curve over 100 levels ----
rows = list(csv.DictReader(open(ROOT / "balance/balance-100-levels.csv", encoding="utf-8")))
levels = [int(r["level"]) for r in rows]
scores = [float(r["difficulty_score"]) for r in rows]
anchors = {1:1.0,12:1.6,23:2.3,34:3.4,45:3.0,56:4.2,67:5.0,78:4.6,89:5.6,100:6.8}

fig, ax = plt.subplots(figsize=(9.6, 4.2))
ax.plot(levels, scores, color=TEAL, lw=2.4, zorder=3)
ax.fill_between(levels, scores, color=TEAL, alpha=0.10, zorder=1)
ax.scatter(list(anchors), [scores[k-1] for k in anchors], s=64,
           color=AMBER, edgecolor="white", lw=1.6, zorder=5)
for k in (1,34,67,100):
    ax.annotate(f"ур.{k}", (k, scores[k-1]), textcoords="offset points",
                xytext=(0,10), ha="center", fontsize=9, color=INK, fontweight="bold")
ax.set_xlim(0,101); ax.set_ylim(0, 7.3)
ax.set_xlabel("Уровень (1–100)", fontsize=10)
ax.set_ylabel("difficulty score", fontsize=10)
ax.grid(axis="y", color=LINE, lw=0.7, alpha=0.7)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.margins(x=0)
assets["chart_curve"] = png_to_datauri(fig)
plt.close(fig)

# ---- Chart 2: ARPDAU before -> after (stacked) ----
labels = ["До\n(ads-only)", "После U3\n(гибрид)"]
inter  = [0.0585, 0.0347]
rew    = [0.0,    0.0160]
iap    = [0.0,    0.0925]
fig, ax = plt.subplots(figsize=(5.6, 4.4))
w = 0.55
b1 = ax.bar(labels, inter, w, label="Interstitial", color=AMBER)
b2 = ax.bar(labels, rew, w, bottom=inter, label="Rewarded", color=GOLD)
b3 = ax.bar(labels, iap, w, bottom=[i+r for i,r in zip(inter,rew)], label="IAP", color=TEAL)
tot = [i+r+p for i,r,p in zip(inter,rew,iap)]
for x,t in enumerate(tot):
    ax.annotate(f"${t:.4f}", (x, t), textcoords="offset points", xytext=(0,6),
                ha="center", fontsize=11, fontweight="bold", color=INK)
ax.annotate("+145%", (1, tot[1]/2), ha="center", fontsize=15, fontweight="bold",
            color="white")
ax.set_ylabel("ARPDAU, $", fontsize=10)
ax.set_ylim(0, 0.163)
ax.grid(axis="y", color=LINE, lw=0.7, alpha=0.7)
for s in ("top","right"): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc="upper left")
assets["chart_arpdau"] = png_to_datauri(fig)
plt.close(fig)

# ============================================================== photos
SH = ROOT / "prototype/screenshots"
for key, f, w in [
    ("shot_home",   SH/"home.jpeg",        380),
    ("shot_map",    SH/"map.jpeg",         380),
    ("shot_answer", SH/"level4-answer.jpeg",420),
    ("shot_win",    SH/"win.jpeg",         380),
    ("shot_l10",    SH/"level10-clean.jpeg",380),
]:
    if f.exists():
        assets[key] = img_to_datauri(f, w)

ART = ROOT / "art"
for i in (1,4,7,10):
    f = ART / f"level-{i:02d}.png"
    if f.exists():
        assets[f"art_{i:02d}"] = img_to_datauri(f, 460, 74)
if (ART/"contact-sheet.png").exists():
    assets["contact"] = img_to_datauri(ART/"contact-sheet.png", 1100, 76)

OUT.write_text(json.dumps(assets), encoding="utf-8")
sizes = {k: f"{len(v)//1024}KB" for k,v in assets.items()}
print("assets:", len(assets))
for k,v in sizes.items(): print(f"  {k}: {v}")
print("total:", sum(len(v) for v in assets.values())//1024, "KB (base64)")
