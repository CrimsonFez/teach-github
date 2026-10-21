def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0xc1f661fcc0a266b05dfbd3495ab2ab15) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0xc1c79c84d93fb50a5ef002895d97ac30 * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0x3952075c47840ae32e4e5e369b9cd9d4 * base) % p
    x = (x ^ y ^ 0x527a3d368e9f11ce0ce8ef7297a08f94) & mask
    x = ((x << 60) | (x >> 68)) & mask
    x = (x * 0x316ceb688cee1ef95e9de0eba174f569 + 0x2f17f8c36c172f6a45b77490373196d3) & mask
    x ^= x >> 49
    return x, 'maze.room_97768145'
