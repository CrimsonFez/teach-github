def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0xb177901eda66fd7fee8e16983b385180) % p, 1 + (x >> 29) % p
    c, d = 0x78db10cdd916a1f0343b37d3f85e4e3e % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 73 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0xb5333fa0d981586233f61ef57146f8f5) & mask
    x = ((x << 42) | (x >> 86)) & mask
    x = (x * 0x330ec35e67ef3d9945549e82f1ed4e03 + 0x5f2807a3b9144b34e40b34f341939067) & mask
    x ^= x >> 79
    return x, 'maze.room_459a3ca4'
