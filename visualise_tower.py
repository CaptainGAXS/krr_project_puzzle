"""
Visualiseur de tour 3D pour pentominos ASP.

Nécessite dans le programme ASP :
    #show occ/4.
    #show layer_weight/2.   % optionnel mais recommandé

Usage:
    clingo instance.lp | python visualize_tower.py instance.lp
    python visualize_tower.py instance.lp solution.txt
"""

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D  # noqa

# ------------------------------------------------------------------ #
#  Couleurs par matériau
# ------------------------------------------------------------------ #

MATERIAL_COLORS = {
    "iron":  (0.70, 0.72, 0.75, 0.92),
    "stone": (0.45, 0.45, 0.48, 0.92),
    "wood":  (0.76, 0.50, 0.22, 0.92),
    "dirt":  (0.52, 0.34, 0.18, 0.92),
}
MATERIAL_WEIGHTS = {"iron": 4, "stone": 3, "wood": 2, "dirt": 1}
DEFAULT_COLOR = (0.6, 0.2, 0.6, 0.9)

# ------------------------------------------------------------------ #
#  Parsing
# ------------------------------------------------------------------ #

def parse_lp_file(filename):
    """Lit material(P, Mat) et les dimensions depuis le fichier .lp."""
    materials = {}
    dims = {"w": 8, "d": 8, "h": 16}

    with open(filename) as f:
        content = f.read()

    for m in re.finditer(r'material\((\w+),\s*(\w+)\)', content):
        materials[m.group(1)] = m.group(2)

    for key in ("w", "d", "h"):
        m = re.search(rf'#const\s+{key}\s*=\s*(\d+)', content)
        if m:
            dims[key] = int(m.group(1))

    return materials, dims


def parse_clingo_output(text):
    """
    Lit depuis la sortie clingo :
        occ(P, X, Y, Z)
        layer_weight(Z, W)   (optionnel)
    """
    occ = {}
    layer_weights = {}

    for m in re.finditer(r'occ\((\w+),(-?\d+),(-?\d+),(-?\d+)\)', text):
        p = m.group(1)
        x, y, z = int(m.group(2)), int(m.group(3)), int(m.group(4))
        occ[(x, y, z)] = p

    for m in re.finditer(r'layer_weight\((-?\d+),(-?\d+)\)', text):
        layer_weights[int(m.group(1))] = int(m.group(2))

    return occ, layer_weights

# ------------------------------------------------------------------ #
#  Rendu
# ------------------------------------------------------------------ #

def build_voxel_arrays(occ, materials, W, D, H):
    filled = np.zeros((W, D, H), dtype=bool)
    colors = np.zeros((W, D, H, 4), dtype=float)

    for (x, y, z), piece in occ.items():
        if 0 <= x < W and 0 <= y < D and 0 <= z < H:
            filled[x, y, z] = True
            mat = materials.get(piece, "")
            colors[x, y, z] = MATERIAL_COLORS.get(mat, DEFAULT_COLOR)

    return filled, colors


def render(occ, materials, layer_weights, W, D, H):
    filled, colors = build_voxel_arrays(occ, materials, W, D, H)

    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor("#1a1a1a")

    # ---- Vue 3D ------------------------------------------ #
    ax3d = fig.add_axes([0.0, 0.0, 0.70, 1.0], projection="3d")
    ax3d.set_facecolor("#1a1a1a")
    ax3d.voxels(filled, facecolors=colors,
                edgecolor=(0, 0, 0, 0.35), linewidth=0.4)

    ax3d.set_xlabel("X", color="white", labelpad=6)
    ax3d.set_ylabel("Y", color="white", labelpad=6)
    ax3d.set_zlabel("Z (hauteur)", color="white", labelpad=6)
    ax3d.tick_params(colors="white", labelsize=7)
    for pane in (ax3d.xaxis.pane, ax3d.yaxis.pane, ax3d.zaxis.pane):
        pane.fill = False
        pane.set_edgecolor("#333333")
    ax3d.set_title("Tour 3D", color="white", fontsize=13, pad=12)

    # ---- Légende ----------------------------------------- #
    present_mats = {materials.get(p) for p in occ.values()} & MATERIAL_COLORS.keys()
    legend_handles = [
        mpatches.Patch(
            color=MATERIAL_COLORS[mat][:3],
            label=f"{mat.capitalize()}  (poids={MATERIAL_WEIGHTS[mat]})"
        )
        for mat in ("iron", "stone", "wood", "dirt")
        if mat in present_mats
    ]
    ax3d.legend(handles=legend_handles,
                loc="upper left",
                facecolor="#2a2a2a",
                edgecolor="#555",
                labelcolor="white",
                fontsize=8)

    # ---- Bar chart poids par étage ----------------------- #
    ax_bar = fig.add_axes([0.68, 0.10, 0.28, 0.80])
    ax_bar.set_facecolor("#1a1a1a")

    if layer_weights:
        zs = sorted(layer_weights)
        ws = [layer_weights[z] for z in zs]
        max_w = max(ws) if ws else 1
        bar_colors = [plt.cm.YlOrRd(w / max_w) for w in ws]
        bars = ax_bar.barh(zs, ws, color=bar_colors,
                           edgecolor="#333", linewidth=0.5, height=0.8)

        for bar, w in zip(bars, ws):
            ax_bar.text(bar.get_width() + max_w * 0.02,
                        bar.get_y() + bar.get_height() / 2,
                        str(w), va="center", color="white", fontsize=7)

        ax_bar.set_xlabel("Poids de l'étage", color="white", fontsize=9)
        ax_bar.set_ylabel("Z", color="white", fontsize=9)
        ax_bar.set_title("Poids par étage", color="white", fontsize=10)
        ax_bar.set_xlim(0, max_w * 1.15)
        ax_bar.invert_yaxis()
        ax_bar.tick_params(colors="white", labelsize=7)
        for spine in ax_bar.spines.values():
            spine.set_edgecolor("#444")
    else:
        ax_bar.text(0.5, 0.5,
                    "Pas de layer_weight\n(ajouter #show layer_weight/2.)",
                    ha="center", va="center", color="gray",
                    transform=ax_bar.transAxes, fontsize=8)

    plt.savefig("tower.png", dpi=150, bbox_inches="tight", facecolor="#1a1a1a")
    print("Sauvegardé → tower.png")
    plt.show()

# ------------------------------------------------------------------ #
#  Main
# ------------------------------------------------------------------ #

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    lp_file = sys.argv[1]

    if len(sys.argv) >= 3:
        with open(sys.argv[2]) as f:
            clingo_text = f.read()
    else:
        print("Lecture depuis stdin… (Ctrl-D pour terminer)")
        clingo_text = sys.stdin.read()

    print(f"Lecture des matériaux depuis {lp_file} …")
    materials, dims = parse_lp_file(lp_file)
    W, D, H = dims["w"], dims["d"], dims["h"]
    print(f"  Tour : {W}×{D}×{H}  —  {len(materials)} matériaux trouvés.")

    print("Parsing de la sortie clingo …")
    occ, layer_weights = parse_clingo_output(clingo_text)
    print(f"  {len(occ)} cubes placés, {len(layer_weights)} étages avec poids.")

    if not occ:
        print("[erreur] Aucun occ/4 trouvé.")
        print("         Vérifiez que #show occ/4. est dans le programme ASP.")
        sys.exit(1)

    print("Rendu …")
    render(occ, materials, layer_weights, W, D, H)


if __name__ == "__main__":
    main()
