def initialize_grid(n):
    grid = [['⬜' for _ in range(n)] for _ in range(n)]
    return grid

def print_grid(grid):
    for row in grid:
        print(' '.join(row))

def simulate_sparse_spiral_growth(n):
    grid = initialize_grid(n)
    states = []
    center = n // 2

    # Phase 1: Initial Center
    grid[center][center] = '🟥'
    states.append(("Initial State", [row[:] for row in grid]))

    # Phase 2: Right-Down Corner
    if n >= 3:
        grid[center][center + 1] = '🟥'
        grid[center + 1][center + 1] = '🟥'
    states.append(("After Right-Down Corner", [row[:] for row in grid]))

    # Phase 3: Bottom Edge (partial)
    if n >= 3:
        for col in range(1, n - 1):
            grid[n - 1][col] = '🟥'
    states.append(("After Bottom Edge", [row[:] for row in grid]))

    # Phase 4: Left Edge (partial)
    if n >= 3:
        for row in range(1, n):
            grid[row][0] = '🟥'
    states.append(("After Left Edge", [row[:] for row in grid]))

    # Phase 5: Top Edge (full)
    if n >= 1:
        for col in range(n):
            grid[0][col] = '🟥'
    states.append(("After Top Edge", [row[:] for row in grid]))

    return states

if __name__ == "__main__":
    # Test with n=5
    n = 5
    print(f"\n--- Testing for n={n} ---")
    spiral_states = simulate_sparse_spiral_growth(n)
    for description, state_grid in spiral_states:
        print(f"\n{description}:")
        print_grid(state_grid)

    # Test with n=3
    n = 3
    print(f"\n--- Testing for n={n} ---")
    spiral_states = simulate_sparse_spiral_growth(n)
    for description, state_grid in spiral_states:
        print(f"\n{description}:")
        print_grid(state_grid)

    # Test with n=7
    n = 7
    print(f"\n--- Testing for n={n} ---")
    spiral_states = simulate_sparse_spiral_growth(n)
    for description, state_grid in spiral_states:
        print(f"\n{description}:")
        print_grid(state_grid)