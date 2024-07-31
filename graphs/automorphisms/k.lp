% Define edges for complete graph
edge(X,Y) :- node(X), node(Y), X != Y.