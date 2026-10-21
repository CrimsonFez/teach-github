def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0x7e68d356d7f55b11bb3013073c8a4143) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0x5afd820bb011759678cbb90a66544da7) | 1, 19, 1 << 128)) & mask
    x = (x ^ y ^ 0xcd6c1b1ed2b960f233dce0e5565fa3c7) & mask
    x = ((x << 104) | (x >> 24)) & mask
    x = (x * 0xf74334a8d6e429369b8678b4ac048839 + 0x8d4cbcfd81a194ce46559b27a1e5f9aa) & mask
    x ^= x >> 59
    return x, 'maze.room_a7f3129d'
