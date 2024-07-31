import argparse
import clingo
import networkx as nx
import matplotlib.pyplot as plt
import math

def solve_and_visualize(n, graph_type):
    # Initialize Clingo control
    ctrl = clingo.Control(["-c", f"n={n}"])
    
    # Load all necessary files
    ctrl.load("common.lp")
    ctrl.load(f"{graph_type}.lp")
    ctrl.load("auto.lp")

    # Ground the program
    ctrl.ground([("base", [])])
    
    # Configure solver to compute all models
    ctrl.configuration.solve.models = 0
    
    # Initialize graph and automorphisms
    G = nx.Graph()
    automorphisms = []
    
    def on_model(model):
        nonlocal G, automorphisms
        # Parse the model to build the graph and automorphisms
        current_automorphism = {}
        for atom in model.symbols(shown=True):
            if atom.name == "node":
                G.add_node(atom.arguments[0].number)
            elif atom.name == "link":
                G.add_edge(atom.arguments[0].number, atom.arguments[1].number)
            elif atom.name == "map":
                current_automorphism[atom.arguments[0].number] = atom.arguments[1].number
        if current_automorphism:
            automorphisms.append(current_automorphism)
    
    # Solve and collect results
    ctrl.solve(on_model=on_model)
    
    # Visualize results
    visualize_results(G, automorphisms)

def visualize_results(G, automorphisms):
    n_automorphisms = len(automorphisms)
    
    # Calculate grid dimensions for automorphisms
    grid_size = math.ceil(math.sqrt(n_automorphisms))
    
    # Create figure with appropriate size
    fig = plt.figure(figsize=(20, 10))
    fig.suptitle(f"Original Graph and {n_automorphisms} Automorphisms", fontsize=16)
    
    # Create grid spec for layout
    gs = fig.add_gridspec(grid_size, grid_size + 1)
    
    # Plot original graph on the left
    ax_orig = fig.add_subplot(gs[:, 0])
    pos = nx.circular_layout(G)
    nx.draw(G, pos, ax=ax_orig, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    ax_orig.set_title("Original Graph")
    
    # Plot automorphisms in a grid on the right
    for i, automorphism in enumerate(automorphisms):
        row = i // grid_size
        col = (i % grid_size) + 1
        ax = fig.add_subplot(gs[row, col])
        G_auto = nx.relabel_nodes(G, automorphism)
        nx.draw(G_auto, pos, ax=ax, with_labels=True, node_color='lightgreen', node_size=500, font_size=10, font_weight='bold')
        ax.set_title(f"Auto {i+1}")
    
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Graph Automorphism Visualizer")
    parser.add_argument("n", type=int, help="Number of nodes")
    parser.add_argument("graph_type", choices=['k', 'c', 'p'], help="Graph type: k (complete), c (cycle), p (path)")
    args = parser.parse_args()
    
    solve_and_visualize(args.n, args.graph_type)

if __name__ == "__main__":
    main()