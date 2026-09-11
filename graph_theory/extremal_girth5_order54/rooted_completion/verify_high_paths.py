"""Independent finite controls for the written high-path theorem."""

from itertools import combinations, permutations
from pathlib import Path
import json
import networkx as nx


def girth5(G):
    for u, v in combinations(G, 2):
        common = set(G[u]) & set(G[v])
        if len(common) > 1 or (G.has_edge(u, v) and common):
            return False
    return True


def main():
    cases = {3: 0, 4: 0}
    graphs = 0
    for G in nx.graph_atlas_g():
        if not girth5(G):
            continue
        graphs += 1
        for size in (3, 4):
            for path in permutations(G, size):
                if not all(G.has_edge(path[i], path[i + 1]) for i in range(size - 1)):
                    continue
                rest = sorted(set(G) - set(path))
                for mask in range(1 << len(rest)):
                    S = {x for i, x in enumerate(rest) if mask >> i & 1}
                    L = [set(G[t]) & S for t in path]
                    for i, j in combinations(range(size), 2):
                        bound = 0 if j - i <= 2 else 1
                        if len(L[i] & L[j]) > bound:
                            raise ValueError("Local intersection bound failed")
                    if len(set().union(*L)) < sum(map(len, L)) - (size == 4):
                        raise ValueError("Union bound failed")
                    cases[size] += 1
    # Sharp local P4 example: 4,5,5,4 low-neighbor sets with one endpoint overlap.
    L = [{4, 5, 6, 7}, set(range(8, 13)), set(range(13, 18)), {4, 18, 19, 20}]
    G = nx.Graph()
    G.add_nodes_from(range(21))
    G.add_edges_from([(0, 1), (1, 2), (2, 3)])
    G.add_edges_from((u, v) for u in range(4) for v in L[u])
    if not girth5(G) or len(set().union(*L)) != 17:
        raise ValueError("Sharp fixture failed")
    remainder = {}
    for r in range(3):
        sets = [set(c) for k in range(2, r + 1) for c in combinations(range(r), k)]
        maximum = 0
        for mask in range(1 << len(sets)):
            chosen = [s for i, s in enumerate(sets) if mask >> i & 1]
            if all(len(a & b) <= 1 for a, b in combinations(chosen, 2)):
                maximum = max(maximum, len(chosen))
        remainder[str(r)] = maximum
    result = dict(
        atlas_girth5_graphs=graphs,
        oriented_path_color_controls={str(k): v for k, v in cases.items()},
        sharp_P4_union=17,
        remainder_family_maxima=remainder,
    )
    expected = Path(__file__).with_name("high_paths_expected.json")
    if json.loads(expected.read_text()) != result:
        raise ValueError("Control totals changed")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
