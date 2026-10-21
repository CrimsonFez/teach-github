def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xcb3b71bf6105235bd548e75fd275b377) & mask
    b = 0xe6ef37ff9aa3d6ce2f9ce9d5d594ad67
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 33)
    x = (x ^ y ^ 0x695883303dffd34112bf09fe0fbd9917) & mask
    x = ((x << 101) | (x >> 27)) & mask
    x = (x * 0xe40a05f7d425165fc61558d35fcd11e1 + 0x9c2c2ef658678dd51e5e9caf6e9b9752) & mask
    x ^= x >> 68
    return x, 'maze.room_844830bd'
