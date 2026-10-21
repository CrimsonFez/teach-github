def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0x931a6776366b576837f70290d2bcf5dc) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0x94dbb6016e54a707763d0edb45c2239e)
    x = (x ^ y ^ 0xd21586e8a60a0ff777ba9cbfcd096238) & mask
    x = ((x << 68) | (x >> 60)) & mask
    x = (x * 0x12f91e8cdd654414f4d64e2fef83f3b + 0x23eb06342b42b77252dc012176ca29a0) & mask
    x ^= x >> 38
    return x, 'maze.room_d52c7b7f'
