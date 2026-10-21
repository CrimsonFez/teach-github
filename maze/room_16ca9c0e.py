def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0x22a55fc5a97b5b78ca786f3fae3c8a80) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 3428) % scale
    y ^= ((x >> 43) * 0x5d528a24e03ad31033801821c4ea084c) & mask
    x = (x ^ y ^ 0x9548bff59b8861574250f2e687fc59e7) & mask
    x = ((x << 85) | (x >> 43)) & mask
    x = (x * 0x7e15c3c6a44aa59f23ac91e9f30fd6fd + 0xcaf23a4c94163b517b45d16e875421da) & mask
    x ^= x >> 59
    return x, 'maze.room_761b2095'
