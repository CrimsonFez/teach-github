from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0xe3b6fb842563c4a6723d1b98afabb6fe) % 24
    base = 2 + ((x >> 17) ^ 0xd6b6659054e5cb73917fe085c766970c) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 67
    x = (x ^ y ^ 0xe2aa63317e02e210c6078e301654732b) & mask
    x = ((x << 89) | (x >> 39)) & mask
    x = (x * 0x40d0cca03966001e5258a38eddfcd4ff + 0x4509fd0ca999b97333aab968f3939ba2) & mask
    x ^= x >> 56
    return x, 'maze.room_a691d386'
