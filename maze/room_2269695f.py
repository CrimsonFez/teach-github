def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x6f14b38d1dae60e1e3188f598508eaeb) & mask
    b = 0x80408eb5630b71c0b70b50da4e86bd91
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 41)
    x = (x ^ y ^ 0x16a3c5723dadc8643159cc48b177e8c6) & mask
    x = ((x << 18) | (x >> 110)) & mask
    x = (x * 0xb54b0b54ab2d43570e037550ae2c37 + 0xd3d19d98128abfcedc375b6588ca106) & mask
    x ^= x >> 55
    return x, 'maze.room_3941a62b'
