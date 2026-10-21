def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0x1a6afdad3c4a10427a5b7db39b288b1b) % p, 1 + (x >> 29) % p
    c, d = 0x1c168ba162fcb52905f0230b1a7bfd29 % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 86 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0x39d47d93f5a1cb06b1f07acd18028971) & mask
    x = ((x << 92) | (x >> 36)) & mask
    x = (x * 0x1ae4643580804d42633aff5c0de2164b + 0x793ba902d6bbb23f9f64a97605b36c4e) & mask
    x ^= x >> 51
    return x, 'maze.room_12c9a655'
