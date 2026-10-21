def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0x505245892a84ccfd1b2b2dd48c5151a7) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0x5628bd1a43423514dbac807ce228124b)
    x = (x ^ y ^ 0x7172116d580e88359b2cc1e6bf610488) & mask
    x = ((x << 31) | (x >> 97)) & mask
    x = (x * 0x46594a36523b86791a5fcb930ae2286f + 0x51339c72c20a7b2c217743e120319da1) & mask
    x ^= x >> 42
    return x, 'maze.room_e1e0c817'
