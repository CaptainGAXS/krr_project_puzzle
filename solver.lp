% The tower
width(4). depth(4). height(4). 

cube(X, Y, Z) :- width(W), depth(D), height(H), X=0..W-1, Y=0..D-1, Z=0..H-1.

% -------------------------------------------------
% selection of the pieces
selected_piece(P) :- piece(P), not not_selected_piece(P).
not_selected_piece(P) :- piece(P), not selected_piece(P).

% list of available variants
available_variant(P, V) :- p3(P, V, _, _, _).

% -------------------------------------------------
% number of cubes of each piece (volume)
piece_volume(P, Vol) :- piece(P), Vol = #count { X, Y, Z : p3(P, 0, X, Y, Z) }.

% the total volume of the selected pieces must be equal to the tower volume
:- width(W), depth(D), height(H), #sum { Vol, P : selected_piece(P), piece_volume(P, Vol) } != W*D*H.

% -------------------------------------------------
% piece placement

% Invalid placement: a piece goes out of the boundaries of the tower
invalid_placement(P, V, X, Y, Z) :- 
    available_variant(P, V), cube(X, Y, Z), 
    p3(P, V, DX, DY, DZ), not cube(X+DX, Y+DY, Z+DZ).

% Valid placement: it stays entirely inside the 4x4x8 grid
valid_placement(P, V, X, Y, Z) :- 
    available_variant(P, V), cube(X, Y, Z), 
    not invalid_placement(P, V, X, Y, Z).

% Single choice: pick exactly one valid placement (VARIANT + ORIGIN coupled) for each selected piece
1 { placement(P, V, X, Y, Z) : valid_placement(P, V, X, Y, Z) } 1 :- selected_piece(P).

% place the cubes of the piece
occ(P, X+DX, Y+DY, Z+DZ) :- 
    placement(P, V, X, Y, Z),
    p3(P, V, DX, DY, DZ).

% not overlapping (P1 < P2 restricts symmetries logically)
:- occ(P1, X, Y, Z), occ(P2, X, Y, Z), P1 < P2.


% -------------------------------------------------

% 4 lateral directions (ignore top and bottom)
face_dir(1, 0, 0). face_dir(-1, 0, 0).
face_dir(0, 1, 0). face_dir( 0,-1, 0).

% Calculate the exposed faces
occupied(X, Y, Z) :- occ(_, X, Y, Z).

% The tower must be entirely filled (no hole)
:- cube(X, Y, Z), not occupied(X, Y, Z).


% Exposed if the neighbor cell is outside the tower
exposed(P, X, Y, Z, DX, DY, DZ) :-
    occ(P, X, Y, Z),
    face_dir(DX, DY, DZ),
    not cube(X+DX, Y+DY, Z+DZ).

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

#show occ/4.