def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xff3c1a0290f93de07e6a44df94d3f59f) | 1
    b = ((x >> 37) ^ 0xa31fc99473a0e73784c201ec64d2e1f7) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0x383e35c2b0be7ac19f21076e4d441da3 + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0x8b130832715c86b9432e1003556363e5) & mask
    x = ((x << 92) | (x >> 36)) & mask
    x = (x * 0x85350994df64d9a8dd24a198c32a35bd + 0xa182a41fb09dabfa439c00f2f5cd134) & mask
    x ^= x >> 66
    return x, 'maze.room_03d037f9'
