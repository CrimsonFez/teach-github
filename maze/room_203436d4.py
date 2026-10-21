def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x391abb3b2540014c9f3c0b97684333cf) | 1
    b = ((x >> 37) ^ 0xd103a826d8d5490efe92ec2d7914de1e) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0x262b254182cf54dc1d62a79706bdda27 + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0xecb94d7b4224c2bd86116bb6449bf1e6) & mask
    x = ((x << 96) | (x >> 32)) & mask
    x = (x * 0x25dbfe4530dde6f54deb60554bfa0e75 + 0xcfc5474c63699182f33c77691640ad0d) & mask
    x ^= x >> 59
    return x, 'maze.room_69f97743'
