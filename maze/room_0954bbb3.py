def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0x8a0620ee403762774b0ca3d7b0806736) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0xecdcc5da67b6a2e397fd8c35f8400897)
    x = (x ^ y ^ 0x52f2b4ab7b3289c8bbfc1970fe30b491) & mask
    x = ((x << 100) | (x >> 28)) & mask
    x = (x * 0x764f0d1559b1aea5161482c34f1bebf9 + 0x4585ce3c50ea35a76c1231b4c50714ce) & mask
    x ^= x >> 70
    return x, 'maze.room_ccc58c87'
