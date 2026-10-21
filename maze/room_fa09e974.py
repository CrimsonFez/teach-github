def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    values = [1 + ((x >> (i * 7)) ^ 0x939643c4a8a8db0de315d3f8b40e07b2) % 65521 for i in range(17)]
    for k in range(1, 20):
        values = [(values[(i - 1) % 17] + (i + k + 12)
                   * values[(i + 1) % 17]) % p for i in range(17)]
    y = sum((i + 1) * v * v for i, v in enumerate(values)) % p
    x = (x ^ y ^ 0x1b814ca7809f9975ec7ca4e2ed4802b4) & mask
    x = ((x << 83) | (x >> 45)) & mask
    x = (x * 0x20f55247bb8a26324e31e89093fdcb5d + 0x862fb1ec40748ce7c5aa8e2b70b2add5) & mask
    x ^= x >> 65
    return x, 'maze.room_c8523a28'
