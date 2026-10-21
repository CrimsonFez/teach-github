def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0x49f3182ba2f48335fda72f0cee98d513) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 5)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0x2a05017c6017a652145dd33f876d7fc5) & mask
    x = ((x << 60) | (x >> 68)) & mask
    x = (x * 0x3b7bd65e50c8298f6b06bb3beb738b0f + 0xd4126715a7259dc41ff87c7be87b032b) & mask
    x ^= x >> 42
    return x, 'maze.room_f3ee6fd4'
