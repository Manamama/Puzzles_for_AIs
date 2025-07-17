def initialize_grid(n):
    grid = [['⬜' for _ in range(n)] for _ in range(n)]
    center = n // 2
    grid[center][center] = '🟥'
    return grid

def print_grid(grid):
    for row in grid:
        print(' '.join(row))

if __name__ == "__main__":
    n = 5
    initial_state = initialize_grid(n)
    print_grid(initial_state)
