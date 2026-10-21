from math import comb

def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    p = (1 << 127) - 1
    n = 40 + (x ^ 0x6b270ef0e946dca3086c49bd51edbbe8) % 24
    base = 2 + ((x >> 17) ^ 0x543eda6db137bf6a4bffaac54176a02a) % 65521
    y = 0
    for k in range(1, 17):
        y = (y + comb(n, k) * pow(base + k, k + 3, p)) % p
    y ^= comb(n + 7, 19) * 582
    x = (x ^ y ^ 0x9c5124bbb45b4398d5b8460b0aa76c64) & mask
    x = ((x << 38) | (x >> 90)) & mask
    x = (x * 0xcb3e1355a542f82bba6a1246399e5f6d + 0x8d32771729cdb98c19b7a4664d4a8b55) & mask
    x ^= x >> 78
    return x, 'maze.room_da9c0166'
