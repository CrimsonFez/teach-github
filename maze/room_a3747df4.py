def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 1727 + x % 100000
    a, b = 0, 1
    for bit in bin(n)[2:]:
        c = a * (2 * b - a) % p
        d = (a * a + b * b) % p
        a, b = (d, (c + d) % p) if bit == '1' else (c, d)
    y = (a + b * 0xd1c1a00530db275550c98dc502f99b0f) % p
    x = (x ^ y ^ 0x9688430680a0cb527faadfc78928d9e1) & mask
    x = ((x << 80) | (x >> 48)) & mask
    x = (x * 0xe5ff108ed9a76d39e5af89549a0c7363 + 0x63b64f701ea77865f36a89f907a21630) & mask
    x ^= x >> 41
    return x, 'maze.room_0d601881'
