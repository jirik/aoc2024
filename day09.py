import sys


def get_checksum(blocks, block_limit):
    # slower than original get_r1, but less code in general
    checksum = 0

    for file_block in list(reversed(blocks))[::2]:
        file_map_pos, file_disk_pos, file_len = file_block
        file_id = file_map_pos // 2
        while file_len > 0:
            target_len_limit = min(file_len, block_limit)
            free_block = next((b for b in blocks[1:file_map_pos:2] if b[2] >= target_len_limit), None)
            if free_block is None:
                target_disk_pos, target_len = file_disk_pos, file_len
            else:
                target_map_pos, target_disk_pos, target_len = free_block[0], free_block[1], min(free_block[2], file_len)
                blocks[target_map_pos] = target_map_pos, target_disk_pos + target_len, free_block[2] - target_len
            for p in range(target_disk_pos, target_disk_pos + target_len):
                checksum += file_id * p
            file_len -= target_len

    return checksum


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        disk_map = [int(c) for c in lines[0]]

        blocks = []
        disk_pos = 0
        for map_pos, length in enumerate(disk_map):
            blocks.append((map_pos, disk_pos, length))
            disk_pos += length

        r1 = get_checksum(blocks[:], 1)
        r2 = get_checksum(blocks[:], 10)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
