def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0x7b3f6cea82f6d1d3b91d701c382d6bea) % 65521 for i in range(8)]
    right = [((0x810ab3d5986bdb6e993f211c0b97899d >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 1920 + coefficient) % p
    x = (x ^ y ^ 0x944bd7e4e467fa4b178a03acecb956da) & mask
    x = ((x << 14) | (x >> 114)) & mask
    x = (x * 0xf71476e21d32e2b1462848b12b4d6359 + 0x160896280ad70aba908adb6629cef471) & mask
    x ^= x >> 50
    return x, 'maze.room_210b191f'
