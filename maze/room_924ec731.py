def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0x5dbcaf1a91387a98df69ee149d2916b6) % 65521 for i in range(8)]
    right = [((0x4950396967674f7d7c85d7fabe6487a2 >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 475 + coefficient) % p
    x = (x ^ y ^ 0xafe9d436977e978ef8b2f3c2881f9be6) & mask
    x = ((x << 112) | (x >> 16)) & mask
    x = (x * 0xb3bba91d61cc11eef10e161c205bc245 + 0x7e4c8860b6e4adbde87b8432374de9db) & mask
    x ^= x >> 39
    return x, 'maze.room_d7960a84'
