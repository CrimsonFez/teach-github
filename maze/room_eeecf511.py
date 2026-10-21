def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0x59947d38192372dd69c687ba8fb403cc >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 52) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0x8d22b897323cd151857f222d1d507e4b) & mask
    x = ((x << 91) | (x >> 37)) & mask
    x = (x * 0x2665787371bfddd407f1d8d720e7d89 + 0x893e5a5e994766a50d21af83009f0c37) & mask
    x ^= x >> 85
    return x, 'maze.room_d06795ba'
