% Generate a permutation
1 { map(X,Y) : node(Y) } 1 :- node(X).
1 { map(X,Y) : node(X) } 1 :- node(Y).

% Ensure the permutation is bijective
:- map(X,Y), map(X,Z), Y != Z.
:- map(X,Y), map(Z,Y), X != Z.

% Check if the permutation preserves degrees
:- degree(X,D), map(X,Y), not degree(Y,D).

% Check if the permutation preserves links
:- link(X,Y), map(X,X1), map(Y,Y1), not link(X1,Y1).
:- not link(X,Y), map(X,X1), map(Y,Y1), link(X1,Y1).

% Output
% #show map/2.