import sys
import networkx as nx
from networkx.algorithms.clique import enumerate_all_cliques


def main():
    for file_path in sys.argv[1:]:
        with open(file_path) as f:
            lines = tuple(ln.strip() for ln in f.readlines())
        edges = [tuple(ln.split('-')) for ln in lines]

        G = nx.Graph()
        G.add_edges_from(edges)
        cliques = list(enumerate_all_cliques(G))
        r1 = sum(1 for c in cliques if len(c) == 3 and any(n[0] == 't' for n in c))
        r2 = ','.join(sorted(max(cliques, key=len)))

        print(file_path, r1, r2)


if __name__ == "__main__":
    main()
