import math, re, sys
from itertools import chain


def get_quadrant_idx(c, size):
    if c < size // 2:
        return 0
    elif c > size // 2:
        return 1
    else:
        return None


def move(robots, step, width, height):
    new_robots = []
    for robot in robots:
        col_s, row_s, col_delta, row_delta = robot
        col = (col_s + step * col_delta) % width
        row = (row_s + step * row_delta) % height
        new_robots.append((col, row, col_delta, row_delta))
    return new_robots


def get_quadrants(robots, width, height):
    quadrants = [ [0] * 2 for _ in range(2)]
    for col, row, _, _ in robots:
        qr, qc = get_quadrant_idx(row, height), get_quadrant_idx(col, width)
        if qr is not None and qc is not None:
            quadrants[qc][qr] += 1
    return quadrants


def print_robots(robots, width, height):
    for row in range(height):
        ln = ''
        for col in range(width):
            robs = [robot for robot in robots if robot[0] == col and robot[1] == row]
            ln += 'X' if len(robs) > 0 else '.'
        print(ln)


def is_trunk(robots, width, *, trunk_height_limit):
    center_col_idx = width // 2
    center_robots_idx = sorted([r[1] for r in robots if r[0] == center_col_idx])

    trunk_height = trunk_height_limit
    prev_r = None
    for r in center_robots_idx:
        if prev_r is None:
            prev_r = r
            continue
        if prev_r + 1 == r:
            trunk_height -= 1
            prev_r = r
        else:
            prev_r = None
            trunk_height = trunk_height_limit
        if trunk_height <= 0:
            return True
    return False

def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        robots = [[int(m.group(0)) for m in re.finditer(r'-?\d+', ln)] for ln in lines]
        width = max(r[0] for r in robots) - min(r[0] for r in robots) + 1
        height = max(r[1] for r in robots) - min(r[1] for r in robots) + 1

        robots_100 = move(robots, 100, width, height)
        quadrants_100 = get_quadrants(robots_100, width, height)
        r1 = math.prod(chain(*quadrants_100))

        r2 = None
        if height > 100:
            r2 = 0
            # let's expect trunk is in the middle column, and it is at least 10 pixels high
            while not is_trunk(robots, width, trunk_height_limit=10):
                robots = move(robots, 1, width, height)
                r2 += 1
            print_robots(robots, width, height)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
