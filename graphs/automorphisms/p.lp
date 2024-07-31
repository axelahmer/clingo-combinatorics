% Define edges for path graph
edge(X,Y) :- node(X), node(Y), Y = X + 1.