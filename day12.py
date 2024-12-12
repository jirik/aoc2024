import sys
from itertools import product

from util import m_add


deltas = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_num_sides(coords, remaining_edges, *, is_outer=True):
    if is_outer:
        fst_row = min(coords, key=lambda x: x[0])[0]
        fst_coord = min([c for c in coords if c[0] == fst_row], key=lambda x: x[1])
    else:
        fst_row = max([e[0] for e in remaining_edges], key=lambda x: x[0])[0]
        fst_coord = min([e[0] for e in remaining_edges if e[0][0] == fst_row], key=lambda x: x[1])
    fst_delta_idx = 1

    n_sides = 0
    coord, side_delta_idx = fst_coord, fst_delta_idx
    while True:
        remaining_edges.remove((coord, side_delta_idx))

        left_delta_idx = (side_delta_idx - 1 + len(deltas)) % len(deltas)
        next_side_coord = m_add(*coord, deltas[side_delta_idx])
        next_left_coord = m_add(*next_side_coord, deltas[left_delta_idx])
        if next_side_coord in coords and next_left_coord not in coords:
            coord = next_side_coord
        elif next_side_coord not in coords:
            n_sides += 1
            side_delta_idx = (side_delta_idx + 1) % len(deltas)
        else:
            n_sides += 1
            coord = next_left_coord
            side_delta_idx = left_delta_idx

        if coord == fst_coord and side_delta_idx == fst_delta_idx:
            while remaining_edges:
                n_sides += get_num_sides(coords, remaining_edges, is_outer=False)
            return n_sides

def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        matrix = [list(ln) for ln in lines]
        size = len(matrix)
        assert len(matrix[0]) == size

        coords_to_check = set(product(range(size), repeat=2))
        r1 = 0
        r2 = 0
        while len(coords_to_check) > 0:
            fst_region_coord = coords_to_check.pop()
            region_coords = set()
            region_letter = matrix[fst_region_coord[0]][fst_region_coord[1]]
            unchecked_region_coords = {fst_region_coord}
            region_edges = set()
            while len(unchecked_region_coords) > 0:
                coord = unchecked_region_coords.pop()
                region_coords.add(coord)
                for nb_delta_idx in range(len(deltas)):
                    nb_delta = deltas[nb_delta_idx]
                    nb_coord = m_add(*coord, nb_delta)
                    nb_r, nb_c = nb_coord
                    if 0 <= nb_r < size and 0 <= nb_c < size and matrix[nb_r][nb_c] == region_letter:
                        if nb_coord not in region_coords:
                            coords_to_check.discard(nb_coord)
                            unchecked_region_coords.add(nb_coord)
                    else:
                        region_edges.add((coord, (nb_delta_idx + 1) % 4))
            area = len(region_coords)
            perimeter = len(region_edges)
            r1 += area * perimeter
            num_sides = get_num_sides(region_coords, region_edges)
            r2 += area * num_sides

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
