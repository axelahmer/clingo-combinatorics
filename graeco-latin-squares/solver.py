import clingo
import argparse

def get_symbols(n):
    greek = 'αβγδεζηθικλμνξοπρστυφχψω'
    latin = 'abcdefghijklmnopqrstuvwx'
    if n == 4:
        return 'AKQJ', '♥♦♣♠'
    elif n <= len(greek):
        return latin[:n], greek[:n]
    else:
        return None, None

def print_solution(model, n):
    grid = [[None for _ in range(n)] for _ in range(n)]
    for atom in model.symbols(shown=True):
        r, c, l, g = [x.number for x in atom.arguments]
        grid[r-1][c-1] = (l-1, g-1)

    latin, greek = get_symbols(n)
    print(f"\n{n}x{n} Graeco-Latin Square:")
    
    if latin and greek:
        for row in grid:
            print(' '.join(f'{latin[l]}{greek[g]}' for l, g in row))
    else:
        for row in grid:
            print(' '.join(f'({l},{g})' for l, g in row))

def solve_and_display(n, hard_mode):
    ctl = clingo.Control(['0', f'-c n={n}'])
    ctl.load("base.lp")
    if hard_mode:
        ctl.load("hard.lp")
    ctl.ground([("base", [])])

    solutions = 0
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            solutions += 1
            print_solution(model, n)
            if input("\nPress Enter for another solution, or 'q' to quit: ").lower() == 'q':
                return
    print(f"Total solutions: {solutions}")

def main():
    parser = argparse.ArgumentParser(
        description="Solve and display Graeco-Latin Squares.")
    parser.add_argument("n", type=int, nargs="?", default=4,
                        help="Size of the square (default: 4)")
    parser.add_argument("--hard", action="store_true",
                        help="Enable hard mode with diagonal constraints")
    args = parser.parse_args()

    solve_and_display(args.n, args.hard)

if __name__ == "__main__":
    main()