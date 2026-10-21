def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0xa29d783ea878a2ce641119ab0598cf4b) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0x6de82e644c0c7bd1237d3819bb73fb15) | 1, 32, 1 << 128)) & mask
    x = (x ^ y ^ 0x12d5b3bd02d6430752428e4a33acad16) & mask
    x = ((x << 109) | (x >> 19)) & mask
    x = (x * 0xd0f1f222fcb1587f08eac7f4b684e911 + 0xf8b517ae2e5296e5136cbfc69a82c5ff) & mask
    x ^= x >> 84
    return x, 'maze.room_cb98fddb'
