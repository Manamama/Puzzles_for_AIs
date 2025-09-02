def initialize_grid(n):
    grid = [['⬜' for _ in range(n)] for _ in range(n)]
    center = n // 2
    grid[center][center] = '🟥'
    return grid, center, center

def print_grid(grid):
    for row in grid:
        print(' '.join(row))
    print() # Add a newline for better separation

def generate_spiral_turns(n, num_turns):
    grid, r, c = initialize_grid(n)
    print("Initial State:")
    print_grid(grid)

    # Directions: Right, Down, Left, Up (as row, col changes)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # (dr, dc)
    
    step_length = 1

    for i in range(num_turns):
        direction_name = ['Right', 'Down', 'Left', 'Up'][i % 4]
        dr, dc = directions[i % 4]
        
        print(f"Move {direction_name} for {step_length} steps:")

        for _ in range(step_length):
            r += dr
            c += dc
            if 0 <= r < n and 0 <= c < n:
                grid[r][c] = '🟥'
            else:
                break 
        
        print_grid(grid)
        
        step_length += 1

if __name__ == "__main__":
    n = 5
    # We will generate the first 5 turns to complete the pattern
    generate_spiral_turns(n, 5)

