def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x4a5d2cb59b3ba7d7230818c4ec66ad39) | 1
    b = ((x >> 37) ^ 0xacc46e86fac8b597f5f66e6ec479d98c) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0x7eef713da49a440b9ba8305f6b80ea6d + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0x775e30ef84b93711bd1b5d596be7b606) & mask
    x = ((x << 57) | (x >> 71)) & mask
    x = (x * 0xd0eb2c98bb8f88cc2d9cd9b055e5545 + 0x99a32f1c0838869d04cab9803739b5da) & mask
    x ^= x >> 64
    return x, 'maze.room_f886811c'
