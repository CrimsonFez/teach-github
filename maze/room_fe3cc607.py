def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0xd65ca52ea70303722f460fa60b042416) % p
    y = pow(base, 15474, p)
    y = (y + pow((base + y + 1) % p, 30, p)) % p
    x = (x ^ y ^ 0xb1435fe1806957c5e9d3c00c0f63cf83) & mask
    x = ((x << 106) | (x >> 22)) & mask
    x = (x * 0xc89e17d4e34f1359b9f593466e7a74b + 0xbf6b63aa485f9e083f024b56344e375e) & mask
    x ^= x >> 75
    return x, 'maze.room_203436d4'
