def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0x7b177889a5cc4754251f69167ffda307) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0xe3054b54c615d65b6ea9bf8b6c5ca3aa) % p
    y = (a ^ b) + (a * b + 0x583c49e211fcf19415e3823700ec363e) % p
    x = (x ^ y ^ 0x9ae93f9074ac78a5101b04448ab64338) & mask
    x = ((x << 112) | (x >> 16)) & mask
    x = (x * 0xe86a1126b2a7b5c03cd52827c32a8ea5 + 0x784e3bf668f07e8390da80071369d804) & mask
    x ^= x >> 87
    return x, 'maze.room_bf31dc67'
