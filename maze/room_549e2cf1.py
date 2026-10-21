def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0x237ed202d105f82dfe102ddd64ca8156) % p
    y = pow(base, 29798, p)
    y = (y + pow((base + y + 1) % p, 29, p)) % p
    x = (x ^ y ^ 0x35453517426ab4fd5186a76f5299456a) & mask
    x = ((x << 28) | (x >> 100)) & mask
    x = (x * 0x21e53daf00e008ea52d5a4d309b6a9d5 + 0xd338bc7a02c060b4ad2ba676dd2a0aa9) & mask
    x ^= x >> 41
    return x, 'maze.room_8e7c5023'
