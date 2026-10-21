def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0x8f55ece9cac9f28a4dafe8833534684c) % p
    b = ((x >> 53) + 0x48d56761d3135d81a27c8e35f5f08090) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 5831) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0x6c124446d138a59ad975fb993fe962b6) & mask
    x = ((x << 14) | (x >> 114)) & mask
    x = (x * 0xce609ac50c60a19022f50a1be35cdd33 + 0xa34302f49182a772f0315df07f64a7c0) & mask
    x ^= x >> 76
    return x, 'maze.room_3dab2912'
