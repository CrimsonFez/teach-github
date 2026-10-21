def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    values = [((x >> (i * 7)) ^ (0xe0cfc2a738bbfa410c82f8e43ec4f36 >> (i * 3))) & 65535
              for i in range(16)]
    width = 1
    while width < len(values):
        for start in range(0, len(values), width * 2):
            for offset in range(width):
                i, j = start + offset, start + offset + width
                values[i], values[j] = values[i] + values[j], values[i] - values[j]
        width *= 2
    y = sum((i + 86) * v * v for i, v in enumerate(values))
    y ^= sum((v & 65535) << (i * 8) for i, v in enumerate(values))
    x = (x ^ y ^ 0x56559fcdd33ae32d53cd0fe9339c01bf) & mask
    x = ((x << 81) | (x >> 47)) & mask
    x = (x * 0x18592ad6156711bb12d874ab6a284b39 + 0x75a04232e97d68a61aa4942a8c718aba) & mask
    x ^= x >> 88
    return x, 'maze.room_74d339c2'
