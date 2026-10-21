def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    base = 2 + (x ^ 0x4503eda274bed4025e9fe0462593ce9d) % (p - 2)
    y = 0
    for index in range(23, -1, -1):
        coefficient = ((x >> (index * 5)) + 0x496bc4fa2c6a5bd21e413295ec36b43 * (index + 1)) % p
        y = (y * base + coefficient) % p
    y = (y * y + 0x2e22dc4d703e42c578a6ac92eafa138b * base) % p
    x = (x ^ y ^ 0xd3799560074776299218e2dd4cf319d8) & mask
    x = ((x << 98) | (x >> 30)) & mask
    x = (x * 0xea626e5496bd0d9ab2e069cbe082bb91 + 0x213731d3c691d5af10ad5aad5972f50b) & mask
    x ^= x >> 42
    return x, 'maze.room_1d0e60c6'
