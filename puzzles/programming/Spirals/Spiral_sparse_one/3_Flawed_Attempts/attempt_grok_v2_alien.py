def red_spiral(n):
    grid = [['⬜'] * n for _ in range(n)]
    x = y = n // 2
    grid[y][x] = '🟥'
    count = 1
    limit = n * n // 2 + 1
    step = 0
    direction = 0

    def print_grid():
        for row in grid:
            print(' '.join(row))
        print()

    print_grid()

    while count < limit:
        for _ in range(step):
            nx, ny = x, y
            if direction == 0: nx += 1
            elif direction == 1: ny += 1
            elif direction == 2: nx -= 1
            else: ny -= 1

            if 0 <= nx < n and 0 <= ny < n:
                x, y = nx, ny
                grid[y][x] = '🟥'
                count += 1
            else:
                print_grid()
                return

        print_grid()
        step += 1
        direction = (direction + 1) % 4
        if count >= limit:
            break

red_spiral(5)

