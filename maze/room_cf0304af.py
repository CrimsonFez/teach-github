def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0x83dbc54040fec51d32050e0c662ed246) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0xb89f28a67ccb5641206d901857601add) | 1, 40, 1 << 128)) & mask
    x = (x ^ y ^ 0xa63c73abcafa6f397f08843ba94c1ceb) & mask
    x = ((x << 76) | (x >> 52)) & mask
    x = (x * 0x5cb988a9e4d7cd8465f828e61006cf3b + 0xedf04500e1f66c6cc1fb8ee790f6ad68) & mask
    x ^= x >> 74
    return x, 'maze.room_99a33c66'
