# Solution: The Via Negativa Proof (Convex Pentagon)

Via: The complement of the pentagon in the plane


**The Answer**: The probability is **50%**.

---

## The Formal Derivation

### Step 1: The Partition of the Plane
Extend each of the 5 sides of the convex pentagon into infinite lines. These lines divide the plane into regions external to the pentagon.

### Step 2: The "Visible Side" Invariant
From any point in an external region, the number of visible sides is constant.
*   Crossing a line (an extension of a side) changes the visibility of *that specific side*.
*   Therefore, moving from one angular sector to the next changes the visible count by exactly $\pm 1$.

### Step 3: The Topological Constraint
For a convex pentagon ($n=5$):
*   You cannot see 1 side (requires non-convexity or being "inside" a vertex angle, impossible at infinity).
*   You cannot see 4 or 5 sides (requires seeing $>180^\circ$ of the shape).
*   **Result**: You can only ever see **2** or **3** sides.

### Step 4: The Parity Argument
Since the visible count changes by $\pm 1$ at each sector boundary, and the only possible values are $\{2, 3\}$, the count must **alternate** between 2 and 3 as you circle the pentagon.

### Step 5: The Symmetry of Probability
*   There are 5 sectors where you see 2 sides.
*   There are 5 sectors where you see 3 sides.
*   In the limit of infinity (uniform angular distribution), the total angle subtended by the "2-side" sectors is exactly equal to the total angle of the "3-side" sectors.
*   **Total Probability**: $P(2) = P(3) = 0.5$.

---

**Note**: This result is independent of the pentagon's specific shape (regular or irregular), provided it remains convex.
