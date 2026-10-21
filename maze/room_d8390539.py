from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0x478eee256df23b9d3167eca00aa6ee5) % 24
    base = 2 + ((x >> 17) ^ 0x884e76972907e5405697a958ef7ac8a5) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 561
    x = (x ^ y ^ 0x906183cefef865913714a3649667af5c) & mask
    x = ((x << 64) | (x >> 64)) & mask
    x = (x * 0xf43e7adcf3c2e84d432b09b7f22fd3e5 + 0xad350ac56e576b97298852bcd4ada5c7) & mask
    x ^= x >> 64
    return x, 'maze.room_9460d420'
