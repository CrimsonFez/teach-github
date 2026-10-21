from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0xf01a107eaa7e529ee168ab5dea50b416) % 24
    base = 2 + ((x >> 17) ^ 0x72d586005aa96820d907f2b6f164e84c) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 820
    x = (x ^ y ^ 0xa67ad99de4304bcc2532bba20cd83240) & mask
    x = ((x << 88) | (x >> 40)) & mask
    x = (x * 0x841a704aaf090468d4f294141087369 + 0x24b95c8ded1172f71318a5b05358de72) & mask
    x ^= x >> 84
    return x, 'maze.room_db61e92e'
