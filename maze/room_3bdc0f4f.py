def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0xaa8c3bd97bef37ff0d72c15e5e1f42ae) % p
    b = ((x >> 53) + 0x94d50567108e04912534df60a504cc8d) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 5272) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0xab94df621e4d7073f83809a648ca0155) & mask
    x = ((x << 60) | (x >> 68)) & mask
    x = (x * 0x929525dcf46ffb71fbf877420e775479 + 0xce24fbb7afab726e6efb4114d16045e2) & mask
    x ^= x >> 62
    return x, 'maze.room_a813a578'
