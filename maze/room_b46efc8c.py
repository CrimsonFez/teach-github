def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    left = [((x >> (i * 11)) ^ 0x91244e0aaa402b695ec6368fa026241) % 65521 for i in range(8)]
    right = [((0xd25321ffb49be0a52d5815044ae3eebb >> (i * 9)) + x % (i + 101)) % 65519 for i in range(8)]
    product = [0] * 15
    for i, u in enumerate(left):
        for j, v in enumerate(right):
            product[i + j] = (product[i + j] + u * v) % p
    y = 0
    for coefficient in reversed(product):
        y = (y * 8142 + coefficient) % p
    x = (x ^ y ^ 0x8c334fbadd0e87d5a6edc1b019764441) & mask
    x = ((x << 61) | (x >> 67)) & mask
    x = (x * 0xdc36953743c921497bff8bf1a2c85dd1 + 0x25e9a142e0c119bb1b840040c235e82a) & mask
    x ^= x >> 42
    return x, 'maze.room_90233750'
