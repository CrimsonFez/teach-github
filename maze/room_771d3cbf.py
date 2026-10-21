def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0xf453615b5d277e9d72e635d89f6b759) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 6)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0xd4fba231d8a4f8573f5d97c9f64bb2d4) & mask
    x = ((x << 81) | (x >> 47)) & mask
    x = (x * 0x80bf66534c7572e78042f78cb9d9c4a1 + 0x646808eaa0e4598730ef858df1670fd1) & mask
    x ^= x >> 64
    return x, 'maze.room_ec551ddb'
