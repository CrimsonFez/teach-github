from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0x15456278d42bdd9592c7c976360a7697) % 20000
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
    y = phi * 0x7a46b4a1fa05c546edad9f78bde10b85 + total * 0xe57ad9bcf91423bf88db72d6e21611fc
    x = (x ^ y ^ 0x7282af6d6f8fdd47d4915f72dc8a0a84) & mask
    x = ((x << 25) | (x >> 103)) & mask
    x = (x * 0xc7aa84fe99a8daceea4fbd685481138b + 0x4401e151e47b4733d300ccedef27ce95) & mask
    x ^= x >> 78
    return x, 'maze.room_8f7ba524'
