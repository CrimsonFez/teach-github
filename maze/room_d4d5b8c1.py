def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0xa48b072d8b78ff6472d144acf188dbac >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 82) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0x2eb0371bca09c60a17d3de18deb3243b) & mask
    x = ((x << 36) | (x >> 92)) & mask
    x = (x * 0x6ca80de4a55bfdc24feced288778d5b9 + 0xeddb022aec24a9fb8ffbf93114cf1e4d) & mask
    x ^= x >> 54
    return x, 'maze.room_b46efc8c'
