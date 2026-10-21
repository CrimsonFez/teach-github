def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0xcda1e3874528598783df05b243497a7c) % p, 1 + (x >> 29) % p
    c, d = 0x1a7988de94a0d47150122c03d4a6bc8d % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 108 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0xc4a4a9f04cba9788bdc40f973fb30a0b) & mask
    x = ((x << 89) | (x >> 39)) & mask
    x = (x * 0xb501549dbca655503f11b6a7c9320d97 + 0x96953d95f8e107448a4f53953e009fd4) & mask
    x ^= x >> 51
    return x, 'maze.room_d11f179c'
