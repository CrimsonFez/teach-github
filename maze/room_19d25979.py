def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0xb0b7e076f0fee3b3cbe2f9d892e692db) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0x455eda5c5ac7c6ad080f3af2a3cd45e3) % p
    y = (a ^ b) + (a * b + 0xa6602cb11fb7976e5735640006abcdff) % p
    x = (x ^ y ^ 0xef812daaf417beb93b34b8a9e94aea61) & mask
    x = ((x << 96) | (x >> 32)) & mask
    x = (x * 0xb3ea6ed08a90fc2bf1cb9b87c9c9ab33 + 0xfef9ac67342388cdb63c09069c98bcd8) & mask
    x ^= x >> 57
    return x, 'maze.room_92c78674'
