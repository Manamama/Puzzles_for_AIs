## Spiral puzzle
#ver. 5.1 (Deepseek AI's for other AIs, partial, with solution) 

Organic Spiral Puzzle
Objective:

Create an n×n grid where a spiral grows outward from the center, painting approximately half the tiles red (🟥) while showing all intermediate states. The spiral should:
Begin at the exact center tile (already red)
Expand clockwise (Right→Down→Left→Up cycles)
Show each distinct growth phase
Naturally preserve whitespace by terminating after filling ~50% of the grid

 
For example, for n=5, the target image should be: 
```

🟥🟥🟥🟥🟥
🟥⬜⬜⬜⬜
🟥⬜🟥🟥⬜
🟥⬜⬜🟥⬜
🟥🟥🟥🟥⬜
```

The code should start by placing a dot in the middle of the matrix and then show the progress of the spiral as this: 
```
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ 🟥 ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜

⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ 🟥 🟥 ⬜
⬜ ⬜ ⬜ 🟥 ⬜
⬜ ⬜ ⬜ ⬜ ⬜

⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ 🟥 🟥 ⬜
⬜ ⬜ ⬜ 🟥 ⬜
⬜ 🟥 🟥 🟥 ⬜

⬜ ⬜ ⬜ ⬜ ⬜
🟥 ⬜ ⬜ ⬜ ⬜
🟥 ⬜ 🟥 🟥 ⬜
🟥 ⬜ ⬜ 🟥 ⬜
🟥 🟥 🟥 🟥 ⬜

🟥 🟥 🟥 🟥 🟥
🟥 ⬜ ⬜ ⬜ ⬜
🟥 ⬜ 🟥 🟥 ⬜
🟥 ⬜ ⬜ 🟥 ⬜
🟥 🟥 🟥 🟥 ⬜

```
Notice the white spaces retained by that algorithm: there is a red spiral and white spiral at the end. 




Key Mechanics:
Initialization:
Start with empty n×n grid (n odd)
Place first red tile at center
Growth Pattern:
Start with step length = 0
After each direction change:
Increment step length by 1
Move step tiles in current direction
Sequence:
1 Right (step=1)
2 Down (step=2)
3 Left (step=3)
4 Up (step=4)
5 Right (step=5)
...until termination
Output Requirements:
Show grid after completing each directional movement
Include initial center-only state
Separate states with blank lines




Termination:
Stop when approximately half the tiles are red (n²/2 + 1)
Final arm may be incomplete







## Almost ideal code expected: 


# ver. 2.2
def red_spiral(n):
    grid = [['⬜'] * n for _ in range(n)]
    x = y = n // 2  # Start from the center
    grid[y][x] = '🟥'
    count = 1
    limit = n * n // 2 + 1  # Fill just over half
    step = 0
    direction = -1  # 0:→, 1:↓, 2:←, 3:↑

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
        print()
        step += 1
        direction = (direction + 1) % 4

red_spiral(5)


