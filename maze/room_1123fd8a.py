def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0x5ee7a2441543bc16267b7e7f152d2b8b) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 1252) % scale
    y ^= ((x >> 43) * 0xee54fc71475cddcb0e838b4b8d596ab9) & mask
    x = (x ^ y ^ 0x2af012593884aeeccc2128b9cf5b9b18) & mask
    x = ((x << 36) | (x >> 92)) & mask
    x = (x * 0xc4e8aed1eb3c6ca03ca5c37f1daa9d51 + 0x28751a6f0aa62ffc2407d56dc7aa0b10) & mask
    x ^= x >> 73
    return x, 'maze.room_053eeb6d'
