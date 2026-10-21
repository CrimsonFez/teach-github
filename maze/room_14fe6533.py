def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0xa791890333251a9ed1eec9e2b665e8a) % p, 1 + (x >> 29) % p
    c, d = 0x3b305e2a5b3582dbb55a3b2fd9a20a4c % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 117 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0xe4e4eb92557335612585b1ca0f3180b1) & mask
    x = ((x << 107) | (x >> 21)) & mask
    x = (x * 0x90c36cac434a485ba285cf65ec6c543 + 0xce117aa6bb5bfeee9a75c7b6a8f84652) & mask
    x ^= x >> 62
    return x, 'maze.room_4896da03'
