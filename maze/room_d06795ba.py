def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0xb9af72a49bf76fb4aaceafe33508e4c6) % 65521 for i in range(8)]
    right = [((0xede5903eaed7492f1beeb943cf8fff98 >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 10000 + coefficient) % p
    x = (x ^ y ^ 0x888b38fd6cbea530a18fea41cf495341) & mask
    x = ((x << 101) | (x >> 27)) & mask
    x = (x * 0x15ebde2e7cd6333760878a5f7d5e6149 + 0x952fd48fbacc8cb532de6a15b5cdaf46) & mask
    x ^= x >> 85
    return x, 'maze.room_1f49565a'
