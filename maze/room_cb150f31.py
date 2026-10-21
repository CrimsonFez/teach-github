from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0xf7989998645b8e7c402723e0a30f601a) % 24
    base = 2 + ((x >> 17) ^ 0xe3188ebc86046e139900cf90e331b0c8) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 593
    x = (x ^ y ^ 0x1e8bdc91dcaa833f8b17ad0ac902ff3d) & mask
    x = ((x << 45) | (x >> 83)) & mask
    x = (x * 0x34442b04f401d8c798b6f13ed58e95f3 + 0x88ec2d88397e3a793681197021ce5a5b) & mask
    x ^= x >> 76
    return x, 'maze.room_1123fd8a'
