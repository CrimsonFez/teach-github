from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0xd87f5689885ad6e43f96b9660286eea) % 24
    base = 2 + ((x >> 17) ^ 0xcc3ad1c70146aee3de3553f5f155f2ba) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 297
    x = (x ^ y ^ 0x51bc0db6c2814022a61a1361634f0ce8) & mask
    x = ((x << 83) | (x >> 45)) & mask
    x = (x * 0x91c48b9816f0414a811db9d82b133d1b + 0xdce0615da1bedba3490f4dcdb66fd191) & mask
    x ^= x >> 80
    return x, 'maze.room_16ca9c0e'
