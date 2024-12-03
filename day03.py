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
            input_str = f.read()

        r_mul = r'mul\((\d{1,3}),(\d{1,3})\)'
        pairs = [
            tuple(int(n) for n in m.group(1, 2))
            for m in re.finditer(r_mul, input_str)
        ]
        r1 = sum(l*r for l, r in pairs)

        switches = ["don't()", "do()"]
        r2 = 0
        enabled = True
        for m in re.finditer('|'.join([r_mul] + [re.escape(d) for d in switches]), input_str):
            try:
                switch_idx = switches.index(m.group(0))
                enabled = bool(switch_idx)
            except ValueError:
                if enabled:
                    r2 += math.prod([int(n) for n in m.group(1, 2)])

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
