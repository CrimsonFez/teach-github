def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0xeda5ba6bd1fec536f3fdfd092f04599f) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0x24cb7bef992a67680a9804cee84e87ea) | 1, 59, 1 << 128)) & mask
    x = (x ^ y ^ 0x500d4a8cb1e08f5c2bb53137359f5a61) & mask
    x = ((x << 108) | (x >> 20)) & mask
    x = (x * 0xf7efe4b8447a463d3268ac2f755e9867 + 0xdcd750c3ff900b8ffb16b67f6df28576) & mask
    x ^= x >> 64
    return x, 'maze.room_f7607f6c'
