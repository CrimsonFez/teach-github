def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0xdb27cd63acc709600afe6d568e3c9744) % 65521 for i in range(8)]
    right = [((0x69dfa8e7cc550b201abfc0ca1ebffa5 >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 9151 + coefficient) % p
    x = (x ^ y ^ 0x1cd5b72e43194da30a15a6c6de0991f0) & mask
    x = ((x << 76) | (x >> 52)) & mask
    x = (x * 0xc1e864ec43196d9bca1d5d786807c5b1 + 0x2a87806dc5d461a8ba87ef8b0a745eb2) & mask
    x ^= x >> 37
    return x, 'maze.room_0a08bfe3'
