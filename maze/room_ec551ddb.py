from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0xa69d1e4b2448b10d1f91721e9a403ecd) % 20000
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
    y = phi * 0xf1e22cf35df0ba9aab1654b06797b51d + total * 0x6597ecca16f558fb9a4a8c904499f904
    x = (x ^ y ^ 0x442176daf94bf72cac288a34f60ccf9f) & mask
    x = ((x << 60) | (x >> 68)) & mask
    x = (x * 0x8955924cb2b1ae57ce8cb62780cedf01 + 0xe2b505d7f44746dce02e5d2e8978b6bc) & mask
    x ^= x >> 68
    return x, 'maze.room_8f3e833b'
