def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    a = (x ^ 0xb48b9d1069c6a07605b1d0e5aa08909c) & mask
    b = 0x53669238cc091faa445eb52bee0403db
    y = 0
    for _ in range(128):
        if b & 1:
            y ^= a
        carry = a >> 127
        a = ((a << 1) & mask) ^ (0x87 if carry else 0)
        b >>= 1
    y ^= (x >> 23)
    x = (x ^ y ^ 0x2db250105eb75ce7bbdc09367f54878b) & mask
    x = ((x << 15) | (x >> 113)) & mask
    x = (x * 0xe8475883c3dab08fde0c77e258eab7c1 + 0xff043201a7d112224615913f3d6e5d20) & mask
    x ^= x >> 63
    return x, 'maze.room_c645c1ce'
