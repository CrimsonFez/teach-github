def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0xc04c9b030efbf19ff1c2c056b5dad61f) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0xf3bf42f1b036246a6d806d23c9877fdb)
    x = (x ^ y ^ 0x4ab407386bb7c5247171099bb1056593) & mask
    x = ((x << 14) | (x >> 114)) & mask
    x = (x * 0x973befd0d22c1b1ea8d5c89279060651 + 0x6c33442e4fcf0c9027a7397ff322f649) & mask
    x ^= x >> 40
    return x, 'maze.room_1d9bac7f'
