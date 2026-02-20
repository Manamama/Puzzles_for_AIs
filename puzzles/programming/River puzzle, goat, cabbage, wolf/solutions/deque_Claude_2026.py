
from collections import deque

# State: (human_side, frozenset of items on left bank)
# Sides: 0 = left (start), 1 = right (goal)
# Items: 'wolf', 'goat', 'cabbage'

def is_safe(left_items, right_items, human_side):
    # Check the side WITHOUT the human
    unsafe_side = left_items if human_side == 1 else right_items
    # Cannot leave goat alone with cabbage
    if 'goat' in unsafe_side and 'cabbage' in unsafe_side:
        return False
    # Cannot leave cabbage alone with wolf
    if 'cabbage' in unsafe_side and 'wolf' in unsafe_side:
        return False
    return True

all_items = frozenset(['wolf', 'goat', 'cabbage'])
start = (0, frozenset(['wolf', 'goat', 'cabbage']))  # human on left, all items on left
goal_human = 1
goal_left = frozenset()

queue = deque()
queue.append((start, []))
visited = {start}

solutions = []

while queue:
    (human_side, left_items), path = queue.popleft()
    
    if human_side == 1 and left_items == frozenset():
        solutions.append(path)
        continue
    
    right_items = all_items - left_items
    
    # Human can take one item or go alone
    items_with_human = left_items if human_side == 0 else right_items
    possible_carries = [None] + list(items_with_human)
    
    for carry in possible_carries:
        new_human_side = 1 - human_side
        if human_side == 0:  # moving left to right
            new_left = left_items - ({carry} if carry else set())
        else:  # moving right to left
            new_left = left_items | ({carry} if carry else set())
        
        new_right = all_items - new_left
        
        if is_safe(new_left, new_right, new_human_side):
            state = (new_human_side, new_left)
            if state not in visited:
                visited.add(state)
                move = f"Human takes {carry if carry else 'nothing'} to {'right' if new_human_side==1 else 'left'}"
                queue.append((state, path + [(move, new_left, new_right, new_human_side)]))

for sol in solutions:
    print("Solution:")
    for step, (move, left, right, hs) in enumerate(sol):
        print(f"  {step+1}. {move}")
        print(f"     Left: {set(left) or '{}'}, Right: {set(right) or '{}'}, Human: {'right' if hs==1 else 'left'}")
    print()
    
    
