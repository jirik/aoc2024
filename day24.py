import sys
import networkx as nx
from networkx.algorithms.dag import topological_sort

ops_dict = {
    'AND': 'and',
    'OR': 'or',
    'XOR': '!=',
}


def keys_to_number(prefix, values):
    bits = [v for k, v in sorted(values.items()) if k.startswith(prefix)]
    return sum(2**i for i, b in enumerate(bits) if b)


def get_z(input_values, connections):
    G = nx.DiGraph()
    G.add_edges_from([(o, r) for r, (_, operands) in connections.items() for o in operands])
    code = '\n'.join(f"{k} = {v}" for k, v in input_values.items())
    for n in topological_sort(G):
        if n in connections:
            op, operands = connections[n]
            o1, o2 = list(operands)
            code += f"\n{n} = {o1} {ops_dict[op]} {o2}"
    locs = {}
    exec(code, globals(), locs)
    return keys_to_number('z', locs)


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        split_idx = lines.index('')
        input_values = {parts[0]: bool(int(parts[1])) for ln in lines[:split_idx] if (parts := ln.split(': '))}

        connections = {}
        for ln in lines[split_idx+1:]:
            o1, op, o2, _, r = ln.split(' ')
            connections[r] = (op, frozenset([o1, o2]))

        r1 = get_z(input_values, connections)

        r2 = None
        if len(input_values) == 90:  # limit to part2 only
            z_keys = sorted(k for k in connections.keys() if k.startswith('z'))
            switched_keys = set()
            for idx, z_key in enumerate(z_keys):
                if 2 <= idx < (len(z_keys) - 1):  # ignore edge nodes as they have different subtree structure, assume their structure is correct
                    nx, ny = f"x{z_key[1:]}", f"y{z_key[1:]}"
                    xor_mains = [(n, c) for n, c in connections.items() if n == z_key and c[0] == 'XOR']
                    if not xor_mains:
                        bad_gate = (z_key, connections[z_key])
                        xor_xy = next((n, c) for n, c in connections.items() if c[0] == 'XOR' and c[1] == frozenset([nx, ny]))
                        good_gate = next((n, c) for n, c in connections.items() if c[0] == 'XOR' and xor_xy[0] in c[1])
                        switch_gates(bad_gate, good_gate, connections, switched_keys)
                        xor_main = bad_gate[0], good_gate[1]
                    else:
                        xor_main = xor_mains[0]

                    xor_xys = [(n, c) for n, c in connections.items() if c[0] == 'XOR' and c[1] == frozenset([nx, ny]) and n in xor_main[1][1]]
                    if not xor_xys:
                        good_gate = next((n, c) for n, c in connections.items() if c[0] == 'XOR' and c[1] == frozenset([nx, ny]))
                        good_node = next(n for n in xor_main[1][1] if connections[n][0] != 'OR')
                        bad_gate = (good_node, connections[good_node])
                        switch_gates(bad_gate, good_gate, connections, switched_keys)

                    or_prevs = [(n, c) for n, c in connections.items() if c[0] == 'OR' and n in xor_main[1][1]]
                    assert len(or_prevs) == 1
                    or_prev = or_prevs[0]

                    prev_z_key = z_keys[idx-1]
                    npx, npy = f"x{prev_z_key[1:]}", f"y{prev_z_key[1:]}"
                    and_prev_xy = [(n, c) for n, c in connections.items() if c[0] == 'AND' and n in or_prev[1][1] and c[1] == frozenset([npx, npy])]
                    assert len(and_prev_xy) == 1

                    prev_xor_main_ops = connections[prev_z_key][1]
                    and_prev_mains = [(n, c) for n, c in connections.items() if c[0] == 'AND' and n in or_prev[1][1] and c[1] == prev_xor_main_ops]
                    assert len(and_prev_mains) == 1

            r2 = ','.join(sorted(switched_keys))
            x = keys_to_number('x', input_values)
            y = keys_to_number('y', input_values)
            assert x + y == get_z(input_values, connections)

        print(file_path, r1, r2)


def switch_gates(conn1, conn2, connections, switched_keys):
    connections[conn2[0]] = conn1[1]
    connections[conn1[0]] = conn2[1]
    switched_keys.update({conn2[0], conn1[0]})


if __name__ == "__main__":
    main()
