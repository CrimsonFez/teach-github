def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0xffa4fca17da655c9db207c9ab7f1c130) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 6909, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0x7deb1b88106d3de491ecca3f5a08f9ca) & mask
    x = ((x << 115) | (x >> 13)) & mask
    x = (x * 0xed7d8537873821046186f32164d00c23 + 0xc3a61f4451144035808e871a00771b39) & mask
    x ^= x >> 81
    return x, 'maze.room_e36026e6'
