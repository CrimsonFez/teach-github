def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0xe1f036c8a468213f74da29fb45573303) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 8914) % scale
    y ^= ((x >> 43) * 0x552641d843284978b0856072ea66664d) & mask
    x = (x ^ y ^ 0x9befe4489ae3402bc69104423fe9e484) & mask
    x = ((x << 59) | (x >> 69)) & mask
    x = (x * 0x580132ce41268c22022a5df2218ce91 + 0xd22fb99b0d4b00cbb4f532150938268e) & mask
    x ^= x >> 54
    return x, 'maze.room_d4d5b8c1'
