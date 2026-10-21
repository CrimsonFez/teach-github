def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0x41ad0d797aa9f067fc0a0f7151394ad2 >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 15) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0xd0d2413308c9121a408cd3472441286f) & mask
    x = ((x << 73) | (x >> 55)) & mask
    x = (x * 0xa3376fdb2287172524c2ef7f9508c7db + 0xe62996729f239f815506c6e6fc5b38f6) & mask
    x ^= x >> 77
    return x, 'maze.room_794aad17'
