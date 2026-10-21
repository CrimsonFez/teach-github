def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0xe83e883b9ca4486802d4a0625f5dfe83 >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 88) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0x252b1b3ac734474482a02074aaffde9b) & mask
    x = ((x << 98) | (x >> 30)) & mask
    x = (x * 0xf174f5d9e5f82e0c1dc2107b85c750f7 + 0xd1972cb2acbefd9e9c4f209072a33a18) & mask
    x ^= x >> 38
    return x, 'maze.room_1bcf29c1'
