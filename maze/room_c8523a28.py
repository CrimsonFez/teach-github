from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0x36a6c8a388114c7c45022a0b61540ea3) % 20000
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
    y = phi * 0x876a1709c194555d97e5e5a103e46790 + total * 0xed55b09ac0b8cb10b86385f89e684a16
    x = (x ^ y ^ 0xaa87cff8c98786afe3771cd082e702da) & mask
    x = ((x << 41) | (x >> 87)) & mask
    x = (x * 0x7723f3d55bbde7cbde5059b258b711e5 + 0x1b3e2b9a37fd97c2fc2e11fa0f91df16) & mask
    x ^= x >> 88
    return x, 'maze.room_30e2d9fb'
