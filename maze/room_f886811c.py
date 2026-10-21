from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0xb68979bae7e58f96bd9e4f77f5e12116
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0xc5a3a84265f27f346093b63266330210)
        value = ((value >> 7) ^ (y << 71) ^ 0x75f960c28747e116765f2d4ee511d143) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0x196b5c3d8f05566ea49ad960a9e066da) & mask
    x = ((x << 98) | (x >> 30)) & mask
    x = (x * 0x2f6dad7b22a1ac321a87513858a7816b + 0x7002fecf64ad61f5cde6a8eaa1010622) & mask
    x ^= x >> 88
    return x, 'maze.room_4ccaa1fc'
