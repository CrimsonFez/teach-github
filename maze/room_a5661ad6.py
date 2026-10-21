def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0xf3ecaea84a7d057cc2f987e578936f96) % p
    y = pow(base, 45922, p)
    y = (y + pow((base + y + 1) % p, 5, p)) % p
    x = (x ^ y ^ 0xc4120da9d84ed53bc0c0035e247832b4) & mask
    x = ((x << 27) | (x >> 101)) & mask
    x = (x * 0x36028294df51ebac24bb0a5f5c2f624d + 0x8f7499025e419d277a64e7d02eb2e558) & mask
    x ^= x >> 65
    return x, 'maze.room_99e0750a'
