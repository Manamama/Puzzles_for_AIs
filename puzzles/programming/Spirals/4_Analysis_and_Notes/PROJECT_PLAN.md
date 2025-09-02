# Project Plan

## Objective
Create an n×n grid where a spiral grows outward from the center, painting approximately half the tiles red (🟥) while showing all intermediate states. The spiral should begin at the exact center tile (already red), expand clockwise (Right→Down→Left→Up cycles), show each distinct growth phase, and naturally preserve whitespace by terminating after filling ~50% of the grid.

## Success Criteria
- Produces the correct spiral pattern as per the example for n=5.
- Shows all distinct growth phases as defined (after each new turn or each new set of tiles).
- Naturally preserves whitespace, creating a sparse spiral.
- Uses `🟥` and `⬜` Unicode characters for grid output.

## Scope Boundaries
- The exact percentage of red tiles is not a strict requirement; approximate is sufficient, following the sparse spiral logic.
- Initial development and testing will focus on n=5, but the underlying code should be universally applicable for odd `n`.