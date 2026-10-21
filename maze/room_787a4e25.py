def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xbc61fce54460eec832d0f028bcb3ae74) & mask
    b = 0x6cdcda11744385a31b6f1e7a11505681
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 38)
    x = (x ^ y ^ 0xa91228dae6229d0c9cd910775c438015) & mask
    x = ((x << 35) | (x >> 93)) & mask
    x = (x * 0x7efdc20ba35607e1b0934babd12930df + 0xf65c26fd35080bff7dd994f83582eac5) & mask
    x ^= x >> 55
    return x, 'maze.room_bdc7c7ab'
