# The Expanding Arm Spiral Puzzle

## 1.  Goal

The application will draw a spiral of red squares (🟥) on an N x N grid, starting from the center. The key is that this is not a standard, tight spiral. It's a sparse spiral that expands rapidly, leaving significant white space (⬜).

For an N=5 grid, the final, completed pattern must look exactly like this:

```
🟥🟥🟥🟥🟥
🟥⬜⬜⬜⬜
🟥⬜🟥🟥⬜
🟥⬜⬜🟥⬜
🟥🟥🟥🟥⬜
```

## 2. The Core Algorithm (The Most Important Rule)

The spiral must be generated using the following precise steps:

* **Start:** Place the first red square in the center of the grid.
* **Movement:** Move in a spiraling sequence of directions: Right -> Down -> Left -> Up, and repeat.
* **The "Expanding Arm" Rule:** This is the crucial part. Unlike a normal spiral that repeats its step count (1, 1, 2, 2, 3, 3...), this spiral's arm length must **increase by one at every single turn**. The sequence of steps taken in each direction will be **1, 2, 3, 4, 5, ...**
  * Move 1 step, then turn.
  * Move 2 steps, then turn.
  * Move 3 steps, then turn.
  * ...and so on.

## 3. Output and Termination Requirements

* **Animation:** The process should be shown by printing the state of the grid after each full directional move is completed.
* **Termination:** The algorithm terminates when the next planned move would place any square outside the grid bounds. That move is never executed.
* **Formatting:** Use 🟥 for red tiles and ⬜ for white tiles. Each row of the matrix should be printed as space-separated symbols.
