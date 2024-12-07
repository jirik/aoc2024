import re, sys
from operator import add, mul


def can_be_true(true_res, res, operands, operators):
    if not operands:
        return true_res == res
    op2 = operands.pop(0)
    candidates = [r for op in operators if (r := op(res, op2)) <= true_res]
    return any(can_be_true(true_res, r, operands[:], operators) for r in candidates)


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        equations = [[int(m.group(0)) for m in re.finditer(r'\d+', ln)] for ln in lines]

        r1 = sum(eq[0] for eq in equations if can_be_true(eq[0], 0, eq[1:], [add, mul]))
        r2 = sum(eq[0] for eq in equations if can_be_true(eq[0], 0, eq[1:], [
            add, mul, lambda x, y: int(f"{x}{y}")]))

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
