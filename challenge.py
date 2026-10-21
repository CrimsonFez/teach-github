from math import comb, factorial, gcd, isqrt
from os import environ
MASK = (1 << 64) - 1
MOD = 1_000_000_007
def rotate(x, shift):
    shift %= 64
    return ((x << shift) | (x >> ((64 - shift) % 64))) & MASK
def mix(x):
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9 & MASK
    x = (x ^ (x >> 27)) * 0x94D049BB133111EB & MASK
    return (x ^ (x >> 31)) & MASK
def primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
    return [n for n in range(2, limit + 1) if sieve[n]]
def fibonacci(n):
    if n == 0:
        return 0, 1
    a, b = fibonacci(n // 2)
    c = a * (2 * b - a) % MOD
    d = (a * a + b * b) % MOD
    return (d, (c + d) % MOD) if n % 2 else (c, d)
def matrix_product(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) % MOD
             for j in range(3)] for i in range(3)]
def matrix_power(matrix, exponent):
    result = [[int(i == j) for j in range(3)] for i in range(3)]
    while exponent:
        if exponent & 1:
            result = matrix_product(result, matrix)
        matrix = matrix_product(matrix, matrix)
        exponent >>= 1
    return result
def determinant(matrix):
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)) % MOD
def polynomial(coefficients, x):
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * x + coefficient) % MOD
    return result
def continued_fraction(terms):
    numerator, denominator = 1, 0
    for term in reversed(terms):
        numerator, denominator = term * numerator + denominator, numerator
    return numerator, denominator
