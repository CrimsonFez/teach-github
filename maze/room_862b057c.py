from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0xee53e037603ab25a9fa7802d70a5ef7e
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0x1168bf824b05baded32d97e4d92df3b5)
        value = ((value >> 7) ^ (y << 71) ^ 0x5c0ceb4d6a194e2932cb93c7b8361d1c) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0xf5e27cd4d8fffd2d4b14390cc94cd24d) & mask
    x = ((x << 80) | (x >> 48)) & mask
    x = (x * 0x6b8b98f90b353171ab1cff656fe23c03 + 0x330ecf8cfe1d1c5327cae0059a790b10) & mask
    x ^= x >> 65
    return x, 'maze.room_16a38f50'
