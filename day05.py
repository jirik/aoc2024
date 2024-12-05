import copy
import itertools
from collections import Counter
from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys

from networkx.algorithms.dag import ancestors, descendants, topological_sort

from util import dijkstra, Graph
from enum import IntEnum, Enum
import networkx as nx


def is_ordered(update, graph):
    for page_idx, page in enumerate(update):
        if any(after_page in graph.predecessors(page) for after_page in update[page_idx+1:]):
            return False
    return True


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        sep_line_idx = lines.index("")
        rules = [tuple(int(p) for p in ln.split('|')) for ln in lines[:sep_line_idx]]

        # part 1
        graph = nx.DiGraph()
        graph.add_edges_from(rules)
        updates = [
            [int(p) for p in ln.split(',')]
            for ln in lines[sep_line_idx+1:]
        ]
        ordered_updates = [u for u in updates if is_ordered(u, graph)]
        r1 = sum(u[len(u)//2] for u in ordered_updates)

        # part 2
        wrong_updates = [u for u in updates if not is_ordered(u, graph)]
        r2 = 0
        for update in wrong_updates:
            g = nx.DiGraph()
            g.add_edges_from([r for r in rules if all(p in update for p in r)])
            fixed_update = list(topological_sort(g))
            r2 += fixed_update[len(fixed_update)//2]

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