def field_multiply(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        a = ((a << 1) ^ (0x11B if a & 0x80 else 0)) & 255
        b >>= 1
    return result
def totient(n):
    result, divisor = n, 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            while n % divisor == 0:
                n //= divisor
            result -= result // divisor
        divisor += 1
    return result - result // n if n > 1 else result
def divisor_sum(n):
    result = 0
    for divisor in range(1, isqrt(n) + 1):
        if n % divisor == 0:
            result += divisor
            if divisor * divisor != n:
                result += n // divisor
    return result
def reverse_bits(n):
    result = 0
    for _ in range(64):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
def cellular(n, rounds):
    for step in range(rounds):
        left, right = rotate(n, 1), rotate(n, 63)
        n = (left ^ (n | right)) & MASK
        n ^= rotate(0x9E3779B97F4A7C15, step)
    return n
def hadamard(values):
    values = values[:]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    return values
def convolution(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] = (result[i + j] + x * y) % MOD
    return result
def fold(state, values):
    for index, value in enumerate(values, 1):
        state = mix(state ^ rotate(value & MASK, index * 7))
        state = (state + index * 0x9E3779B97F4A7C15) & MASK
    return state
def generate_number(seed):
    state = seed & MASK
    ps = primes(311)
    for index, prime in enumerate(ps, 1):
        residue = pow(prime, index * index + 17, MOD)
        state = mix(state ^ rotate(residue, prime))
        state = (state + comb(prime + index, index % 13 + 1)) & MASK
    terms = [2 + ((state >> (i * 3)) & 15) for i in range(18)]
    numerator, denominator = continued_fraction(terms)
    state = fold(state, [numerator, denominator, numerator // denominator])
    fa, fb = fibonacci(10_000 + state % 90_000)
    state = fold(state, [fa, fb, fa * fb % MOD])
    coefficients = [(prime * prime + state % (prime + 1)) % MOD for prime in ps]
    state = fold(state, [polynomial(coefficients, state % MOD)])
    matrix = [[(state >> (i * 9 + j * 5)) % 997 + int(i == j) for j in range(3)] for i in range(3)]
    powered = matrix_power(matrix, 97 + state % 431)
    state = fold(state, [entry for row in powered for entry in row])
    state = fold(state, [determinant(powered), determinant(matrix)])
    inverse = pow(1 + state % (MOD - 1), MOD - 2, MOD)
    state = fold(state, [inverse, pow(inverse, 37, MOD)])
    exact_root = isqrt((state << 96) + numerator * denominator)
    state = fold(state, [exact_root, factorial(83) % MOD])
    combination_sum = sum(comb(97, k) * pow(k + 3, 11, MOD) for k in range(31))
    state = fold(state, [combination_sum % MOD])
    arithmetic = [1001 + (state >> shift) % 900_000 for shift in (0, 11, 23, 37)]
    for n in arithmetic:
        phi, sigma = totient(n), divisor_sum(n)
        state = fold(state, [phi, sigma, n // gcd(n, sigma)])
    moduli = [101, 103, 107, 109]
    residues = [(state >> (i * 11)) % p for i, p in enumerate(moduli)]
    product = 101 * 103 * 107 * 109
    reconstruction = 0
    for residue, modulus in zip(residues, moduli):
        partial = product // modulus
        reconstruction += residue * partial * pow(partial, -1, modulus)
    state = fold(state, [reconstruction % product])
    octets = [(state >> (8 * i)) & 255 for i in range(8)]
    for round_index in range(19):
        octets = [field_multiply(octets[i], 3) ^ octets[(i + 1) % 8]
                  ^ ((round_index * 29 + i * 17) & 255) for i in range(8)]
    state = fold(state, octets)
    state = mix(state ^ reverse_bits(state))
    state = fold(state, [cellular(state, 73)])
    spectrum = hadamard([(state >> (i * 4)) & 255 for i in range(16)])
    state = fold(state, [value * value for value in spectrum])
    left = [(state >> (i * 7)) % 1009 for i in range(8)]
    right = [pow(prime, 5, MOD) for prime in ps[:9]]
    state = fold(state, convolution(left, right))
    partitions = [1] + [0] * 47
    for part in range(1, 17):
        for total in range(part, len(partitions)):
            partitions[total] = (partitions[total] + partitions[total - part]) % MOD
    state = fold(state, partitions[24:])
    a, b = 1 + state % 65521, 1 + (state >> 17) % 65519
    for step in range(1, 29):
        a, b = (a * a - b * b + step) % MOD, (2 * a * b + step * step) % MOD
    state = fold(state, [a, b, (a * a + b * b) % MOD])
    scale = 1 << 48
    orbit = 1 + state % (scale - 1)
    for step in range(41):
        orbit = (4 * orbit * (scale - orbit) // scale + step + 1) % scale
        state = mix(state ^ orbit)
    bernoulli = [comb(40, k) * pow(3, k) * pow(5, 40 - k) for k in range(41)]
    state = fold(state, [sum(bernoulli[::2]) % MOD, sum(bernoulli[1::2]) % MOD])
    walk = [1] + [0] * 16
    for step in range(23):
        walk = [(walk[(i - 1) % 17] + (i + step + 1) * walk[(i + 1) % 17])
                % MOD for i in range(17)]
    state = fold(state, walk)
    triangle = [1]
    for row in range(1, 24):
        triangle = [1] + [(triangle[i - 1] + triangle[i]) % MOD
                          for i in range(1, len(triangle))] + [1]
        state = mix(state ^ polynomial(triangle, row + 2))
    remainders = [pow(2 + state % (p - 2), (p - 1) // 2, p) for p in ps[10:30]]
    state = fold(state, remainders)
    permutation = list(range(16))
    for i in range(15, 0, -1):
        state = mix(state + i)
        j = state % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    rank = sum(sum(x < value for x in permutation[i + 1:]) * factorial(15 - i)
               for i, value in enumerate(permutation))
    state = fold(state, [rank, gcd(rank + 1, state | 1)])
    return 1 + mix(state) % 100
if __name__ == "__main__":
    seed = environ.get("CHALLENGE_SEED")
    if not seed:
        raise SystemExit("Fork the repository and run Actions > Reveal the number.")
    print(generate_number(int(seed, 16)))
