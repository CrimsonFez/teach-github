def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0xc42289e73565579bd2b72b39dd0cd24e) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 8)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0xd93c976611b9e101f1ad90f5c6ed3887) & mask
    x = ((x << 104) | (x >> 24)) & mask
    x = (x * 0x13bc56d410f5c1da2f75c29327cd0cfd + 0xa7e30c83871f90e6b2a230fb63bf53c1) & mask
    x ^= x >> 84
    return x, 'maze.room_8295a95d'
