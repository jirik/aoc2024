import math, re, sys


def combo_to_literal(operand, registers):
    return operand if operand < 4 else registers[operand - 4]


def print_state(program, regs, out, pos):
    print('Registers:' + '     '.join('{:15d}'.format(r) for r in regs))
    print('Program: ' + ''.join((f">{p}<" if i == pos else f" {p} ") for i, p in enumerate(program)))
    print('Out: ' + ','.join(str(i) for i in out))


def process(program, regs):
    pos = 0
    out = []
    while pos < len(program):
        opcode, operand = program[pos:pos + 2]
        match opcode:
            case 0: regs[0] = regs[0] // int(math.pow(2, combo_to_literal(operand, regs)))
            case 1: regs[1] = regs[1] ^ operand
            case 2: regs[1] = combo_to_literal(operand, regs) % 8
            case 3: pos = operand - 2 if regs[0] != 0 else pos
            case 4: regs[1] = regs[1] ^ regs[2]
            case 5: out.append(combo_to_literal(operand, regs) % 8)
            case 6: regs[1] = regs[0] // int(math.pow(2, combo_to_literal(operand, regs)))
            case 7: regs[2] = regs[0] // int(math.pow(2, combo_to_literal(operand, regs)))
        pos += 2
    return out


def get_next_three_bits(program, prev_bits=0, pos=0):
    if pos == len(program):
        return prev_bits
    for three_bits in range(8):
        out = process(program, [prev_bits * 8 + three_bits, 0, 0])
        if out and out[0] == program[-(pos + 1)]:
            maybe_bits = get_next_three_bits(program, prev_bits * 8 + three_bits, pos + 1)
            if maybe_bits is not None:
                return maybe_bits


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        regs = [int(re.search(r'\d+', ln).group()) for ln in lines[:3]]
        program = [int(m.group()) for m in re.finditer(r'\d+', lines[4])]

        out = process(program, regs[:])
        r1 = ','.join(str(i) for i in out)

        r2 = get_next_three_bits(program)

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
