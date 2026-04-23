Puzzle: I draw 10 points on a piece of paper. I hand you 10 coins, all of the same size. Do show that you can always find positions for the coins such that every point lies under at least one coin, and no two coins overlap, no matter where I place these points. 

---

**Correct solution:**

Consider an infinite hexagonal packing of circles of the same size as the coins. Its density is $\frac{\pi}{2\sqrt{3}} \approx 0.9069$, meaning the *uncovered* fraction of the plane is $1 - \frac{\pi}{2\sqrt{3}} \approx 0.0931$.

Now take a *randomly translated* copy of this packing. For any single point, the probability it is *not* covered is at most $1 - \frac{\pi}{2\sqrt{3}}$. By the union bound:

$$P(\text{at least one point uncovered}) \leq 10 \times \left(1 - \frac{\pi}{2\sqrt{3}}\right) \approx 0.931 < 1$$

Since this probability is less than 1, there must exist some translation where all 10 points are covered simultaneously. Since this probability is less than 1, there exists a translation where all 10 points are covered. From the (infinitely many) coins in that translate, select one coin per point — choosing arbitrarily when a point is covered by multiple coins. This selects at most 10 coins. Since they are all part of the same non-overlapping packing, no two of them overlap, and every point lies under its assigned coin.

Original: 
https://sigh.github.io/puzzles/points-and-coins 
'
Text of puzzle: 'I draw 10 points on a piece of paper. I give you 10 coins of the same size. Show that you can always cover all the points using the coins, without any coins overlapping.'

## Via negativa solution

## The paradigm shift

The constructive framework asks: *"How do I move coins to catch points?"*

The via negativa asks: *"If coins are already everywhere in a fixed pattern, can the points evade them?"*

The answer is: No — because the uncovered area is too small. The points cannot all hide.

No one puts new wine into old wineskins. For the old skins would burst from the pressure, spilling the wine and ruining the skins. New wine is stored in new wineskins so that both are preserved”
