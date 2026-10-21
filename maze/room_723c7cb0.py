def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0xccaece59b71a659163aa08775584ee3a) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 332, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0xc62e16b3f4d78e6da9594716556c4570) & mask
    x = ((x << 32) | (x >> 96)) & mask
    x = (x * 0x48f957b8510b4c1ea8ef71147d47e5fb + 0xa993915702299edcaaec2171a9d7e351) & mask
    x ^= x >> 44
    return x, 'maze.room_c3efffb9'
