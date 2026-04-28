% -------------------------------------------------
% Piece placement

% list of available variants
available_variant(P, V) :- selected_piece(P), p3(P, V, _, _, _).

% Invalid placement: a piece goes out of the boundaries of the tower
invalid_placement(P, V, X, Y, Z) :- 
    available_variant(P, V), cube(X, Y, Z), 
    p3(P, V, DX, DY, DZ), not cube(X+DX, Y+DY, Z+DZ).

% Valid placement: it stays entirely inside the grid
valid_placement(P, V, X, Y, Z) :- 
    available_variant(P, V), cube(X, Y, Z), 
    not invalid_placement(P, V, X, Y, Z).

% Single choice: pick exactly one valid placement (VARIANT + ORIGIN coupled) for each selected piece
1 { placement(P, V, X, Y, Z) : valid_placement(P, V, X, Y, Z) } 1 :- selected_piece(P).

% place the cubes of the piece
occ(P, X+DX, Y+DY, Z+DZ) :- 
    placement(P, V, X, Y, Z),
    p3(P, V, DX, DY, DZ).

% not overlapping
:- occ(P1, X, Y, Z), occ(P2, X, Y, Z), P1 != P2.

% -----
% Limit symmetries
% Identify the first placed piece by its ID
first_piece(MinP) :- MinP = #min { P : selected_piece(P) }.

% Break X-axis and Y-axis reflections & rotations on the 3x3 base
% Limit the X origin parameter to at most 1 (width/2)
:- first_piece(P), placement(P, _, X, _, _), X > 1.

% Limit the Y origin to be <= X to break diagonal reflection symmetry
:- first_piece(P), placement(P, _, X, Y, _), Y > X.

% -------------------------------------------------
% Weight constraint
% 4 lateral directions (ignore top and bottom)
face_dir(1, 0, 0). face_dir(-1, 0, 0).
face_dir(0, 1, 0). face_dir( 0,-1, 0).

% Calculate the exposed faces
occupied(X, Y, Z) :- occ(_, X, Y, Z).

% Number of exposed lateral faces for each (X,Y) coordinate of the grid.
exposed(0,0,2). exposed(0,1,1). exposed(0,2,2).
exposed(1,0,1). exposed(1,1,0). exposed(1,2,1).
exposed(2,0,2). exposed(2,1,1). exposed(2,2,2).

% Calculate each layer weight
layer(Z) :- height(H), Z = 0..H-1.

layer_weight(Z, W) :- 
    layer(Z), 
    W = #sum { N*FW, P, X, Y : occ(P, X, Y, Z), exposed(X,Y,N), material(P, Mat), material_weight(Mat, FW) }.

% Each layer must have a strictly higher weight than the layer above it (W(Z) > W(Z+1))
:- layer_weight(Z, W1), layer_weight(Z+1, W2), W1 < W2.
% variations/challenges:
% with a maximum weight difference of d.
#const d=100000.
:- layer_weight(Z, W1), layer_weight(Z+1, W2), W1 - W2 > d.

% -------------------------------------------------
#show selected_piece/1.
#show material/2.
#show material_weight/2.
#show occ/4.
#show layer_weight/2.