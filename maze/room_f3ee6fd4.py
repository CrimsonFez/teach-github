from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    n = 1001 + (x ^ 0xa037f19cb1362e33abb8071f84ab0a7e) % 20000
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
    y = phi * 0x5bd7651eff2d53fcf72b970845a8ae0e + total * 0x522a722894ad029dbd2aa48fb6b64090
    x = (x ^ y ^ 0xaa41d03d7301de9d9201832f39df550) & mask
    x = ((x << 28) | (x >> 100)) & mask
    x = (x * 0x61b52b4b0df41b8b8af3f88655fe66cd + 0x8746f610c8d51addd20c721317c5df8a) & mask
    x ^= x >> 51
    return x, 'maze.room_cd84bed2'
