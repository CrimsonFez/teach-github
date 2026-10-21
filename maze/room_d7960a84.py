def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0xa7058a8f3350105d996d0e1832906819) % p
    b = ((x >> 53) + 0x9f6060d9847cee7f182d662aa3e3d5e1) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 6117) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0xf8cc130c074d4167ed72d43981a9d1c6) & mask
    x = ((x << 63) | (x >> 65)) & mask
    x = (x * 0xaa61d1e65071a04ce2db0b1c7239df + 0xd887c305154a60f782f3c876c7c72ee8) & mask
    x ^= x >> 49
    return x, 'maze.room_f79bd257'
