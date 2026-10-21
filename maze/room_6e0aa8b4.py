def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 1218 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0x50c15e4000013d4b27cb39c87e1f1daf) % p
    x = (x ^ y ^ 0x3fe7f41d3ea3cb322b7731c80e1640ae) & mask
    x = ((x << 13) | (x >> 115)) & mask
    x = (x * 0x3aa4d5e3847c8039e5f941cd1b72d3a1 + 0x6087b10a6108a955b33c0c8f3148a05b) & mask
    x ^= x >> 82
    return x, 'maze.room_e41aad86'
