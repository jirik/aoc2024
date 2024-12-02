import copy
from collections import Counter
from operator import add
from functools import reduce, lru_cache
from itertools import pairwise, permutations, combinations, groupby
import re, os, math, sys
from util import dijkstra, Graph
from enum import IntEnum, Enum


def get_pair_type(l, r):
    delta = r - l
    if abs(delta) > 3 or delta == 0:
        return 0
    elif delta > 0:
        return 1
    else:
        return -1


def is_report_safe(report):
    fst_pair = get_pair_type(report[0], report[1])
    if fst_pair == 0:
        return False
    return all(get_pair_type(l, r) == fst_pair for l, r in pairwise(report))


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        reports = [[int(s) for s in str_nums] for ln in lines if (str_nums := re.split(r' +', ln))]

        r1 = sum(int(is_report_safe(report)) for report in reports)
        r2 = sum(
            int(any(
                is_report_safe(report)
                for report in [
                    main_report[:sep_idx] + main_report[sep_idx+1:]
                    for sep_idx in range(len(main_report))
                ]
            ))
            for main_report in reports
        )

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
