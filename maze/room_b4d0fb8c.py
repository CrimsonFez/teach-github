def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0xafbd9c38cd18212e0dcd0ee6da0f0105) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0xffb3114029edd55a83ca99db9698e140) | 1, 57, 1 << 128)) & mask
    x = (x ^ y ^ 0xfcca3293605e7eff85cf36e1b08c7ed7) & mask
    x = ((x << 97) | (x >> 31)) & mask
    x = (x * 0x44b16ec891693ee34903039b105ce283 + 0xb87c1fdaaa4b9f46150c311a7188904f) & mask
    x ^= x >> 69
    return x, 'maze.room_72eece71'
