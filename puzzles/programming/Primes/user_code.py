
import itertools

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

min_sum = float('inf')
best_set = None

for perm in itertools.permutations('123456789'):
    a = int(''.join(perm[0:3]))
    b = int(''.join(perm[3:6]))
    c = int(''.join(perm[6:9]))
    if is_prime(a) and is_prime(b) and is_prime(c):
        current_sum = a + b + c
        if current_sum < min_sum:
            min_sum = current_sum
            best_set = (a, b, c)

print("Minimal sum:", min_sum)
print("Primes:", best_set)
