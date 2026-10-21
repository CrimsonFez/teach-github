def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0x4c1feb66e93d497ebda6d21f02f19ce8) % 65521 for i in range(8)]
    right = [((0xbd198642c41bfde640dc12486fce2b48 >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 9291 + coefficient) % p
    x = (x ^ y ^ 0xf5664e473a5231c4faf4daadd12d6243) & mask
    x = ((x << 78) | (x >> 50)) & mask
    x = (x * 0x8fc08466dfb40972e97956143025ad67 + 0xd73d0a674ace31b3e264573433ca67a9) & mask
    x ^= x >> 54
    return x, 'maze.room_60161d18'
