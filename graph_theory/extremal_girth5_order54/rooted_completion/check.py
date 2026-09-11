"""Definition-level controls for the completion encoding and its normalization."""

from pathlib import Path
from collections import Counter
from itertools import combinations
import json, time
import networkx as nx
import numpy as np
from pysat.solvers import Solver
from model import build, decode, root_defect_bound

P = Path(__file__).resolve().parent


def graph_check(n, edges, counts):
    A = np.zeros((n, n), dtype=np.int64)
    for u, v in edges:
        if not 0 <= u < v < n or A[u, v]:
            return False
        A[u, v] = A[v, u] = 1
    if Counter(map(int, A.sum(axis=1))) != Counter(counts):
        return False
    A2 = A @ A
    return not np.any(A2 * A) and not np.any(np.triu(A2, 1) > 1)


def normalize(G, root):
    parents = sorted(G[root], key=lambda p: (G.degree(p), p))
    parts = [sorted(set(G[p]) - {root}) for p in parents]
    tree = [root, *parents, *sum(parts, [])]
    if len(set(tree)) != len(tree):
        raise ValueError("Radius-two vertices repeat")
    outside = sorted(set(G) - set(tree))
    sizes = list(map(len, parts))
    first = parts[0]
    for b in range(1, len(parts)):
        used = set()
        row = {}
        for i, u in enumerate(first):
            nb = set(G[u]) & set(parts[b])
            if len(nb) > 1:
                raise ValueError("Not a matching")
            if nb:
                row[i] = next(iter(nb))
                used.update(nb)
        left = iter(sorted(set(parts[b]) - used))
        parts[b] = [row[i] if i in row else next(left) for i in range(len(parts[b]))]

    def mask(i):
        u = first[i]
        bits = [parts[b][i] in G[u] for b in range(1, len(parts))] + [
            x in G[u] for x in outside
        ]
        return sum(int(x) << j for j, x in enumerate(bits))

    order = sorted(range(len(first)), key=mask, reverse=True)
    parts = [[part[i] for i in order] + part[len(first) :] for part in parts]
    old = [root, *parents, *sum(parts, []), *outside]
    label = {u: i for i, u in enumerate(old)}
    edges = sorted(tuple(sorted((label[u], label[v]))) for u, v in G.edges())
    return sizes, len(outside), edges


def fixed_check(G, root):
    sizes, a, es = normalize(G, root)
    counts = dict(Counter(dict(G.degree()).values()))
    cnf, data = build(sizes, counts, G.number_of_edges(), outside=a)
    if not graph_check(len(G), es, counts):
        raise ValueError("Control is not girth five")
    if not set(es).issubset(set(data["fixed"]) | set(data["E"])):
        raise ValueError("Normalization lost a real edge")
    with Solver(name="g4", bootstrap_with=cnf) as s:
        if not s.solve(
            assumptions=[x if e in es else -x for e, x in data["E"].items()]
        ):
            raise ValueError("Known graph rejected")
        if decode(data, s.get_model()) != es:
            raise ValueError("Decode mismatch")
    return dict(
        n=len(G),
        edges=G.number_of_edges(),
        root=root,
        sizes=sizes,
        outside=a,
        variables=cnf.nv,
        clauses=len(cnf.clauses),
    )


def main():
    t = time.perf_counter()
    r = {}
    G = nx.petersen_graph()
    G.remove_edge(0, 1)
    r["petersen_deleted_edge"] = [fixed_check(G, v) for v in G]
    r["hoffman_singleton"] = fixed_check(nx.hoffman_singleton_graph(), 0)
    # Independent full-assignment check with one vertex outside the root ball.
    root = next(v for v in G if len(G[v]) == 3 and normalize(G, v)[1] == 1)
    sizes, a, es = normalize(G, root)
    counts = dict(Counter(dict(G.degree()).values()))
    cnf, data = build(sizes, counts, G.number_of_edges(), outside=a)
    items = list(data["E"].items())
    accepted = 0
    if len(items) > 14:
        raise ValueError("Small exhaustive fixture unexpectedly large")
    with Solver(name="g4", bootstrap_with=cnf) as solver:
        for mask in range(1 << len(items)):
            es = sorted(
                data["fixed"] + [e for i, (e, x) in enumerate(items) if mask >> i & 1]
            )
            expected = graph_check(len(G), es, counts)
            ans = solver.solve(
                assumptions=[
                    x if mask >> i & 1 else -x for i, (e, x) in enumerate(items)
                ]
            )
            if ans != expected:
                raise ValueError(("Exhaustive mismatch", mask, expected, ans))
            accepted += ans
    r["one_outside_exhaustive"] = dict(
        root=root,
        sizes=sizes,
        outside=a,
        edge_variables=len(items),
        assignments=1 << len(items),
        accepted=accepted,
    )
    fixture = P.parent / "lower_bound_54_185.json"
    j = json.loads(fixture.read_text())
    G = nx.Graph()
    G.add_nodes_from(range(j["n"]))
    G.add_edges_from(j["edges"])
    r["known_54_185"] = [fixed_check(G, root) for root in (50, 52, 14)]
    r["root_defect_bounds"] = {z: root_defect_bound(z) for z in range(1, 12)}
    r["seconds"] = time.perf_counter() - t
    expected = json.loads((P / "controls_expected.json").read_text())
    semantic = json.loads(json.dumps({k: v for k, v in r.items() if k != "seconds"}))
    if semantic != expected:
        raise ValueError("Control output differs from expected")
    print(json.dumps(r, indent=2))


if __name__ == "__main__":
    main()
