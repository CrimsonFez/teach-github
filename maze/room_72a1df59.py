def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0xcbee01e9bae2ea8f4d17ed340127d92d) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 6)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0xcd4151a88aec8b250792f7e57836ea5d) & mask
    x = ((x << 82) | (x >> 46)) & mask
    x = (x * 0x6443684e74d00385b882f107356af041 + 0xce2ddbc5f063ff56193419bbe4d1c4b2) & mask
    x ^= x >> 56
    return x, 'maze.room_29ac1668'
