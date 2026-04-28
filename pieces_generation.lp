% pieces_generation.lp
% material(PIECE_NAME, MATERIAL)
% associated_n(PIECE_NAME, N)
% Associate each piece with a material and a number n
material(p4q2, dirt).
associated_n(p4q2, 1).

material(p4y, dirt).
associated_n(p4y, 2).

material(p4t, dirt).
associated_n(p4t, 3).

material(p4o, dirt).
associated_n(p4o, 4).

material(p4s, dirt).
associated_n(p4s, 5).

material(p4l, dirt).
associated_n(p4l, 6).

material(p4q1, dirt).
associated_n(p4q1, 7).

material(p4i, dirt).
associated_n(p4i, 8).

% - - -

material(p5v, wood).
associated_n(p5v, 1).

material(p5u, wood).
associated_n(p5u, 2).

material(p5f3D, stone).
associated_n(p5f3D, 3).

material(p5t, wood).
associated_n(p5t, 5).

material(p5v3D, wood).
associated_n(p5v3D, 4).

material(p5t3D, wood).
associated_n(p5t3D, 6).

material(p5w, wood).
associated_n(p5w, 7).

material(p5x, wood).
associated_n(p5x, 8).

% ----------------------------------------------------
% ----------------------------------------------------
% ----------------------------------------------------

% Selection of the pieces based on the associated_n value
#const n=3.
selected_piece(P) :-
    piece(P),
    associated_n(P, K),
    K <= n.

% p3(PIECE, VARIANT, X, Y, Z)
p3(P, R, X, Y, Z) :-
    norm_bit(P, R, X, Y, Z),
    keep_rot(P, R),
    selected_piece(P).


available_variant(P, V) :- selected_piece(P), p3(P, V, _, _, _).

% -----------------------
% Define a weight for each material
material_weight(iron, 7).
material_weight(stone, 5).
material_weight(wood, 3).
material_weight(dirt, 1).