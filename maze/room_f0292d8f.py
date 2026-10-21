def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0x1f75de90c2bc32f9ce5b9f2dc62b5d46) % p, 1 + (x >> 29) % p
    c, d = 0xfcff44b67cc44a88742d8b0a37c9b1aa % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 109 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0xedcddab7786c9ab3631a8b2346d1b951) & mask
    x = ((x << 114) | (x >> 14)) & mask
    x = (x * 0xa5a0d9be71ed105afb61efa156dab827 + 0xa83c29ae5eba53489db749e91693beba) & mask
    x ^= x >> 70
    return x, 'maze.room_9a1bcaa5'
