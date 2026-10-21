def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0x6cc76fca6328dc400c84d6bf41ffebea) % p
    b = ((x >> 53) + 0xbcf815b402c116a5f3ff1ee2257c69f5) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 852) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0x759c68d8a119e3ed472af6ae4e5ccac0) & mask
    x = ((x << 57) | (x >> 71)) & mask
    x = (x * 0xfc8463285467ddd792d29e7100a4ab39 + 0x9bf3b4444a0a45edf56487d3e9185730) & mask
    x ^= x >> 40
    return x, 'maze.room_6c9e5aed'
