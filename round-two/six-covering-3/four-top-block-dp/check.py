"""Definition-level exact controls for the written proof and block-label DP."""

import json
from itertools import product
from pathlib import Path
from random import Random
from time import monotonic

from budget import (CHARGE, actual_value, balanced_vertices, charge35, divisors,
                    exact_budget, footprints, literal_charge, local_table,
                    require, sharp_function, subset_dp, validate)


def equal(actual, expected, label):
    if actual != expected:
        raise RuntimeError(f"{label}: {actual!r} != {expected!r}")


def primitive_controls():
    vertices = balanced_vertices()
    for omega in vertices:
        require(all(w >= 0 for w in omega), "negative balanced weight")
        for d in (2, 3):
            for r in range(d):
                equal(sum(omega[j] for j in range(6) if j % d == r), 6 // d,
                      "proper-period moment")
    edges = 0
    for mask in range(64):
        equal(min(sum(omega[j] for j in range(6) if mask & (1 << j))
                  for omega in vertices), CHARGE[mask], "balanced minimum")
        f = sharp_function(mask)
        equal(sum(f), -CHARGE[mask], "sharp signed total")
        for j in range(6):
            require(f[j] >= (-1 if mask & (1 << j) else 0), "sharp signs")
        differences = []
        for c in range(3):
            even = next(j for j in range(6) if j % 2 == 0 and j % 3 == c)
            odd = next(j for j in range(6) if j % 2 == 1 and j % 3 == c)
            differences.append(f[even] - f[odd])
        equal(len(set(differences)), 1, "additive proper-period membership")
        for j in range(6):
            if not mask & (1 << j):
                require(CHARGE[mask] <= CHARGE[mask | (1 << j)], "charge monotonicity")
                edges += 1
    return {"masks": 64, "vertices": len(vertices), "monotone_edges": edges,
            "charge_histogram": {str(c): CHARGE.count(c) for c in sorted(set(CHARGE))}}


def profile_controls():
    rng = Random(803)
    ds = (1, 5, 7, 35)
    phase_cases = ((0, 0, 0, 0), (0, 0, 0, 5), (0, 0, 0, 7), (0, 0, 0, 1),
                   (0, 2, 3, 17), (0, 2, 3, 7), (0, 2, 3, 3), (0, 4, 6, 0))
    count = 0
    for rs in phase_cases:
        weights = [rng.randrange(8) for _ in range(35)]
        for mask in range(16):
            members = tuple(i for i in range(4) if mask & (1 << i))
            for chosen in product(range(6), repeat=len(members)):
                js = [0] * 4
                for i, j in zip(members, chosen):
                    js[i] = j
                equal(charge35(rs, mask, js, weights),
                      literal_charge(35, ds, rs, mask, js, weights), "cofactor profile")
                count += 1
    return {"phase_tuples": len(phase_cases), "set_profile_cases": count}


def literal_maximum(B, C, b, u, v, rs=None, fixed=None):
    fixed = {} if fixed is None else fixed
    ds = divisors(C)
    choices = []
    for i, d in enumerate(ds):
        if d in fixed:
            choices.append((fixed[d],))
        elif rs is not None:
            choices.append(tuple((t, rs[i]) for t in range(B)))
        else:
            choices.append(tuple((t, r) for t in range(B) for r in range(d)))
    return max(actual_value(B, C, b, u, v, phases) for phases in product(*choices))


def optimizer_controls():
    rng = Random(821)
    full_cases = 0
    four_cases = 0
    values = []
    for B in (6, 12, 18):
        T = B // 6
        for b in divisors(T):
            for case in range(2):
                C = 5
                u = [[rng.randrange(4) for _ in range(C)] for _ in range(B)]
                v = [[rng.randrange(3) for _ in range(C)] for _ in range(b)]
                fixed = {} if case == 0 else {1: (T, 0)}
                if fixed:
                    u[T] = [0] * C
                a = exact_budget(B, C, b, u, v, fixed)
                equal(a, literal_maximum(B, C, b, u, v, fixed=fixed), "full-cofactor phases")
                values.append(a)
                full_cases += 1
    for B, b, rs, fixed in (
            (6, 1, (0, 0, 0, 0), {}),
            (6, 1, (0, 2, 3, 1), {}),
            (12, 2, (0, 0, 0, 5), {1: (0, 0)}),
            (12, 2, (0, 2, 3, 17), {5: (7, 2)})):
        C = 35
        u = [[rng.randrange(4) for _ in range(C)] for _ in range(B)]
        v = [[rng.randrange(3) for _ in range(C)] for _ in range(b)]
        for d, (t, r) in fixed.items():
            for z in range(r, C, d):
                u[t][z] = 0
        T, ds, fixed = validate(B, C, b, u, v, fixed)
        U = footprints(C, ds, u)
        tables = [local_table(B, C, b, ds, rs, q, U, v, fixed) for q in range(T)]
        a = subset_dp(tables, len(ds))
        equal(a, literal_maximum(B, C, b, u, v, rs, fixed), "four-resource literal phases")
        values.append(a)
        four_cases += 1
    return {"full_cofactor_cases": full_cases, "four_resource_fixed_cofactor_cases": four_cases,
            "maxima": values}


