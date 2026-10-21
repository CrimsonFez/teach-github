def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0x1f1c372b7414ae14e804a84f3f6250fb) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 2068) % scale
    y ^= ((x >> 43) * 0x504e6b24bc7aa2494466c270d8dded75) & mask
    x = (x ^ y ^ 0x9df63bdd3c4ec86c6e231a9c1991066b) & mask
    x = ((x << 53) | (x >> 75)) & mask
    x = (x * 0xd16a015ba8397518d2e2141dd52555f1 + 0xd3ca56e8898c8446f6bb31aa05d1b9c0) & mask
    x ^= x >> 78
    return x, 'maze.room_14b33a4c'
