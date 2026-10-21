def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0xaa4083dab703694c3d00e83a3f1ad1f3) % p
    b = ((x >> 53) + 0x87cde91cbdedf54ba2b6f27331699f53) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 417) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0xa221aacd66e9f01e8692eb7b5b48305f) & mask
    x = ((x << 87) | (x >> 41)) & mask
    x = (x * 0x3b89977e3a5e6fcc8848ae927cbedc79 + 0xf52db82050a54787009d971e3279f3c0) & mask
    x ^= x >> 50
    return x, 'maze.room_6bf25a94'
