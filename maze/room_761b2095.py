def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0xe65004ea5eb6690801cfe83ffab08776 >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 74) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0xed6037f64971c5fa3c83ec0eaf302a07) & mask
    x = ((x << 13) | (x >> 115)) & mask
    x = (x * 0xc314a35ac6d4fe99c7e620ce612d3ebb + 0x204b3677f99879096390ab6bc192bca1) & mask
    x ^= x >> 58
    return x, 'maze.room_cc328666'
