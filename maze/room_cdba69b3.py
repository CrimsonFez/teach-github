from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0xe817d79c22f70d126d5a6c1a0661e25e) % 24
    base = 2 + ((x >> 17) ^ 0xd49ee1bfb4dfdd5b5ed55892f5695d15) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 99
    x = (x ^ y ^ 0xb63ab378f9b3e326d2f7e2dbe1f749e7) & mask
    x = ((x << 96) | (x >> 32)) & mask
    x = (x * 0x7bdf1ffc9097fad70b68a5d2e590b5d + 0xe9072728fc4b7123bb3c4a7f2074e7d6) & mask
    x ^= x >> 85
    return x, 'maze.room_6259a135'
