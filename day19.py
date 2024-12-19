import re, sys
from functools import lru_cache


@lru_cache(maxsize=None)
def get_num_opts(design, patterns):
    if not design:
        return 1
    opts = [p for p in patterns if re.match(p, design)]
    if not opts:
        return 0
    return sum(get_num_opts(design[len(p.pattern):], patterns) for p in opts)


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        patterns = tuple(re.compile(s) for s in lines[0].split(', '))
        designs = lines[2:]

        r1 = sum(1 for d in designs if get_num_opts(d, patterns))
        r2 = sum(get_num_opts(d, patterns) for d in designs)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
