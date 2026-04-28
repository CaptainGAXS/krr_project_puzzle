% puzzleGenerator.lp
% material(PIECE_NAME, MATERIAL)
% -----------------------
% number of cubes of each piece (volume)
piece_volume(P, Vol) :- piece(P), Vol = #count { DX, DY, DZ : bit(P, DX, DY, DZ) }.

% -------------------------------------------------
% the total volume of the selected pieces must be equal to the tower volume of base 3x3 and height n
% selection of the pieces (n of 5 cubes + n of 4 cubes)
n { selected_piece(P) : piece(P), piece_volume(P, 4) } n.
n { selected_piece(P) : piece(P), piece_volume(P, 5) } n.


% Prioritize the selection of pieces with higher volume
#heuristic placement(P, V, X, Y, Z) : valid_placement(P, V, X, Y, Z). [100, level]
#heuristic material(P, M) : selected_piece(P), list_material(M). [1, sign]
% -------------------------------------------------
list_material(dirt).
list_material(wood).
list_material(stone).

% Attribute a material to each piece
1 { material(P, M) : list_material(M) } 1 :- selected_piece(P).

% At least one piece of each material must be selected
:- list_material(M), not material(_, M).

% p3(PIECE, VARIANT, X, Y, Z)
p3(P, R, X, Y, Z) :-
    selected_piece(P),
    norm_bit(P, R, X, Y, Z),
    keep_rot(P, R).

material_weight(stone, 5).
material_weight(wood, 3).
material_weight(dirt, 1).