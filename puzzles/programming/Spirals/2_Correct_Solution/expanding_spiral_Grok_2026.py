#ver. 4.1, Grok's
def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()

def generate_expanding_spiral(n=5):
    grid = [['⬜'] * n for _ in range(n)]
    y = x = n // 2
    grid[y][x] = '🟥'
    print("Start:")
    print_grid(grid)

    dirs = [(0,1), (1,0), (0,-1), (-1,0)]  # right, down, left, up
    dir_idx = 0
    arm_length = 1
    placed = 1

    while True:
        dy, dx = dirs[dir_idx]
        moved = 0

        for _ in range(arm_length):
            y += dy
            x += dx
            if not (0 <= y < n and 0 <= x < n):
                print("Stop: next would exit bounds")
                print("Final grid:")
                print_grid(grid)
                return
            if grid[y][x] == '⬜':
                grid[y][x] = '🟥'
                placed += 1
            moved += 1

        print(f"After {moved} steps {['→','↓','←','↑'][dir_idx]}:")
        print_grid(grid)

        dir_idx = (dir_idx + 1) % 4
        arm_length += 1

generate_expanding_spiral(5)


