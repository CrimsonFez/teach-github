from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0x7ed57f1ec4f95f8001692748d4dac479) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0x7bc03dfc4552c9cd636cae3b16b312c5 + 0x17650ebbb4fc1c2f9cf2a958c28aed61) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0x7bbb341b115c4b48636e15d1a2620217) & mask
    x = ((x << 32) | (x >> 96)) & mask
    x = (x * 0x17354d8f3c86a3d9a148db60b4006bdf + 0x87fc5b46c0258e0432f3476f3116e292) & mask
    x ^= x >> 73
    return x, 'maze.room_19d25979'
