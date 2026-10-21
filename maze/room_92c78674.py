def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0xd7cf05ea481d478aa97c5de38c63b18a) % p
    y = pow(base, 40672, p)
    y = (y + pow((base + y + 1) % p, 75, p)) % p
    x = (x ^ y ^ 0xa00d1cebbeac7418d603d00ed127e5f0) & mask
    x = ((x << 77) | (x >> 51)) & mask
    x = (x * 0x743b7dfacecde29b939eed59241dad0b + 0x934f0d9d58fac4fa7b3c5e703196fb97) & mask
    x ^= x >> 70
    return x, 'maze.room_21e15e7f'
