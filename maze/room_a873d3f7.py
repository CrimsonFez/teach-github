def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0xd7c04e3817532958f59a969154c48efc) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0x88500722918f22b0b7e2d6b706c8e4a2 >> (k % 17))) & mask
    y ^= ((x << 28) & mask)
    x = (x ^ y ^ 0xb2ed517a5cc2eea4e831f3573e81294c) & mask
    x = ((x << 56) | (x >> 72)) & mask
    x = (x * 0xd50e053e9e2ed4f426e362773dd529d + 0x18d39124429e53e3d124f3699eb8c3a1) & mask
    x ^= x >> 51
    return x, 'maze.room_00037648'
