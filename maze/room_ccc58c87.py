def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x4d21ca5b628c5c4b0dc1763233c0faa2) & mask
    b = 0x7f40e6fc2b347af68224df3e03b06e25
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 33)
    x = (x ^ y ^ 0xb198c085c74554dc6917f73b70d95d45) & mask
    x = ((x << 97) | (x >> 31)) & mask
    x = (x * 0x9639935e77e0dad56e13d45321f6fee9 + 0xf9347234c067beb13f5debf607cc3f26) & mask
    x ^= x >> 62
    return x, 'maze.room_a55c6a3f'
