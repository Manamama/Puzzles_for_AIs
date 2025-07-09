# A simple script to solve the specific water jug problem as defined by the user.
# No assumptions about "classic" versions of the puzzle will be made.

# Parameters as provided by the user's snippet
jug1_capacity = 6
jug2_capacity = 12
target = 6

# Initial state
jug1 = 0
jug2 = 0

print(f"Solving for a target of {target}L using jugs of {jug1_capacity}L and {jug2_capacity}L.")
print(f"Initial state: ({jug1}, {jug2})")

# --- The simplest sequence of actions to satisfy the constraint ---

# Step 1: Fill the 6-liter jug.
jug1 = jug1_capacity
print(f"Step 1: Fill the {jug1_capacity}L jug. State: ({jug1}, {jug2})")

# Step 2: Check the constraint.
if jug1 == target or jug2 == target:
    print("\nConstraint satisfied. Solution found.")
else:
    # This part would contain the search algorithm for a non-trivial case,
    # but for this specific problem, the solution is found immediately.
    print("\nConstraint not yet satisfied.")

