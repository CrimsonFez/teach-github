def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0x75787f6bee44e4a586f64da046974306) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0x2b94a197358609cf2f2a84a380ea08e9)
    x = (x ^ y ^ 0xa4de400ac913d34f91e1f89b760e122a) & mask
    x = ((x << 57) | (x >> 71)) & mask
    x = (x * 0x44d6b17fd67453f976c6fd4316328d93 + 0xaa1bc79d3c4bac7d81ad487863b74fd1) & mask
    x ^= x >> 63
    return x, 'maze.room_2269695f'
