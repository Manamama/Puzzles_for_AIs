def print_spiral(n):
    emoji_list = ["🟥", "⬜"]
    matrix = [["⬜" for _ in range(n)] for _ in range(n)]
    count = 0
    x, y = n // 2, n // 2  # Starting point at the center
    step = 1
    direction = 0

    # Place the first red square and print initial state
    matrix[y][x] = emoji_list[0]
    count += 1
    print_matrix(matrix)

    while count < n*n/2 + 1:
        for _ in range(step):
            # Compute next position
            next_x, next_y = x, y
            if direction == 0:
                next_x += 1  # Move right
            elif direction == 1:
                next_y += 1  # Move down
            elif direction == 2:
                next_x -= 1  # Move left
            else:
                next_y -= 1  # Move up
            
            # Check if the next position is within bounds
            if 0 <= next_x < n and 0 <= next_y < n:
                x, y = next_x, next_y  # Update position
                matrix[y][x] = emoji_list[0]  # Assign red element
                count += 1
            else:
                print_matrix(matrix)  # Print final state before exiting
                return  # Exit if next move is out of bounds

        direction = (direction + 1) % 4  # Update direction
        print_matrix(matrix)  # Print intermediate result
        step += 1

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(row))
    print()

# Test for n=5
print_spiral(5)

# Test for n=6
print_spiral(6)
