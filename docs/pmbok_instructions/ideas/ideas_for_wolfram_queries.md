Query: "Number of ways to arrange 5 distinct books on a shelf where 2 specific books must be adjacent"Why it should work: This is a permutation problem with a constraint (adjacency), which Wolfram Alpha can handle by treating the two books as a single “block” (4! × 2 = 48 ways). It’s unusual due to the specific constraint but remains a standard combinatorial task.
Expected output: The API should return 48, possibly with an explanation of the block method and permutations.
Avoiding failure: This avoids complex group theory or specialized data, sticking to discrete math.

Query: "Speed of sound in helium at 100°C"Why it should work: Wolfram Alpha has data on physical properties of gases (e.g., helium’s molar mass, specific heat ratio) and can compute the speed of sound using the formula sqrt(γRT/M). The temperature (100°C) adds a slight twist but is well within the API’s capabilities.
Expected output: Approximately 1110 m/s, with possible additional details like comparisons to air.
Avoiding failure: Unlike the high-pressure tungsten query, this uses standard conditions and available data.

Query: "Area of a regular octagon inscribed in a circle of radius 5"Why it should work: This is a geometry problem requiring the formula for the area of a regular n-gon inscribed in a circle (A = (n/2) × r^2 × sin(2π/n)). For an octagon (n=8), it’s a straightforward computation that Wolfram Alpha can handle. It’s unusual due to the specific shape and context.
Expected output: Approximately 141.42 square units, possibly with a diagram or derivation.
Avoiding failure: This avoids complex constraints or symmetry considerations, unlike the dodecahedron coloring query.

Query: "Probability that a random walk on a 1D lattice returns to the origin after 10 steps"Why it should work: Random walk problems are well-supported in Wolfram Alpha, especially for simple cases like a 1D lattice (equal probability of moving left or right). The probability of returning to the origin after 2n steps involves binomial coefficients, which the API can compute.
Expected output: For 10 steps, the probability is (10 choose 5) / 2^10 ≈ 0.246, with possible visualizations of the walk.
Avoiding failure: This is simpler than the multi-component failure rate query, focusing on a single, well-defined probabilistic model.

Query: "Magnetic field strength at the center of a square loop of side 10 cm carrying 2 A current"Why it should work: This is a physics problem using the Biot-Savart law, which Wolfram Alpha can compute for simple geometries like a square loop. It’s unusual due to the square shape (less common than circular loops) but still within the API’s electromagnetic capabilities.
Expected output: A numerical value (approximately 2.83×10^-5 T), possibly with a derivation or plot.
Avoiding failure: This avoids extreme conditions or relativistic effects, unlike the neutron star query.

Query: "Number of positive integer solutions to x + y + z = 30 where x ≤ 10 and y ≥ 5"Why it should work: This is a combinatorial problem solvable using generating functions or direct counting, which Wolfram Alpha supports. The constraints make it slightly unusual but keep it within the API’s parsing capabilities.
Expected output: The number of solutions (likely computed via inclusion-exclusion or generating functions), possibly listing some solutions.
Avoiding failure: This is more straightforward than the integer partition query, with fewer constraints.

Query: "Wavelength of light emitted when an electron in a hydrogen atom transitions from n=4 to n=2"Why it should work: This is a quantum mechanics problem using the Rydberg formula, which Wolfram Alpha can compute. It’s unusual due to the specific energy levels but standard for atomic physics.
Expected output: Approximately 486.1 nm (Balmer series, H-alpha line), with possible spectral details.
Avoiding failure: This avoids the complexity of general relativity or high-pressure data, focusing on a well-known physical system.

Query: "Volume of a torus with inner radius 3 cm and outer radius 7 cm"Why it should work: The volume of a torus (2π^2 × R × r^2) is a standard geometric calculation that Wolfram Alpha can handle. The specific radii make it slightly unusual but computable.
Expected output: Approximately 987.6 cm^3, possibly with a diagram or formula.
Avoiding failure: This is simpler than the dodecahedron or high-pressure queries, relying on standard geometry.

