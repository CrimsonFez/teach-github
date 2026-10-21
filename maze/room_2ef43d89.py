def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0xb5bf70e161fd2403323e14b303dc7abb) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 1597, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0x47099e0280529f913a92b23a51aeb41c) & mask
    x = ((x << 79) | (x >> 49)) & mask
    x = (x * 0xa72ec04136924f2560ae212fd0742cd5 + 0x30d39226d0f75ec430524586d33abb9) & mask
    x ^= x >> 55
    return x, 'maze.room_22ef5891'
