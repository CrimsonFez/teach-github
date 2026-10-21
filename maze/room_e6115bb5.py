from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0x685b907dc8b4183aa124a764c9500f82) % 20000
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
    y = phi * 0xd7d8d77fafd9a43208eb517067f01c6a + total * 0xafb000ad2e01d4a9c3ac0423f44285b4
    x = (x ^ y ^ 0x2e282a6b1615a191a438bc539494d379) & mask
    x = ((x << 19) | (x >> 109)) & mask
    x = (x * 0xbaa81355a26daa4c59d069999902b5b9 + 0xef183c4eeb8ed58d3b547cf71d8ec5c7) & mask
    x ^= x >> 71
    return x, 'maze.room_a873d3f7'
