def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xb536b07b63a0da404839bec3b663094d) | 1
    b = ((x >> 37) ^ 0xbfbabe1b0c6400ae7a2d26be0b0055d8) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0xbe347901207157a7024bc2d918eb0401 + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0x4ac6822303e82065b263d5cd04d98d81) & mask
    x = ((x << 106) | (x >> 22)) & mask
    x = (x * 0x1c7146d91e9abf1be3de1959dd4d2bbd + 0xcc812e1e283823e9c7d687bae420aec7) & mask
    x ^= x >> 38
    return x, 'maze.room_5a4600f7'
