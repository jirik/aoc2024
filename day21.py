import sys
from collections import defaultdict
from functools import lru_cache
from itertools import pairwise, permutations, product
from util import m_add, m_sub

numeric_keypad = tuple(tuple(ln) for ln in ['789', '456', '123', ' 0A'])
direction_keypad = tuple(tuple(ln) for ln in [' ^A', '<v>'])
dir_to_deltas = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}


def get_coord(keypad, char):
    return next((r, c) for r, c in product(range(len(keypad)), range(len(keypad[0]))) if keypad[r][c] == char)


def get_paths(keypad, from_char, to_char):
    result = set()
    from_coord = get_coord(keypad, from_char)
    to_coord = get_coord(keypad, to_char)
    delta_row, delta_col = m_sub(to_coord, from_coord)
    vert_chars = ('v' if delta_row > 0 else '^') * abs(delta_row)
    horiz_chars = ('>' if delta_col > 0 else '<') * abs(delta_col)
    for path in set(permutations(vert_chars + horiz_chars)):
        coord = from_coord
        for direction in path:
            coord = m_add(*coord, dir_to_deltas[direction])
            if keypad[coord[0]][coord[1]] == ' ':
                break
        else:
            result.add(compress_path(''.join(path) + 'A'))
    return result


def compress_path(path):
    result = defaultdict(int)
    for from_char, to_char in pairwise('A' + path):
        result[from_char, to_char] += 1
    return frozenset(result.items())


@lru_cache(maxsize=None)
def get_shortest_length(path, depth):
    min_path = 0
    for (from_char, to_char), count in path:
        sub_paths = get_paths(direction_keypad, from_char, to_char)
        if depth == 1:
            min_path += min(sum(m[1] for m in p) for p in sub_paths) * count
        else:
            min_path += min(get_shortest_length(p, depth - 1) for p in sub_paths) * count
    return min_path


def get_complexity(code, depth):
    return sum(
        min(get_shortest_length(p, depth=depth)
            for p in get_paths(numeric_keypad, from_char, to_char))
        for from_char, to_char in pairwise('A' + code)
    )


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        r1 = sum(int(ln[:-1]) * get_complexity(ln, 2) for ln in lines)
        r2 = sum(int(ln[:-1]) * get_complexity(ln, 25) for ln in lines)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
