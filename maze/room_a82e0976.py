def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0xa7b09cad4e34874380c5467f2af1aeef) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0xed77b4ba45002714d3dd3158a776cbf >> (k % 17))) & mask
    y ^= ((x << 38) & mask)
    x = (x ^ y ^ 0x8b43374e4f33d9dd492c0cfb0a6e19ea) & mask
    x = ((x << 39) | (x >> 89)) & mask
    x = (x * 0x2a46685e81b0d9b2381183d90d8b680f + 0x7a0b4409df56cf3eb8454d25b114aeb3) & mask
    x ^= x >> 52
    return x, 'maze.room_b4d0fb8c'
