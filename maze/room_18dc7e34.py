from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0xd8d5fa46411f775839d30fc0aa9e2fa9) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0x4108c1b0d5b3f2ea57fcff8f57b4baf5 + 0xe3104b35a196d95e9abb4bb20f93d8f3) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0x7ebb1565555e4dac19dffc23f2800860) & mask
    x = ((x << 102) | (x >> 26)) & mask
    x = (x * 0x210dc1d883eaa646d0dc7a7ef3eedcf7 + 0xe6a3426724c1e9f06d4721eb9a145c1f) & mask
    x ^= x >> 82
    return x, 'maze.room_f2c3d6f6'
