def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0xb06cd24f81c0cb1bd4181c2aa259eee0) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 2256, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0xe9e78ff7f59680e73850450fdcbce1b4) & mask
    x = ((x << 40) | (x >> 88)) & mask
    x = (x * 0x666e8f34d8035454ddcbcb212df8e2e7 + 0x4de573bdfb34e5f054acc56188f702f0) & mask
    x ^= x >> 37
    return x, 'maze.room_9e5af1c3'
