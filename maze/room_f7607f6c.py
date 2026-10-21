from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0xf2b1c71ec5430d8a4611c5bf2392b7aa) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0x57e25d738d8a98237588a6dd7f94c30d + 0xeb4f5d468d3b7d7994eb42db671cd715) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0x496e4c3c77cb22321e1bd4d66d92d952) & mask
    x = ((x << 13) | (x >> 115)) & mask
    x = (x * 0xc32ccc18738f600df4f422ea505719e9 + 0x8b233ffe2ea9b7abf6e3aa9d776e9b31) & mask
    x ^= x >> 46
    return x, 'maze.room_c987c563'
