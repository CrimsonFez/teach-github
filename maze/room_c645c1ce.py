from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0x2cef4eadc7f8685e1004141eb8a83b66) % 24
    base = 2 + ((x >> 17) ^ 0x1f66d3f243f5183548360bc9d7ad52f8) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 404
    x = (x ^ y ^ 0xaa875b242e115a5aa015de679b512e91) & mask
    x = ((x << 13) | (x >> 115)) & mask
    x = (x * 0xa66dbe40c19df56130efae5a59c9fc33 + 0x28234f1023aa968733113ce885b93b3d) & mask
    x ^= x >> 51
    return x, 'maze.room_d9edbf82'
