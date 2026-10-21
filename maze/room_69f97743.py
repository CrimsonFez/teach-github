from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0xa47fc01b7587e1294840b423702b3532
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0xe8849a6ab621dd61963f7ffcaa8f61ed)
        value = ((value >> 7) ^ (y << 71) ^ 0x1fb833844c45f817b2b46a6b19220c7a) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0xdba87502266c8af47b3c58284c09bc4) & mask
    x = ((x << 26) | (x >> 102)) & mask
    x = (x * 0xc7b68c67c04c0560dc7556ccc396a571 + 0xb8419e294c55a0984980fd0f2067309b) & mask
    x ^= x >> 42
    return x, 'maze.room_b89243a8'
