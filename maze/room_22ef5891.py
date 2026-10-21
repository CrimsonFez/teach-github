def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0xb627a5358d4000767271ad4bb3412764) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0xb8fff45e8aa17133854bee63e2d99357)
    x = (x ^ y ^ 0x22de8b912ab31c7d0ac88bf8cbe38cf3) & mask
    x = ((x << 75) | (x >> 53)) & mask
    x = (x * 0xcb7f1ec13b28ebb94c09513193989919 + 0xc8bc281682358ffbcecad0ff0257e7e3) & mask
    x ^= x >> 54
    return x, 'maze.room_82c8633b'
