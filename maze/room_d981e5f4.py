def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 1859 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0x94812517bc71c7cdf54e0ea5ee1e0512) % p
    x = (x ^ y ^ 0x954f4d7cd408a73cc869b90c4438a629) & mask
    x = ((x << 64) | (x >> 64)) & mask
    x = (x * 0x75f0be5bcb724a36a67097fe1d552845 + 0xafb561040ffec49038ea7a3694fde111) & mask
    x ^= x >> 63
    return x, 'maze.room_bdfe6ef4'
