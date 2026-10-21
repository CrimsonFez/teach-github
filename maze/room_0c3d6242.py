def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 3901 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0x9fd9a1344ab8ee590906a193d164ee4c) % p
    x = (x ^ y ^ 0x5cf40670046e6b485e42ebf4f20dc65d) & mask
    x = ((x << 71) | (x >> 57)) & mask
    x = (x * 0x20c2744fe68ee7abc52c5398eaed2683 + 0xedbfefb92fbb167d6cc34b0a765f3d5f) & mask
    x ^= x >> 53
    return x, 'maze.room_f0292d8f'
