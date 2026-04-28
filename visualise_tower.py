import re
import sys
import numpy as np
import matplotlib.pyplot as plt

def parse_clingo_input(text):
    """Extrait tous les occ(P,X,Y,Z), layer_weight(Z,W), material(P,M) et material_weight(M,W) d'une chaîne de texte."""
    parsed_occ = []
    weights = {}
    materials = {}
    material_weights = {}
    
    # Parse material(...)
    matches_mat = re.findall(r'material\(([^,]+),\s*([^)]+)\)', text)
    for m in matches_mat:
        materials[m[0].strip()] = m[1].strip()
        
    # Parse material_weight(...)
    matches_mw = re.findall(r'material_weight\(([^,]+),\s*(\d+)\)', text)
    for m in matches_mw:
        material_weights[m[0].strip()] = int(m[1].strip())
    
    # Parse occ(...)
    pattern_occ = r'occ\(([^,]+),(\d+),(\d+),(\d+)\)'
    matches_occ = re.findall(pattern_occ, text)
    max_x, max_y, max_z = 0, 0, 0
    for match in matches_occ:
        piece = match[0]
        x, y, z = int(match[1]), int(match[2]), int(match[3])
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)
        parsed_occ.append((piece, x, y, z))
        
    # Parse layer_weight(...)
    pattern_weight = r'layer_weight\((\d+),\s*(\d+)\)'
    matches_weight = re.findall(pattern_weight, text)
    for match in matches_weight:
        z, w = int(match[0]), int(match[1])
        weights[z] = w
        
    return parsed_occ, max_x + 1, max_y + 1, max_z + 1, weights, materials, material_weights

def visualize(parsed_data, dimensions, materials, material_weights, weights):
    if not parsed_data:
        print("Aucune donnée occ(P,X,Y,Z) trouvée à visualiser.")
        return

    max_x, max_y, max_z = dimensions
    filled = np.zeros((max_x, max_y, max_z), dtype=bool)
    colors = np.empty(filled.shape, dtype=object)

    # Identifie toutes les pièces uniques
    unique_pieces = list(set(d[0] for d in parsed_data))
    
    # Assigne des nuances par matériau
    material_groups = {}
    for p in unique_pieces:
        mat = materials.get(p, 'inconnu')
        material_groups.setdefault(mat, []).append(p)

    piece_colors = {}
    # Palettes de couleurs (colormaps) par matériau et plages de teintes (min, max)
    base_cmaps = {
        'iron': ('Greys', 0.3, 0.5),     # Gris classique
        'stone': ('Greys', 0.6, 0.8),    # Gris foncé
        'wood': ('YlOrBr', 0.6, 0.9),    # Marron
        'dirt': ('Greys', 0.9, 1.0),     # Noir
        'inconnu': ('Purples', 0.4, 0.9)
    }
    
    for mat, pieces in material_groups.items():
        cmap_info = base_cmaps.get(mat.lower(), ('Purples', 0.4, 0.9))
        cmap_name, shade_min, shade_max = cmap_info
        cmap = plt.get_cmap(cmap_name)
        n_pieces = len(pieces)
        for i, p in enumerate(pieces):
            if n_pieces == 1:
                shade = (shade_min + shade_max) / 2
            else:
                shade = shade_min + (shade_max - shade_min) * (i / (n_pieces - 1))
            piece_colors[p] = cmap(shade)

    # Remplit la grille 3D
    for piece, x, y, z in parsed_data:
        filled[x, y, z] = True
        colors[x, y, z] = piece_colors[piece]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Affiche les voxels
    ax.voxels(filled, facecolors=colors, edgecolors='k', linewidth=0.5)

    # Légende avec les matériaux et leur poids
    import matplotlib.patches as mpatches
    legend_handles = []
    
    # On ajoute chaque matériau trouvé dans la tour à la légende
    for mat in sorted(material_groups.keys()):
        cmap_info = base_cmaps.get(mat.lower(), ('Purples', 0.4, 0.9))
        cmap_name, shade_min, shade_max = cmap_info
        cmap = plt.get_cmap(cmap_name)
        # On utilise une nuance moyenne pour représenter le matériau
        color = cmap((shade_min + shade_max) / 2)
        weight = material_weights.get(mat, "?")
        label = f"{mat.capitalize()} ({weight} kg/face)"
        patch = mpatches.Patch(color=color, label=label)
        legend_handles.append(patch)

    ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1.05, 0.5), title="Materials & Weights")
    
    if weights:
        weight_text = "Layer weights:\n" + "\n".join([f"Layer {z}: {w} kg" for z, w in sorted(weights.items())[::-1]])
        fig.text(0.02, 0.5, weight_text, fontsize=10, va='center', bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))

    # Masquer le quadrillage et les axes
    ax.set_axis_off()
    ax.set_title('3D Tower Visualization')
    
    # Ajustement de l'affichage pour montrer la bonne échelle
    ax.set_box_aspect([max_x, max_y, max_z])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Collez la sortie de clingo contenant vos occ(...), material(...) etc. puis appuyez sur Entrée pour valider :")
    try:
        user_input = input()
    except KeyboardInterrupt:
        print("\nAnnulé.")
        sys.exit(0)

    # Chargement
    parsed_data, dim_x, dim_y, dim_z, weights, materials, material_weights = parse_clingo_input(user_input)
    
    # Affichage
    visualize(parsed_data, (dim_x, dim_y, dim_z), materials, material_weights, weights)
