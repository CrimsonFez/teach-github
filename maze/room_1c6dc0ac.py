def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0xc3f9dc8268a6b7feb7a8369fc4bc8874) % p, 1 + (x >> 29) % p
    c, d = 0x82c6fed87c140c53aeb8d8468648efe % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 125 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0xda8ac25397714d17edbd1edb6653a6f8) & mask
    x = ((x << 56) | (x >> 72)) & mask
    x = (x * 0xaba0a7c246e93598adaf66a22bbd14cf + 0x39013a996ddfc6c87c423fc0f306c9ef) & mask
    x ^= x >> 81
    return x, 'maze.room_13906765'
