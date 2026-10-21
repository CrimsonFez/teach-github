def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0xeabd43361b66dcdc76577e345a88dc86) % 65521 for i in range(8)]
    right = [((0x99d8da505babb9a0ec657ffad61615dc >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 6372 + coefficient) % p
    x = (x ^ y ^ 0x2dc75d1477ad91d325bfa7a407f578a) & mask
    x = ((x << 18) | (x >> 110)) & mask
    x = (x * 0xff4fed77e1c2b394333e1a22e9415a89 + 0x3e3baebe482c256d22588558b5696648) & mask
    x ^= x >> 38
    return x, 'maze.room_0ea85d42'
