# Assumptions Log

- A1: Starting tile is at the exact center `(n//2, n//2)`.
- A2: Spiral expands clockwise following the sequence: Right → Down → Left → Up.
- A3: A "distinct growth phase" is defined as the completion of each segment of movement (e.g., after moving right, then after moving down, etc.), or after each new set of tiles.
- A4: `n` (grid size) will be an odd number, ensuring a single exact center tile.
- A5: The output should use `🟥` for red tiles and `⬜` for white tiles.