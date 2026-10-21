def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0xb62823852c3aaebcc5299c320e0f172d) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0x643be804e57baca14b612f8892c2739d * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0x7e8c2bb1d72c77051bffe445e405ec4e * base) % p
    x = (x ^ y ^ 0xb7e910e2976565e12a49774017989480) & mask
    x = ((x << 31) | (x >> 97)) & mask
    x = (x * 0x9f8a3d349db19e1b4a0c12af7f48f1a3 + 0xb80edc0197f3923e6e68ffe3981534d0) & mask
    x ^= x >> 51
    return x, 'maze.room_2ef43d89'
