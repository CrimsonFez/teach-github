def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0x71f6e115e5b55544ee951c349ed48f70) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 7780) % scale
    y ^= ((x >> 43) * 0xc55bc6fe5c6f357b1da93f67bbc27da6) & mask
    x = (x ^ y ^ 0x1bc35d40ff8678f9a888e3f813798b10) & mask
    x = ((x << 78) | (x >> 50)) & mask
    x = (x * 0xd3d142b02bd5b47cc7d11ce731fe2abb + 0xe043a722ffa80181d6162adac3766903) & mask
    x ^= x >> 66
    return x, 'maze.room_c30de89d'
