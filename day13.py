import re, sys


def get_min_tokens(machine, *, add_to_prize=0):
    axes = [0, 1]

    a, b, prize = machine
    prize = tuple(i+add_to_prize for i in prize)
    bn = min(prize[axis] // b[axis] for axis in axes)
    mods = set()
    prev_zeros = None
    min_tokens = None
    while bn >= 0:
        dx, dy = [p-bb*bn for p, bb in zip(prize, b)]
        ax, ax_mod = divmod(dx, a[0])
        ay, ay_mod = divmod(dy, a[1])
        if ax_mod == ay_mod == 0 and ax == ay:
            min_tokens = ax * 3 + bn
            break
        mod = ax_mod, ay_mod
        if mod in mods and not prev_zeros:
            break
        mods.add(mod)
        if mod == (0, 0):
            if prev_zeros:
                bn_prev, ax_prev, ay_prev = prev_zeros
                bn_delta = bn - bn_prev
                ax_delta = ax - ax_prev
                ay_delta = ay - ay_prev
                steps = (ay - ax) / (ax_delta - ay_delta)
                if steps >= 0 and steps.is_integer():
                    b_final = bn + bn_delta * steps
                    a_final = ax + ax_delta * steps
                    min_tokens = int(a_final * 3 + b_final)
                break
            prev_zeros = bn, ax, ay
        bn -= 1
    return min_tokens


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        machines = [
            [tuple(int(m.group()) for m in re.finditer(r'\d+', ln)) for ln in lines[i:i+3]]
            for i in range(0, len(lines), 4)
        ]

        r1 = sum(get_min_tokens(m) or 0 for m in machines)
        r2 = sum(get_min_tokens(m, add_to_prize=10000000000000) or 0 for m in machines)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
