import clingo
import numpy as np
import time
import argparse
from termcolor import colored

def generate_costs(n):
    return np.random.randint(1, 101, size=(n, n))

def print_matrix(costs, assignments):
    n = costs.shape[0]
    col_width = 4  # Fixed width for each column
    
    print(" " * 3 + "".join(f"{i:>{col_width}}" for i in range(1, n+1)))
    
    for i in range(n):
        print(f"{i+1:2d}", end=" ")
        for j in range(n):
            cost = costs[i, j]
            if (i+1, j+1) in assignments:
                print(colored(f"{cost:>{col_width}d}", "yellow", attrs=["bold"]), end="")
            else:
                print(f"{cost:>{col_width}d}", end="")
        print()

def print_solution(model, costs, solve_time):
    assignments = set((atom.arguments[0].number, atom.arguments[1].number) 
                      for atom in model.symbols(shown=True) if atom.name == "assign")
    total_cost = sum(costs[i-1, j-1] for i, j in assignments)
    
    solution_type = "Optimal" if model.optimality_proven else "Intermediate"
    print(colored(f"\n{solution_type} Solution {model.number}", "cyan", attrs=["bold"]))
    print(colored(f"Time: {solve_time:.2f}s", "magenta"))
    print()
    print_matrix(costs, assignments)
    print()
    print(f"Total cost: {colored(str(total_cost), 'green', attrs=['bold'])}")

def main(n):
    costs = generate_costs(n)
    
    ctl = clingo.Control(["-c", f"n={n}", "--opt-mode=optN", "0"])
    ctl.load("base.lp")
    ctl.add("base", [], "\n".join(f"cost({i},{j},{cost})." for i, row in enumerate(costs, 1) for j, cost in enumerate(row, 1)))
    ctl.ground([("base", [])])
    
    print(colored("Solving assignment problem...", "cyan"))

    start_time = time.time()
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            solve_time = time.time() - start_time
            print_solution(model, costs, solve_time)

        result = handle.get()
        if result.satisfiable:
            print(colored("\nAll optimal solutions found.", "green", attrs=["bold"]))
        elif result.unsatisfiable:
            print(colored("\nProblem is unsatisfiable", "red", attrs=["bold"]))
        else:
            print(colored("\nSolving was interrupted", "yellow", attrs=["bold"]))
        
        print(colored(f"Total time: {time.time() - start_time:.2f}s", "magenta"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the Assignment Problem")
    parser.add_argument("-n", type=int, default=5, help="Number of agents and tasks (default: 5)")
    args = parser.parse_args()

    main(args.n)