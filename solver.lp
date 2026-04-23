% The tower
width(8). depth(8). height(16). 

cube(X, Y, Z) :- width(W), depth(D), height(H), X=0..W-1, Y=0..D-1, Z=0..H-1.

% -------------------------------------------------
% piece selection

% guess which variant
available_variant(P, V) :- p3(P, V, _, _, _).

% For each pentomino, we choose one variant
1 { selected_variant(P, V) : available_variant(P, V) } 1 :- piece(P).

% -------------------------------------------------
% selection of the pieces
selected_piece(P) :- piece(P), not not_selected_piece(P).
not_selected_piece(P) :- piece(P), not selected_piece(P).

% -------------------------------------------------
% piece placement

% guess the position of the origin of the piece
1 { origin(P, X0, Y0, Z0) : cube(X0, Y0, Z0) } 1 :- selected_piece(P).

% place the others cube of the piece
occ(P, X0+X, Y0+Y, Z0+Z) :- 
    origin(P, X0, Y0, Z0),
    selected_variant(P, V),
    p3(P, V, X, Y, Z).

% ensure inside the tower
:- occ(P, X, Y, Z), not cube(X, Y, Z).

% not overlapping
:- occ(P1, X, Y, Z), occ(P2, X, Y, Z), P1 != P2.


% -------------------------------------------------

% Define a weight for each material
material_weight(iron,4).
material_weight(stone, 3).
material_weight(wood, 2).
material_weight(dirt, 1).

% 6 cubes directions
face_dir( 1, 0, 0). face_dir(-1, 0, 0).
face_dir( 0, 1, 0). face_dir( 0,-1, 0).
face_dir( 0, 0, 1). face_dir( 0, 0,-1).

% Calculate the exposed faces
occupied(X, Y, Z) :- occ(_, X, Y, Z).

% Exposed if the neighbor cell is not occupied
exposed(P, X, Y, Z, DX, DY, DZ) :-
    occ(P, X, Y, Z),
    face_dir(DX, DY, DZ),
    not occupied(X+DX, Y+DY, Z+DZ).

% Calculate each layer weight
layer(Z) :- height(H), Z = 0..H-1.

% Layer weight = sum of every exposed cube weight
layer_weight(Z, W) :-
    layer(Z),
    W = #sum { FW, P, X, Y, DX, DY, DZ :
               exposed(P, X, Y, Z, DX, DY, DZ),
               material(P, Mat),
               material_weight(Mat, FW) }.

% each layer must be heavier than the above one
:- layer_weight(Z, W1), layer_weight(Z+1, W2), W1 < W2.

#show selected_piece/1.
#show selected_variant/2.
#show origin/4.
#show layer_weight/2.