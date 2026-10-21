def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0x5c657922a9f361f2a6bc14fe670d27f0) % p
    b = ((x >> 53) + 0x74ebedb079957d9930a15d6fc15c912b) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 15) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0xdd2801e460a2360c6f833d4a6551bedc) & mask
    x = ((x << 109) | (x >> 19)) & mask
    x = (x * 0x1b6bfa63e8c9bbdad32fff2389f7d2dd + 0xc3474c71ee75eec1cfdedfcfc1cb22f0) & mask
    x ^= x >> 59
    return x, 'maze.room_72a1df59'
