import sys
from collections import defaultdict
from itertools import product


deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def m_add(row, col, delta_coord):
    return row + delta_coord[0], col + delta_coord[1]


def get_tails(row, col, matrix):
    mh, mw = len(matrix), len(matrix[0])
    h = 0
    coords = {(row, col): 1}
    while len(coords) > 0 and h < 9:
        h += 1
        new_coords = defaultdict(int)
        for (c, rating), delta in product(coords.items(), deltas):
            nr, nc = m_add(*c, delta)
            if 0 <= nr < mh and 0 <= nc < mw and matrix[nr][nc] == h:
                new_coords[(nr, nc)] += rating
        coords = new_coords
    return coords if h == 9 else {}


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        matrix = [[int(c) for c in ln] for ln in lines]

        mh, mw = len(matrix), len(matrix[0])
        all_tails = [get_tails(r, c, matrix)
                     for r, c in product(range(mh), range(mw))
                     if matrix[r][c] == 0]
        r1 = sum(len(tails) for tails in all_tails)
        r2 = sum(sum(tails.values()) for tails in all_tails)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
