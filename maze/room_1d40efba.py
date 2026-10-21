def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 3131 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0x3b6d6c3c6d207eaf4067156dded5ca06) % p
    x = (x ^ y ^ 0xfa0767a21109605d731b837d63e57da6) & mask
    x = ((x << 52) | (x >> 76)) & mask
    x = (x * 0xffdce32a57b3ad083b3aa1ee856c7247 + 0xfbc8ca3c664ae30ec122a083053f25ac) & mask
    x ^= x >> 45
    return x, 'maze.room_14fe6533'
