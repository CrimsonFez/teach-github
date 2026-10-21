from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0x3ae1efafcfeca745ea69ffdec7a86e2e) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0x68d50207a67f05c20685bf37f166e9b1 + 0xcd1913bf9041daff5b8a7d2cdce21777) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0x7fb00c47686783aeb355aeec7cc7e21b) & mask
    x = ((x << 71) | (x >> 57)) & mask
    x = (x * 0x421ded189c5cdc62e8ef2815392b73f9 + 0x173dd95f36f1a79d1a5e9e8fba710940) & mask
    x ^= x >> 56
    return x, 'maze.room_f3633160'
