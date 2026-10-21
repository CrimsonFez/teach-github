from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0xdcac6ef292a89d4ce971610a50ccaeb8) % 20000
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
    y = phi * 0x60b44e47ab5d25ca379eed8ec7b9c2c1 + total * 0x1d63bc7d28f3566674fd0ebdfcd96b68
    x = (x ^ y ^ 0x44fdfbe2e575cee38b2461be099077e0) & mask
    x = ((x << 48) | (x >> 80)) & mask
    x = (x * 0x33a93e107416633b5b0060ef52884cf9 + 0xc9518a9cc1ff85a51c186ab614c39472) & mask
    x ^= x >> 46
    return x, 'maze.room_8c2ab3f3'
