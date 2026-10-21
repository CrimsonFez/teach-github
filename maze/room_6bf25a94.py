def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0xdb974a4a576dc5b15bc6c812f9970616) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 6)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0x97e7aec90cd4785e4cf5b144bb7ee1db) & mask
    x = ((x << 31) | (x >> 97)) & mask
    x = (x * 0x40d8074a73de7d17f768546e9a9d5ab5 + 0x2f3208a2cdc4430d8acfe9ecb9539cd) & mask
    x ^= x >> 65
    return x, 'maze.room_692f463e'
