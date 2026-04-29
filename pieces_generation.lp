% pieces_generation.lp
% material(PIECE_NAME, MATERIAL)
% associated_n(PIECE_NAME, N)
% Associate each piece with a material and a number n
material(p4q2, dirt).
associated_n(p4q2, 1).

material(p4y, dirt).
associated_n(p4y, 2).

material(p4t, iron).
associated_n(p4t, 3).

material(p4o, iron).
associated_n(p4o, 4).

material(p4s, wood).
associated_n(p4s, 5).

material(p4l, wood).
associated_n(p4l, 6).

material(p4q1, iron).
associated_n(p4q1, 7).

material(p4i, iron).
associated_n(p4i, 8).

% - - -

material(p5v, wood).
associated_n(p5v, 1).

material(p5u, stone).
associated_n(p5u, 2).

material(p5f3D, iron).
associated_n(p5f3D, 3).

material(p5t, wood).
associated_n(p5t, 5).

material(p5v3D, stone).
associated_n(p5v3D, 4).

material(p5t3D, iron).
associated_n(p5t3D, 6).

material(p5w, wood).
associated_n(p5w, 7).

material(p5x, stone).
associated_n(p5x, 8).

% ----------------------------------------------------
% ----------------------------------------------------
% ----------------------------------------------------

% Selection of the pieces based on the associated_n value
selected_piece(P) :-
    piece(P),
    associated_n(P, K),
    K <= n.

% p3(PIECE, VARIANT, X, Y, Z)
p3(P, R, X, Y, Z) :-
    norm_bit(P, R, X, Y, Z),
    keep_rot(P, R),
    selected_piece(P).

% -----------------------
% Define a weight for each material
material_weight(iron, 4).
material_weight(stone, 3).
material_weight(wood, 2).
material_weight(dirt, 1).