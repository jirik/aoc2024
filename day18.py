import re, sys

from util import m_add


deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_next_options(col, row, walls, size, checked_coords):
    maybe_opts = [m_add(col, row, d) for d in deltas]
    opts = {
        (c, r) for c, r in maybe_opts
        if 0 <= c < size and 0 <= r < size and (c, r) not in walls and (c, r) not in checked_coords
    }
    return opts


def get_best_move(queue):
    min_v = min(queue.values())
    best_k = next(k for k, v in queue.items() if v == min_v)
    return best_k, min_v


def get_shortest_path(size, walls):
    checked_coords = {(0, 0)}
    r1 = None
    queue = {o: 1 for o in get_next_options(0, 0, walls, size, checked_coords)}
    while True:
        if len(queue) == 0:
            break
        coord, price = get_best_move(queue)
        del queue[coord]
        if coord == (size - 1, size - 1):
            r1 = price
            break
        if coord in checked_coords:
            continue
        checked_coords.add(coord)
        opt_price = price + 1
        for opt in get_next_options(*coord, walls, size, checked_coords):
            if opt not in queue or opt_price < queue[opt]:
                queue[opt] = opt_price
    return r1


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        all_walls = [tuple(int(m.group()) for m in re.finditer(r'\d+', ln)) for ln in lines]
        size = 7 if len(all_walls) < 30 else 71
        walls = set(all_walls[:12] if len(all_walls) < 30 else all_walls[:1024])

        r1 = get_shortest_path(size, walls)

        pth_len = None
        wall_idx = len(all_walls) - 1
        while pth_len is None:
            pth_len = get_shortest_path(size, set(all_walls[:wall_idx+1]))
            wall_idx -= 1
        r2 = ','.join(map(str, all_walls[wall_idx + 2]))

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
