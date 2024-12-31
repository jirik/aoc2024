import sys
from itertools import product, groupby


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            input_str = f.read()
        matrices = [s.split('\n') for s in input_str.split('\n\n')]
        height_limit = len(matrices[0])

        grouper = lambda m: m[0]
        heights = [[[sum(1 for r in m if r[ci] == '#') for ci in range(len(m[0]))] for m in ms]
                   for _, ms in groupby(sorted(matrices, key=grouper), key=grouper)]

        r1 = sum(1 for lk in product(*heights) if all(sum(t) <= height_limit for t in zip(*lk)))
        r2 = None

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
