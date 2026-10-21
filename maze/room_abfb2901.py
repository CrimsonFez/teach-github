def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0x3f7fd5ff025bf30889c033f5f9d7ced) % p
    y = pow(base, 50937, p)
    y = (y + pow((base + y + 1) % p, 78, p)) % p
    x = (x ^ y ^ 0xc695f694ace636723b61b0fd4491afd2) & mask
    x = ((x << 40) | (x >> 88)) & mask
    x = (x * 0xcb6b7e90898a6ff28bb5212c9f7efa0d + 0x40b225edd3cb8029c5981660df2e2dab) & mask
    x ^= x >> 42
    return x, 'maze.room_48c22b02'
