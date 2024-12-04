import copy
import itertools
from collections import Counter
from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum

def m_add(row, col, delta_coord):
    return row + delta_coord[0], col + delta_coord[1]

def get_opposite_letters(row, col, delta_coord, matrix):
    r1, c1 = m_add(row, col, delta_coord)
    r2, c2 = m_add(row, col, tuple(c*-1 for c in delta_coord))
    return matrix[r1][c1], matrix[r2][c2]

def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        matrix = [list(ln) for ln in lines]
        w = len(matrix[0])
        h = len(matrix)

        # part 1
        deltas = list(itertools.product([-1, 0, 1], repeat=2))
        word = "XMAS"
        n_xmas = 0
        for row, col in itertools.product(range(h), range(w)):
            for delta in deltas:
                r, c = row, col
                ltr = matrix[r][c]
                ltr_idx = 0
                while ltr == word[ltr_idx]:
                    r, c = m_add(r, c, delta)
                    ltr = matrix[r][c] if 0 <= r < h and 0 <= c < w else None
                    ltr_idx += 1
                    if ltr_idx == len(word):
                        n_xmas += 1
                        break
        r1 = n_xmas

        # part 2
        deltas = [(1, 1), (1, -1)]
        n_x_mas = 0
        for row, col in itertools.product(range(1, h-1), range(1, w-1)):
            if matrix[row][col] == 'A' and all(
                    set(get_opposite_letters(row, col, delta, matrix)) == {'S', 'M'}
                    for delta in deltas
            ):
                n_x_mas += 1
        r2 = n_x_mas

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
