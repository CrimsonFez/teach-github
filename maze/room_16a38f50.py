def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 2550 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0x7cd3bd2f607716a37f4a1edb00dde38d) % p
    x = (x ^ y ^ 0x44785a8c7d8a936ed6d0a7c07894a96a) & mask
    x = ((x << 30) | (x >> 98)) & mask
    x = (x * 0xde624c345aa67dfac2666261ee7d9b71 + 0xe0afa2a336e9885b59816ba98e821a) & mask
    x ^= x >> 50
    return x, 'maze.room_b5cf9694'
