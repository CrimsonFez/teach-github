def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0xe78f14c408969d9afabb3343dae77f64) % 65521 for i in range(8)]
    right = [((0xa084e69b742e52685f9c9211ad55f180 >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 1094 + coefficient) % p
    x = (x ^ y ^ 0x6e74e5e2f56d20bb3e4cb72b8d743f75) & mask
    x = ((x << 17) | (x >> 111)) & mask
    x = (x * 0x2fbf45cfab17032b40b424229c882e07 + 0x947cbda878ba80a81fc6ff89b1e680c) & mask
    x ^= x >> 62
    return x, 'maze.room_3bdc0f4f'
