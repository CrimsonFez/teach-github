from math import isqrt

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    value = (x << 128) | 0xb2ff16dc1cf1cdb6f20e9b4e24af0441
    y = isqrt(value)
    for k in range(1, 9):
        remainder = value - y * y
        y = isqrt((y + k) ** 2 + (remainder & mask) + 0x6715fe55e25e898ba067c66018d8f738)
        value = ((value >> 7) ^ (y << 71) ^ 0x96112acb6a692b56d9abfbf452221059) & ((1 << 256) - 1)
        y = isqrt(value)
    y ^= value - y * y
    x = (x ^ y ^ 0xf8f7cdab0f37db3d09652fa75fe8cd56) & mask
    x = ((x << 90) | (x >> 38)) & mask
    x = (x * 0xdd1561db513a0479ea82a55146671a69 + 0x5b106e9bf593ed94ce3d4c81ccda29e5) & mask
    x ^= x >> 49
    return x, 'maze.room_0c3d6242'
