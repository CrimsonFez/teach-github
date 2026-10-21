from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0x2793eee2fc1545477765a61870103084
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0xb97b3c566488bd879ae3cffb37d373fd)
        value = ((value >> 7) ^ (y << 71) ^ 0x292bcc0b74c502d8e14738388d6ab1dc) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0x949aeaf73615f2687e3c7cc33be594ea) & mask
    x = ((x << 87) | (x >> 41)) & mask
    x = (x * 0x4db157822d171d467b8da8c555661e23 + 0xfa2dff4762a0064a5b180c156a150f82) & mask
    x ^= x >> 52
    return x, 'maze.room_a3747df4'
