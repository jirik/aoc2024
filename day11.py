import sys
from functools import lru_cache


def blink(stone):
    if stone == 0:
        new_stones = (1,)
    elif (s := f"{stone}") and (len_s := len(s)) % 2 == 0:
        new_stones = int(s[:len_s//2]), int(s[len_s//2:])
    else:
        new_stones = (stone*2024,)
    return new_stones


@lru_cache(maxsize=None)
def get_num_stones(stone, blinks):
    new_stones = blink(stone)
    if blinks == 1:
        return len(new_stones)
    else:
        return sum(get_num_stones(s, blinks - 1) for s in new_stones)


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        stones = [int(c) for c in lines[0].split(' ')]

        r1 = sum(get_num_stones(s, 25) for s in stones)
        r2 = sum(get_num_stones(s, 75) for s in stones)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
