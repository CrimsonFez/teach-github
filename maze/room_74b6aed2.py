def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0x2de339fafe224fdcd6b80a4f50b2c565) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0x3788d43398acd86514e107f018ee77c >> (k % 17))) & mask
    y ^= ((x << 22) & mask)
    x = (x ^ y ^ 0x9fdb61be0c4bdb796abd82aeb966a545) & mask
    x = ((x << 115) | (x >> 13)) & mask
    x = (x * 0x91601cd801e68e001b855b6b83e909a5 + 0xcbdd7745c06b171d276d4bbec9a10579) & mask
    x ^= x >> 68
    return x, 'maze.room_c3bc3be8'
