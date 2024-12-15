import copy, sys
from itertools import product, chain

from util import m_add

deltas = {
    '^': (-1, 0),
    '<': (0, -1),
    '>': (0, 1),
    'v': (1, 0),
}


def print_matrix(matrix, robot):
    for r in range(len(matrix)):
        row = matrix[r]
        ln = ''
        for c in range(len(row)):
            ln += '@' if robot == (r, c) else matrix[r][c]
        print(ln)


def move_robot(robot, delta, matrix):
    can_move = False
    affected_coords = {robot}
    while True:
        next_coords = {m_add(*bc, delta) for bc in affected_coords} - affected_coords
        if any(matrix[r][c] == '#' for r, c in next_coords):
            break
        boxes = {(r, c) for r, c in next_coords if matrix[r][c] in '[]O'}
        boxes.update({(r, c - 1) for r, c in next_coords if matrix[r][c] == ']'})
        boxes.update({(r, c + 1) for r, c in next_coords if matrix[r][c] == '['})
        affected_coords.update(boxes)
        if all(matrix[r][c] == '.' for r, c in next_coords):
            can_move = True
            break
    if can_move:
        robot = m_add(*robot, delta)
        old_values = {}
        for r, c in affected_coords:
            old_values[(r, c)] = matrix[r][c]
            matrix[r][c] = '.'
        for coord, v in old_values.items():
            r, c = m_add(*coord, delta)
            matrix[r][c] = v
    return robot, matrix


def make_all_moves(robot, moves, matrix):
    for move in moves:
        robot, matrix = move_robot(robot, deltas[move], matrix)
    return robot, matrix


def make_wider(matrix):
    size = len(matrix)
    m2 = [['.'] * size * 2 for _ in range(size)]
    for r1, c1 in product(range(size), repeat=2):
        char = matrix[r1][c1]
        m2[r1][c1 * 2] = char if char != 'O' else '['
        m2[r1][c1 * 2 + 1] = char if char != 'O' else ']'
    return m2


def get_gps_sum(matrix):
    return sum(r * 100 + c
               for r, c in product(range(len(matrix)), range(len(matrix[0])))
               if matrix[r][c] in ['O', '['])


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        split_idx = lines.index('')
        matrix = [list(ln) for ln in lines[:split_idx]]
        moves = list(chain(*lines[split_idx + 1:]))
        robot = next((r, c) for r, c in product(range(len(matrix)), range(len(matrix[0]))) if matrix[r][c] == '@')
        matrix[robot[0]][robot[1]] = '.'

        _, matrix1 = make_all_moves(robot, moves, copy.deepcopy(matrix))
        r1 = get_gps_sum(matrix1)

        robot2 = robot[0], robot[1] * 2
        _, matrix2 = make_all_moves(robot2, moves, make_wider(matrix))
        r2 = get_gps_sum(matrix2)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
