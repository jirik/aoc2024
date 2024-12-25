import copy, math, os, re, sys
from collections import Counter, deque, defaultdict
from enum import IntEnum, Enum
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby, cycle, product, chain
from operator import add

import networkx as nx
import sympy
from networkx.algorithms.clique import enumerate_all_cliques
from networkx.algorithms.dag import ancestors, descendants, topological_sort

from util import dijkstra, Graph, m_add, m_sub, m_mul


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        r1 = None
        r2 = None

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
