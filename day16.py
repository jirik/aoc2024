import sys
from itertools import product

from util import m_add


deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_next_options(row, col, delta_idx, matrix, *, prev_price=0, prev_positions=None):
    prev_positions = prev_positions or set()
    opts = {
        (row, col, (delta_idx+1)%4): 1000,
        (row, col, (delta_idx+4-1)%4): 1000,
    }
    r, c = m_add(row, col, deltas[delta_idx])
    if matrix[r][c] != '#':
        opts[(r, c, delta_idx)] = 1
    return {k: (prev_price + price, prev_positions.union({(row, col, delta_idx)})) for k, price in opts.items()}


def get_best_move(queue):
    min_v = min([p for p, _ in queue.values()])
    best_k = next(k for k, v in queue.items() if v[0] == min_v)
    return best_k, queue[best_k]


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        matrix = [list(ln) for ln in lines]
        height = len(matrix)
        width = len(matrix[0])
        row, col = next((r, c) for r, c in product(range(height), range(width)) if matrix[r][c] == 'S')
        matrix[row][col] = '.'

        delta_idx = 1
        best_spots =set()
        checked_positions = {(row, col, delta_idx)}
        queue = get_next_options(row, col, delta_idx, matrix)
        r1 = None
        while True:
            position, (price, prev_positions) = get_best_move(queue)
            if r1 is not None and price > r1:
                break
            del queue[position]
            r, c, d = position
            if matrix[r][c] == 'E':
                best_spots.update(prev_positions, {position})
                if r1 is None:
                    r1 = price
            if position in checked_positions:
                continue
            checked_positions.add(position)
            next_opts = get_next_options(r, c, d, matrix, prev_price=price, prev_positions=prev_positions)
            for triplet, (price, prev_positions) in next_opts.items():
                if triplet not in queue or price < queue[triplet][0]:
                    queue[triplet] = (price, prev_positions)
                elif price == queue[triplet][0]:
                    queue[triplet][1].update(prev_positions)

        r2 = len({(r, c) for r, c, _ in best_spots})

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
