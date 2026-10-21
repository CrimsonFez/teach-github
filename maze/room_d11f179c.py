def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0xfbbfc6eea99c182fb0ca9cae3997a12c) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0x58be373c81a3d9b9f6eeab9263dee0d * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0x2fd7a163432e16a9126e517e33797057 * base) % p
    x = (x ^ y ^ 0x9c4abbd4815182d532975cf9558883ba) & mask
    x = ((x << 44) | (x >> 84)) & mask
    x = (x * 0x56f38d82ee01c7d19eaa5c74af88802f + 0x39b9e891a6e471dc26fdb62908c84d5c) & mask
    x ^= x >> 64
    return x, 'maze.room_9a9465a2'
