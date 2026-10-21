def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0x1d7e8b56646ebcb378c5ce304cad62df) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 5729, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0x876463bc33be9e552dfe0f9710c12ed8) & mask
    x = ((x << 70) | (x >> 58)) & mask
    x = (x * 0x9538bcbfea0d54372c93d1bc20e317ed + 0x143f0cbc1613d7e834cdbe221c1b9c80) & mask
    x ^= x >> 63
    return x, 'maze.room_cb686fce'
