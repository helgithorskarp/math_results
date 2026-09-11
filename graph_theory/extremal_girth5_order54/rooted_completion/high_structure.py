"""Uniform high-path theorem: high components have at most three vertices."""

from pysat.formula import IDPool
from pysat.card import CardEnc, EncType


def add_structure(cnf, data, z):
    if not 0 <= z <= 11:
        raise ValueError('The center-count theorem is restricted to z <= 11')
    pool = IDPool(start_from=cnf.nv + 1)
    n = data["n"]
    X = data["X"]
    fixed = data["fixed_degrees"]
    H = {}
    for u, v in data["fixed"] + list(data["E"]):
        if (u in fixed and fixed[u] != 8) or (v in fixed and fixed[v] != 8):
            continue
        terms = ([data["E"][u, v]] if (u, v) in data["E"] else []) + [
            X[w, 8] for w in (u, v) if w not in fixed
        ]
        y = pool.id(("high_edge", u, v))
        H[u, v] = y
        cnf.extend([[-y, t] for t in terms])
        cnf.append([y] + [-t for t in terms])
    centers = []
    for u in range(n):
        terms = [y for e, y in H.items() if u in e]
        c = pool.id(("high_center", u))
        centers.append(c)
        if len(terms) < 2:
            cnf.append([-c])
            continue
        cnf.extend(
            CardEnc.atmost(
                lits=terms, bound=2, vpool=pool, encoding=EncType.seqcounter
            ).clauses
        )
        cnf.extend(
            [c] + a
            for a in CardEnc.atmost(
                lits=terms, bound=1, vpool=pool, encoding=EncType.seqcounter
            ).clauses
        )
        cnf.extend(
            [-c] + a
            for a in CardEnc.atleast(
                lits=terms, bound=2, vpool=pool, encoding=EncType.seqcounter
            ).clauses
        )
    for (u, v), y in H.items():
        cnf.append([-y, -centers[u], -centers[v]])
    bound = 0 if z <= 8 else 1 if z <= 10 else 2
    cnf.extend(
        CardEnc.atmost(
            lits=centers, bound=bound, vpool=pool, encoding=EncType.seqcounter
        ).clauses
    )
    data["high_structure"] = dict(edge_variables=len(H), maximum_P3_components=bound)
    return H, centers
