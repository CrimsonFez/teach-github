def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 4552 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0x358c7e220749a684787f69a089263c36) % p
    x = (x ^ y ^ 0x29076a11ba70077009c2d7561a75b669) & mask
    x = ((x << 42) | (x >> 86)) & mask
    x = (x * 0x62391ff7542785de27f3e5c87a2e6cfb + 0x9a4ba7729df5bee10daca74753d90b38) & mask
    x ^= x >> 50
    return x, 'maze.room_f1bdd8a3'
