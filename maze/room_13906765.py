def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0x7a9f07850fb1fc07f12a7befdde864da) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0x7926a12c3b147f3dcccbc64ba0aae667 * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0xb5606ab0a729ad48e150c68a4ef85af2 * base) % p
    x = (x ^ y ^ 0x37b239837d70759028c6d0622bb7f943) & mask
    x = ((x << 77) | (x >> 51)) & mask
    x = (x * 0x6b401141cebf6c7056b69c5d8f401aa5 + 0x63d55fb69bb1aadeb8e7611476637318) & mask
    x ^= x >> 57
    return x, 'maze.room_723c7cb0'
