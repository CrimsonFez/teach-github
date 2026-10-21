from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0x2c07415bc02b582029dab3768878950c) % 24
    base = 2 + ((x >> 17) ^ 0x8bc4db8beaa12f20b4e64914358c6873) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 806
    x = (x ^ y ^ 0xce31d04990d5a7cf4029a9a5d59ebf7) & mask
    x = ((x << 30) | (x >> 98)) & mask
    x = (x * 0x8b0bf219ff19aad2a51eb4e62ae6fda5 + 0x26215ca24a589b6aa037c4638b5635bb) & mask
    x ^= x >> 39
    return x, 'maze.room_6515ebe3'
