def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0x3308b0ec67012e13333b010c59e7dec6) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0xa286ec67df7eab9411e0d097292199a1 >> (k % 17))) & mask
    y ^= ((x << 24) & mask)
    x = (x ^ y ^ 0xb5f520a61294b35cbb07e5475c4e9c94) & mask
    x = ((x << 109) | (x >> 19)) & mask
    x = (x * 0x531c81a83fcd4b536b475fa5120647a3 + 0x1c367483b72e85fce7758f5ca77c77a1) & mask
    x ^= x >> 37
    return x, 'maze.room_806b1f9c'
