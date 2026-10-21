def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xafe773558dda74160cda7e16fc6b525a) | 1
    b = ((x >> 37) ^ 0xfaac3a484798d19fc9c5f17e77277fc3) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0xad7167fabfdc34bc2bc1e73a37612609 + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0x3857f276ecb018cdfc4236ed414654b3) & mask
    x = ((x << 55) | (x >> 73)) & mask
    x = (x * 0xbf52550c1826d217ca59d2120213baab + 0x8b3cc3d36343e215e8132753760b4f6d) & mask
    x ^= x >> 62
    return x, 'maze.room_15c0300f'
