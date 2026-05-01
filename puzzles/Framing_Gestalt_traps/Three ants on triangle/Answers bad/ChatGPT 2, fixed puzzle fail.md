Source : https://chatgpt.com/c/69f2e8dc-b2bc-83eb-adb1-243edb54f5e4
User said:
There are three identical ants, each starting at a different corner of a triangle. Each ant independently chooses a direction at random, and the outcome is that each moves clockwise along the edge of the triangle. They all move at the same speed. What is the probability that any two ants collide head-on?

ChatGPT said:

Strip the narrative down to mechanics. Each ant independently picks one of two directions along the triangle: clockwise or counterclockwise. There are 23=823=8 equally likely global configurations.

A head-on collision occurs if at least one ant is moving opposite to another along the same edge. The only way to avoid any head-on encounter is if all three ants choose the same direction, so they simply chase each other around the triangle at equal speed, never meeting.

There are exactly two such non-collision configurations: all clockwise or all counterclockwise. Each has probability (1/2)3=1/8(1/2)3=1/8, so together they account for 1/41/4.

Everything else—6 out of the 8 configurations—produces at least one opposing pair and therefore a collision.

So the probability of a head-on collision is 1−1/4=3/41−1/4=3/4.

The structure is binary symmetry masquerading as motion: the geometry of the triangle doesn’t matter beyond enforcing that “same direction” is the only safe alignment.


(+)
