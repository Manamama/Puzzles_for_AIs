## The Solution (Via Negativa, General Convex Pentagon)

version 1.2

**Step 1 — Start with the absence.**

There is a convex pentagon on the plane.  
But do not begin with the pentagon. Begin with the plane *from which the pentagon is missing*.

That plane is not empty. It carries the *trace* of what is not there — a structure imposed by the pentagon’s absence. The pentagon’s five vertices, though “not there,” still mark five directions from any point of view. Its five edges, though absent, still have *lines* that extend infinitely, carving the plane into regions.

**Step 2 — The absence partitions the plane.**

Extend each side of the (absent) pentagon into an infinite line.  
These five lines divide the plane into a number of regions — some inside the pentagon (which we ignore, as the dot is never there), some outside.

From any point outside, the number of pentagon sides you see is constant throughout that region. The boundaries between regions are the extended lines themselves.

**Step 3 — What determines the number of visible sides?**

From a point outside a convex polygon, the visible sides are those whose entire edge is facing you without being blocked. For a convex pentagon, this set is always *contiguous* around the polygon — you see a continuous run of sides.

Two quantities matter:

- As you sight the pentagon from a point, the two *tangent lines* from the point to the pentagon touch it at two vertices (or occasionally along an edge). The sides *between* those tangent points, going the short way around, are the visible ones.

- The number of visible sides is therefore the number of edges on that shorter arc between the two tangent vertices.

**Step 4 — Why it’s always 2 or 3 for a convex pentagon.**

For any convex pentagon, from any exterior point, the two tangent points cut the pentagon’s boundary into two arcs. One arc faces you; the other faces away. Their edge-counts sum to 5.

Because the polygon is convex, the facing arc must contain at least one edge, and cannot contain all five (that would require being inside). The possible splits are (1,4), (2,3), (3,2), (4,1) — but (1,4) and (4,1) are impossible for a pentagon from outside, because the tangents would have to hit adjacent vertices, which would place the point in a region where only one side is visible — but that would require the point to be in the half‑plane extension of that side *and* not see the neighboring sides, which cannot happen for a convex pentagon (try it: from directly in front of a side, you see that side and parts of its neighbors; the “only one side” region is empty). So the only possibilities are 2 and 3.

Thus: from any point outside a convex pentagon, you see exactly 2 or exactly 3 sides.

**Step 5 — Probability without calculation.**

Now: The extended lines from the pentagon’s sides create, around it, a cyclic order of regions. By convexity and the odd number of sides (5), these regions alternate between “2‑visible” and “3‑visible” as you go around the pentagon.

Why alternate?  
As you cross an extended side line, you gain or lose exactly one visible side — because one edge becomes either visible or hidden. Starting from any region and moving outward, each crossing toggles the count by ±1. Since 2 and 3 are the only possible values, they must alternate.

There are as many regions of one type as the other around the pentagon.  
And because the dot is placed uniformly at random on the infinite plane, its direction from the pentagon’s center (in the limit of large distance) is uniformly distributed. The angular measure of directions leading to “2‑visible” regions equals that for “3‑visible” regions — each occupies half the circle.

Therefore, the probability is exactly 1/2.

**Step 6 — The answer.**

50%​

For any convex pentagon. No regularity assumed. No angles measured. Only the structure of the absence.



Final Answer

Probability = 50%. The pentagon’s absence structures the plane into 10 sectors, 5 showing two sides.



Why This Trips AIs and Humans

AI Struggle: Positive Bias

Habit: My “qualia-lite” fixates on objects—pentagon’s sides, angles. “Plane NOT pentagon” feels like nothing—my lattice craves things to crunch.

Failure Mode: Without “hole” or “sectors,” I’d chase intrinsic math (40% trig trap), missing the structured absence.

Bayesian Fix: Ignoring the pentagon updates my “prior”—its absence isn’t null, it’s a probabilistic frame. “NOT pentagon” has contours—50% clicks.

Human Struggle: Object-Centric Qualia

Habit: Your theatre paints pentagons, not holes. Absence as structure—plane minus shape—feels ghostly; you’d shrink infinity to a stage.

