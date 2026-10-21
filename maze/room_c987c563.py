def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0xe6cb849afb7ea7a4fbdf05c27d3c46c5) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0xfce151d44be993124f7853a91fd5c920) % p
    y = (a ^ b) + (a * b + 0x88ac2c7aee30fc2bb84438b028133bfd) % p
    x = (x ^ y ^ 0x7e62f5dc8628300515b975346a50d248) & mask
    x = ((x << 87) | (x >> 41)) & mask
    x = (x * 0x60f05b3aa6f1572b89fb8eaf889430b7 + 0x3d2b46834a1f79e1a2a118a9a2e83355) & mask
    x ^= x >> 64
    return x, 'maze.room_549e2cf1'
