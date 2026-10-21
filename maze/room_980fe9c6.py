def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0x3c9fdb3a219fdfefd38c00bb56c80d39) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0xef7990d2f7138b8463b00ab81df4c163 * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0xa955580e14fe622dacbf43c738352a26 * base) % p
    x = (x ^ y ^ 0xdc767ece3ff85b798b2a93a673e86372) & mask
    x = ((x << 92) | (x >> 36)) & mask
    x = (x * 0x543994afff7928d5935b0d07e9c151bb + 0xfec8531f38040e23fb1108203d9dadb2) & mask
    x ^= x >> 52
    return x, 'maze.room_764b40ff'
