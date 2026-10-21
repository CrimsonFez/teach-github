def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a, b = 1, (x ^ 0x31c35d039cea273de5b1f56dc9342dbd) % p
    coefficient = 2 + (x >> 61) % 31
    for k in range(1, 30):
        a, b = b, (a + coefficient * b + k * 0x36d3afbc10337db09e7434dfd6283135) % p
    y = (a ^ b) + (a * b + 0xaf20b6cbb49402649d02aba1ecb89c59) % p
    x = (x ^ y ^ 0xf7bcbe55095faa83c96ce6addcb41e7b) & mask
    x = ((x << 37) | (x >> 91)) & mask
    x = (x * 0x7e84fb89832f6736082d8a778372ba1b + 0xdb70f733f870e9251c5108a9306fccf1) & mask
    x ^= x >> 61
    return x, None
