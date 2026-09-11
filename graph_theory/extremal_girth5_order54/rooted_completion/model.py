"""Exact girth-five completions of a root ball, with optional distant vertices.

See README.md for the graph-to-formula and formula-to-graph proofs.
"""

from itertools import combinations, product
from collections import Counter
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType


def build(
    sizes,
    counts,
    edge_target,
    moore=True,
    symmetry=True,
    outside=0,
    minimum_high_defect=0,
):
    pool = IDPool()
    cnf = CNF()
    r = len(sizes)
    parts = []
    v = r + 1
    for n in sizes:
        parts.append(tuple(range(v, v + n)))
        v += n
    outsiders = list(range(v, v + outside))
    v += outside
    if sizes != sorted(sizes) or sum(counts.values()) != v:
        raise ValueError("Root dimensions")
    n = v
    parent = {u: i + 1 for i, P in enumerate(parts) for u in P}
    children = sorted(parent)
    vertices = children + outsiders
    blocks = parts + [(x,) for x in outsiders]
    fixed = [(0, i + 1) for i in range(r)] + [
        (i + 1, u) for i, P in enumerate(parts) for u in P
    ]
    fixed_degrees = {0: r, **{i + 1: s + 1 for i, s in enumerate(sizes)}}
    remaining = Counter(counts)
    remaining.subtract(fixed_degrees.values())
    if any(x < 0 for x in remaining.values()):
        raise ValueError("Impossible fixed degrees")
    degrees = sorted(d for d in counts if counts[d])

    def card(lits, bound, mode="eq", guard=None):
        if bound < 0 and mode == "ge":
            return
        if bound < 0 or (mode != "le" and bound > len(lits)):
            cs = [[]]
        elif mode == "le" and bound >= len(lits):
            return
        elif not lits:
            cs = [[]] if bound else []
        else:
            fn = {"eq": CardEnc.equals, "le": CardEnc.atmost, "ge": CardEnc.atleast}[
                mode
            ]
            cs = fn(lits, bound=bound, vpool=pool, encoding=EncType.seqcounter).clauses
        cnf.extend(([-guard] + c if guard else c) for c in cs)

    E = {}
    for a, b in combinations(range(len(blocks)), 2):
        for i, u in enumerate(blocks[a]):
            for j, w in enumerate(blocks[b]):
                if symmetry and a == 0 and b < r and i != j:
                    continue
                E[u, w] = pool.id(("edge", u, w))

    def edge(u, w):
        return E.get(tuple(sorted((u, w))))

    X = {(u, d): pool.id(("degree", u, d)) for u in vertices for d in degrees}
    for d in degrees:
        card([X[u, d] for u in vertices], remaining[d])
    for u in vertices:
        card([X[u, d] for d in degrees], 1)
        incident = [edge(u, w) for w in vertices if w != u and edge(u, w)]
        for d in degrees:
            card(incident, d - (u in parent), guard=X[u, d])
        for P in parts:
            terms = [edge(u, w) for w in P if w != u and edge(u, w)]
            if len(terms) > 1:
                # Pairwise clauses make the matching restriction directly visible.
                cnf.extend([-a, -b] for a, b in combinations(terms, 2))
    # Every triangle in the variable part uses three distinct blocks.
    triangles = 0
    cycles4 = 0
    for a, b, c in combinations(range(len(blocks)), 3):
        for u, w, x in product(blocks[a], blocks[b], blocks[c]):
            es = [edge(u, w), edge(w, x), edge(x, u)]
            if all(es):
                cnf.append([-e for e in es])
                triangles += 1
    # A repeated real branch in a four-cycle is already ruled out by matchings.
    # Each outside vertex has its own singleton block.
    for a, b, c, d in combinations(range(len(blocks)), 4):
        for u, w, x, y in product(blocks[a], blocks[b], blocks[c], blocks[d]):
            for cycle in ((u, w, x, y), (u, w, y, x), (u, x, w, y)):
                es = [edge(cycle[i], cycle[(i + 1) % 4]) for i in range(4)]
                if all(es):
                    cnf.append([-e for e in es])
                    cycles4 += 1
    # Normalize the first branch's neighbor masks in descending order.
    if symmetry:
        previous = None
        for i, u in enumerate(parts[0]):
            bits = [edge(u, P[i]) for P in parts[1:]] + [edge(u, x) for x in outsiders]
            choices = {}
            for mask in range(1 << len(bits)):
                d = 1 + mask.bit_count()
                if d not in degrees:
                    continue
                y = pool.id(("mask", u, mask))
                choices[mask] = y
                cnf.append([-y, X[u, d]])
                for j, e in enumerate(bits):
                    cnf.append([-y, e if mask >> j & 1 else -e])
            card(list(choices.values()), 1)
            if previous:
                cnf.extend(
                    [-x, -y]
                    for a, x in previous.items()
                    for b, y in choices.items()
                    if a < b
                )
            previous = choices
    # Necessary sphere inequalities at parents and all remaining vertices.
    Y = {}
    if moore:

        def typed_edge(u, w, d):
            e = edge(u, w)
            if e is None:
                return None
            key = (u, w, d)
            if key not in Y:
                y = pool.id(("typed", *key))
                Y[key] = y
                x = X[w, d]
                cnf.extend([[-y, e], [-y, x], [y, -e, -x]])
            return Y[key]

        for i, P in enumerate(parts):
            lits = [
                X[u, d] for u in P for d in degrees for _ in range(d - min(degrees))
            ]
            # Root degree plus child degrees <= n-1.
            card(
                lits,
                n
                - 1
                - r
                - min(degrees) * len(P)
                - (minimum_high_defect if len(P) + 1 == 8 else 0),
                "le",
            )
        for u in vertices:
            lits = [
                typed_edge(u, w, d)
                for w in vertices
                if w != u and edge(u, w)
                for d in degrees
                for _ in range(d - min(degrees))
            ]
            for d in degrees:
                card(
                    lits,
                    n
                    - 1
                    - (fixed_degrees[parent[u]] if u in parent else 0)
                    - min(degrees) * (d - (u in parent))
                    - (minimum_high_defect if d == 8 else 0),
                    "le",
                    guard=X[u, d],
                )
    data = dict(
        n=n,
        sizes=sizes,
        counts=counts,
        edge_target=edge_target,
        parts=parts,
        parent=parent,
        children=children,
        vertices=vertices,
        outsiders=outsiders,
        minimum_high_defect=minimum_high_defect,
        fixed=fixed,
        fixed_degrees=fixed_degrees,
        E=E,
        X=X,
        Y=Y,
        triangles=triangles,
        cycles4=cycles4,
    )
    if sum(d * c for d, c in counts.items()) != 2 * edge_target:
        raise ValueError("Edge total does not match degrees")
    return cnf, data


