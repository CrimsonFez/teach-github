def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0x48c4d00290c277d505284b0f96dc39cf) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0x3ed4f5487871e891764850735f1329d4 * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0xb37d4a9b9a503401d61e14dce8693fd5 * base) % p
    x = (x ^ y ^ 0x947919e3056f7f06892deaea5dd1b7d5) & mask
    x = ((x << 68) | (x >> 60)) & mask
    x = (x * 0xa02b787bc52975292a0983d8b5ead65f + 0x6ad09e5664fed1056ae9b9d69075eb33) & mask
    x ^= x >> 39
    return x, 'maze.room_3f239cb0'
