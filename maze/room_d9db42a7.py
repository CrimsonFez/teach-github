from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0xb70720004fe97d8cb8e6b8f00285c190) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0xcbb83573e0b003be678e67481f39aa51 + 0xc9a6c8f45c090c0a9c97b2a985d40c26) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0x2ccdbfd23b9fb21e537073488651d06d) & mask
    x = ((x << 65) | (x >> 63)) & mask
    x = (x * 0x3530b97e3aa47bd356bd3aa2acdbd553 + 0x3bfb3beb8a5bf3c5bc8489cb872be208) & mask
    x ^= x >> 46
    return x, 'maze.room_0e0f1092'