def root_defect_bound(z):
    if not 1 <= z <= 11:
        raise ValueError("Remaining positive high-degree levels are 1 through 11")
    return max(a for a in range(6) if z * a * (a + 4) <= 256 - 19 * z)


def target(z, a, c, **kwargs):
    if not 0 <= a <= root_defect_bound(z):
        raise ValueError("Root deficit outside exhaustive range")
    if not 0 <= c <= (5 - a) // 2:
        raise ValueError("Impossible high-neighbor count")
    return build(
        [5] * (3 + a + c) + [6] * (5 - a - 2 * c) + [7] * c,
        {6: z + 4, 7: 50 - 2 * z, 8: z},
        187,
        outside=a,
        minimum_high_defect=a,
        **kwargs
    )


def decode(data, model):
    pos = set(model)
    return sorted(
        tuple(sorted(e))
        for e in data["fixed"] + [e for e, x in data["E"].items() if x in pos]
    )


def verify(n, edges, counts=None):
    N = [set() for _ in range(n)]
    for u, v in edges:
        if not 0 <= u < v < n or v in N[u]:
            raise ValueError("Malformed edge")
        N[u].add(v)
        N[v].add(u)
    if counts is not None and Counter(map(len, N)) != Counter(counts):
        raise ValueError("Wrong degrees")
    for u, v in combinations(range(n), 2):
        if v in N[u] and N[u] & N[v]:
            raise ValueError("Triangle")
        if len(N[u] & N[v]) > 1:
            raise ValueError("Four-cycle")
    return dict(
        n=n,
        edges=len(edges),
        degrees=dict(Counter(map(len, N))),
        girth_at_least_five=True,
    )
