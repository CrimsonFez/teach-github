def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xd4605d867fb4094f341e562bbf019060) | 1
    b = ((x >> 37) ^ 0x981509ed418251526f22b7878f88f3a) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0x3a4a6c1c56283a8dbdcc27bdf3095e1d + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0x73839b91e0373f9e66439eaa136d0cd9) & mask
    x = ((x << 83) | (x >> 45)) & mask
    x = (x * 0x944ac5eab44e6ce691e71fe43b9c4b87 + 0xd091ac23b06b53a8ac67bca05750d5b6) & mask
    x ^= x >> 72
    return x, 'maze.room_862b057c'
