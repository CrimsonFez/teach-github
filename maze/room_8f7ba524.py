def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0x9660a91ac2db0874ebd6a9e764468671) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0xf296f20ba03219cb364a86dfb66eab66 >> (k % 17))) & mask
    y ^= ((x << 8) & mask)
    x = (x ^ y ^ 0xa7304a7597faecad3a4befa3a97cef95) & mask
    x = ((x << 22) | (x >> 106)) & mask
    x = (x * 0x8b4ff359f6fb8e78414e91be7a058b8f + 0xf96a95b7b1a40577c06505897aef0e8d) & mask
    x ^= x >> 49
    return x, 'maze.room_cf0304af'
