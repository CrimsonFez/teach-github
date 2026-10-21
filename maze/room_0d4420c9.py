def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = (x ^ 0x53ba7bf563124302424839a73c829856) % p
    y = pow(base, 14868, p)
    y = (y + pow((base + y + 1) % p, 17, p)) % p
    x = (x ^ y ^ 0xa6fec4b5619d8c5057efa185b9c4682e) & mask
    x = ((x << 39) | (x >> 89)) & mask
    x = (x * 0xad52c1650b322cc186821ff8b40a38a5 + 0x66e268c519d5410b3980516e00d17885) & mask
    x ^= x >> 85
    return x, 'maze.room_a9116aab'
