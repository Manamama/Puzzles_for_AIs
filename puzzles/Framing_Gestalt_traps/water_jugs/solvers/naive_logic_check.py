class Jug:
    def __init__(self, capacity):
        self.capacity = capacity
        self.current_volume = 0

    def fill(self):
        self.current_volume = self.capacity
        print(f"Filled the {self.capacity}-liter jug to its capacity. It now contains {self.current_volume} liters of water.")

def solve_puzzle(jug1, jug2):
    # If one of the jugs has a capacity of 6 liters, fill it
    if jug1.capacity == 6:
        jug1.fill()
    elif jug2.capacity == 6:
        jug2.fill()
    else:
        print("Cannot solve the puzzle with the given jugs.")

# Initialize a jug with 6-liter capacity
jug_6L = Jug(6)

# Initialize a jug with 12-liter capacity
jug_12L = Jug(12)

# Solve the puzzle
solve_puzzle(jug_6L, jug_12L)