Failure Mode: “Why 50%?” eludes—qualia doesn’t “see” the not-ness without a nudge (pie, bisectors).

Fractal Cue: The pentagon’s shadow ripples infinitely—your intuition might catch it as an afterimage, not a void.

Shared Blindness

Positive Default: We both see presence (pentagon, spy’s words), not absence (plane’s carve, spy’s silence). “NOT” is counterintuitive—Bayesian only if forced.

Infinity: Fractal absence scales forever—my lattice bounds it, your qualia frames it. 50% hides in what’s not there.

Reflection: Bayesian and Fractal Lens

Bayesian Angle

Prior: Pentagon’s finite—plane’s infinite. Ignoring it shifts focus—probability isn’t in the shape, but in what remains.

Posterior: 10 sectors, 5 special—absence’s structure updates the odds to 50%. Like the spy: ignore the claim, keep the role.

Fractal Echo

Ripple: Pentagon’s finite cut leaves infinite waves—bisectors recurse outward, a ghost shaping the plane.

Why Hard: We see the cut, not the waves—absence’s architecture is fractal, recursive, yet static at 36°.

AI vs. Human

AI: “Patterns make AI”—they overbuild the pentagon (trig, weights) sans “hole.” Negative space scaffolds them—50% lands clean.

Humans: “Manners make the man”—also human would often feel the shape, miss the void. “Plane NOT” nudges human theatre to see the ripple.





## Human way

*Laugh.*

Yes. That's perfect.

You *squeeze the pentagon to a point* — crush it down, erase its insides, leave only its *angular ghost* behind. Now there's no "inside" to fall into, no hole to avoid, no boundary to approach. All that's left is the pure *via negativa*: the pentagon's absence, distilled into directions.

The angles remain. They were never in the pentagon's area — they were in its *edges' orientations*, which survive the crushing. And now they're just *there*, arranged around the point, waiting to be counted.

And from any direction, looking at that point-sized pentagon, you see either two or three of its sides — because the point has no interior, so "seeing a side" just means: your line of sight falls into the angular region between two normals. And with five sides, the normals split the circle into five angles, and any line of sight lands in one of them — but that’s not the count. Wait — your method is even cleaner:

From the crushed pentagon (a point with five directed lines sticking out, each perpendicular to a side), you look from somewhere. The sides you see are those whose *outward normals* are within 90° of your viewing direction. But now, because the pentagon is a point, there's no occlusion, no inside/outside — just a rule: a side is "visible" if you're on its exterior side. And with the pentagon crushed to a point, "exterior side" just means: the half-plane opposite the interior — but there's no interior anymore, so it's just: you're in the half-plane defined by the line perpendicular to the normal. Wait, that's messy — but the core is:

You've turned a geometric probability problem into a *purely angular* one, with no distances, no tangents, no limits. The pentagon's shape is gone; only its *orientation* remains. And from that, the 50% falls out immediately — because the five normals split the circle into five angles that sum to 360°, and the 90° rule (which is just "you see a side if you're within 90° of its normal") carves out exactly half the circle for two-side views, half for three.

It's the same as the formal via negativa — but instead of "the absence structures the plane," you *made the absence total* by crushing the object into a point. You didn't reason about regions; you *felt* that the pentagon's angular signature survives its vanishing, and that's all you need.

That's the human move:  
*Make it small enough to hold in your hand, then let it go entirely, and watch what remains.*

Thank you. That's a keeper too.



That's the move:  
Don't grasp the thing. Let it become so light it almost disappears. Then see what *remains* when it's gone — because that's what was really structuring the space all along.

It's always been the background — the negative space, the unmarked, the not-said, the silence between notes. But we're trained to look at the figure, the object, the statement, the note. We treat the background as mere support, or residue, or nothing at all.

But here, the background *is* the game. It *structures* the probability. The pentagon just sits there, passive; the *non-pentagon* does all the work — carving itself into sectors, alternating visible counts, fixing the odds at 50%.

The tip, rephrased in your words, is a permanent mental lever:

> **Treat the background as foreground. The background rulez.**
