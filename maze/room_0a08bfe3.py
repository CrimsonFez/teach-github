def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0xba326c31e1a19e3794f6fb3a22ba4bcd) % p
    b = ((x >> 53) + 0x8ef23584c8d3c24ae944d561e0f3cdcf) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 5583) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0x198dd97da63c3844efa93c96b42655ea) & mask
    x = ((x << 30) | (x >> 98)) & mask
    x = (x * 0xdcd473020d14b6ef75b0b98621f404d3 + 0x387f35b2249963d69134001f98787317) & mask
    x ^= x >> 82
    return x, 'maze.room_90d49034'
