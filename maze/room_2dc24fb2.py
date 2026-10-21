def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xc1cb2f84460309bf48d3fd7658d84c20) & mask
    b = 0x34d038129aaf92b0c4f11116d52dfafb
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 56)
    x = (x ^ y ^ 0x39fe71aae835615a26986114f8129267) & mask
    x = ((x << 40) | (x >> 88)) & mask
    x = (x * 0x5ac99d8040234d8d89e1d25d1415dc8f + 0xbf5272149bda4f99b8c7264b1e20f068) & mask
    x ^= x >> 84
    return x, 'maze.room_d8390539'
