def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0x373129ef2964e9a461444ee50c0c6b7) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 6395) % scale
    y ^= ((x >> 43) * 0xe58b5aad7a75f64439672530ff809b70) & mask
    x = (x ^ y ^ 0x438cd192d9607c1198829e284d341a25) & mask
    x = ((x << 106) | (x >> 22)) & mask
    x = (x * 0xc04c9291f9ee7ea0a2a77c1d6fafc269 + 0x100ca7edc05383152241c7cc638104fb) & mask
    x ^= x >> 57
    return x, 'maze.room_eeecf511'
