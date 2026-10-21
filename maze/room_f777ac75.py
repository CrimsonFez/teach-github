from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0xeeead77e7dec12eb8c0a1508ba78849e
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0x75c2cf011e956f823e5be5905516c861)
        value = ((value >> 7) ^ (y << 71) ^ 0x26e90a0e4d8fa33131b4f6968b694d46) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0x93d02532f756d43a5ef935c6dfd570fe) & mask
    x = ((x << 98) | (x >> 30)) & mask
    x = (x * 0xdca73c7cd0d4a57374ef11c246921a2d + 0xa2f557e167f5ef68f11a978ddd4fa939) & mask
    x ^= x >> 82
    return x, 'maze.room_f940eee5'
