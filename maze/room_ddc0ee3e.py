def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0x1f85171414a886e008db71f81c344f44) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0x5e9ba1f32f7871ced4364ca534726631) | 1, 59, 1 << 128)) & mask
    x = (x ^ y ^ 0x8dd18aa302e27291dabe5f60a072857) & mask
    x = ((x << 51) | (x >> 77)) & mask
    x = (x * 0x8e2c3cd866ecc00818af7370f0f8bdad + 0x7c225199e0d13e3d8836b1a69a7a4d5c) & mask
    x ^= x >> 83
    return x, 'maze.room_98074d85'
