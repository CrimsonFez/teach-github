def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0x5df7598f685c72130e2268e0c33b7455) % p
    y = pow(base, 20855, p)
    y = (y + pow((base + y + 1) % p, 35, p)) % p
    x = (x ^ y ^ 0x65451624e25f79fed1402ed661e2690a) & mask
    x = ((x << 113) | (x >> 15)) & mask
    x = (x * 0x54de380b54af2c6bc6feb1e194bce297 + 0xa5c403655bf2f5b6405dd5addcaef195) & mask
    x ^= x >> 66
    return x, 'maze.room_e012a34c'
