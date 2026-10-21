def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 5951 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0x6e310badf864c0cc8cb12235ee6c9d73) % p
    x = (x ^ y ^ 0x347dafed42180e7602cdb2d63aa5f730) & mask
    x = ((x << 57) | (x >> 71)) & mask
    x = (x * 0x28158651d066253971e9908ebd4ceda3 + 0xd177c98692166fd4c4ab620d3012eb29) & mask
    x ^= x >> 59
    return x, 'maze.room_176230a5'
