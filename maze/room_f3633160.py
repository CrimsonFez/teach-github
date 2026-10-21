def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0xf30bca69c6b528f719c939eadde3cacb) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0x11b644297ab3edabdf81bc8465f2138d) % p
    y = (a ^ b) + (a * b + 0xb0520d833911fddd8650c79f044843f1) % p
    x = (x ^ y ^ 0x704a6e966edaae4ab0ebae7d84cbf29) & mask
    x = ((x << 14) | (x >> 114)) & mask
    x = (x * 0x7ba832f689d8a72518dc67724899042d + 0xf5fe4a9215c1a09d25c8777eb7fc9877) & mask
    x ^= x >> 68
    return x, 'maze.room_abfb2901'
