Puzzle: Spiral rightwards to inwards

Wow. Try coding it rightwards. 
Start:
⬜ ⬜ ⬜ ⬜ 🟥
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜
⬜ ⬜ ⬜ ⬜ ⬜


Spiral Rightwards:
⬜⬜⬜⬜🟥
🟥🟥🟥⬜🟥
🟥⬜🟥⬜🟥
🟥⬜⬜⬜🟥
🟥🟥🟥🟥🟥

Start from the top right corner of the matrix.
Initialize the step size to the matrix size.
Begin moving in a rightwards direction, filling the matrix with the desired elements.
After completing a rightwards movement, decrement the step size.
Change the direction to downward and continue filling the matrix.
Repeat the  movements, decrementing the step size until the entire matrix is filled, leaving the white tiles between.

Task: code it in python.
