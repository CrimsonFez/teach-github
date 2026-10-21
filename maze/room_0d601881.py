def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0x87d75d31fa99b13bba28ff848ee99221) % p, 1 + (x >> 29) % p
    c, d = 0x823e3ea3ef779806376729073c8402bf % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 52 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0xcb77cd247d066a11707bd182a229dc9c) & mask
    x = ((x << 114) | (x >> 14)) & mask
    x = (x * 0xcbffe57e1128039703ed2cd11006203f + 0xb6480c525ec095a7290a9fae1c3897ce) & mask
    x ^= x >> 69
    return x, 'maze.room_980fe9c6'
