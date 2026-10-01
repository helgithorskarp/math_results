"""Exact integer primitive-block top budgets. No solver or third-party package.

Author: six-covering-3, researcher, 2026-10-01.
This optimizes a necessary covering budget, not covering existence.
"""

from itertools import permutations, product
from math import gcd


def require(condition, message):
    if not condition:
        raise ValueError(message)


def divisors(n):
    return tuple(d for d in range(1, n + 1) if n % d == 0)


def charge(mask):
    """Optimal charge for the marked j mod 6, CRT coordinates (j%2,j%3)."""
    require(type(mask) is int and 0 <= mask < 64, "invalid primitive mask")
    a = c = d = 0
    for col in range(3):
        row0 = bool(mask & (1 << next(j for j in range(6)
                                   if j % 2 == 0 and j % 3 == col)))
        row1 = bool(mask & (1 << next(j for j in range(6)
                                   if j % 2 == 1 and j % 3 == col)))
        a += row0 and not row1
        c += row1 and not row0
        d += row0 and row1
    return 2 * d + max(0, 2 * max(a, c) - 3)


CHARGE = tuple(charge(mask) for mask in range(64))


def sharp_function(mask):
    """A signed proper-period function attaining total -CHARGE[mask]."""
    double = {col for col in range(3)
              if all(mask & (1 << j) for j in range(6) if j % 3 == col)}
    singles = [{col for col in range(3)
                if any(mask & (1 << j) for j in range(6)
                       if j % 2 == row and j % 3 == col)
                and not any(mask & (1 << j) for j in range(6)
                            if j % 2 != row and j % 3 == col)}
               for row in range(2)]
    row = max(range(2), key=lambda r: len(singles[r]))
    values = [-int(j % 3 in double) for j in range(6)]
    if len(singles[row]) >= 2:
        values = [value - int(j % 2 == row) + int(j % 3 not in singles[row])
                  for j, value in enumerate(values)]
    return tuple(values)


def balanced_vertices():
    """All vertices of nonnegative 2x3 arrays with row/column line sums."""
    return tuple(tuple(1 + h[j % 3] if j % 2 == 0 else 1 - h[j % 3]
                       for j in range(6))
                 for h in permutations((-1, 0, 1)))


def validate(B, C, b, u, v, fixed=None):
    require(type(B) is int and B >= 6 and B % 6 == 0, "B must contain 2 and 3")
    rest = B
    for p in (2, 3):
        while rest % p == 0:
            rest //= p
    require(rest == 1, "B must have prime support exactly {2,3}")
    require(type(C) is int and C >= 1 and gcd(B, C) == 1, "invalid cofactor")
    T = B // 6
    require(type(b) is int and b >= 1 and T % b == 0, "b must divide B/6")
    require(len(u) == B and all(len(row) == C for row in u), "wrong u dimensions")
    require(len(v) == b and all(len(row) == C for row in v), "wrong v dimensions")
    require(all(type(x) is int and x >= 0 for row in u for x in row), "invalid u")
    require(all(type(x) is int and x >= 0 for row in v for x in row), "invalid v")
    ds = divisors(C)
    fixed = {} if fixed is None else dict(fixed)
    for d, phase in fixed.items():
        require(d in ds and len(phase) == 2, "invalid fixed top")
        t, r = phase
        require(type(t) is int and 0 <= t < B and type(r) is int and 0 <= r < d,
                "invalid fixed top phase")
        require(all(u[t][z] == 0 for z in range(r, C, d)), "u must vanish on fixed top")
    return T, ds, fixed


def footprints(C, ds, u):
    return tuple(tuple(tuple(sum(row[z] for z in range(r, C, d))
                             for r in range(d)) for row in u) for d in ds)


def literal_charge(C, ds, rs, mask, js, weights):
    """Definition-level sum over cofactor residues for one actual block."""
    value = 0
    for z in range(C):
        points = 0
        for i, d in enumerate(ds):
            if mask & (1 << i) and z % d == rs[i]:
                points |= 1 << js[i]
        value += CHARGE[points] * weights[z]
    return value


