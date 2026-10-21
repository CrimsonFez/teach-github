def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0x29f5176da9dcf8695154f82a3bcf7f27) % p
    y = pow(base, 14425, p)
    y = (y + pow((base + y + 1) % p, 28, p)) % p
    x = (x ^ y ^ 0x4dd164a16e60d7b1a0d39a596df291fd) & mask
    x = ((x << 17) | (x >> 111)) & mask
    x = (x * 0xc85e6644d7b332f946945099fc5f279 + 0x5df9ffa2798ea1329b404348a1111b66) & mask
    x ^= x >> 67
    return x, 'maze.room_8609c53e'
