def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0xff4d087861d3016d58ccb44cfbd3005f) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 4558) % scale
    y ^= ((x >> 43) * 0x4c7f6de0d8e4ebe1ea017991a7daa9d) & mask
    x = (x ^ y ^ 0xdc46a055a0ea22fbf1da5261d81b931) & mask
    x = ((x << 56) | (x >> 72)) & mask
    x = (x * 0xd23a9eb7660e6e52992066a73419ac1b + 0x44b735bc44e2f5829c16c27d32cb133e) & mask
    x ^= x >> 80
    return x, 'maze.room_f11ba5cb'
