def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0xb0b07008222b7429c2874cd91f088239) % p
    y = pow(base, 56993, p)
    y = (y + pow((base + y + 1) % p, 83, p)) % p
    x = (x ^ y ^ 0x1e00e6f9d1c393250537ac6580fd9a39) & mask
    x = ((x << 29) | (x >> 99)) & mask
    x = (x * 0x1b70189eb0a4ba20f77204d5ae0561bf + 0x8d0c9ca51da8adf55bd2bf54131a8a0a) & mask
    x ^= x >> 49
    return x, 'maze.room_15587eb4'
