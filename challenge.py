"""Follow the calculation through all 200 rooms."""

from importlib import import_module

FIRST_ROOM = 'maze.room_a5661ad6'
ROOM_COUNT = 200
MASK = (1 << 128) - 1


def walk():
    state = 0xa3eeace2f4f2e486e60a5d5658b3c2c6
    room = FIRST_ROOM
    visited = set()
    while room is not None:
        if room in visited or len(visited) >= ROOM_COUNT:
            raise RuntimeError('The room chain contains a loop.')
        visited.add(room)
        state, room = import_module(room).step(state)
        if type(state) is not int or not 0 <= state <= MASK:
            raise RuntimeError('A room returned an invalid state.')
    if len(visited) != ROOM_COUNT:
        raise RuntimeError('The calculation did not visit all 200 rooms.')
    return state


def generate_number():
    return 1 + walk() % 100

# we do some trolling

if __name__ == '__main__':
    print(generate_number())


#hello
#i want a conflict

#hi guys

