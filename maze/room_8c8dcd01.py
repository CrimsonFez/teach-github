def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0xa0298c29a01ddf39d4885f2cd717f83) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0xb3b0a450004abb37c1810b935e9acb41)
    x = (x ^ y ^ 0x429d9a60ebc7c2f7f43ecec652c2d0a) & mask
    x = ((x << 103) | (x >> 25)) & mask
    x = (x * 0x3d2bcc4488d2d6657d0c31f4b169a7e3 + 0xb3892c07cad32aa3f3ead893a97bcbe) & mask
    x ^= x >> 81
    return x, 'maze.room_2dc24fb2'
