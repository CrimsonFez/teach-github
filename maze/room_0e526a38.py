def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x7acfbd939232039716395c30d00465a8) & mask
    b = 0x1836b330f89cd043aeba881b5e8c85d
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 35)
    x = (x ^ y ^ 0x2cda8fe8b11304cbb092fa5180f8c1a4) & mask
    x = ((x << 115) | (x >> 13)) & mask
    x = (x * 0xf80652e83852d8315b6cb1460867b66d + 0x7bee39af5c0a7e796f03a1234cbbf00d) & mask
    x ^= x >> 48
    return x, 'maze.room_cdba69b3'
