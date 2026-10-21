def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0xc315d5401784a16cf65c730c72074017) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 6)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0xfbe702914db315add3f0af31bb12488c) & mask
    x = ((x << 106) | (x >> 22)) & mask
    x = (x * 0xbed1f47b9f6b9cc99fbd53d5c410a263 + 0x38aae0c139b9b58f65c5f85167dc1ee4) & mask
    x ^= x >> 44
    return x, 'maze.room_3b4bd8c9'
