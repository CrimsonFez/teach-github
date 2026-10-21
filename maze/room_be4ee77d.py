def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0xb3e7b6011c8d5660a3e73a0759534c8d) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0xe248b302c136f79bcba6b2f369a511d7) % p
    y = (a ^ b) + (a * b + 0x5f8216441415af202d8eeb79da90fb02) % p
    x = (x ^ y ^ 0xa08d1092790c2268295aa42b658cfba1) & mask
    x = ((x << 50) | (x >> 78)) & mask
    x = (x * 0xf1531bd76e9f54ced25d5a0aa452cc7 + 0x24381d5b6ce6801a0f23b1d384747ee8) & mask
    x ^= x >> 82
    return x, 'maze.room_0d4420c9'
