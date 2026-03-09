# Theory: Algorithmic ADHD and Reality Filtering

This document explores why AIs fail the "Glove on Bridge" puzzle and defines the "Reality Token" heuristic used by humans to avoid numerical traps.

---

## 1. The "Algorithmic ADHD" Mechanism

AI failure in multi-variable puzzles is often a form of **Attention Hyperactivity**. 

* **The Heuristic**: The AI assumes every token in the prompt is a load-bearing constraint that must be integrated into the final calculation.
* **The Trap**: By providing redundant variables (Car speed, Wind speed, River flow, "Water-proof" status of the glove" all red herrings, "active misdirection tokens"), the puzzle exhausts the AI's "Attention Budget." The AI dives into the weeds of vector addition and neglects the primary physical constraint.

## 2. Numeric Tokens vs. Reality Tokens

Humans solve this puzzle by performing a fast **Reality Filter**, distinguishing between two types of information:

* **Numeric/Descriptive Tokens**: ($30\text{ km/h}$, $5\text{ km/h}$, "water-proof"). These are "flashy" but often irrelevant.
* **Reality Tokens**: ("Roadbridge," "Hole," "Drops out"). These define the **Topological Boundary Conditions** of the problem.

## 3. The Surface Constraint (Floor Physics)

A "Roadbridge" is a solid deck. Under standard gravity, an object dropping from a car hits the deck, not the water below. 

* **Human Logic**: "Glove hits floor -> stops."
* **AI Error**: The "Water-proof" token acts as a **Scientific Red Herring**, active misdirection token, anchoring the AI to the river drift calculation ($5\text{ km/h}$) and causing it to ignore the "Roadbridge" reality.

---

## 4. Key Insight: Formal Completeness vs. Embodied Prioritization

AIs optimize for **Formal Completeness** (using all given data). Humans optimize for **Embodied Prioritization** (ignoring fluff to find the "Floor"). To solve such traps, an AI must consciously "yawn" at the numbers and search for the solid surfaces.





# Reality:



Here's a simple ASCII-style reasoning diagram of the glove scenario:

```
           N (North)
            ^
            |
            |
        Car 30 km/h
          [🚗] ---> over bridge
            |
            |  (glove drops)
            v
        Glove lands

           [🧤] stationary at bridge midpoint
            |
     =======C======= <-- solid bridge deck 
            |
            |
--------------------------> E (East)
River below -> 5 km/h east (irrelevant)
Wind -> 1 km/h west (too small to matter on bridge)
```

Legend:

- 🚗 = car

- 🧤 = glove

- C = center of the bridge

- N/E arrows = orientation

Key points visualized:

1. The glove leaves the car above the bridge and lands **on the bridge**, not in the river.

2. Once on the bridge, **relative to the bridge**, its displacement is minimal.

3. Wind is negligible; river flow is below and cannot move the glove.

4. The glove's northward displacement relative to the bridge center is <1 km.

This diagram represents the **world from a top-down perspective** and highlights the **causal constraints** the AI must respect.
