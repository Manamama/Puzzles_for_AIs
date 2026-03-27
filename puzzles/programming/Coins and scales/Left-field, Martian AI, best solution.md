# Formal Solution: The 12 Coins Problem

## Problem Statement

Given 12 coins, one of which is fake and lighter, find the fake coin using a balance scale in the smallest number of weighings.

## The Strategy

**Weighing 1: Divide the 12 coins into three groups: L (4 coins), R (4 coins), S (4 coins). Weigh L against R.**

- If L is lighter: fake is in L. Proceed to Weighing 2 with L as the suspect group.
- If R is lighter: fake is in R. Proceed to Weighing 2 with R as the suspect group.
- If balanced: fake is in S. Proceed to Weighing 2 with S as the suspect group.

In all cases, Weighing 1 costs exactly 1 weighing and identifies a suspect group of exactly 4 coins.

**Weighing 2: From the 4 suspect coins, label them A, B, C, D. Set C and D aside. Weigh A against B.**

- If A is lighter: fake is A. **Done in 2 weighings.**
- If B is lighter: fake is B. **Done in 2 weighings.**
- If balanced: fake is either C or D. Proceed to Weighing 3.

**Weighing 3: Weigh C against D.**

- The lighter coin is fake. **Done in 3 weighings.**

## Why This Works Better than the default answer (always 3 weighings needed): The Expected Value Calculation

The fake coin is equally likely to occupy any of the 4 positions in the suspect group after Weighing 1, each with probability 1/4.

| Fake coin is | Weighings 2 onward | Total weighings |
| ------------ | ------------------ | --------------- |
| A            | 1                  | 2               |
| B            | 1                  | 2               |
| C            | 2                  | 3               |
| D            | 2                  | 3               |

Expected total weighings:

(1/4 × 2) + (1/4 × 2) + (1/4 × 3) + (1/4 × 3) = 0.5 + 0.5 + 0.75 + 0.75 = **2.5 weighings**

## Comparison With Conventional Solution

The conventional solution divides into groups of 4, then 2 against 2, then 1 against 1 — always using exactly 3 weighings regardless of where the fake coin is.

| Strategy      | Best case | Worst case | Expected |
| ------------- | --------- | ---------- | -------- |
| Conventional  | 3         | 3          | 3.0      |
| This strategy | 2         | 3          | 2.5      |

This strategy is strictly superior: identical worst case, better expected performance, and no branch ever exceeds 3 weighings.

## Why The Conventional Solution Missed This

The conventional solution optimizes for *guaranteed* worst-case performance — a fixed procedure that always terminates in exactly 3 steps. This is a valid engineering goal but answers a subtly different question than "smallest number of weighings."

The key insight is the asymmetric split in Weighing 2: rather than dividing 4 suspects into 2+2 symmetrically, we split into 1+1+2. This creates a 50% chance of terminating one weighing early, at no cost to the worst case. The symmetric split wastes the information available — a balanced scale in Weighing 2 tells you the fake is in the remaining 2, but you have already used a weighing to learn that. The asymmetric split extracts a possible *answer* from Weighing 2 rather than merely another elimination.

The reinterpretation of "smallest" from "worst-case minimum" to "statistically minimum" is what makes the better solution visible.









## Trick:  Reinterpretation of "Smallest"

The conventional reading of "smallest number of weighings" assumes a fixed worst-case procedure. We reinterpret it statistically: find the strategy that minimizes the *expected* number of weighings across all equally likely positions of the fake coin, while never exceeding 3 weighings in any case.

Since the fake coin is equally likely to be any of the 12 coins, minimizing expected weighings is strictly more faithful to "smallest number" than minimizing worst case alone.



This has a name in puzzle theory: **reframing the objective function.** It is a known technique, taught in creativity courses, not exotic.




