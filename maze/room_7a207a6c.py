def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    moduli = (65521, 65519, 65497)
    product = moduli[0] * moduli[1] * moduli[2]
    y = 0
    for index, modulus in enumerate(moduli):
        residue = ((x >> (index * 31)) ^ 0xe44b49579c919d1ad37d91f206efb66b) % modulus
        partial = product // modulus
        y += residue * partial * pow(partial, -1, modulus)
    y = (y % product) ^ ((x // product) * 0xa6916d8762f518d4fe0b7b436f5f3d04)
    x = (x ^ y ^ 0xe2d5ed393a39685ab954204f0d30a89b) & mask
    x = ((x << 72) | (x >> 56)) & mask
    x = (x * 0xcf9b7a38fdb85aa11aacf051c28a99af + 0x80045347d4401385647886ff4dfa752c) & mask
    x ^= x >> 49
    return x, 'maze.room_0e526a38'
