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




Critical Constraints:
Step length increments after EVERY direction change
Terminate when count reaches n²/2 + 1
Never repaint already red tiles
Maintain strict Right→Down→Left→Up cycle
Show all intermediate states
Why This Works:
Continuous step increment (1,2,3,4...) creates expanding arms
~50% fill limit preserves natural whitespace
Direction cycling produces clean spiral pattern
Early termination leaves some arms incomplete
Visual Hallmarks:
Growing spiral arms with increasing length
Approximately equal red and white areas
Some incomplete arms at edges
Clear clockwise rotation
This specification accurately describes the working code's behavior without introducing false patterns. The key insight is that the organic sparsity emerges from:
Continuous step increment (not every 2 directions)
Careful fill limiting
Strict direction cycling

