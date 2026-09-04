**50%**  

For any convex pentagon, if you choose a random point far away (or equivalently, a random direction from which to view it), the number of sides you see is either **2** or **3**. These two possibilities are equally likely, so the probability of seeing exactly two sides is exactly **½**, or **50%**.

### Why?

Imagine standing far from the pentagon. The sides you see are those whose **outward normals** point roughly toward you—more precisely, a side is visible if its outward normal lies within 90° of your viewing direction.

The five outward normals are spaced around the full circle. Their angular gaps are the **exterior angles** of the pentagon, which sum to 360°. As you rotate your viewing direction, a moving 180° “window” sweeps over these normals. Because there are an odd number of normals (5), the window always contains either 2 or 3 of them.  

A classic fact: for any odd number of points on a circle (with no two opposite), exactly **half** of all viewing directions make the window contain the smaller number (2), and half make it contain the larger number (3). Thus the probability is 1/2.

*(If you pick a point uniformly in a large disk instead of a direction at infinity, the probability tends to the same 50% as the disk grows.)*