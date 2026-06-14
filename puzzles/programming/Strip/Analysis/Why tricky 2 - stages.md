Harder than it looks, but not for the reason most people think.

The difficulty is not recognizing lines, labels, or even the fold. Modern vision models are generally capable of extracting:

measurements: - 3 cm vertical - 3 cm horizontal - 5 cm overlap - 75 cm total 

and can usually identify:

objects: - flat strip - folded strip 

The real difficulty is selecting the correct abstraction level.

There are roughly five stages:

PNG ↓ Drawing primitives ↓ Diagram objects ↓ Geometric model ↓ Solving model ↓ Answer 

Most failures occur between stages 3 and 4.

Stage 1: PNG → Drawing primitives

Usually easy.

Extract:

line: dashed: true dimension: value: 3 cm 

etc.

This is basically OCR + shape detection.

I would expect a good vision model to get this mostly right.

Stage 2: Drawing primitives → Diagram objects

Still relatively easy.

Infer:

piece_A: rectangle piece_B: folded rectangle 

and

overlap: 5 cm 

This is already more semantic.

Stage 3: Diagram objects → Geometric model

This is where things get dangerous.

The model must decide:

fold: interpretation: ? 

There are multiple plausible choices.

Wrong model

fold: consumes_length: - 3 up - 3 top 

This is essentially what produced 41.5.

Correct model

fold: path: - 3 up - 3 across - 3 down 

This produces 43.

Notice that the image itself does not literally contain:

9 cm 

anywhere.

The model must infer a material path through the folded object.

That is not OCR anymore.

That is geometric reasoning.

Stage 4: Geometric model → Solver YAML

This is where your first YAML was unusually good.

You encoded:

path: - vertical - horizontal - vertical 

without yet solving.

That representation almost forces the correct solution later.

In fact, I'd say your first YAML already contained about 80% of the solution information.

Not numerically.

Structurally.

Why the right YAML is the key

Imagine two YAMLs.

Wrong:

fold: rise: 3 top: 3 

Correct:

fold: rise: 3 top: 3 descent: 3 

The difference is one line.

Yet the answer changes.

That is because the puzzle's entropy is concentrated almost entirely in the representation.

Once the representation is right:

material_length: 9 projection: 3 

the arithmetic is trivial.

How difficult is it for an AI?

I'd estimate:

TaskDifficultyOCR labelsLowDetect foldLowExtract measurementsLowBuild object graphMediumInfer material pathHighChoose correct abstractionVery HighSolve after correct abstractionTrivial

The surprising thing is that the last step is the easiest.

The hard part is answering:

What exactly is the thing I am looking at?

rather than:

Given the thing, what is the answer?

Why your YAML experiment is interesting

Most benchmark puzzles score only the final answer.

But this puzzle reveals something deeper.

There is a hidden latent object:

material_path: - up 3 - across 3 - down 3 

Humans who solve the puzzle correctly usually construct that object mentally.

Humans who fail usually construct:

material_path: - up 3 - across 3 

or some equivalent incomplete representation.

The algebra then merely reflects whichever object was built.

So if I were designing a system to solve this class of puzzle robustly, I would not train it to predict the answer.

I would train it to emit a structural YAML first.

Because the answer becomes almost a by-product of having selected the correct intermediate representation.

