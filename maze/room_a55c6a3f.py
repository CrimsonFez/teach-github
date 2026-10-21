from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0xde8f50605d8d2a0bc76a46af3f22d9dd) % 24
    base = 2 + ((x >> 17) ^ 0xfc3df9bc817d95e03a77b60e8538701b) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 570
    x = (x ^ y ^ 0x1b7359c50231af9af33dd8f7c485d7d1) & mask
    x = ((x << 66) | (x >> 62)) & mask
    x = (x * 0xa759e9a057cf0f474d26df12cdce83df + 0x309f4c56368a1622badd94807262ab5e) & mask
    x ^= x >> 63
    return x, 'maze.room_daf503f1'
