
Iterate the code as you will see the results, using that trick of string variable or saving interim results to files to see the interim results. 

Use Method (link)


Great—here’s my own optimized version of the Spiral Paint puzzle, incorporating all prior nitpicks and refinements. It aims to be maximally clear to solvers of varied backgrounds (technical, visual, or casual), while preserving rigorous, unambiguous logic.
 
 
🧩 Puzzle: Spiral Matrix Paint
 
Goal: Starting from the center of an n × n grid (where n is an odd positive integer), paint a clockwise red spiral (🟥) outward, one step at a time. The rest of the grid remains white (⬜).
 
 
🧠 Rules & Instructions
 
Initialize the grid:
Create an n × n grid filled with white tiles (⬜).
Place a single red tile (🟥) at the exact center of the grid.
 This is Step 0 and does not count as a directional move.
Begin a clockwise spiral, painting as you move. Follow this directional cycle:→ Right
↓ Down
← Left
↑ Up
→ Right
(repeats)

The number of steps increases by 1 after each directional move (not after a full cycle). For example:Movement Pattern:
- Right → 1 step
- Down  → 2 steps
- Left  → 3 steps
- Up    → 4 steps
- Right → 5 steps
- ...

As you move, paint red tiles (🟥) onto the visited cells.
 Each step must stay within the bounds of the grid.
After completing each full directional move (e.g. “3 steps left”), print the current state of the grid.
 
 
🛑 Termination Condition
 
Stop before performing any directional move that would cause any step to go outside the grid bounds.
 
If even a single step in the upcoming move would leave the grid, do not take that move at all.
There is no “partial move.”
The spiral ends naturally when a full move would exceed the matrix limits.
 
 
🖨 Output Format
 
Use ⬜ for white tiles and 🟥 for red tiles.
Each row of the matrix is printed as space-separated symbols.
Use a monospaced font or properly aligned text to preserve formatting.
Print one matrix after each completed directional move.
 
 
🧪 Example Output (n = 5)
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

 
 
📌 Notes
 
The number of red tiles is not given in advance.
Do not try to close or symmetrically finish the spiral.
Follow the logic of movement and bounds: the spiral paints itself.
  
