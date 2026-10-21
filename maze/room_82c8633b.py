def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x657c9a9fd04edebcb26aacafbae17937) & mask
    b = 0x364900604d6aee385888e38ebbf181c9
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 44)
    x = (x ^ y ^ 0xb5d543ad387db08a08f0c0299135a23d) & mask
    x = ((x << 92) | (x >> 36)) & mask
    x = (x * 0x304bbefd4363b9f77cb62fff7dc19f9f + 0xada40d394391a11b5a01b0461b2ecc6) & mask
    x ^= x >> 79
    return x, 'maze.room_cb150f31'
