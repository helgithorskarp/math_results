"""Expose the exact weighted gap as a necessary constraint in the rooted model."""

from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.pb import PBEnc


def add_energy(cnf, data, budget=None):
    n = data["n"]
    counts = data["counts"]
    children = data["children"]
    X = data["X"]
    Y = data["Y"]
    parts = data["parts"]
    fixed = data["fixed_degrees"]
    pool = IDPool(start_from=cnf.nv + 1)
    if set(counts) - {6, 7, 8}:
        raise ValueError("Energy identity requires degrees 6,7,8")
    for (u, v), e in data["E"].items():
        for a, b in ((u, v), (v, u)):
            for d in counts:
                if d <= 6 or not counts[d] or (a, b, d) in Y:
                    continue
                y = pool.id(("energy_typed", a, b, d))
                Y[a, b, d] = y
                x = X[b, d]
                cnf.extend([[-y, e], [-y, x], [y, -e, -x]])
    S = sum((d - 6) * k for d, k in counts.items())
    natural_budget = S * S - 114 * S + 64 * n - 19 * counts.get(8, 0)
    if budget is None:
        budget = natural_budget
    if budget > natural_budget:
        raise ValueError("Budget exceeds stated identity")

    def q(d, s):
        return (
            (s - 8) ** 2
            if d == 6
            else (s - 7) * (s - 8) if d == 7 else (s - 5) * (s - 9)
        )

    Z = {}
    sinks = []
    cost_lits = []
    cost_weights = []
    for u in range(n):
        if u == 0:
            constant = sum(d - 6 for v, d in fixed.items() if v != 0)
            terms = []
            weights = []
        elif u in fixed:
            constant = fixed[0] - 6
            P = parts[u - 1]
            terms = [X[v, d] for v in P for d in counts if d > 6 and counts[d]]
            weights = [d - 6 for v in P for d in counts if d > 6 and counts[d]]
        else:
            constant = fixed[data["parent"][u]] - 6 if u in data["parent"] else 0
            terms = [y for (v, w, d), y in Y.items() if v == u]
            weights = [d - 6 for (v, w, d), y in Y.items() if v == u]
        possible_degrees = (
            [fixed[u]] if u in fixed else sorted(d for d in counts if counts[d])
        )
        local = []
        scores = []
        for d in possible_degrees:
            maxs = min(
                2 * d,
                n - 1 - 6 * d - (data.get("minimum_high_defect", 0) if d == 8 else 0),
            )
            for s in range(maxs + 1):
                cost = q(d, s)
                if not 0 <= cost <= budget:
                    continue
                if not constant <= s <= constant + sum(weights):
                    continue
                y = pool.id(("localtype", u, d, s))
                Z[u, d, s] = y
                local.append(y)
                scores.append(s)
                if u not in fixed:
                    cnf.append([-y, X[u, d]])
                if cost:
                    cost_lits.append(y)
                    cost_weights.append(cost)
                if d == 8 and s == 5:
                    sinks.append(y)
        cnf.extend(
            CardEnc.equals(
                lits=local, bound=1, vpool=pool, encoding=EncType.seqcounter
            ).clauses
        )
        # Sum(weights * terms) + constant = Sum(scores * selected types).
        # Negated type literals keep every PB coefficient nonnegative.
        cnf.extend(
            PBEnc.equals(
                lits=terms + [-y for y in local],
                weights=weights + scores,
                bound=sum(scores) - constant,
                vpool=pool,
            ).clauses
        )
    cnf.extend(
        PBEnc.atmost(
            lits=cost_lits, weights=cost_weights, bound=budget, vpool=pool
        ).clauses
    )
    minimum_sinks = max(0, counts.get(8, 0) - budget // 5)
    if minimum_sinks:
        cnf.extend(
            CardEnc.atleast(
                lits=sinks, bound=minimum_sinks, vpool=pool, encoding=EncType.seqcounter
            ).clauses
        )
    data["energy"] = dict(
        budget=budget,
        natural_budget=natural_budget,
        types=len(Z),
        minimum_high_sinks=minimum_sinks,
    )
    return Z
