def initialize_grid(n):
    grid = [['⬜' for _ in range(n)] for _ in range(n)]
    center = n // 2
    grid[center][center] = '🟥'
    return grid

def print_grid(grid):
    for row in grid:
        print(' '.join(row))

def move_right(grid, r, c, steps):
    for i in range(steps):
        c += 1
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            grid[r][c] = '🟥'
        else:
            # Handle out of bounds if necessary, though for initial steps it shouldn't happen
            pass
    return grid, r, c

if __name__ == "__main__":
    n = 5
    grid = initialize_grid(n)
    print_grid(grid)
    print("\n")

    # Initial position after placing center dot
    r, c = n // 2, n // 2

    # First move: Right (1 step)
    grid, r, c = move_right(grid, r, c, 1)
    print_grid(grid)

