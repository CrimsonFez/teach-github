def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0xc1985f34c2b10ce542d40dfdbfb7c299) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 6162, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0x4b35261b62f7fe682752c38f9339b2bb) & mask
    x = ((x << 53) | (x >> 75)) & mask
    x = (x * 0x49e5726902855e01f72818f5bfaceecf + 0xbada8da5758ca97fa0ea595396416124) & mask
    x ^= x >> 71
    return x, 'maze.room_9765313e'
