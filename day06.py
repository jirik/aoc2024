import copy, sys
from itertools import cycle, tee

def m_add(row, col, delta_coord):
    return row + delta_coord[0], col + delta_coord[1]

def get_visited(row, col, delta, delta_iterator, visited, matrix, *, check_obstacles=False):
    h = len(matrix)
    w = len(matrix[0])
    visited.add((row, col, delta))
    next_row, next_col = m_add(row, col, delta)
    possible_obstacles = set()
    while 0 <= next_row < h and 0 <= next_col < w:
        if matrix[next_row][next_col] == '#':
            delta = next(delta_iterator)
            vis = (row, col, delta)
            if vis in visited:
                return None, None
            visited.add(vis)
            next_row, next_col = m_add(row, col, delta)
        else:
            if check_obstacles:
                was_already_visited = next((True for r, c, _ in visited if r == next_row and c == next_col), False)
                if not was_already_visited:
                    alt_matrix = copy.deepcopy(matrix)
                    alt_matrix[next_row][next_col] = '#'
                    delta_iterator, alt_iterator = tee(delta_iterator)
                    alt_visited = get_visited(row, col, delta, alt_iterator, set(visited), alt_matrix)[0]
                    if alt_visited is None:
                        possible_obstacles.add((next_row, next_col))
            row, col = next_row, next_col
            vis = (row, col, delta)
            if vis in visited:
                return None, None
            visited.add(vis)
            next_row, next_col = m_add(row, col, delta)
    return {(r, c) for r, c, _ in visited}, possible_obstacles

def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())

        matrix = [list(ln) for ln in lines]
        guard = '^'
        start_row, start_col = next((matrix.index(row), row.index(guard)) for row in matrix if guard in row)

        deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        delta_iterator = cycle(deltas)
        delta = next(delta_iterator)
        visited, obstacles = get_visited(start_row, start_col, delta, delta_iterator, set(), matrix, check_obstacles=True)

        r1 = len(visited)
        r2 = len(obstacles)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
