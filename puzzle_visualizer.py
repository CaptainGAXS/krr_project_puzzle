"""
Script pour coller une entrée ASP, visualiser les pièces sélectionnées avec la couleur du matériau, puis afficher la solution comme visualise_tower.py.
"""
import re
import sys
import numpy as np
import matplotlib.pyplot as plt

# --- Couleurs associées aux matériaux ---
MATERIAL_COLORS = {
    'iron': 'gray',
    'stone': 'saddlebrown',
    'wood': 'peru',
    'dirt': 'green',
    'unknown': 'purple',
    'inconnu': 'purple',
}

def parse_facts(input_str):
    facts = re.findall(r'(\w+\([^)]*\))', input_str)
    parsed = {}
    for fact in facts:
        m = re.match(r'(\w+)\(([^)]*)\)', fact)
        if m:
            pred, args = m.group(1), m.group(2).split(',')
            if pred not in parsed:
                parsed[pred] = []
            parsed[pred].append(tuple(arg.strip() for arg in args))
    return parsed

def show_piece(ax, voxels, color, title=None):
    if not voxels:
        ax.set_axis_off()
        return
    xs, ys, zs = zip(*voxels)
    X_max, X_min = max(xs), min(xs)
    Y_max, Y_min = max(ys), min(ys)
    Z_max, Z_min = max(zs), min(zs)
    size_x = X_max - X_min + 1
    size_y = Y_max - Y_min + 1
    size_z = Z_max - Z_min + 1
    arr = np.zeros((size_x, size_y, size_z), dtype=bool)
    for (x, y, z) in voxels:
        arr[x - X_min, y - Y_min, z - Z_min] = True
    ax.voxels(arr, edgecolor='black', facecolor=color, alpha=0.9)
    ax.set_box_aspect((size_x, size_y, size_z))
    ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=10, pad=0)

def show_tower(voxels, colors, legend_handles=None, layer_weights=None):
    if not voxels:
        print("No piece to display.")
        return
    xs, ys, zs = zip(*voxels)
    X_max, X_min = max(xs), min(xs)
    Y_max, Y_min = max(ys), min(ys)
    Z_max, Z_min = max(zs), min(zs)
    size_x = X_max - X_min + 1
    size_y = Y_max - Y_min + 1
    size_z = Z_max - Z_min + 1
    arr = np.zeros((size_x, size_y, size_z), dtype=bool)
    color_arr = np.empty(arr.shape, dtype=object)
    for (x, y, z), color in zip(voxels, colors):
        arr[x - X_min, y - Y_min, z - Z_min] = True
        color_arr[x - X_min, y - Y_min, z - Z_min] = color
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.voxels(arr, facecolors=color_arr, edgecolor='k', linewidth=0.5)
    ax.set_box_aspect((size_x, size_y, size_z))
    ax.set_axis_off()
    plt.title("Solution (Tower)")
    if legend_handles:
        ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1.05, 0.5), title="Material & Weight")
    if layer_weights:
        weight_text = "Layer weights:\n" + "\n".join([f"Layer {z}: {w}" for z, w in sorted(layer_weights.items())[::-1]])
        fig.text(0.02, 0.5, weight_text, fontsize=10, va='center', bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
    plt.show()

def main():
    print("Paste your ASP input and press Ctrl+D (or Ctrl+Z on Windows) to finish:")
    input_str = sys.stdin.read()
    facts = parse_facts(input_str)

    material_map = {piece: mat for piece, mat in facts.get('material', [])}
    material_weight = {mat: w for mat, w in facts.get('material_weight', [])}
    selected = [p[0] for p in facts.get('selected_piece', [])]
    occs = facts.get('occ', [])
    occ_by_piece = {}
    for piece, x, y, z in occs:
        occ_by_piece.setdefault(piece, []).append((int(x), int(y), int(z)))
    layer_weights = {int(z): int(w) for z, w in facts.get('layer_weight', [])}

    # Préparer la légende matériaux/poids
    import matplotlib.patches as mpatches
    mats_in_selection = set(material_map.get(piece, 'unknown') for piece in selected)
    legend_handles = []
    for mat in sorted(mats_in_selection):
        color = MATERIAL_COLORS.get(mat, 'purple')
        weight = material_weight.get(mat, '?')
        label = f"{mat.capitalize()} ({weight})"
        patch = mpatches.Patch(color=color, label=label)
        legend_handles.append(patch)

    # Affichage des pièces sélectionnées
    n = len(selected)
    if n == 0:
        print("No selected piece.")
        return
    fig, axs = plt.subplots(1, n, figsize=(3*n+2, 3), subplot_kw={'projection': '3d'})
    if n == 1:
        axs = [axs]
    for ax, piece in zip(axs, selected):
        voxels = occ_by_piece.get(piece, [])
        color = MATERIAL_COLORS.get(material_map.get(piece, 'wood'), 'peru')
        show_piece(ax, voxels, color=color, title=piece)
    # Légende à droite
    fig.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1.01, 0.5), title="Material & Weight")
    plt.suptitle("Selected pieces")
    plt.tight_layout(rect=[0, 0, 0.88, 1])
    plt.show()

    # Affichage de la solution (tour)
    all_voxels = []
    all_colors = []
    for piece in selected:
        voxels = occ_by_piece.get(piece, [])
        color = MATERIAL_COLORS.get(material_map.get(piece, 'wood'), 'peru')
        all_voxels.extend(voxels)
        all_colors.extend([color]*len(voxels))
    show_tower(all_voxels, all_colors, legend_handles=legend_handles, layer_weights=layer_weights)

if __name__ == "__main__":
    main()
