def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0x59c068c9c9b1798c7099de43707a86a3) % 65521 for i in range(8)]
    right = [((0xde66413eeb737e9e6cfbdc3343f0541 >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 3006 + coefficient) % p
    x = (x ^ y ^ 0x425551546721b21510b65e8370dfeffa) & mask
    x = ((x << 56) | (x >> 72)) & mask
    x = (x * 0xe53d1060f44f98d1f9b68a97b1a8220f + 0xaf53f3198fb9e806b3faf05eb91d8c69) & mask
    x ^= x >> 47
    return x, 'maze.room_56305c37'
