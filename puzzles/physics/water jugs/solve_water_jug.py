
from collections import deque

def solve_water_jug_puzzle():
    jug1_capacity = 12
    jug2_capacity = 6
    target_amount = 6

    # State: (jug1_current, jug2_current)
    initial_state = (0, 0)
    
    # Queue for BFS: (state, path_to_state)
    queue = deque([(initial_state, [])])
    
    # Set to store visited states
    visited = set([initial_state])

    while queue:
        current_state, path = queue.popleft()
        j1, j2 = current_state

        # Check if goal is reached
        if j1 == target_amount or j2 == target_amount:
            return path + [f"Goal reached: ({j1}, {j2})"]

        # Possible actions
        # 1. Fill jug1
        next_state = (jug1_capacity, j2)
        if next_state not in visited:
            visited.add(next_state)
            queue.append((next_state, path + [f"Fill 12L Jug: {next_state}"]))

        # 2. Fill jug2
        next_state = (j1, jug2_capacity)
        if next_state not in visited:
            visited.add(next_state)
            queue.append((next_state, path + [f"Fill 6L Jug: {next_state}"]))

        # 3. Empty jug1
        next_state = (0, j2)
        if next_state not in visited:
            visited.add(next_state)
            queue.append((next_state, path + [f"Empty 12L Jug: {next_state}"]))

        # 4. Empty jug2
        next_state = (j1, 0)
        if next_state not in visited:
            visited.add(next_state)
            queue.append((next_state, path + [f"Empty 6L Jug: {next_state}"]))

        # 5. Pour from jug1 to jug2
        pour_amount = min(j1, jug2_capacity - j2)
        next_state = (j1 - pour_amount, j2 + pour_amount)
        if next_state not in visited:
            visited.add(next_state)
            queue.append((next_state, path + [f"Pour 12L to 6L: {next_state}"]))

        # 6. Pour from jug2 to jug1
        pour_amount = min(j2, jug1_capacity - j1)
        next_state = (j1 + pour_amount, j2 - pour_amount)
        if next_state not in visited:
            visited.add(next_state)
            queue.append((next_state, path + [f"Pour 6L to 12L: {next_state}"]))
            
    return "No solution found."

if __name__ == "__main__":
    solution = solve_water_jug_puzzle()
    for step in solution:
        print(step)
