# Define the state space for the river puzzle

# A state is represented by a tuple: (human, wolf, goat, cabbage)
# 0 represents the initial bank
# 1 represents the destination bank

initial_state = (0, 0, 0, 0)
goal_state = (1, 1, 1, 1)

def is_valid_state(state):
    human, wolf, goat, cabbage = state

    # Check the left bank (0)
    if human == 0: # Human is on the left bank
        # No conflicts if human is present
        pass
    else: # Human is on the right bank, check left bank for conflicts
        if goat == 0 and cabbage == 0:
            return False # Goat and Cabbage left alone on left bank
        if wolf == 0 and cabbage == 0:
            return False # Cabbage and Wolf left alone on left bank

    # Check the right bank (1)
    if human == 1: # Human is on the right bank
        # No conflicts if human is present
        pass
    else: # Human is on the left bank, check right bank for conflicts
        if goat == 1 and cabbage == 1:
            return False # Goat and Cabbage left alone on right bank
        if wolf == 1 and cabbage == 1:
            return False # Cabbage and Wolf left alone on right bank

    return True

def get_next_states(current_state):
    human, wolf, goat, cabbage = current_state
    possible_next_states = []

    # Determine the current bank and the destination bank
    current_bank = human
    destination_bank = 1 - human

    # Option 1: Human moves alone
    new_state_list = list(current_state)
    new_state_list[0] = destination_bank # Move human
    next_state = tuple(new_state_list)
    if is_valid_state(next_state):
        possible_next_states.append(next_state)

    # Option 2: Human moves with Wolf
    if wolf == current_bank: # Wolf is on the same bank as human
        new_state_list = list(current_state)
        new_state_list[0] = destination_bank # Move human
        new_state_list[1] = destination_bank # Move wolf
        next_state = tuple(new_state_list)
        if is_valid_state(next_state):
            possible_next_states.append(next_state)

    # Option 3: Human moves with Goat
    if goat == current_bank: # Goat is on the same bank as human
        new_state_list = list(current_state)
        new_state_list[0] = destination_bank # Move human
        new_state_list[2] = destination_bank # Move goat
        next_state = tuple(new_state_list)
        if is_valid_state(next_state):
            possible_next_states.append(next_state)

    # Option 4: Human moves with Cabbage
    if cabbage == current_bank: # Cabbage is on the same bank as human
        new_state_list = list(current_state)
        new_state_list[0] = destination_bank # Move human
        new_state_list[3] = destination_bank # Move cabbage
        next_state = tuple(new_state_list)
        if is_valid_state(next_state):
            possible_next_states.append(next_state)

    return possible_next_states

def solve_puzzle():
    queue = [(initial_state, [])] # (current_state, path_to_current_state)
    visited = set()
    visited.add(initial_state)

    while queue:
        current_state, path = queue.pop(0)

        if current_state == goal_state:
            return path + [current_state] # Add the goal state to the path

        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [current_state]))

    return None # No solution found


print(f"Initial state: {initial_state}")
print(f"Goal state: {goal_state}")

# Test some states
print(f"Is initial state valid? {is_valid_state(initial_state)}")
print(f"Is goal state valid? {is_valid_state(goal_state)}")
print(f"Is (0, 0, 1, 1) valid? (Human left, Wolf left, Goat right, Cabbage right) -> Should be False (Goat and Cabbage alone on right) {is_valid_state((0, 0, 1, 1))}")
print(f"Is (0, 1, 0, 1) valid? (Human left, Wolf right, Goat left, Cabbage right) -> Should be False (Cabbage and Wolf alone on right) {is_valid_state((0, 1, 0, 1))}")
print(f"Is (1, 0, 0, 0) valid? (Human right, Wolf left, Goat left, Cabbage left) -> Should be False (Goat and Cabbage alone on left) {is_valid_state((1, 0, 0, 0))}")
print(f"Is (1, 0, 1, 0) valid? (Human right, Wolf left, Goat right, Cabbage left) -> Should be False (Cabbage and Wolf alone on left) {is_valid_state((1, 0, 1, 0))}")
print(f"Is (0, 1, 1, 0) valid? (Human left, Wolf right, Goat right, Cabbage left) -> Should be True {is_valid_state((0, 1, 1, 0))}")

print("\nTesting get_next_states:")
print(f"Next states from initial state {initial_state}: {get_next_states(initial_state)}")

print("\nSolving puzzle:")
solution = solve_puzzle()
if solution:
    print("Solution found!")
    for i, state in enumerate(solution):
        print(f"Step {i}: {state}")
else:
    print("No solution found.")