"""Exact local-support reduction; witnesses do not allocate the actual tail."""

from itertools import combinations

D = (1, 3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315)
PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
BASE = tuple(n for n in range(8, 2521)
             if 2520 % n == 0 and n not in {d for d, _ in PREFIX})


def pair_below(p, q):
    """An injective assignment of smaller labels into larger labels."""
    return ((q[0] % p[0] == 0 and q[1] % p[1] == 0) or
            (q[1] % p[0] == 0 and q[0] % p[1] == 0))


def minimal_pairs(allowed):
    pairs = tuple(combinations(allowed, 2))
    return tuple(p for p in pairs
                 if not any(t != p and pair_below(t, p) for t in pairs))


def constraints():
    return tuple({"B": (1,) + rest, "required": k,
                  "pairs": minimal_pairs(tuple(d for d in D if d not in (1,) + rest))}
                 for b, k in ((2, 3), (4, 2), (7, 1))
                 for rest in combinations(D[1:], b - 1))


def implies(strong, weak):
    return (strong["required"] >= weak["required"] and
            all(any(pair_below(q, p) for q in weak["pairs"])
                for p in strong["pairs"]))


def frontier():
    by_pairs = {}
    for row in constraints():
        if (row["pairs"] not in by_pairs or
                row["required"] > by_pairs[row["pairs"]]["required"]):
            by_pairs[row["pairs"]] = row
    rows = tuple(by_pairs.values())
    return tuple(sorted((r for r in rows
                         if not any(t != r and implies(t, r) for t in rows)),
                        key=lambda r: (-r["required"], r["B"])))


def validate_base(phases):
    if (not isinstance(phases, list) or
            any(not isinstance(row, list) or len(row) != 2 for row in phases)):
        raise ValueError("expected [original modulus, phase] pairs")
    if any(type(d) is not int or type(a) is not int or not 0 <= a < d
           for d, a in phases):
        raise ValueError("invalid original modulus or phase")
    if sorted(d for d, a in phases) != list(BASE):
        raise ValueError("choose exactly one phase at each of the36 free base labels")


def initial_holes():
    return tuple(tuple(x % 315 for x in range(r, 2520, 8)
                       if all(x % d != a for d, a in PREFIX))
                 for r in range(1, 8))


def after_base(phases):
    validate_base(phases)
    chosen = tuple(PREFIX) + tuple(map(tuple, phases))
    return tuple(tuple(sorted(x % 315 for x in range(r, 2520, 8)
                              if all(x % d != a for d, a in chosen)))
                 for r in range(1, 8))


def pair_witness(points, pairs):
    """A direct containment witness, including empty fibers."""
    if not points:
        return {"empty": True, "classes": []}
    for d, e in pairs:
        # An empty first class is represented by one unused phase, if present.
        # All occupied phases are retained. No arbitrary local normalization.
        occupied = set(x % d for x in points)
        phases = sorted(occupied)
        if len(occupied) < d:
            phases.append(next(a for a in range(d) if a not in occupied))
        for a in phases:
            remainder = [x for x in points if x % d != a]
            if not remainder:
                return {"empty": False, "classes": [[d, a]]}
            b = remainder[0] % e
            if all(x % e == b for x in remainder):
                return {"empty": False, "classes": [[d, a], [e, b]]}
    return None


def evaluate_fibers(fibers, rows=None):
    if len(fibers) != 7:
        raise ValueError("all seven labeled fibers, including empties, are required")
    result = []
    for row in frontier() if rows is None else rows:
        witnesses = [pair_witness(points, row["pairs"]) for points in fibers]
        qualified = [r for r, witness in enumerate(witnesses, 1) if witness is not None]
        result.append({"B": list(row["B"]), "required": row["required"],
                       "Q": len(qualified), "qualified": qualified,
                       "passed": len(qualified) >= row["required"],
                       "witnesses": witnesses})
    return result


def evaluate(phases):
    holes = after_base(phases)
    rows = evaluate_fibers(holes)
    return {"agent": "six-covering-3", "role": "researcher",
            "prefix": [list(p) for p in PREFIX], "base_phases": phases,
            "fibers": [list(v) for v in holes], "sizes": list(map(len, holes)),
            "predicates": rows, "passed": all(row["passed"] for row in rows),
            "scope": "Equivalent to all9241 q=3 cuts at this base assignment; passing gives no tail witness."}
