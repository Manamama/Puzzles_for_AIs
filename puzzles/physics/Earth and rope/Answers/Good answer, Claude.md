Let r = 6,378,000 m and h = 1 m.

**Step 1: tangent length d**

The lifted point is at distance r + h from the centre. The tangent from that point to the sphere gives a right triangle:

$$d = \sqrt{(r+h)^2 - r^2} = \sqrt{2rh + h^2} = \sqrt{12{,}756{,}001} \approx 3571.56 \text{ m}$$

**Step 2: the angle α**

The arc removed on each side subtends angle α at the centre, where:

$$\alpha = \arctan\!\left(\frac{d}{r}\right) = \arctan\!\left(\frac{3571.56}{6{,}378{,}000}\right) \approx 5.601 \times 10^{-4} \text{ rad}$$

**Step 3: extra length**

The original rope had arc 2πr. The new rope has two tangent segments of length d plus the remaining arc 2(π − α)r:

$$\Delta c = 2d - 2\alpha r = 2(3571.56) - 2(5.601\times10^{-4})(6{,}378{,}000)$$

$$= 7143.119 - 7142.364 = \boxed{0.755 \text{ mm}}$$

The near-cancellation of two ~7 km quantities down to sub-millimetre is what makes this problem so counterintuitive — and so lethal for models that lose numerical precision early.


