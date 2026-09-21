#!/usr/bin/env python3
"""Exact, dependency-free validation; not a finite proof of the general theorem."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parameters(n, k):
    require(type(n) is int and type(k) is int and 1 <= k <= n,
            "expected integers 1 <= k <= n")


def vertices(n, k):
    parameters(n, k)
    ans = []
    for support in combinations(range(n), k):
        for signs in product((-1, 1), repeat=k):
            v = [0] * n
            for i, s in zip(support, signs):
                v[i] = s
            ans.append(tuple(v))
    return sorted(ans)


def inequalities(n, k):
    """The original H-description, independent of the support criterion."""
    parameters(n, k)
    rows = set()
    for i in range(n):
        for s in (-1, 1):
            a = [0] * n
            a[i] = s
            rows.add((tuple(a), 1))
    for a in product((-1, 1), repeat=n):
        rows.add((a, k))
    return sorted(rows)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def active_normals(v, rows):
    require(all(dot(a, v) <= b for a, b in rows), "infeasible vertex")
    return [a for a, b in rows if dot(a, v) == b]


def normal_test(d, active):
    return all(dot(a, d) < 0 for a in active)


def support_test(v, d):
    require(len(v) == len(d) and any(d), "invalid direction")
    inside = [i for i, x in enumerate(v) if x]
    return (all(v[i] * d[i] < 0 for i in inside)
            and 2 * sum(abs(d[i]) for i in inside) > sum(map(abs, d)))


def displacement_test(v, d, k):
    """Evaluate strict body membership at a uniform rational small step."""
    t = Fraction(1, 4 * sum(map(abs, d)) + 1)
    x = tuple(Fraction(a) + t * b for a, b in zip(v, d))
    return max(map(abs, x)) < 1 and sum(map(abs, x)) < k


def solve_square(rows):
    """Exact Gauss-Jordan on a selected square subsystem; None if singular."""
    n = len(rows)
    a = [[Fraction(x) for x in normal] + [Fraction(rhs)]
         for normal, rhs in rows]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        z = a[j][j]
        a[j] = [x / z for x in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                z = a[i][j]
                a[i] = [x - z * y for x, y in zip(a[i], a[j])]
    return tuple(a[i][-1] for i in range(n))


def capacity(n, k):
    return comb(n - 1, k - 1) if 2 * k <= n else comb(n, k)


def primal(n, k):
    parameters(n, k)
    signs = list(product((-1, 1), repeat=n))
    if 2 * k > n:
        return [(d, Fraction(1, 2 ** (n - k))) for d in signs]
    weight = Fraction(1, k * 2 ** (n - k))
    return [(tuple(s * (n if i == j else 1) for i, s in enumerate(d)), weight)
            for j in range(n) for d in signs]


def array_check(rows, n, k):
    parameters(n, k)
    require(rows and all(len(r) == n and all(type(x) is int and x in (0, 1)
                                           for x in r) for r in rows),
            "malformed binary array")
    patterns = set(product((0, 1), repeat=k))
    return all({tuple(r[i] for i in f) for r in rows} == patterns
               for f in combinations(range(n), k))


def check_all():
    counts = Counter()
    digest = hashlib.sha256()

    def record(*items):
        digest.update(json.dumps(items, separators=(",", ":")).encode() + b"\n")

    # Independent vertex completeness: enumerate all bases of the H-system.
    for n, k in [(n, k) for n in range(1, 4) for k in range(1, n + 1)] + [(4, 2)]:
        hs = inequalities(n, k)
        actual = set()
        for basis in combinations(hs, n):
            counts["linear_bases"] += 1
            x = solve_square(basis)
            if x is not None and all(dot(a, x) <= b for a, b in hs):
                actual.add(x)
        expect = set(vertices(n, k))
        require(actual == expect, "H-basis vertex enumeration disagrees")
        counts["vertex_systems"] += 1
        counts["enumerated_vertices"] += len(actual)
        record("vertices", n, k, sorted(expect))

    # Full signed direction grids, with zeros and exact ties included.
    for n in range(1, 5):
        for k in range(1, n + 1):
            vs = vertices(n, k)
            hs = inequalities(n, k)
            active = [active_normals(v, hs) for v in vs]
            best = 0
            for d in product(range(-2, 3), repeat=n):
                if not any(d):
                    continue
                total = 0
                rounded = tuple(1 if x >= 0 else -1 for x in d)
                flags = []
                for v, ac in zip(vs, active):
                    actual = normal_test(d, ac)
                    require(actual == support_test(v, d), "entering criterion disagrees")
                    require(actual == displacement_test(v, d, k), "displacement disagrees")
                    if actual and 2 * k > n:
                        require(normal_test(rounded, ac), "sign rounding lost a vertex")
                        counts["rounding_incidences"] += 1
                    total += actual
                    flags.append(int(actual))
                    counts["grid_vertex_direction_pairs"] += 1
                require(total <= capacity(n, k), "capacity exceeded in grid")
                best = max(best, total)
                record("grid", n, k, d, flags)
            counts["grid_systems"] += 1
            record("grid_best", n, k, best)

    # All absolute-value multisets from {0,1,2,n}, through n=8.
    # Sign changes and coordinate permutations preserve capacities. Each
    # candidate is checked against active H-normals, not just weight sums.
    for n in range(1, 9):
        for k in range(1, n + 1):
            hs = inequalities(n, k)
            minus_vertices = [tuple(-int(i in f) for i in range(n))
                              for f in combinations(range(n), k)]
            active = [active_normals(v, hs) for v in minus_vertices]
            best = 0
            for d in combinations_with_replacement(sorted({0, 1, 2, n}), n):
                if not any(d):
                    continue
                cover = [normal_test(d, ac) for ac in active]
                require(sum(cover) <= capacity(n, k), "multiset capacity exceeded")
                for v, flag in zip(minus_vertices, cover):
                    require(flag == support_test(v, d), "multiset criterion disagrees")
                best = max(best, sum(cover))
                counts["capacity_multisets"] += 1
                record("capacity", n, k, d, [int(x) for x in cover])
            require(best == capacity(n, k), "capacity witness missing")
            counts["capacity_systems"] += 1

    # Replay every incidence in the exact finite fractional primal certificate.
    for n in range(1, 7):
        for k in range(1, n + 1):
            vs = vertices(n, k)
            hs = inequalities(n, k)
            active = [active_normals(v, hs) for v in vs]
            certificate = primal(n, k)
            loads = [Fraction(0) for _ in vs]
            for d, weight in certificate:
                flags = [normal_test(d, ac) for ac in active]
                require(sum(flags) == capacity(n, k), "primal column not maximum")
                for i, flag in enumerate(flags):
                    if flag:
                        loads[i] += weight
                counts["primal_incidences"] += len(vs)
                record("primal", n, k, d, str(weight), [int(x) for x in flags])
            require(all(x == 1 for x in loads), "fractional primal load not one")
            mass = sum(w for _, w in certificate)
            dual = Fraction(len(vs), capacity(n, k))
            theorem = 2 ** k * (Fraction(n, k) if 2 * k <= n else Fraction(1))
            require(mass == dual == theorem, "primal/dual objective mismatch")
            counts["fractional_systems"] += 1
            record("objectives", n, k, str(mass), str(dual))

    fixture = json.loads((HERE / "witness.json").read_text())
    rows = fixture["rows"]
    require(array_check(rows, 5, 3), "ten-row certificate invalid")
    require(len(rows) == 10 and len(set(map(tuple, rows))) == 10, "wrong witness size")
    vs = vertices(5, 3)
    active = [active_normals(v, inequalities(5, 3)) for v in vs]
    dirs = [tuple(2 * bit - 1 for bit in row) for row in rows]
    require(all(any(normal_test(d, ac) for d in dirs) for ac in active),
            "array to illumination conversion failed")
    counts["witness_vertices"] = len(vs)
    record("ten_row_witness", rows)

    # Parity arrays attain the equality case in all these representative sizes.
    for n in range(2, 8):
        rows_p = [r + (sum(r) % 2,) for r in product((0, 1), repeat=n - 1)]
        require(array_check(rows_p, n, n - 1), "parity array failed")
        counts["parity_arrays"] += 1
        record("parity", n, rows_p)

    # Exhaust all potential extra columns over k=2 and k=3 full arrays:
    # precisely the two parity functions can retain strength k.
    for k in (2, 3):
        base = list(product((0, 1), repeat=k))
        valid = []
        for f in product((0, 1), repeat=2 ** k):
            counts["extra_functions"] += 1
            if array_check([r + (b,) for r, b in zip(base, f)], k + 1, k):
                valid.append(f)
        parity = tuple(sum(r) % 2 for r in base)
        require(set(valid) == {parity, tuple(1 - x for x in parity)},
                "extra-column characterization failed")
        for f in valid:
            for g in valid:
                require(not array_check([r + (a, b) for r, a, b in zip(base, f, g)],
                                        k + 2, k), "two extra columns wrongly accepted")
                counts["rejected_double_extensions"] += 1
        record("extra_functions", k, valid)

    # Negative controls and malformed-certificate rejection.
    require(not array_check(rows[:-1], 5, 3), "deleted row not detected")
    counts["negative_controls"] += 1
    require(not any(normal_test((1, 1, 1, 1), active_normals(v, inequalities(4, 2)))
                    for v in vertices(4, 2)), "strict threshold tie accepted")
    counts["negative_controls"] += 1
    require(not support_test((-1, -1, 0), (1, 0, 0)), "zero support coordinate accepted")
    counts["negative_controls"] += 1
    broken = primal(5, 3)[1:]
    require(any(sum(w for d, w in broken if normal_test(d, ac)) < 1 for ac in active),
            "fractional certificate deletion not detected")
    counts["negative_controls"] += 1
    for action in (lambda: parameters(0, 0), lambda: parameters(2, 3),
                   lambda: parameters(3, 1.5), lambda: array_check([[0, 2]], 2, 1),
                   lambda: array_check([[0]], 2, 1),
                   lambda: support_test((-1, 0), (0, 0))):
        try:
            action()
        except ValueError:
            counts["negative_controls"] += 1
        else:
            raise ValueError("malformed input accepted")

    return {"schema": 1, "status": "pass", "counts": dict(sorted(counts.items())),
            "entrywise_sha256": digest.hexdigest(),
            "example": {"n": 5, "k": 3, "ordinary": 10, "fractional": "8",
                        "one_direction_capacity": 10, "vertices": 80},
            "scope": "Finite exact validation; all-parameter proof is in PROOF.md."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="emit without expected.json comparison")
    args = parser.parse_args()
    result = check_all()
    if not args.emit:
        expected = json.loads((HERE / "expected.json").read_text())
        require(result == expected, "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
