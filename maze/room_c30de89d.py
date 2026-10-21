def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0x8c3054e7f053c20bdd0c3b1347981d30 >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 39) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0xd602e12a5e1b329e4ab0cd9b88d87274) & mask
    x = ((x << 88) | (x >> 40)) & mask
    x = (x * 0xb6d53337838055a1aab88e53f654d741 + 0xd8d1b51ae3e1eecfff4dd11f30196812) & mask
    x ^= x >> 60
    return x, 'maze.room_894ffc0e'
