def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0x9d53de0d6ce4bbf60ce11040bb5564e) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0xcda68246239255d08cd77a43c43b5172) | 1, 10, 1 << 128)) & mask
    x = (x ^ y ^ 0xb297baccfba450dec912463578f178dc) & mask
    x = ((x << 46) | (x >> 82)) & mask
    x = (x * 0x15ac7dae01a1905c939b4f1324eacbd9 + 0xe2df45ef0f63f2c9e34d49ee88312e7) & mask
    x ^= x >> 48
    return x, 'maze.room_d9db42a7'
