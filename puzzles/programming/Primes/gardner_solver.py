
import itertools

# This script solves the puzzle by following the specific heuristic reasoning
# laid out by Martin Gardner, as opposed to a pure brute-force search.

def is_prime(n):
    """A standard function to check for primality."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_solution_from_partitions(first_digits, middle_digits, last_digits):
    """
    This function implements Gardner's core idea:
    1. Construct a list of all possible prime numbers by combining one digit from each category.
    2. Search through combinations of those candidate primes to find a set of three that is
       mutually exclusive in its digit use.
    """
    
    # Step 1: Generate all possible primes that can be formed from the digit categories.
    # For example, if first_digits={1,2,4}, a candidate number would be 153, 287, 469, etc.
    candidate_primes = []
    for h in first_digits:
        for m in middle_digits:
            for l in last_digits:
                num = int(f'{h}{m}{l}')
                if is_prime(num):
                    # We store the prime and the set of digits it used for later comparison.
                    candidate_primes.append((num, {h, m, l}))
    
    print(f"Generated {len(candidate_primes)} candidate primes for this attempt.")

    # Step 2: Search for a combination of three candidate primes that uses all 9 unique digits.
    # This is done by checking if the digit sets of the three primes are disjoint.
    for combo in itertools.combinations(candidate_primes, 3):
        p1_num, p1_digits = combo[0]
        p2_num, p2_digits = combo[1]
        p3_num, p3_digits = combo[2]

        # The union of the three digit sets must equal the original 9 digits.
        # A simpler way to check this is to see if the sets are mutually exclusive (disjoint),
        # as they are all of size 3.
        if p1_digits.isdisjoint(p2_digits) and p1_digits.isdisjoint(p3_digits) and p2_digits.isdisjoint(p3_digits):
            solution = sorted([p1_num, p2_num, p3_num])
            print(f"Found a valid set: {solution} with sum {sum(solution)}")
            return solution
            
    print("No valid set of three primes found for these digit partitions.")
    return None

# --- Main execution block ---

# Gardner's first assumption is that the minimal sum will come from three 3-digit numbers.
# He then partitions the 9 digits into categories based on their position in the number.

# --- Gardner's First Attempt ---
# He reasons that the last digits must be from {1, 3, 7, 9}.
# To get the smallest sum, he wants to use the smallest digits (like 1) as first digits.
# So, he reserves {3, 7, 9} for the last digits.
# This leaves {1, 2, 4, 5, 6, 8} for the first and middle positions.
# He chooses the smallest possible first digits: {1, 2, 4}.
# This forces the remaining digits, {5, 6, 8}, to be the middle digits.
print("--- Gardner's First Attempt ---")
first_digits_1 = {1, 2, 4}
middle_digits_1 = {5, 6, 8}
last_digits_1 = {3, 7, 9}
print(f"Partitioning digits into: First={first_digits_1}, Middle={middle_digits_1}, Last={last_digits_1}")
find_solution_from_partitions(first_digits_1, middle_digits_1, last_digits_1)


# --- Gardner's Second Attempt ---
# His first attempt failed, so he moves to the next logical set of first digits.
# He keeps '1' and '2' but tries '5' instead of '4'.
# First digits: {1, 2, 5}.
# The remaining digits are {3, 4, 6, 7, 8, 9}.
# To keep the numbers small, the last digits should still be odd and large, so {3, 7, 9} is the logical choice.
# This leaves the remaining digits, {4, 6, 8}, to be the middle digits.
# This is the step that leads to the unique solution.
print("\n--- Gardner's Second Attempt ---")
first_digits_2 = {1, 2, 5}
middle_digits_2 = {4, 6, 8}
last_digits_2 = {3, 7, 9}
print(f"Partitioning digits into: First={first_digits_2}, Middle={middle_digits_2}, Last={last_digits_2}")
solution = find_solution_from_partitions(first_digits_2, middle_digits_2, last_digits_2)

if solution:
    print(f"\nFinal Answer: The primes are {solution} with a sum of {sum(solution)}.")
