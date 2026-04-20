import matplotlib.pyplot as plt
import numpy as np
import re
import math

def lire_pieces(filepath):
    pieces = {}
    with open(filepath, 'r') as f:
        for line in f:
            # Cherche les motifs de type bit(nom_piece, x, y, z)
            matches = re.finditer(r'bit\(([^,]+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)', line)
            for m in matches:
                name = m.group(1).strip()
                x = int(m.group(2))
                y = int(m.group(3))
                z = int(m.group(4))
                
                if name not in pieces:
                    # On utilise un set pour éviter les doublons (par ex: dans bit(3b, 0, 1, 0))
                    pieces[name] = set() 
                pieces[name].add((x, y, z))
                
    # Conversion du set en liste
    return {k: list(v) for k, v in pieces.items()}

def afficher_pieces_3d(pieces):
    num_pieces = len(pieces)
    cols = 10  # Plus de colonnes pour moins d'espacement vertical
    rows = math.ceil(num_pieces / cols)
    
    # Ajustement de la taille de la figure pour éviter l'écrasement
    fig = plt.figure(figsize=(12, 2.5 * rows))
    fig.suptitle('Visualisation des pièces 3D', fontsize=16)
    
    for i, (name, coords) in enumerate(pieces.items(), 1):
        ax = fig.add_subplot(rows, cols, i, projection='3d')
        
        if not coords:
            continue
            
        # Trouver les bornes pour centrer et dimensionner les voxels
        xs, ys, zs = zip(*coords)
        X_max, X_min = max(xs), min(xs)
        Y_max, Y_min = max(ys), min(ys)
        Z_max, Z_min = max(zs), min(zs)
        
        # Dimensions exactes de la pièce
        size_x = X_max - X_min + 1
        size_y = Y_max - Y_min + 1
        size_z = Z_max - Z_min + 1
        
        # Création de la grille de voxels ajustée à la pièce
        voxels = np.zeros((size_x, size_y, size_z), dtype=bool)
        
        for (x, y, z) in coords:
            voxels[x - X_min, y - Y_min, z - Z_min] = True
            
        # Affichage
        ax.voxels(voxels, edgecolor='black', facecolors='#1f77b4', alpha=0.8)
        ax.set_title(f'Pièce : {name} ({len(coords)} cubes)', fontsize=10, pad=0)
        
        # Cette ligne est la clé : elle force les proportions de la "boîte 3D" 
        # à correspondre exactement au nombre de cubes (size_x, size_y, size_z).
        # Ainsi 1 unité en X == 1 unité en Y == 1 unité en Z -> de vrais cubes !
        ax.set_box_aspect((size_x, size_y, size_z))
        
        # Masquer les axes pour un rendu plus propre
        ax.set_axis_off()
        
    plt.tight_layout()
    # Espace supplémentaire pour le titre principal
    plt.subplots_adjust(top=0.9)
    
    # Sauvegarde en haute qualité (pratique s'il y a beaucoup de pièces)
    plt.savefig('pieces_3d_hd.png', dpi=300, bbox_inches='tight')
    
    plt.show()

if __name__ == "__main__":
    # Assurez-vous que le chemin vers pieces.db est correct
    fichier_db = 'pieces.db'
    try:
        pieces = lire_pieces(fichier_db)
        afficher_pieces_3d(pieces)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier_db}' est introuvable.")