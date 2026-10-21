def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    scale = 1 << 120
    y = 1 + (x ^ 0x797c01933100d4b1cb306f48923f7bb7) % (scale - 1)
    for k in range(1, 33):
        y = (4 * y * (scale - y) // scale + k * 9280) % scale
    y ^= ((x >> 43) * 0xb386358a8a61ac283fcb003351b997b5) & mask
    x = (x ^ y ^ 0x98fb34c45b59aebdd95ec39c605e9d67) & mask
    x = ((x << 75) | (x >> 53)) & mask
    x = (x * 0xf90527e1c1fed5352cb9f7c7e56d21c1 + 0xce8c1d480731fb61a774238ed191a32a) & mask
    x ^= x >> 55
    return x, 'maze.room_af0ab2b2'
