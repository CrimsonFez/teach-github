def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0xf309063567dffdd4e93a652639224509) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0x32f2e264ccdcb8c3e704386e27d33932 * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0xd4bf76690a0cbb9fb4b502d30b744bbf * base) % p
    x = (x ^ y ^ 0xb27024144af53f02849220bb609b897) & mask
    x = ((x << 39) | (x >> 89)) & mask
    x = (x * 0xfd33f43279a737362776cb307c135dbf + 0x36fc0cafe07013ec06349e31453f81d9) & mask
    x ^= x >> 63
    return x, 'maze.room_29233cfb'
