def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0xdcda69f839fa93188c6f8124b9b931fd) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0xfc878bbbc9cb6dd555405497ad6545b3) % p
    y = (a ^ b) + (a * b + 0x8f3ad0b865f3bc6b68076f6716f78260) % p
    x = (x ^ y ^ 0x4b4154209874bdc42853a31e95419cae) & mask
    x = ((x << 41) | (x >> 87)) & mask
    x = (x * 0x5d6b7745a57bd61eee320bd226843f33 + 0x96217ed3f60e47f075fae6c75a085cd9) & mask
    x ^= x >> 81
    return x, 'maze.room_f0580cea'
