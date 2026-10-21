def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0x3b7644fc11241e4703c51161fa43c50a) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0x9fc9241bdc89e3c83b7bdb04f475e4fa >> (k % 17))) & mask
    y ^= ((x << 23) & mask)
    x = (x ^ y ^ 0x8da43450430a76f465929e4e7b3c5402) & mask
    x = ((x << 109) | (x >> 19)) & mask
    x = (x * 0x1dfa17a20db1f7457df173fa9aa71289 + 0x842a326c51be2948ac5a81b2f0cd5a7d) & mask
    x ^= x >> 67
    return x, 'maze.room_fb619cb2'
