def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xcb425e879157d835dfe6232d64d8b31c) & mask
    b = 0x58740166e124f29edeea64157e2e0f0d
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 59)
    x = (x ^ y ^ 0x601eed2b593fa7f4b83f7540f8cc3116) & mask
    x = ((x << 18) | (x >> 110)) & mask
    x = (x * 0xe2882ff984589b0f1b6b718ce346f6f + 0x991da750f2d8b77e9d99e5f078389263) & mask
    x ^= x >> 69
    return x, 'maze.room_747df634'
