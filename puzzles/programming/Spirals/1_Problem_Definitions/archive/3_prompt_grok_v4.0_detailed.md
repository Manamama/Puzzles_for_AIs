Objective: Write a Python function red_spiral(n) that creates an n × n grid and paints a sparse, clockwise spiral of red squares () starting from the center, using white squares () as the background. The spiral moves in a sequence of increasing steps (1, 2, 3, …) in directions Right, Down, Left, Up, cycling clockwise, painting exactly floor(n²/2) + 1 tiles. Print the grid after each directional move (or when a move is skipped due to bounds), using space-separated emojis and a blank line between grids.
Requirements:
Input: A positive integer n (e.g., n=5, n=6, n=8), representing the grid size.
Grid Setup:
Create an n × n grid initialized with  (white square emoji, U+2B1C).
Use standard indexing: rows as y, columns as x (e.g., grid[y][x]).
Starting Point:
Begin at the center (floor(n/2), floor(n/2)), e.g., (2, 2) for n=5.
Paint the center with  (red square emoji, U+1F7E5) and count it as one tile.
Print the initial grid.
Spiral Movement:
Move in a clockwise spiral: Right, Down, Left, Up, repeating.
Use a direction indicator (e.g., 0=Right, 1=Down, 2=Left, 3=Up) and cycle it using modulo (e.g., (direction + 1) % 4).
Each move attempts k steps (k=1, 2, 3, …), increasing linearly per move (not paired like Ulam spirals: 1, 1, 2, 2, …).
Compute next positions incrementally (e.g., for Right, x += 1; for Down, y += 1) without direction arrays or complex formulas.
Painting Rules:
For each step, if the position (x, y) is within bounds (0 ≤ x, y < n), paint it  and increment the tile count.
The spiral’s path naturally avoids overlaps due to its linear steps and clockwise pattern; no explicit collision checks are needed.
Termination:
Stop when exactly floor(n²/2) + 1 tiles are painted (e.g., 12 for n=5, 19 for n=6, 33 for n=8).
Check the tile limit before starting each move, allowing the final move to complete fully if within bounds.
If a step is out of bounds, print the current grid and terminate without painting further.
Output:
Print the grid after each directional move (e.g., after k steps in one direction) or when a move is skipped due to bounds.
Each grid is printed with space-separated emojis, one row per line, followed by a blank line.
For n=5, expect 6 grids (initial + 5 moves); for n=6, expect 7 grids; for n=8, expect 10 grids.
Constraints:
Use minimal code: avoid imports (e.g., math.floor), direction arrays, flags for validity, or redundant checks.
Prefer Python’s integer division (//) for floor operations.
Start the step counter at 0 and increment it to achieve moves of 1, 2, 3, … steps.
Use a single loop structure with nested steps, combining bounds checking and painting greedily.
Assume n is a positive integer; no input validation required.
Example Output for n=5:
Initial grid (1 tile at (2, 2)):⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ 🟥 ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
After 1 step Right (2 tiles):⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ 🟥 🟥 ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
After 2 steps Down (4 tiles):⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ 🟥 🟥 ⬜
⬜ ⬜ ⬜ 🟥 ⬜
⬜ ⬜ ⬜ 🟥 ⬜
After 3 steps Left (7 tiles):⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ 🟥 🟥 ⬜
⬜ ⬜ ⬜ 🟥 ⬜
🟥 🟥 🟥 🟥 ⬜
After 4 steps Up (11 tiles):🟥 ⬜ ⬜ ⬜ ⬜
🟥 ⬜ ⬜ ⬜ ⬜
🟥 ⬜ 🟥 🟥 ⬜
🟥 ⬜ ⬜ 🟥 ⬜
🟥 🟥 🟥 🟥 ⬜
After 5 steps Left (12 tiles, terminates):🟥 🟥 🟥 🟥 🟥
🟥 ⬜ ⬜ ⬜ ⬜
🟥 ⬜ 🟥 🟥 ⬜
🟥 ⬜ ⬜ 🟥 ⬜
🟥 🟥 🟥 🟥 ⬜
Test Cases:
red_spiral(5): 12 tiles, 6 grids, as above.
red_spiral(6): 19 tiles, 7 grids, ending in a partial top-row turn.
red_spiral(8): 33 tiles, 10 grids, ending in a full top-row turn.
Hints:
Use a single while loop for moves, with a nested for loop for steps.
Initialize the step counter at 0, incrementing it to start moves at 1 step.
Terminate with return on out-of-bounds or break after reaching the tile limit, avoiding validity flags.
Trust the spiral’s path to avoid overlaps due to its linear, clockwise design.
Use // for integer division to compute the tile limit without imports.
Print after each move or on termination, ensuring the correct grid count.
Anti-Patterns to Avoid:
Do not use Ulam spiral steps (1, 1, 2, 2, …).
Avoid direction arrays (e.g., [(1, 0), (0, 1), …]); use incremental updates (x += 1, y += 1).
Do not stop mid-move when the tile limit is reached; complete the move if within bounds.
Avoid redundant checks for painted tiles, as the spiral’s path is unique.
Do not use imports like math.floor or extra flags for move validity.
Do not print per step (e.g., 13 grids for n=5); print per move (6 grids for n=5).


