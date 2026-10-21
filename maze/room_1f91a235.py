def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0xed1e65d40fbb4453eadf8729017da614) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0x8d09a5fba6d58efd823a74c8396affec * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0xe59c070e513ae67620d4ba345fa3faa1 * base) % p
    x = (x ^ y ^ 0x5a3e10fa723597efcee748c0d7992ddf) & mask
    x = ((x << 13) | (x >> 115)) & mask
    x = (x * 0xa2c3d43fc14a21a522b340f0a7e6f2fd + 0x2c9e9d0dae7e52856e07a3a141a0e460) & mask
    x ^= x >> 53
    return x, 'maze.room_551bfdee'
