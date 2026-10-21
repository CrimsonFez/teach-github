def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0x95fdf8013d379af4cc8631159feb8290) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 6)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0x4459352aaebf8b4e9e2099e07a2ac67) & mask
    x = ((x << 106) | (x >> 22)) & mask
    x = (x * 0xd52a733ebbd24180773b0da2ab60463 + 0xa7da783317a84821a84c236c9313eb95) & mask
    x ^= x >> 72
    return x, 'maze.room_4cd6bd58'
