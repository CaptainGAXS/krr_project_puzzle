% The tower
width(8). depth(8). height(16). 

cube(X, Y, Z) :- width(W), depth(D), height(H), X=0..W-1, Y=0..D-1, Z=0..H-1.

