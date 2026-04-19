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