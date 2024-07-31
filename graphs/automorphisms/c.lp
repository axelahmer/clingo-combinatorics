% Define edges for cycle graph
edge(X,Y) :- node(X), node(Y), Y = X + 1.
edge(n,1) :- node(n), node(1).