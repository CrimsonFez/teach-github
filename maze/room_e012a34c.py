def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x5be202f93a8b4a875e170f1daf03c054) | 1
    b = ((x >> 37) ^ 0x25dde013af5c4d47db54dd5aa2f7b724) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0x5b57aa43577d5f20a9892f4623afa389 + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0x266a0c4b7e1f401b8a7ef8955456cea) & mask
    x = ((x << 77) | (x >> 51)) & mask
    x = (x * 0x8a897d9aea0d6d285a492a579357fcbd + 0x1b22be6762045414c8d7ebd9b4d0bdfb) & mask
    x ^= x >> 70
    return x, 'maze.room_c5bbb79d'
