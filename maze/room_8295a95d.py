from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0xf7dc0cf8521cec48d17531f782355e22) % 20000
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
    y = phi * 0xe884e430e067fae372ed5ac4f39b521a + total * 0xcfc1388f005d963801acd80affb26c87
    x = (x ^ y ^ 0xb5893a8a39e420cd4c91fcbc0395d) & mask
    x = ((x << 106) | (x >> 22)) & mask
    x = (x * 0x767f63eee68e2b0d2f5462e36ca167ad + 0x82e94ea5d1d854292d9f20397125184d) & mask
    x ^= x >> 74
    return x, 'maze.room_907abdfd'
