from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0xea1e82b4055e7c75be784eab6b36ed6c
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0x1abfa4833a64897fcd052c3c4825b54f)
        value = ((value >> 7) ^ (y << 71) ^ 0x12533c8647d53243a7010caf8075bb1e) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0xf6cdd18b2c319b2bb108d81537375a9f) & mask
    x = ((x << 89) | (x >> 39)) & mask
    x = (x * 0xd1a07e2abc27bba69c4c4b5f6eacd1 + 0xf1778286e678896353b4acaa49cdc8dc) & mask
    x ^= x >> 52
    return x, 'maze.room_6e0aa8b4'
