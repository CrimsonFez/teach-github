def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0x8b32d2c3562deacb9ad426fc0a8b8da0) % p, 1 + (x >> 29) % p
    c, d = 0xd1ec0f60e0ea050035d9ab45f37b3d2d % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 89 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0x299c79ace4b56ea651f0a10a523a15d7) & mask
    x = ((x << 112) | (x >> 16)) & mask
    x = (x * 0x2eb4a565cf70421ce0a52fe138570863 + 0x2f0b6a20fa2a13affcf19287a26c8759) & mask
    x ^= x >> 65
    return x, 'maze.room_d1579196'
