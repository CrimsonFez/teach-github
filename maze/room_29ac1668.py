from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0x2aee3825f2e9d93fb6c341a7b080707f) % 20000
    remaining, phi, factor = n, n, 2
    while factor * factor <= remaining:
        if remaining % factor == 0:
            while remaining % factor == 0:
                remaining //= factor
            phi -= phi // factor
        factor += 1
    if remaining > 1:
        phi -= phi // remaining
    total = 0
    for divisor in range(1, isqrt(n) + 1):
        if n % divisor == 0:
            total += divisor
            if divisor * divisor != n:
                total += n // divisor
    y = phi * 0x7f054e573a244453d61dd4164d8c3ffd + total * 0x8d55560bd0ab09fc5b2a1243ff56cf87
    x = (x ^ y ^ 0x22d74fa79c91d6a3c257b318484dba7b) & mask
    x = ((x << 116) | (x >> 12)) & mask
    x = (x * 0x499af96904f9ba9e82b2de7a288bb6cf + 0xf6f00c4624b7c8f4fe60209d71ff187) & mask
    x ^= x >> 45
    return x, 'maze.room_74b6aed2'
