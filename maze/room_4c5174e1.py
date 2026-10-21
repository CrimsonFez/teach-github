def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = (x ^ 0x6d731a3b796ead367b1a88f903222c2e) % p, 1 + (x >> 29) % p
    c, d = 0xb97acb0eb33069ddac4ceb927c048d8e % p, 1 + (x >> 61) % p
    e, f, g, h = 1, 0, 0, 1
    exponent = 111 + x % 1024
    while exponent:
        if exponent & 1:
            e, f, g, h = ((e*a + f*c) % p, (e*b + f*d) % p,
                          (g*a + h*c) % p, (g*b + h*d) % p)
        a, b, c, d = ((a*a + b*c) % p, (a*b + b*d) % p,
                      (c*a + d*c) % p, (c*b + d*d) % p)
        exponent >>= 1
    y = (e + 3*f + 5*g + 7*h) % p
    x = (x ^ y ^ 0xd81c66a332ef428cb3c5d516646cf01f) & mask
    x = ((x << 53) | (x >> 75)) & mask
    x = (x * 0x24de284371a0deef116ef07cc3641b6b + 0xeea161a33967cdcbaef0a03979a0c25a) & mask
    x ^= x >> 83
    return x, 'maze.room_1f91a235'
