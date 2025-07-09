from collections import deque

def water_jug_solver(jug1_capacity, jug2_capacity, target):
    """
    Solves the water jug puzzle using Breadth-First Search.
    Finds the shortest path to measure the target amount.
    """
    # A set to keep track of visited states to avoid infinite loops.
    # A state is represented by a tuple: (water_in_jug1, water_in_jug2)
    visited_states = set()

    # A queue for the BFS algorithm.
    # Each item is a tuple: ( (jug1, jug2), path_to_this_state )
    queue = deque([((0, 0), [(0, 0)])])

    while queue:
        (current_jugs, path) = queue.popleft()
        jug1, jug2 = current_jugs

        # If we've already processed this state, skip it.
        if current_jugs in visited_states:
            continue
        
        visited_states.add(current_jugs)

        # Check if we have satisfied the constraint (reached the target).
        if jug1 == target or jug2 == target:
            print(f"Solution found in {len(path) - 1} steps!")
            return path

        # --- Generate all possible next states (actions) ---

        # 1. Fill jug1
        queue.append(((jug1_capacity, jug2), path + [(jug1_capacity, jug2)]))
        # 2. Fill jug2
        queue.append(((jug1, jug2_capacity), path + [(jug1, jug2_capacity)]))
        # 3. Empty jug1
        queue.append(((0, jug2), path + [(0, jug2)]))
        # 4. Empty jug2
        queue.append(((jug1, 0), path + [(jug1, 0)]))
        
        # 5. Pour from jug1 to jug2
        pour_amount = min(jug1, jug2_capacity - jug2)
        queue.append(((jug1 - pour_amount, jug2 + pour_amount), path + [(jug1 - pour_amount, jug2 + pour_amount)]))

        # 6. Pour from jug2 to jug1
        pour_amount = min(jug2, jug1_capacity - jug1)
        queue.append(((jug1 + pour_amount, jug2 - pour_amount), path + [(jug1 + pour_amount, jug2 - pour_amount)]))

    # If the queue becomes empty and we haven't found a solution
    return None

# --- Solve the classic puzzle: 5L and 3L jugs to get 4L ---
jug5_cap = 5
jug3_cap = 3
target_amount = 4

solution_path = water_jug_solver(jug5_cap, jug3_cap, target_amount)

if solution_path:
    print(f"Goal: Measure exactly {target_amount} liters.")
    print(f"Jugs capacity: ({jug5_cap}L, {jug3_cap}L)")
    print("-" * 30)
    for i, state in enumerate(solution_path):
        if i == 0:
            print(f"Step {i}: Start state\t-> Jugs: {state}")
        else:
            # Describe the action that led to this state
            prev_state = solution_path[i-1]
            action = ""
            if state[0] > prev_state[0] and prev_state[0] == 0: action = "Fill 5L jug"
            elif state[1] > prev_state[1] and prev_state[1] == 0: action = "Fill 3L jug"
            elif state[0] < prev_state[0] and state[0] == 0: action = "Empty 5L jug"
            elif state[1] < prev_state[1] and state[1] == 0: action = "Empty 3L jug"
            elif state[0] < prev_state[0]: action = "Pour from 5L jug to 3L jug"
            elif state[1] < prev_state[1]: action = "Pour from 3L jug to 5L jug"
            
            print(f"Step {i}: {action}\t-> Jugs: {state}")
else:
    print("No solution found.")

# --- Analysis of the user's provided snippet ---
# The user's snippet (6L and 12L jugs, target 6L) is a trivial case.
# The greatest common divisor of 6 and 12 is 6. Any measurable amount
# must be a multiple of the GCD. Since the target (6) is a multiple
# of the GCD, a solution exists. In this case, it's trivial:
# Step 1: Fill the 6L jug. -> (6, 0). Solved.
print("\n--- Analysis of the 6L/12L puzzle ---")
trivial_solution = water_jug_solver(6, 12, 6)
if trivial_solution:
    print("The 6L/12L puzzle is solvable, as shown by the path:", trivial_solution)
else:
    print("The 6L/12L puzzle is not solvable.")
