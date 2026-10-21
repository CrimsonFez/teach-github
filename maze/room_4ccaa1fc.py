def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 4733 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0xdb3372d9eb0a69c394766e92fef56201) % p
    x = (x ^ y ^ 0xb085fd1ac45257c2fe8503793d0628b2) & mask
    x = ((x << 94) | (x >> 34)) & mask
    x = (x * 0x75da6ce424078ec69ea93a6c96e0debf + 0xc6d93570ffd148f5d7848e93242d5838) & mask
    x ^= x >> 67
    return x, 'maze.room_1c6dc0ac'
