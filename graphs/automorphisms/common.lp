% Define the number of nodes
#const n = 5.

% Define nodes
node(1..n).

% Define undirected link from edge
link(X,Y) :- edge(X,Y).
link(X,Y) :- edge(Y,X).

% Calculate degree
degree(X,D) :- node(X), D = #count{ Y : link(X,Y) }.