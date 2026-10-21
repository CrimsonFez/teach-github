from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0x8d4b073e895bbfeb2a9b2d7db3fb5788) % 20000
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
    y = phi * 0x873d35469dbccada20564879e85edbb5 + total * 0xd5da8ba5d6a9049a4fa5f1e47fa65b95
    x = (x ^ y ^ 0x45fce32e47cf41ca8c4ac46ab78fba74) & mask
    x = ((x << 88) | (x >> 40)) & mask
    x = (x * 0xf4ae7e0a2ced9b3018439fbe7f373b4f + 0xfa9fda519d193893b187b58711d7a68f) & mask
    x ^= x >> 62
    return x, 'maze.room_a82e0976'
