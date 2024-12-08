import sys
from collections import defaultdict
from itertools import product


def m_add(row, col, delta_coord):
    return row + delta_coord[0], col + delta_coord[1]


def m_sub(coord1, coord2):
    return coord1[0] - coord2[0], coord1[1] - coord2[1]


def get_antinode_coords(matrix, antennas, *, limited=True):
    h = len(matrix)
    w = len(matrix[0])
    antinode_coords = set()
    for freq, coords in antennas.items():
        for an1, an2 in product(coords, repeat=2):
            if an1 != an2:
                delta = m_sub(an1, an2)
                r, c = m_add(*an1, delta) if limited else m_add(*an2, delta)
                idx = 0
                while (not limited or idx < 1) and 0 <= r < h and 0 <= c < w:
                    antinode_coords.add((r, c))
                    r, c = m_add(r, c, delta)
                    idx += 1
    return antinode_coords


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        matrix = [list(ln) for ln in lines]
        h = len(matrix)
        w = len(matrix[0])
        antennas = defaultdict(list)
        for row, col in product(range(h), range(w)):
            chr = matrix[row][col]
            if chr != '.':
                antennas[chr].append((row, col))

        r1 = len(get_antinode_coords(matrix, antennas))
        r2 = len(get_antinode_coords(matrix, antennas, limited=False))

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
