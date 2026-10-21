def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0x7be3aa5c67fae725f8575b95b786da2a) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 2899, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0xe76e8c3460902c1ed5d6708c94b1f957) & mask
    x = ((x << 44) | (x >> 84)) & mask
    x = (x * 0x5fcf64173e8e44ba60bc9736b1e0fc3 + 0xd397356246a3c37fa99d84a21c0cc6cb) & mask
    x ^= x >> 68
    return x, 'maze.room_e87c0402'
