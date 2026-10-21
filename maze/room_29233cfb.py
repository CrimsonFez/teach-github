def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    numerator, denominator = 1, 0
    for index in range(23, -1, -1):
        term = 2 + (((x ^ 0xbd951b7b6404247572fe10db90e3f305) >> (index * 5)) & 31)
        numerator, denominator = term * numerator + denominator, numerator
    quotient, remainder = divmod(numerator * 1897, denominator)
    y = (numerator << 37) ^ denominator ^ (remainder << 71) ^ quotient
    x = (x ^ y ^ 0xbe9d4635bc246c5f565de5a91620d897) & mask
    x = ((x << 19) | (x >> 109)) & mask
    x = (x * 0x3eac9e70a3b74b5fd73d698aa595d289 + 0xda20552493486c402ecce79f2a50774d) & mask
    x ^= x >> 84
    return x, 'maze.room_7a207a6c'
