from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0xaebb9794e512ead6f0e1c12f5a4481bf) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0x1f4ca25fc3bca9fb313ac98acb834ed + 0x74016e45759ffcaaa50e383524782597) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0x76f31674aea8a97c7a7d59d467c1bf8f) & mask
    x = ((x << 106) | (x >> 22)) & mask
    x = (x * 0xb9e68a83de3f6975a118305e6f4487e5 + 0x118565cb46f732b41e2e1e7cf9f7bf7e) & mask
    x ^= x >> 43
    return x, 'maze.room_0a11db92'
