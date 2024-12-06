import copy, sys
from itertools import cycle, product

def m_add(row, col, delta_coord):
    return row + delta_coord[0], col + delta_coord[1]

def get_visited(row, col, matrix):
    h = len(matrix)
    w = len(matrix[0])
    deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    delta_iterator = cycle(deltas)
    delta = next(delta_iterator)
    visited = {(row, col, delta)}
    next_row, next_col = m_add(row, col, delta)
    while 0 <= next_row < h and 0 <= next_col < w:
        if matrix[next_row][next_col] == '#':
            delta = next(delta_iterator)
            vis = (row, col, delta)
            if vis in visited:
                return None
            visited.add(vis)
            next_row, next_col = m_add(row, col, delta)
        else:
            row, col = next_row, next_col
            vis = (row, col, delta)
            if vis in visited:
                return None
            visited.add(vis)
            next_row, next_col = m_add(row, col, delta)
    return {(r, c) for r, c, _ in visited}

def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        matrix = [list(ln) for ln in lines]
        guard = '^'
        start_row, start_col = next((matrix.index(row), row.index(guard)) for row in matrix if guard in row)

        r1 = len(get_visited(start_row, start_col, matrix))

        r2 = 0
        for row_idx, col_idx in product(range(len(matrix)), range(len(matrix[0]))):
            if matrix[row_idx][col_idx] == '.':
                m = copy.deepcopy(matrix)
                m[row_idx][col_idx] = '#'
                visited = get_visited(start_row, start_col, m)
                if visited is None:
                    r2 += 1

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