def partition_relaxation(tables, k):
    """Prior unsafe equality's upper relaxation, intentionally ignoring labels."""
    maxima = [max(value for table in tables if (value := table[mask]) is not None)
              for mask in range(1 << k)]
    dp = [0] * (1 << k)
    for mask in range(1, 1 << k):
        anchor = mask & -mask
        group = mask
        best = None
        while group:
            if group & anchor:
                value = maxima[group] + dp[mask ^ group]
                best = value if best is None else max(best, value)
            group = (group - 1) & mask
        dp[mask] = best
    return dp[-1]


def strict_controls():
    B, C, b = 6, 5, 1
    u = [[10] * C if t == 0 else ([20, 0, 0, 0, 0] if t == 2 else [0] * C)
         for t in range(B)]
    v = [[1, 0, 0, 0, 0]]
    new = exact_budget(B, C, b, u, v)
    equal(new, 71, "strict optimal charge budget")
    old = 0
    for alpha, beta, r in product(range(B), range(B), range(C)):
        old = max(old, sum(u[alpha]) + u[beta][r]
                  + (2 if alpha != beta and r == 0 else 0))
    equal(old, 72, "old distinct-point budget")
    B, C, b = 12, 35, 2
    u = [[10] * C if t in (0, 6) else [0] * C for t in range(B)]
    v = [[int(z == 0) for z in range(C)], [0] * C]
    rs = (0, 0, 0, 0)
    U = footprints(C, divisors(C), u)
    tables = [local_table(B, C, b, divisors(C), rs, q, U, v, {}) for q in range(2)]
    exact = subset_dp(tables, 4)
    relaxed = partition_relaxation(tables, 4)
    equal(exact, 482, "actual-label budget")
    equal(relaxed, 484, "independent-group relaxation")
    return {"optimal_charge_fixture": {"old": old, "new": new},
            "label_fixture": {"exact": exact, "independent_group_upper": relaxed}}


def invalid_controls():
    B, C, b = 6, 5, 1
    u, v = [[0] * C for _ in range(B)], [[0] * C]
    cases = (lambda: exact_budget(30, C, b, [[0] * C for _ in range(30)], v),
             lambda: exact_budget(B, C, 2, u, [[0] * C, [0] * C]),
             lambda: exact_budget(B, 3, b, [[0] * 3 for _ in range(B)], [[0] * 3]),
             lambda: exact_budget(B, C, b, u, v, {5: (6, 0)}),
             lambda: exact_budget(B, C, b, u, v, work_limit=0),
             lambda: exact_budget(B, C, b, u, [[-1] * C]))
    for i, run in enumerate(cases):
        try:
            run()
        except ValueError:
            continue
        raise RuntimeError(f"malformed input {i} accepted")
    return len(cases)


def cover_controls():
    """Literal coverage/footprints, with known tops and positive known weights."""
    B, C, N, b = 12, 5, 60, 2
    T = B // 6
    ds = divisors(C)
    base = ((2, 0), (3, 0), (4, 1), (6, 1), (12, 11))
    require(all(any(x % n == a for n, a in base) for x in range(N)), "control is not a cover")
    rng = Random(851)
    cases = negative = positive_known = 0
    for translation in range(4):
        cover = tuple((n, (a + translation) % n) for n, a in base)
        full = cover + ((N, (7 + translation) % N),)
        phases = tuple((next(a % B for n, a in full if n == B * d),
                        next(a % d for n, a in full if n == B * d)) for d in ds)
        for known_mask in range(1 << len(cover)):
            known = tuple(item for i, item in enumerate(cover) if known_mask & (1 << i))
            for variant in range(2):
                weight = [rng.randrange(6) for _ in range(N)]
                u_x = [0 if any(x % n == a for n, a in known) else weight[x] for x in range(N)]
                v_base = [rng.randrange(6) if variant == 0 else 1 for _ in range(b * C)]
                v_x = [v_base[x % (b * C)] for x in range(N)]
                u = [[u_x[next(x for x in range(N) if x % B == t and x % C == z)]
                      for z in range(C)] for t in range(B)]
                v = [[v_base[next(x for x in range(b * C) if x % b == q and x % C == z)]
                      for z in range(C)] for q in range(b)]
                top = {B * d for d in ds}
                known_outside = tuple((n, a) for n, a in known if n not in top)
                free_outside = tuple((n, a) for n, a in full if n not in top and (n, a) not in known)
                lhs = sum(u_x) + sum(v_x) - sum(v_x[x] for n, a in known_outside
                                                for x in range(a, N, n))
                rhs = sum(u_x[x] + v_x[x] for n, a in free_outside for x in range(a, N, n))
                rhs += actual_value(B, C, b, u, v, phases)
                require(lhs <= rhs, "actual-phase completion inequality fails")
                # Separate literal periodic demand check; prescribed top footprints
                # stay on the right through the marked-point charge.
                known_top = tuple((n, a) for n, a in known if n in top)
                positive_known += any(v_x[x] > 0 for n, a in known_top for x in range(a, N, n))
                negative += lhs < 0
                cases += 1
    return {"actual_phase_cases": cases, "positive_known_top_cases": positive_known,
            "negative_effective_demands": negative}


def main():
    started = monotonic()
    result = {"primitive": primitive_controls(), "profiles": profile_controls(),
              "optimizers": optimizer_controls(), "strict": strict_controls(),
              "covers": cover_controls(), "rejected_inputs": invalid_controls()}
    expected = Path(__file__).with_name("expected-python.json")
    if expected.exists():
        equal(result, json.loads(expected.read_text()), "published Python output")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"Elapsed author check: {monotonic() - started:.3f}s", file=__import__('sys').stderr)


if __name__ == "__main__":
    main()
