from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0xbc227c5b4750d325aca9629ed7b628ae
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0x1d801db7930a638f514b0643f928f032)
        value = ((value >> 7) ^ (y << 71) ^ 0xdf15ed0e7e01bddf1e0e5da32d29ddc7) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0xbc15855f10bd72db9f211878c3e85e2d) & mask
    x = ((x << 29) | (x >> 99)) & mask
    x = (x * 0xfecdfd4a5c9611622bdf5ccf1e8679d3 + 0x423886aec220366a8fcfa676a4684b21) & mask
    x ^= x >> 78
    return x, 'maze.room_381f92a5'
