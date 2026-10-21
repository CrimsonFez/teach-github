def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0x9b276f0815f41f78342454cabd276d35) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 9)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0x94f66f807aa678b5073c9ad41b0fae8d) & mask
    x = ((x << 96) | (x >> 32)) & mask
    x = (x * 0x79a3cc603fe52a99d4f80012794f1ac1 + 0x36e08b46f09621475d84c2b5ead3ab10) & mask
    x ^= x >> 41
    return x, 'maze.room_e6115bb5'
