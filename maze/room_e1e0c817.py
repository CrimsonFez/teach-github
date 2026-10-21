def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xe7f4cef7dbfae90b44b886d5811354cf) & mask
    b = 0x571cf8967899a26496dc933ccdae0a31
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 40)
    x = (x ^ y ^ 0x2b53534e2820bc9cd50df18577f8ae29) & mask
    x = ((x << 73) | (x >> 55)) & mask
    x = (x * 0xcf4d3b907eb10357a9f53685dcfa2383 + 0x7ad662ea768a22762f7438518a1f9695) & mask
    x ^= x >> 53
    return x, 'maze.room_36710976'
