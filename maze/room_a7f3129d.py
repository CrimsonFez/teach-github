from math import factorial

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    permutation = list(range(16))
    selector = (x ^ 0x25226187ba92a8f520a580e3d3b95fe4) & mask
    for i in range(15, 0, -1):
        selector = (selector * 0x1f257261e065f67bb898a90e480eb71b + 0xf33ac319b709464efeb8a4d81769cba2) & mask
        j = selector % (i + 1)
        permutation[i], permutation[j] = permutation[j], permutation[i]
    y = 0
    for i, value in enumerate(permutation):
        smaller = sum(other < value for other in permutation[i + 1:])
        y += smaller * factorial(15 - i)
    y ^= selector
    x = (x ^ y ^ 0xc4bed9194059ad128f50897fb72025e5) & mask
    x = ((x << 99) | (x >> 29)) & mask
    x = (x * 0xa3c18561237d996f24590b7222813173 + 0x393d4ecfa287ebffb46592436d313d0a) & mask
    x ^= x >> 69
    return x, 'maze.room_2f4e6c2c'
