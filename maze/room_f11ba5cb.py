def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0x67da3323b1a19e3ba2252bdb93c6efd1 >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 17) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0xe1c5427ad8ff7d0f07ae5237b1935204) & mask
    x = ((x << 100) | (x >> 28)) & mask
    x = (x * 0x1d1d29b1b211e35ae323dc2fc58d19fb + 0x32a31028be01d4ea08b860d4f9b48cad) & mask
    x ^= x >> 86
    return x, 'maze.room_96c72707'
