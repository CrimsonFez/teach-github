def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x335cd7d830729288c1084960ef49497d) | 1
    b = ((x >> 37) ^ 0x34e8a3bf8defdd3531f2507cd915c952) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0x2726429519c88864517e78ace395c231 + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0xc22aaa5642b40ed3e47715b199cb4783) & mask
    x = ((x << 29) | (x >> 99)) & mask
    x = (x * 0xb3faeef2fabc8320b27e0acd60306acb + 0xdca01a8a46e30a5a87e3c7cb829e19ec) & mask
    x ^= x >> 53
    return x, 'maze.room_f777ac75'
