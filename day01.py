import copy
from collections import Counter
from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        line_pairs = [[int(s) for s in str_nums] for ln in lines if (str_nums := re.split(r' +', ln))]
        lists = list(zip(*line_pairs))
        o_lists = [sorted(l) for l in lists]
        sorted_pairs = list(zip(*o_lists))
        r1 = sum(abs(l - r) for l, r in sorted_pairs)

        lefts, rights = lists
        c = Counter(rights)
        r2 = sum(l*c.get(l, 0) for l in lefts)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
