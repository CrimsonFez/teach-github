def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0xaeb886f3a89c50d299371908601b1f76) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 9)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0x27b1e503b418e75272ed18b6d5789a95) & mask
    x = ((x << 108) | (x >> 20)) & mask
    x = (x * 0x5d05b43cf6eb27c417c37f13a188346d + 0x2cd7038ca78686764aa5f7d705efd80d) & mask
    x ^= x >> 56
    return x, 'maze.room_82dafd71'
