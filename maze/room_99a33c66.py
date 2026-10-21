from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0x25ac1cbd031c23404292f26729e3eeea) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0x1855b4759884fd39ce7e6683133cab6f + 0xb892b0ba2e3cdc350dedea8426aab47) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0xe97e44b901174488d5de337e8f1eed68) & mask
    x = ((x << 50) | (x >> 78)) & mask
    x = (x * 0x967b5e3ab87e028e15af6f73c0b032ed + 0xbf3048cf328cd43c1fea309f1e88bc02) & mask
    x ^= x >> 82
    return x, 'maze.room_12a9897b'
