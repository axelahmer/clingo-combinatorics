#const n = 4.
dim(1..n).

% Place exactly one pair of symbols in each cell
1 { place(R,C,L,G) : dim(L), dim(G) } 1 :- dim(R), dim(C).

% No repeated pairs anywhere
:- place(R1,C1,L,G), place(R2,C2,L,G), (R1,C1) != (R2,C2).

% No repeated Latin symbols in rows or columns
:- place(R,C1,L,_), place(R,C2,L,_), C1 != C2.
:- place(R1,C,L,_), place(R2,C,L,_), R1 != R2.

% No repeated Greek symbols in rows or columns
:- place(R,C1,_,G), place(R,C2,_,G), C1 != C2.
:- place(R1,C,_,G), place(R2,C,_,G), R1 != R2.

#show place/4.