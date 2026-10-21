def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x6ca476212b0c847015b0e02807d057d) | 1
    b = ((x >> 37) ^ 0x2514fe7a04bd21498daecbbd31a3403) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0xff488627deb2dba7d2966f24bc459b61 + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0xfddc7870b31d5906d8930bef3ad4ca73) & mask
    x = ((x << 30) | (x >> 98)) & mask
    x = (x * 0x9f942c698bd9703e6e1f791a3c0a88f5 + 0xfecbe628a3dccea336625f2b8c302868) & mask
    x ^= x >> 56
    return x, 'maze.room_ec0bd3b5'
