def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0xa755a3a85da298024c721faa83c9511b) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0x504632f5e8223f25e783e67ba9c9dcd0)
    x = (x ^ y ^ 0x492e5d6129c1022dcc9f84417260d57d) & mask
    x = ((x << 84) | (x >> 44)) & mask
    x = (x * 0x6f5ad0e6e5f7196b07851f2551b1b4c7 + 0x3c9f0996bffc02ad812c647b5fe0692b) & mask
    x ^= x >> 78
    return x, 'maze.room_32cf88c3'
