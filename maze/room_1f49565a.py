def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    a = (x ^ 0xfdcea36c0acc2f92ff180b894298cfc3) % p
    b = ((x >> 53) + 0x455583d9a0f3b95cd657927ba9b996aa) % p
    for k in range(1, 19):
        a, b = ((a*a - b*b + k) % p,
                (2*a*b + k*k + 8008) % p)
    y = (a*a + b*b + a) % p
    x = (x ^ y ^ 0xa8ed40b83f95f84dae30fd91911715de) & mask
    x = ((x << 101) | (x >> 27)) & mask
    x = (x * 0x7bdf92f85855930fd9279adc73d8dac9 + 0x9a0ab62278ad23cff313de630d6d2831) & mask
    x ^= x >> 63
    return x, 'maze.room_5fe37e1e'
