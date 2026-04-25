import re
import sys
import numpy as np
import matplotlib.pyplot as plt

def read_materials(db_path="pieces.db"):
    """Lit le fichier pieces.db pour extraire les matériaux associés aux pièces."""
    materials = {}
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Cherche material(piece, materiel).
            matches = re.findall(r'material\(([^,]+),\s*([^)]+)\)\.', content)
            for piece, mat in matches:
                materials[piece.strip()] = mat.strip()
    except FileNotFoundError:
        print(f"Attention : {db_path} introuvable.")
    return materials

def parse_clingo_input(text):
    """Extrait tous les occ(P,X,Y,Z) et layer_weight(Z,W) d'une chaîne de texte."""
    parsed_occ = []
    weights = {}
    
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
        
    return parsed_occ, max_x + 1, max_y + 1, max_z + 1, weights

def visualize(parsed_data, dimensions, materials, weights):
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
    # Palettes de couleurs (colormaps) par matériau
    base_cmaps = {
        'iron': 'Blues',    # Nuances de bleu
        'stone': 'Greys',   # Nuances de gris (clair à foncé)
        'wood': 'Oranges',  # Nuances de orange/brun
        'dirt': 'Greens',   # Nuances de vert
        'inconnu': 'Purples'# Violet par défaut
    }
    
    for mat, pieces in material_groups.items():
        cmap_name = base_cmaps.get(mat.lower(), 'Purples')
        cmap = plt.get_cmap(cmap_name)
        n_pieces = len(pieces)
        for i, p in enumerate(pieces):
            # On prend des teintes entre 0.4 (déjà bien visible) et 0.9 (foncé)
            shade = 0.6 if n_pieces == 1 else 0.4 + (0.5 * i / (n_pieces - 1))
            piece_colors[p] = cmap(shade)

    # Remplit la grille 3D
    for piece, x, y, z in parsed_data:
        filled[x, y, z] = True
        colors[x, y, z] = piece_colors[piece]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Affiche les voxels
    ax.voxels(filled, facecolors=colors, edgecolors='k', linewidth=0.5)

    # Légende avec les pièces et leur matériaux
    import matplotlib.patches as mpatches
    legend_handles = []
    for piece in unique_pieces:
        color = piece_colors[piece]
        mat = materials.get(piece, "inconnu")
        label = f"Pièce: {piece} ({mat})"
        patch = mpatches.Patch(color=color, label=label)
        legend_handles.append(patch)

    ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1.05, 0.5), title="Pièces & Matériaux")
    
    if weights:
        weight_text = "Poids par couche:\n" + "\n".join([f"Couche {z}: {w} kg" for z, w in sorted(weights.items())[::-1]])
        fig.text(0.02, 0.5, weight_text, fontsize=10, va='center', bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))

    ax.set_xlabel('Largeur (X)')
    ax.set_ylabel('Profondeur (Y)')
    ax.set_zlabel('Hauteur (Z)')
    ax.set_title('Visualisation de la Tour 3D')
    
    # Ajustement de l'affichage pour montrer la bonne échelle
    ax.set_box_aspect([max_x, max_y, max_z])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Collez la sortie de clingo contenant vos occ(...) puis appuyez sur Entrée pour valider :")
    try:
        user_input = input()
    except KeyboardInterrupt:
        print("\nAnnulé.")
        sys.exit(0)

    # Chargement
    materials = read_materials("pieces.db")
    parsed_data, dim_x, dim_y, dim_z, weights = parse_clingo_input(user_input)
    
    # Affichage
    visualize(parsed_data, (dim_x, dim_y, dim_z), materials, weights)
