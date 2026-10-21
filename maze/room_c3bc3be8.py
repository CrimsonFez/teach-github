def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0xc4f0ef4b7a142493d6021b5b3da156c7) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0x60e6328f7f13db1f172c8619b2806834) | 1, 48, 1 << 128)) & mask
    x = (x ^ y ^ 0x8421bd787b0c596fcf9d36c6abb4b7a3) & mask
    x = ((x << 88) | (x >> 40)) & mask
    x = (x * 0xcaa7efb47a1d1314a7ee6d8c3cdd12d7 + 0x1a5c1cc6a6ac578f64fd7c1ee6415f0d) & mask
    x ^= x >> 49
    return x, 'maze.room_dbab0614'
