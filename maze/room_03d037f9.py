from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0x92643ef2e111a32f4d7bd3299b642853
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0x70748b27543dbe2ddcc43b19dbb33923)
        value = ((value >> 7) ^ (y << 71) ^ 0xd6cd0ab4886e33d33bf7052fe84da8e) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0x45794bd6f5682da4e53a410a2599f286) & mask
    x = ((x << 102) | (x >> 26)) & mask
    x = (x * 0xeaa6a252eb07d296bc8457bf250528b + 0x3feb9842795068abc1418a74de4a5a12) & mask
    x ^= x >> 80
    return x, 'maze.room_d981e5f4'
