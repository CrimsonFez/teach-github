def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0x48d65d69b1ed0f07e3e729cece6905d7) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0x477df66713d2e9f464c1b4bb1cd66bd0 >> (k % 17))) & mask
    y ^= ((x << 43) & mask)
    x = (x ^ y ^ 0x7609f8bb794ee7e187e66cadb443a163) & mask
    x = ((x << 30) | (x >> 98)) & mask
    x = (x * 0xc455e087cdff7965e78959972a7c62c3 + 0x1fc0ef785118c5700834d78f364d664c) & mask
    x ^= x >> 86
    return x, 'maze.room_d5fcf1bb'
