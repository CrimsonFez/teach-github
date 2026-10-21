def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    y = (x ^ 0x68944685a93c8e777b60274386f6b496) & mask
    for k in range(29):
        left = ((y << 1) | (y >> 127)) & mask
        right = (y >> 1) | ((y & 1) << 127)
        y = (left ^ (y | right) ^ (0xa3386423c9057e51f736e303546fe368 >> (k % 17))) & mask
    y ^= ((x << 42) & mask)
    x = (x ^ y ^ 0x261460c52666f9683a30c51f73c6063c) & mask
    x = ((x << 67) | (x >> 61)) & mask
    x = (x * 0x60fb0438c14205577eb960612926a6a5 + 0xe54501b0077c05982ad34d9e4e29ca86) & mask
    x ^= x >> 86
    return x, 'maze.room_ddc0ee3e'
