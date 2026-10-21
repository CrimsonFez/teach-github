def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 3932 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0xbd2a0c64169eafdb0022879f182c8f3f) % p
    x = (x ^ y ^ 0xaea4cf76f03a0279235d74d6cc84ddf1) & mask
    x = ((x << 109) | (x >> 19)) & mask
    x = (x * 0x3b44e39f01a513b1abbf52e3e560ae49 + 0x9bf0ecde8953e5bdb025e3a584d7e01e) & mask
    x ^= x >> 65
    return x, 'maze.room_4c5174e1'