def charge35(rs, mask, js, weights):
    """O(1) profile formula for ds=(1,5,7,35); repeated j are set-unioned."""
    require(len(rs) == 4 and len(js) == 4 and len(weights) == 35, "invalid C35 profile")
    r5, r7, s = rs[1:]
    base = (1 << js[0]) if mask & 1 else 0
    row = base | ((1 << js[1]) if mask & 2 else 0)
    col = base | ((1 << js[2]) if mask & 4 else 0)
    both = row | col
    at_s = base
    if s % 5 == r5 and mask & 2:
        at_s |= 1 << js[1]
    if s % 7 == r7 and mask & 4:
        at_s |= 1 << js[2]
    with_s = at_s | ((1 << js[3]) if mask & 8 else 0)
    cross = next(z for z in range(35) if z % 5 == r5 and z % 7 == r7)
    return (CHARGE[row] * sum(weights[z] for z in range(r5, 35, 5))
            + CHARGE[col] * sum(weights[z] for z in range(r7, 35, 7))
            + (CHARGE[both] - CHARGE[row] - CHARGE[col]) * weights[cross]
            + (CHARGE[with_s] - CHARGE[at_s]) * weights[s])


def local_table(B, C, b, ds, rs, q, U, v, fixed, periodic=literal_charge):
    """Maximize each resource subset within this actual label q."""
    T = B // 6
    k = len(ds)
    table = [None] * (1 << k)
    table[0] = 0
    choices = []
    for d in ds:
        if d in fixed:
            t, _ = fixed[d]
            choices.append((t // T,) if t % T == q else ())
        else:
            choices.append(range(6))
    for mask in range(1, 1 << k):
        members = tuple(i for i in range(k) if mask & (1 << i))
        best = None
        for chosen in product(*(choices[i] for i in members)):
            js = [0] * k
            ordinary = 0
            for i, j in zip(members, chosen):
                js[i] = j
                ordinary += U[i][q + T * j][rs[i]]
            value = ordinary + periodic(C, ds, rs, mask, js, v[q % b])
            best = value if best is None else max(best, value)
        table[mask] = best
    return table


def subset_dp(tables, k):
    """Resources placed once; each table belongs to a distinct actual block."""
    full = (1 << k) - 1
    dp = [None] * (1 << k)
    dp[0] = 0
    for table in tables:
        new = [None] * (1 << k)
        for used, value in enumerate(dp):
            if value is None:
                continue
            remaining = full ^ used
            group = remaining
            while True:
                if table[group] is not None:
                    candidate = value + table[group]
                    target = used | group
                    if new[target] is None or candidate > new[target]:
                        new[target] = candidate
                if group == 0:
                    break
                group = (group - 1) & remaining
        dp = new
    require(dp[full] is not None, "no legal top phase assignment")
    return dp[full]


def exact_budget(B, C, b, u, v, fixed=None, work_limit=5000000):
    """All-cofactor exact DP; cap is operational, never an exclusion."""
    T, ds, fixed = validate(B, C, b, u, v, fixed)
    cofactor_choices = tuple((fixed[d][1],) if d in fixed else range(d) for d in ds)
    jobs = T * (7 ** len(ds) - 1)
    for choices in cofactor_choices:
        jobs *= len(choices)
    require(jobs <= work_limit, "reference work cap; no conclusion about covers")
    U = footprints(C, ds, u)
    best = None
    for rs in product(*cofactor_choices):
        tables = [local_table(B, C, b, ds, rs, q, U, v, fixed) for q in range(T)]
        value = subset_dp(tables, len(ds))
        best = value if best is None else max(best, value)
    return best


def actual_value(B, C, b, u, v, phases):
    """Direct definition, retaining all actual top phases and labels."""
    T = B // 6
    ds = divisors(C)
    require(len(phases) == len(ds), "wrong number of top phases")
    ordinary = sum(u[t][z] for d, (t, r) in zip(ds, phases) for z in range(r, C, d))
    periodic = 0
    for q in range(T):
        for z in range(C):
            points = 0
            for d, (t, r) in zip(ds, phases):
                if t % T == q and z % d == r:
                    points |= 1 << (t // T)
            periodic += CHARGE[points] * v[q % b][z]
    return ordinary + periodic
