def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0x10e18b910a176a0fe1b5c7fb813fb4b) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0xcb17eeeb10199233a044376c5e9f3300 * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0x6806c64efb90e976780130bde8c8dea9 * base) % p
    x = (x ^ y ^ 0x148d41ae56f2ea249d186b9c19f1954f) & mask
    x = ((x << 70) | (x >> 58)) & mask
    x = (x * 0x9b67ac93374f58376ebcb7ae07e98cfd + 0x29ca3099f68a9d135ec729a64d9cefa0) & mask
    x ^= x >> 37
    return x, 'maze.room_4ad94c3f'
