def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0x6a584e58d7af35f85672dd4308f9a83b) % 65521 for i in range(8)]
    right = [((0x25473cec9a8f1f6344fdb60988ed4e24 >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 6996 + coefficient) % p
    x = (x ^ y ^ 0xd934b4b9cf5ee97d16666fda0c26ec64) & mask
    x = ((x << 49) | (x >> 79)) & mask
    x = (x * 0xb68a5341d198fb3fd7f9ee76fafa6ccd + 0xb8171402373c4320e3e0798e37e0bdb3) & mask
    x ^= x >> 71
    return x, 'maze.room_02a85936'
