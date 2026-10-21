from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0x71a3bc6d980f3455a7a95c318b194dc4) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0x43ced08b6cb13b04fb95e28d50170dfb + 0xb8fc94e2bb2c4f1a30e16c343b5050a2) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0x5621af0ac40cb8b5922352ca943afca5) & mask
    x = ((x << 93) | (x >> 35)) & mask
    x = (x * 0x8e5f1fb1ea0cf915a28ae756b9b74831 + 0x6284ca6e1f7784c025ee0837d542243a) & mask
    x ^= x >> 59
    return x, 'maze.room_be4ee77d'
