from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0x7f2f14e41d7ffc7b67ade74791bb1b9e
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0xb77def278d51045fad8cdd0f3aa9d15a)
        value = ((value >> 7) ^ (y << 71) ^ 0x83a550aa1f248f9a69536c130d06c7b0) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0xeb233914596fd40516aac139b44fbe49) & mask
    x = ((x << 16) | (x >> 112)) & mask
    x = (x * 0xc8672606be56ca8ae55ceebbb09e9c51 + 0xf5cff616bfa2385fcfd64a62dd066379) & mask
    x ^= x >> 62
    return x, 'maze.room_1d40efba'
