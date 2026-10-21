def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0x586876125ad055960e01fb4706dab5da) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0x189cd984199fa010cf67c1bc7c4e062 >> (k % 17))) & mask
    y ^= ((x << 26) & mask)
    x = (x ^ y ^ 0xe8aac32bbc6bda7323259b806b11ac94) & mask
    x = ((x << 83) | (x >> 45)) & mask
    x = (x * 0x6b51da703a02464261ddb5c22e2bb34d + 0xeefd7051c300460d1a3da4f0e00d8e0e) & mask
    x ^= x >> 83
    return x, 'maze.room_3e6c97ac'
