def step(state):
    mask = (1 << 128) - 1
    x = state & mask
    odd = (x ^ 0x5949ec1cbb978b7aa7dcbe8ff973206b) | 1
    y = 1
    for _ in range(7):
        y = (y * (2 - odd * y)) & mask
    y = (y + pow((x ^ 0xb6d9175ad5756341a1fd39fea02b979b) | 1, 37, 1 << 128)) & mask
    x = (x ^ y ^ 0x33d7cb1147bb6c633197d472415ab5e4) & mask
    x = ((x << 88) | (x >> 40)) & mask
    x = (x * 0x65f034cfb4213847c09487b4a155880b + 0xaf582dcaef99a9879e50b3130c85ec7e) & mask
    x ^= x >> 66
    return x, 'maze.room_18dc7e34'
