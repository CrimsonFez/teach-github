from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0xfd6d9d0f05d1b1d70a0304e9df119c51) % 20000
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
    y = phi * 0x532fb48d12e8f022893a28033b7feaaa + total * 0x4eff1df1756e18eca97b0a06247f9934
    x = (x ^ y ^ 0x6eea0113733cceab3629fd26e747a0f5) & mask
    x = ((x << 111) | (x >> 17)) & mask
    x = (x * 0x15a5cd88ba0076182eb95cce975585fb + 0xd89e2c7b2575db442a0d4e025f2757bf) & mask
    x ^= x >> 74
    return x, 'maze.room_766e04a3'
