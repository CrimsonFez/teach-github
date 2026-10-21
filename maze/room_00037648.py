def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0xb6ba4b0f6b2a1a47db7a209f383f15cd) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0x4032b0c3c3f5927444b5039155950176) | 1, 35, 1 << 128)) & mask
    x = (x ^ y ^ 0x2da4e8d8e84acbfa63f45b744913329f) & mask
    x = ((x << 21) | (x >> 107)) & mask
    x = (x * 0x32bfbfffc610419fc3be8336fdb1f4e7 + 0x1bb5dbc1bffbef60692519b01417c32f) & mask
    x ^= x >> 83
    return x, 'maze.room_559a5bec'
