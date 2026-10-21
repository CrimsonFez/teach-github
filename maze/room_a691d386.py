def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0x7b869044d28b0dde92a67fa8ff43cf98) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 2141) % scale
    y ^= ((x >> 43) * 0xaae23c83b5c966dc22e910230c5019eb) & mask
    x = (x ^ y ^ 0x55b598ef59e7760d5829ab02602f1e7c) & mask
    x = ((x << 39) | (x >> 89)) & mask
    x = (x * 0x648753ab07933f75163594f448117159 + 0x9916e5926f3d9c7e7fa83f48fd1a06d4) & mask
    x ^= x >> 84
    return x, 'maze.room_7a7fa340'
