def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0xae9a16d16e4918bb691fa8882a3fbfd4) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0x223da596c681c69a79ffc6ce85a9daa9) % p
    y = (a ^ b) + (a * b + 0x162683651b0c352162bcf331d8b3ae75) % p
    x = (x ^ y ^ 0x4f94becab2dcc169a9e545a7f3be0d3) & mask
    x = ((x << 29) | (x >> 99)) & mask
    x = (x * 0x2167e18a29a001fa09a12c10352f5493 + 0x48b6ff7486123d7a1b93709590b8bc1f) & mask
    x ^= x >> 71
    return x, 'maze.room_fe3cc607'
