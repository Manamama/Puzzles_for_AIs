
import math
from itertools import permutations, combinations
import time

def is_prime(n):
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

def get_primes_from_digits(digits):
    primes = set()
    for p in permutations(digits):
        num = int("".join(p))
        if is_prime(num):
            primes.add(num)
    return primes

def solve_puzzle():
    all_digits = "123456789"
    min_sum = float('inf')
    result_primes = None

    # Partitions of the number 9 into 3 parts
    partitions = [(3, 3, 3), (2, 3, 4), (1, 4, 4), (1, 3, 5), (1, 2, 6)]

    start_time = time.time()

    for p_sizes in partitions:
        size1, size2, size3 = p_sizes
        
        # Iterate through all ways to partition the set of 9 digits
        for d1_tuple in combinations(all_digits, size1):
            remaining_digits1 = sorted(list(set(all_digits) - set(d1_tuple)))
            
            for d2_tuple in combinations(remaining_digits1, size2):
                # Avoid duplicate partitions for sizes like (1,4,4) and (3,3,3)
                if size1 == size2 and d1_tuple > d2_tuple:
                    continue

                d3_tuple = tuple(sorted(list(set(remaining_digits1) - set(d2_tuple))))

                if size2 == size3 and d2_tuple > d3_tuple:
                    continue
                
                primes1 = get_primes_from_digits(d1_tuple)
                if not primes1:
                    continue
                
                primes2 = get_primes_from_digits(d2_tuple)
                if not primes2:
                    continue

                primes3 = get_primes_from_digits(d3_tuple)
                if not primes3:
                    continue

                for p1 in primes1:
                    for p2 in primes2:
                        for p3 in primes3:
                            current_sum = p1 + p2 + p3
                            if current_sum < min_sum:
                                min_sum = current_sum
                                result_primes = sorted((p1, p2, p3))
                                print(f"New minimum sum: {min_sum} with primes {result_primes}")

    end_time = time.time()
    
    print("\n--- Puzzle Solved ---")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    if result_primes:
        print(f"The three primes are: {result_primes[0]}, {result_primes[1]}, and {result_primes[2]}")
        print(f"Their sum is: {min_sum}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    solve_puzzle()
