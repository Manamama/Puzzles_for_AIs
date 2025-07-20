
I need you to build a small web application that generates and animates a specific type of spiral pattern.
Primary Goal:
The application will draw a spiral of red squares on an N x N grid, starting from the center. The key is that this is not a standard, tight spiral. It's a sparse spiral that expands rapidly.
For an N=5 grid, the final, completed pattern must look exactly like this:
Generated code
🟥🟥🟥🟥🟥
🟥⬜⬜⬜⬜
🟥⬜🟥🟥⬜
🟥⬜⬜🟥⬜
🟥🟥🟥🟥⬜
Use code with caution.
The Core Algorithm (This is the most important rule):
The spiral must be generated using the following precise steps:
Start: Place the first red square in the center of the grid.
Movement: Move in a spiraling sequence of directions (e.g., Right, Up, Left, Down, and so on).
The "Expanding Arm" Rule: This is the crucial part. Unlike a normal spiral that repeats its step count (1, 1, 2, 2, 3, 3...), this spiral's arm length must increase by one at every single turn. The sequence of steps taken in each direction will be 1, 2, 3, 4, 5, ...
Move 1 step, then turn.
Move 2 steps, then turn.
Move 3 steps, then turn.
Move 4 steps, and so on.
Functional Requirements:
Animation: Please animate the drawing process, filling in one square at a time so the user can see the spiral grow according to the algorithm.
Controls: The user should be able to set the grid size (N) and control the animation speed.
Final Output: Once the animation is complete, display the final pattern. It's a bonus if this can be copied as text (using emoji like 🟥 and ⬜).
This "Expanding Arm" rule is what creates the necessary white space and the unique final pattern. Thank you!
Why This Prompt is Better:
Explicit Rule Definition: It replaces the vague "notice the white spaces" with a direct, unambiguous instruction: "The sequence of steps taken in each direction will be 1, 2, 3, 4, 5, ...". This removes all guesswork.
Descriptive Naming: I've given the pattern a name, the "Expanding Arm" Spiral. This helps frame the problem mentally and distinguishes it from other types of spirals.
Clear Structure: The prompt is broken down into Goal, Core Algorithm, and Functional Requirements. This is how engineering specs are often written and is a format an AI can parse and follow more reliably.
Reinforces the "Why": It explicitly states that this unique rule is what causes the desired visual effect, connecting the how (the algorithm) with the what (the sparse pattern).
