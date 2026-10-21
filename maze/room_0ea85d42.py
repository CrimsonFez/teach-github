def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0xf0f86a7d4925b7926d9d57c68f9b19ed) % p
    b = ((x >> 53) + 0x5114c0f03cc546d08b687b9b1e9f8bc0) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 2113) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0x31fa26e09b330495645b7e7cb2088203) & mask
    x = ((x << 100) | (x >> 28)) & mask
    x = (x * 0xd87a00f5f27a88cc9d540de55428eb59 + 0x7407d28dd66b5ad6e14d4777ba4a76e2) & mask
    x ^= x >> 55
    return x, 'maze.room_771d3cbf'
