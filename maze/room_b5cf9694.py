def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0xc41982c733bd210af087470e50908465) % p, 1 + (x >> 29) % p
    c, d = 0x2ca610cfe3771f46cc4d430d672e266b % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 90 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0x75e87cb4387e6390731e5e1547f97898) & mask
    x = ((x << 96) | (x >> 32)) & mask
    x = (x * 0x224361d7fba25492f737fd56cbb44741 + 0x2b24770ff811992e2ecea2e7a8cc9080) & mask
    x ^= x >> 68
    return x, 'maze.room_2a98d4ba'
