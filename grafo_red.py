from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).parent

C = {"R4": "#7a7a7a", "L1": "#CE1126", "L4": "#E8A000", "L5": "#005A97"}

ORIG, DEST = "Manresa", "Ciutadella"
NODES = {
    "Manresa":       (0.6, 6.4),
    "La Sagrera":    (5.6, 5.2),
    "La Pau":        (9.2, 3.7),
    "Verdaguer":     (1.7, 3.7),
    "Urquinaona":    (2.6, 1.5),
    "Arc de Triomf": (4.6, 2.5),
    "Ciutadella":    (6.4, 0.3),
}

NODE_LABELS = {
    "Manresa":       (0.6, 6.95, "center", "Manresa (origin)"),
    "La Sagrera":    (5.6, 5.75, "center", "La Sagrera"),
    "La Pau":        (9.2, 4.25, "center", "La Pau"),
    "Verdaguer":     (1.25, 3.7, "right", "Verdaguer"),
    "Urquinaona":    (2.15, 1.5, "right", "Urquinaona"),
    "Arc de Triomf": (5.05, 2.65, "left", "Arc de Triomf"),
    "Ciutadella":    (6.85, 0.3, "left", "Ciutadella | Vila Olímpica\n(UPF, destination)"),
}

EDGES = [
    ("Manresa", "La Sagrera", "R4", "R4 · 71 min", -0.08, False, 0.50, (0.0, 0.45)),
    ("Manresa", "Arc de Triomf", "R4", "R4 · 78 min", 0.12, False, 0.22, (-0.55, -0.1)),
    ("Arc de Triomf", "Urquinaona", "L1", "L1 · 1.05 min", 0.0, False, 0.50, (0.1, -0.42)),
    ("La Sagrera", "Urquinaona", "L1", "L1 · 9.19 min", 0.0, False, 0.30, (0.75, -0.05)),
    ("La Sagrera", "Verdaguer", "L5", "L5 · 6.77 min", 0.12, False, 0.50, (0.0, 0.55)),
    ("Verdaguer", "Urquinaona", "L4", "L4 · 5.20 min", 0.0, False, 0.50, (-0.75, 0.0)),
    ("Urquinaona", "Ciutadella", "L4", "L4 · 4.37 min", 0.10, False, 0.50, (-0.1, -0.5)),
    ("La Pau", "Ciutadella", "L4", "L4 · 12.33 min", -0.10, False, 0.50, (0.75, -0.2)),
    ("La Sagrera", "La Pau", "L4", "L4 extension · 5.14 min\n(via Sagrera-AV, Santander)",
     -0.15, True, 0.50, (0.55, 0.55)),
]

plt.rcParams["font.family"] = "DejaVu Sans"
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(-0.6, 10.6)
ax.set_ylim(-0.6, 7.2)
ax.axis("off")

DASH = (0, (4, 2.5))
R = 0.32

for a, b, line, label, rad, dashed, lpos, (dx, dy) in EDGES:
    (x1, y1), (x2, y2) = NODES[a], NODES[b]
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle="-|>,head_length=9,head_width=5",
        color=C[line], lw=3.2, linestyle=DASH if dashed else "-",
        shrinkA=22, shrinkB=22, zorder=2,
    ))
    ax.text(x1 + (x2 - x1) * lpos + dx, y1 + (y2 - y1) * lpos + dy, label,
            fontsize=9.5, color="#222", ha="center", va="center", zorder=5,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=C[line], lw=1))

for name, (x, y) in NODES.items():
    filled = name in (ORIG, DEST)
    ax.add_patch(plt.Circle((x, y), R, fc="#222" if filled else "white",
                            ec="#222", lw=2, zorder=4))

for x, y, ha, text in NODE_LABELS.values():
    ax.text(x, y, text, fontsize=11, fontweight="bold", ha=ha, va="center", zorder=6)

legend = [
    Line2D([0], [0], color=C["R4"], lw=3, label="Rodalies R4 (no congestion)"),
    Line2D([0], [0], color=C["L1"], lw=3, label="L1 → Hospital de Bellvitge"),
    Line2D([0], [0], color=C["L5"], lw=3, label="L5 → Cornellà Centre"),
    Line2D([0], [0], color=C["L4"], lw=3, label="L4 → La Pau (R1–R3) / → Trinitat Nova (R4)"),
    Line2D([0], [0], color=C["L4"], lw=3, ls=DASH, label="New L4 link (extended network G₁ only)"),
]
leg = ax.legend(handles=legend, loc="upper right", fontsize=9.5, frameon=True)
leg.get_frame().set_edgecolor("#bbb")

ax.text(10.55, -0.45,
        "Routes: R1 Arc–L1–Urquinaona–L4 · R2 Sagrera–L1–Urquinaona–L4 · "
        "R3 Sagrera–L5–Verdaguer–L4 · R4 Sagrera–new L4–La Pau–L4",
        fontsize=8.3, ha="right", va="bottom", color="#444")

fig.tight_layout()
fig.savefig(OUT / "network_graph.png", dpi=300)
fig.savefig(OUT / "network_graph.svg")
plt.show()