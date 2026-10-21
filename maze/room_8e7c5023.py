def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0x743fb27e4ed204d57d5e302deaa6def4) | 1
    b = ((x >> 37) ^ 0x46756c7014fe6f7aba0b2562db5db0d4) | 1
    y = 0
    while b:
        quotient, remainder = divmod(a, b)
        y = (y * 0x7528fe4b49b4c7b7926bc3976f908d85 + quotient) & mask
        a, b = b, remainder
    y ^= a
    x = (x ^ y ^ 0xc165641a0939972581915d352dd0381c) & mask
    x = ((x << 68) | (x >> 60)) & mask
    x = (x * 0xdf2a5808d6a056aeffd38c649ab9237f + 0x2f5ab4927439db4349d0764e538ed633) & mask
    x ^= x >> 70
    return x, 'maze.room_3e7c08b4'
