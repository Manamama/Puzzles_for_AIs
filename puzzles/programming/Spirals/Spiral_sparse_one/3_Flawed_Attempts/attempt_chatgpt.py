#Version of ChatGPT:
def print_spiral(n):
    emoji_list = ["🟥", "⬜"]
    matrix = [["⬜" for _ in range(n)] for _ in range(n)]

    # For even n, center is offset one tile to top-left
    x = y = (n - 1) // 2 if n % 2 == 1 else n // 2 - 1

    count = 0
    step = 1
    direction = 0
    total = (n * n + 1) // 2  # Fill ~half

    def in_bounds(x, y):
        return 0 <= x < n and 0 <= y < n

    while count < total:
        for _ in range(step):
            if in_bounds(x, y) and matrix[y][x] == "⬜":
                matrix[y][x] = emoji_list[0]
                count += 1

            # Spiral direction: right, down, left, up
            if direction == 0:
                x += 1
            elif direction == 1:
                y += 1
            elif direction == 2:
                x -= 1
            else:
                y -= 1

        direction = (direction + 1) % 4
        print_matrix(matrix)  # Print every direction change
        step += 1  # Always increase step (not just every other)

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(row))
    print()



