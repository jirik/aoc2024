import copy, math, os, re, sys
from collections import Counter, deque, defaultdict
from enum import IntEnum, Enum
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby, cycle, product
from operator import add

import networkx as nx
from networkx.algorithms.dag import ancestors, descendants, topological_sort

from util import dijkstra, Graph


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        r1 = None
        r2 = None

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
