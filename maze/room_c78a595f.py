def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0x9ffd0af8ee2ec2ae49d6856cc8f73f11 >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 26) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0x6d32a0f883cbcc01e51031d5ad4e15c4) & mask
    x = ((x << 96) | (x >> 32)) & mask
    x = (x * 0xe197376e5d9cfc6163cb18e6a778dbe1 + 0x52cfa687390685930d604d3f5a4c1ae4) & mask
    x ^= x >> 74
    return x, 'maze.room_924ec731'
