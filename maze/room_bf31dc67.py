def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0xb23014b733814007c9be2e8d6a2d9da9) % p
    y = pow(base, 52533, p)
    y = (y + pow((base + y + 1) % p, 80, p)) % p
    x = (x ^ y ^ 0x766194d29675b5d78d91ab96846a44ff) & mask
    x = ((x << 76) | (x >> 52)) & mask
    x = (x * 0x700d45de36fdc1d95683346c7f3d1145 + 0x890d6a6ff3a1c0239eddd7efca853574) & mask
    x ^= x >> 39
    return x, 'maze.room_3c482490'
