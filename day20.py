import sys
from collections import defaultdict
from itertools import product
from util import m_add


deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def find_cheats(matrix, path, max_dist, min_save):
    height = len(matrix)
    width = len(matrix[0])
    path_dict = {c: path.index(c) for c in path}
    cheats = defaultdict(set)
    for idx, coord in enumerate(path):
        checked_coords = {coord}
        dist = 0
        while dist < max_dist:
            dist += 1
            next_opts = {
                (r, c) for coord2 in checked_coords for r, c in [m_add(*coord2, d) for d in deltas]
                if (r, c) not in checked_coords and 0 <= r < height and 0 <= c < width
            }
            for coord2 in next_opts:
                r, c = coord2
                if matrix[r][c] != '#':
                    idx2 = path_dict[coord2]
                    max_save = idx2 - (idx + dist)
                    if max_save >= min_save:
                        cheats[max_save].add((coord, coord2))
                checked_coords.add(coord2)
    return cheats


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        matrix = [list(ln) for ln in lines]
        height = len(matrix)
        width = len(matrix[0])
        start = next((r, c) for r, c in product(range(height), range(width)) if matrix[r][c] == 'S')
        end = next((r, c) for r, c in product(range(height), range(width)) if matrix[r][c] == 'E')

        path = [start]
        while True:
            coord = path[-1]
            next_opts = [m_add(*coord, d) for d in deltas]
            next_coords = [(r, c) for r, c in next_opts if matrix[r][c] != '#' and (r, c) not in path]
            assert len(next_coords) == 1
            next_coord = next_coords[0]
            path.append(next_coord)
            if next_coord == end:
                break

        cheats1 = find_cheats(matrix, path, max_dist=2, min_save=100 if height > 15 else 2)
        r1 = sum(len(v) for v in cheats1.values())

        cheats2 = find_cheats(matrix, path, max_dist=20, min_save=100 if height > 15 else 50)
        r2 = sum(len(v) for v in cheats2.values())

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
