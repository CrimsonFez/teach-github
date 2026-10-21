def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0x9488620e0b8bbadab3429da3f952981a >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 5) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0x85455387ce7f95cde08bb9d67c951229) & mask
    x = ((x << 66) | (x >> 62)) & mask
    x = (x * 0x3993a1112d234a550d9b61efd929bb4b + 0x9ffbdc5b66604c0dd9ef02614d53acf7) & mask
    x ^= x >> 40
    return x, 'maze.room_a4f68c4f'
