% pieces_generation.lp
% material(PIECE_NAME, MATERIAL)
% associated_n(PIECE_NAME, N)
% Associate each piece with a material and a number n, randomly
% - - -
% 4 cubes
% - - -

material(p4q2, dirt).
associated_n(p4q2, 1).
% - - -

material(p4y, dirt).
associated_n(p4y, 2).

% - - -
material(p4t, dirt).
associated_n(p4t, 3).

% - - -
material(p4o, dirt).
associated_n(p4o, 4).

% - - -
material(p4s, dirt).
associated_n(p4s, 5).

% - - -
material(p4l, dirt).
associated_n(p4l, 6).

% - - -
material(p4q1, dirt).
associated_n(p4q1, 7).

% - - -
material(p4i, dirt).
associated_n(p4i, 8).

% ---------------------------------------
% 5 cubes
% ---------------------------------------
material(p5v, wood).
associated_n(p5v, 1).

material(p5v3D, wood).
associated_n(p5v3D, 4).
% - - -
material(p5u, wood).
associated_n(p5u, 2).

% - - -
material(p5t, wood).
associated_n(p5t, 5).

material(p5t3D, wood).
associated_n(p5t3D, 6).

% - - -
material(p5w, wood).
associated_n(p5w, 7).

% - - -
material(p5x, wood).
associated_n(p5x, 8).

% - - -
material(p5y, wood).
associated_n(p5y, a).

material(p5y3D, wood).
associated_n(p5y3D, a).

% - - -

material(p5f, stone).
associated_n(p5f, a).

material(p5f3D, stone).
associated_n(p5f3D, 3).
% - - - 
material(p5z, wood).
associated_n(p5z, a).

material(p5z3D, wood).
associated_n(p5z3D, a).

% - - -
material(p5i, stone).
associated_n(p5i, a).


% - - -
material(p5l, stone).
associated_n(p5l, a).

material(p5l3D, dirt).
associated_n(p5l3D, a).

% - - -
material(p5p, stone).
associated_n(p5p, a).

material(p5p3D, stone).
associated_n(p5p3D, a).

% - - -
material(p5n, stone).
associated_n(p5n, a).

% - - -
material(p5c3D, iron).
associated_n(p5c3D, a).

material(p5c3D2, iron).
associated_n(p5c3D2, a).

% - - -
material(p5s3D, dirt).
associated_n(p5s3D, a).

% - - -
material(p5g3D, dirt).
associated_n(p5g3D, a).

% - - -
material(p5j3D, stone).
associated_n(p5j3D, a).

% ----------------------------------------------------
% ----------------------------------------------------
% ----------------------------------------------------

% for the selection of the pieces depending on the associated_n value (n = number of layer)
size4(P) :- bit(P,_,_,_), 4 = #count { X,Y,Z : bit(P,X,Y,Z) }.
size5(P) :- bit(P,_,_,_), 5 = #count { X,Y,Z : bit(P,X,Y,Z) }.
#const n=3.
piece_used(P) :-
    piece(P),
    associated_n(P, K),
    K <= n.


% p3(PIECE, VARIANT, X, Y, Z)
p3(P, R, X, Y, Z) :-
    norm_bit(P, R, X, Y, Z),
    keep_rot(P, R),
    piece_used(P).

% -----------------------
% Define a randomweight for each material
material(iron; stone; wood; dirt).

1 { material_weight(M, W) : W=1..20 } 1 :- material(M).




% -------------------------------------------------
% selection of the pieces
2*n { selected_piece(P) : piece_used(P) } 2*n.

% list of available variants
available_variant(P, V) :- selected_piece(P), p3(P, V, _, _, _).

% -------------------------------------------------
% number of cubes of each piece (volume)
piece_volume(P, Vol) :- piece_used(P), Vol = #count { DX, DY, DZ : bit(P, DX, DY, DZ) }.

% the total volume of the selected pieces must be equal to the tower volume
:- width(W), depth(D), height(H), #sum { Vol, P : selected_piece(P), piece_volume(P, Vol) } != W*D*H.


