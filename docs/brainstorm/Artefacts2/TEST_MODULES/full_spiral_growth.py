def initialize_grid(n):
    grid = [['⬜' for _ in range(n)] for _ in range(n)]
    center = n // 2
    grid[center][center] = '🟥'
    return grid, center, center

def print_grid(grid):
    for row in grid:
        print(' '.join(row))

def count_red_tiles(grid):
    count = 0
    for r in grid:
        for cell in r:
            if cell == '🟥':
                count += 1
    return count

def simulate_spiral_growth(n):
    grid, r, c = initialize_grid(n)
    states = [("Initial State", [row[:] for row in grid])]

    dr = [0, 1, 0, -1]  # Right, Down, Left, Up
    dc = [1, 0, -1, 0]
    
    direction_idx = 0
    steps_to_take = 1
    steps_taken_in_direction = 0
    turns_taken = 0
    total_cells = n * n
    target_red_tiles = total_cells // 2 # Approximately half

    while True:
        for _ in range(steps_to_take):
            new_r, new_c = r + dr[direction_idx], c + dc[direction_idx]

            if 0 <= new_r < n and 0 <= new_c < n and grid[new_r][new_c] == '⬜':
                r, c = new_r, new_c
                grid[r][c] = '🟥'
                steps_taken_in_direction += 1
            else:
                # Cannot move further in this direction or cell already red, break this segment
                break

        # After completing a segment of movement
        # Only append state if we actually moved and changed the grid
        if steps_taken_in_direction > 0:
            states.append((f"After {['Right', 'Down', 'Left', 'Up'][direction_idx]} {steps_to_take} steps", [row[:] for row in grid]))
        
        # Reset steps_taken_in_direction for the next segment
        steps_taken_in_direction = 0

        direction_idx = (direction_idx + 1) % 4
        turns_taken += 1

        # Increase steps_to_take after every two turns (after Right and Down, then Left and Up)
        if turns_taken % 2 == 0:
            steps_to_take += 1

        # Termination condition: approximately half the tiles are red
        if count_red_tiles(grid) >= target_red_tiles:
            break

    return states

if __name__ == "__main__":
    n = 5
    spiral_states = simulate_spiral_growth(n)

    for description, state_grid in spiral_states:
        print(f"\n{description}:")
        print_grid(state_grid)