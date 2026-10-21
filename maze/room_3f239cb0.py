def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0x2f8a899505760c225328170249421271) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 3950, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0xfe0bfee830b4263f7b26861804c8a5b3) & mask
    x = ((x << 98) | (x >> 30)) & mask
    x = (x * 0x348345426617bd821de8507355f7c837 + 0xebf454c1d1f13360e8b4b6a6dfe5319b) & mask
    x ^= x >> 56
    return x, 'maze.room_8c8dcd01'
