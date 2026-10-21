def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0x2f5cd380ac564cac9c9249c3dedf68a7) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0xe46721f0b5c50cc9979387c26aee3622) % p
    y = (a ^ b) + (a * b + 0xd9ba6496248c7ba3f7d2ef04756aeece) % p
    x = (x ^ y ^ 0x4f48d62972d1a1ad8eac5aec9d6209c2) & mask
    x = ((x << 25) | (x >> 103)) & mask
    x = (x * 0xb1db5c1b68a8af0f0866a9b2379764db + 0x7872e0b9ee5aaac954e2d4f7a3852987) & mask
    x ^= x >> 50
    return x, 'maze.room_55cdf85e'
