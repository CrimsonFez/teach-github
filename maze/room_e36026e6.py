def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0x285238ac5b1d19c5ad6882216c69e9c8) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0xdd139d0dfa8bb3dbd24401b6f68eea37)
    x = (x ^ y ^ 0x5df710d68185665dd8e0a6472de12f80) & mask
    x = ((x << 96) | (x >> 32)) & mask
    x = (x * 0x35ac1bf48b4496260242dc20e6d65c77 + 0xc2c71c3a08c76b8f58d4bab5f56973c7) & mask
    x ^= x >> 80
    return x, 'maze.room_787a4e25'
