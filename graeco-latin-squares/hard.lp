% No repeated Latin or Greek symbols on main diagonal
:- place(R,R,L,_), place(C,C,L,_), R != C.
:- place(R,R,_,G), place(C,C,_,G), R != C.