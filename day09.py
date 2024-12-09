import sys


def get_r1(disk_map):
    r1 = 0
    disk_pos = 0
    map_pos = 0
    end_map_pos = len(disk_map) - 1
    while map_pos <= end_map_pos:
        is_file = map_pos % 2 == 0
        if is_file:
            file_id = map_pos // 2
            while disk_map[map_pos] > 0:
                r1 += disk_pos * file_id
                disk_map[map_pos] -= 1
                disk_pos += 1
        else:
            while disk_map[map_pos] > 0 and map_pos <= end_map_pos:
                end_is_file = end_map_pos % 2 == 0
                end_value = disk_map[end_map_pos]
                if not end_is_file or end_value == 0:
                    end_map_pos -= 1
                    continue
                end_file_id = end_map_pos // 2
                r1 += end_file_id * disk_pos
                disk_map[map_pos] -= 1
                disk_map[end_map_pos] -= 1
                disk_pos += 1

        map_pos += 1

    return r1


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        disk_map = [int(c) for c in lines[0]]

        r1 = get_r1(disk_map[:])
        r2 = None

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
