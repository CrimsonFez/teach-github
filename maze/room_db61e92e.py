def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0x8d92d60c0013e47bda194667293e86d1) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 7953) % scale
    y ^= ((x >> 43) * 0x79b25dbdc8808fe79ea5821c074f2fbd) & mask
    x = (x ^ y ^ 0x791169d40d76c563705c39be4a3548c2) & mask
    x = ((x << 89) | (x >> 39)) & mask
    x = (x * 0xb0eb5bb3ccb26494511b41c4162f429f + 0x572820cc1e73d083bcfdc9cdddf4ac96) & mask
    x ^= x >> 69
    return x, 'maze.room_c78a595f'
