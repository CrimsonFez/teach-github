def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0x1987e5caa99fc4706eb37b3a40d15527) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 1672, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0xbe531fe5e7546f1290dcdb36839d2d25) & mask
    x = ((x << 83) | (x >> 45)) & mask
    x = (x * 0xf9cf234c4116e310131e57f49c5eced9 + 0x3d12076c417f9b137d10e50cd1989f66) & mask
    x ^= x >> 83
    return x, 'maze.room_0954bbb3'
