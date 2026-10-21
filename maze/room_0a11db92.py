def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0x8525a7fd8db454ffb6d7c2eaf07f8da6) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0xc83a3e9298442e70b458044948859119) % p
    y = (a ^ b) + (a * b + 0xe2588624620f9639fec4164e585f832d) % p
    x = (x ^ y ^ 0xb754c4c5b7a0306dd29a0fa68a797139) & mask
    x = ((x << 20) | (x >> 108)) & mask
    x = (x * 0x4fdef178173614d79f1764cbeb7f8c1f + 0x426c600f5d266d57855679dcbca6e335) & mask
    x ^= x >> 83
    return x, 'maze.room_19e7842f'
