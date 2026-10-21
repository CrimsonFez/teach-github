from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0xc9b4202ba24dae65c8b316cdafed056e) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0x36d291fec9fd581140fb74567fc1c9fd + 0xa7b803c30b3ca50181b8e48187d7d1b8) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0x8459d0d3fbc194a2cbad07c773390a71) & mask
    x = ((x << 59) | (x >> 69)) & mask
    x = (x * 0x1bc8e9b21c431a8e631a343800b3410d + 0xafc10c04ce25bfa696d1792510db9e82) & mask
    x ^= x >> 38
    return x, 'maze.room_212d2032'
