def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0x814b1744d4d6108c8ffa0ac769416725) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0x9171669226665c8cbc538473f095947c >> (k % 17))) & mask
    y ^= ((x << 37) & mask)
    x = (x ^ y ^ 0xc7ce7efa472e9e503df518312cebdb7f) & mask
    x = ((x << 116) | (x >> 12)) & mask
    x = (x * 0xf1cfc17c7299ba3e2bbba0b5c32ba865 + 0xaf9472006f85428e3026a51dcce1c933) & mask
    x ^= x >> 56
    return x, 'maze.room_e734db14'
