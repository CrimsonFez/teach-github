def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0x826627e47d5f2c67fe4e947bdfce6bfd) % p
    b = ((x >> 53) + 0x56250d607968ec2648b09bea99741152) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 2457) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0x18fd7d1e334649d0d74c72ea416e0c2d) & mask
    x = ((x << 43) | (x >> 85)) & mask
    x = (x * 0x98e91de23c7f6a44e26c26feebec0cf7 + 0xc705c5761c85378eec7583f3670387ad) & mask
    x ^= x >> 71
    return x, 'maze.room_fa09e974'
