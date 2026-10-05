#!/usr/bin/env python3
"""Independent bounds, not a replacement for a complete CFSG catalogue proof.

CPython 3.11+, standard library only. The finite catalogue interface and
structural torus bounds are documented in BASE_CHECK.md. No GAP class data
or author's count output is read. Permutations map 0-based points to images;
compose(g,h) means g after h. Cyclic subgroups are literal sets of permutations.
"""

from collections import Counter, deque
from fractions import Fraction
from itertools import permutations
from math import factorial, gcd, isqrt, lcm
from pathlib import Path
import argparse
import hashlib
import json


def primes_of(n):
    if n < 1:
        raise ValueError("positive integer required")
    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ans.append(n)
    return ans


def prime_powers(limit):
    ans = {}
    for p in range(2, limit + 1):
        if primes_of(p) != [p]:
            continue
        q, f = p, 1
        while q <= limit:
            if q in ans:
                raise AssertionError("duplicate prime-power parametrization")
            ans[q] = (p, f)
            q *= p
            f += 1
    return sorted(ans.items())


def tau(n):
    answer = 1
    for p in primes_of(n):
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        answer *= exponent + 1
    return answer


def psl2_partition_count(q):
    p = primes_of(q)[0]
    d = gcd(2, q - 1)
    # One cyclic subgroup per p-1 unipotent generators; every other
    # nontrivial cyclic subgroup lies in a unique maximal torus.
    return (1 + (q*q - 1)//(p - 1)
            + q*(q + 1)//2 * (tau((q - 1)//d) - 1)
            + q*(q - 1)//2 * (tau((q + 1)//d) - 1))


def psl2_partition_histogram(q):
    p = primes_of(q)[0]
    d = gcd(2, q - 1)
    hist = Counter({1: 1, p: q*q - 1})
    for order, multiplicity in (((q - 1)//d, q*(q + 1)//2),
                                ((q + 1)//d, q*(q - 1)//2)):
        for e in range(2, order + 1):
            if order % e == 0:
                phi_e = sum(gcd(a, e) == 1 for a in range(1, e + 1))
                hist[e] += multiplicity * phi_e
    if sum(hist.values()) != q*(q*q - 1)//d:
        raise AssertionError("PSL2 partition does not cover group order")
    return dict(sorted(hist.items()))


def suzuki8_partition_count():
    q, plus, minus = 8, 13, 5
    sylow_nontrivial = (q*q + 1) * ((q - 1) + (q*q - q)//2)
    split = q*q * (q*q + 1)//2 * (tau(q - 1) - 1)
    high = q*q * (q - 1) * minus//4 * (tau(plus) - 1)
    low = q*q * (q - 1) * plus//4 * (tau(minus) - 1)
    return 1 + sylow_nontrivial + split + high + low


def suzuki8_partition_histogram():
    q, plus, minus = 8, 13, 5
    return {1: 1, 2: (q*q + 1)*(q - 1),
            4: (q*q + 1)*(q*q - q),
            5: q*q*(q - 1)*plus//4 * (minus - 1),
            7: q*q*(q*q + 1)//2 * (q - 2),
            13: q*q*(q - 1)*minus//4 * (plus - 1)}


def compose(g, h):
    return tuple(g[h[i]] for i in range(len(g)))


def perm_order(g):
    seen = set()
    order = 1
    for i in range(len(g)):
        if i in seen:
            continue
        j, length = i, 0
        while j not in seen:
            seen.add(j)
            j = g[j]
            length += 1
        if j != i:
            raise AssertionError("invalid permutation cycle")
        order = lcm(order, length)
    return order


def perm_from_cycles(n, cycles):
    g = list(range(n))
    used = set()
    for cycle in cycles:
        if used.intersection(cycle):
            raise ValueError("cycles must be disjoint")
        used.update(cycle)
        for i, point in enumerate(cycle):
            g[point - 1] = cycle[(i + 1) % len(cycle)] - 1
    if sorted(g) != list(range(n)):
        raise AssertionError("malformed generator")
    return tuple(g)


def even(g):
    return sum(g[i] > g[j] for i in range(len(g))
               for j in range(i + 1, len(g))) % 2 == 0


def closure(n, generators, expected_order):
    identity = tuple(range(n))
    group = {identity}
    todo = deque([identity])
    while todo:
        g = todo.popleft()
        for h in generators:
            gh = compose(g, h)
            if gh not in group:
                group.add(gh)
                todo.append(gh)
                if len(group) > expected_order:
                    raise AssertionError("generator closure exceeds expected order")
    if len(group) != expected_order:
        raise AssertionError("incomplete or wrong generated group")
    return group


def cyclic_count(group):
    n = len(next(iter(group)))
    identity = tuple(range(n))
    cyclic = set()
    histogram = Counter()
    for g in group:
        order = perm_order(g)
        histogram[order] += 1
        powers = []
        h = identity
        for _ in range(order):
            if h not in group:
                raise AssertionError("power outside represented group")
            powers.append(h)
            h = compose(h, g)
        if h != identity or len(set(powers)) != order:
            raise AssertionError("cycle-order and power-order disagree")
        cyclic.add(frozenset(powers))
    if sum(histogram.values()) != len(group):
        raise AssertionError("histogram is incomplete")
    # This second identity checks literal set canonicalization. It is not
    # presented as independence from the permutation enumeration itself.
    def phi(t):
        return sum(gcd(a, t) == 1 for a in range(1, t + 1))
    weighted = sum((Fraction(count, phi(order))
                    for order, count in histogram.items()), Fraction())
    if weighted != len(cyclic):
        raise AssertionError("literal and element-order counts disagree")
    return {"order": len(group), "cyclic_count": len(cyclic),
            "element_order_histogram": dict(sorted(histogram.items()))}


def literal_controls():
    result = {}
    for n in (5, 6, 7):
        group = {g for g in permutations(range(n)) if even(g)}
        if len(group) != factorial(n) // 2:
            raise AssertionError("alternating permutation order mismatch")
        result[f"A{n}"] = cyclic_count(group)
    result["S5"] = cyclic_count(set(permutations(range(5))))
    # Standard natural generators from the primary ATLAS M11 page.
    a = perm_from_cycles(11, [(2, 10), (4, 11), (5, 7), (8, 9)])
    b = perm_from_cycles(11, [(1, 4, 3, 8), (2, 5, 6, 9)])
    if (perm_order(a), perm_order(b), perm_order(compose(a, b))) != (2, 4, 11):
        raise AssertionError("ATLAS generator order check failed")
    result["M11"] = cyclic_count(closure(11, (a, b), 7920))
    if result["A5"]["cyclic_count"] != 32 or result["S5"]["cyclic_count"] != 67:
        raise AssertionError("hand-checkable A5/S5 normalization failed")
    return result


def catalogue_rows(limit):
    rows = []
    for n in range(5, 10):
        rows.append({"name": f"A{n}", "order": factorial(n) // 2,
                     "outer_order": 4 if n == 6 else 2})
    # q>=114 already has q(q^2-1)/2 > limit. Skip the duplicate
    # presentations PSL(2,4), PSL(2,5)=A5 and PSL(2,9)=A6.
    if 114 * (114**2 - 1) // 2 <= limit:
        raise AssertionError("prime-power parameter bound is invalid")
    for q, (_, f) in prime_powers(113):
        if q < 4 or q in (4, 5, 9):
            continue
        d = gcd(2, q - 1)
        order = q * (q*q - 1) // d
        if order <= limit:
            rows.append({"name": f"PSL(2,{q})", "q": q,
                         "order": order, "outer_order": d * f})
    # Higher-rank/Suzuki/sporadic portion: primary simple-by-order table.
    # These data DO NOT certify that no other family can occur.
    others = [
        ("PSL(3,3)", 5616, 2), ("PSU(3,3)", 6048, 2),
        ("PSL(3,4)", 20160, 12), ("PSp(4,3)", 25920, 2),
        ("Sz(8)", 29120, 3), ("PSU(3,4)", 62400, 4),
        ("PSU(3,5)", 126000, 6), ("PSL(3,5)", 372000, 2),
        ("M11", 7920, 1), ("M12", 95040, 2),
        ("J1", 175560, 1), ("M22", 443520, 2), ("J2", 604800, 2),
    ]
    rows.extend({"name": name, "order": order, "outer_order": out}
                for name, order, out in others if order <= limit)
    if len(rows) != 53 or len({r["name"] for r in rows}) != 53:
        raise AssertionError("expected finite catalogue interface changed")
    return sorted(rows, key=lambda row: (row["order"], row["name"]))


def compare_evidence(path, rows, controls):
    data = path.read_bytes()
    author = json.loads(data)
    by_name = {row["name"]: row for row in rows}
    names = set()
    for claim in author["counts"]:
        name = claim["name"]
        if name == "L3(2)":
            name = "PSL(2,7)"
        elif name.startswith("L2("):
            name = "PSL(2," + name[3:]
        if name in names:
            raise AssertionError("duplicate author count")
        names.add(name)
        row = by_name[name]
        if name in controls:
            independent = controls[name]
            count = independent["cyclic_count"]
            histogram = independent["element_order_histogram"]
        else:
            count = row["partition_exact_count"]
            histogram = row["partition_order_histogram"]
        observed = Counter()
        for order, size in zip(claim["class_orders"], claim["class_sizes"], strict=True):
            if order < 1 or size < 1:
                raise AssertionError("malformed conjugacy-class evidence")
            observed[order] += size
        if (claim["order"] != row["order"] or count != claim["cyclic_count"]
                or histogram != dict(observed)):
            raise AssertionError(f"independent evidence disagrees for {name}")
    required = {row["name"] for row in rows
                if row["method"] != "Lucchini square-root bound"}
    if names != required:
        raise AssertionError("author count coverage differs from residual catalogue")
    return {"input_sha256": hashlib.sha256(data).hexdigest(),
            "matched_cyclic_counts": len(names),
            "matched_complete_order_histograms": len(names),
            "status": "INDEPENDENT_COUNTS_MATCH"}


def compare_catalogue(path, rows):
    data = path.read_bytes()
    author = json.loads(data)
    remaining = {row["name"]: row for row in rows}
    for claim in author["rows"]:
        name = claim["name"]
        if name == "L3(2)":
            name = "PSL(2,7)"
        elif name == "U4(2)":
            name = "PSp(4,3)"
        elif name.startswith("L2("):
            name = "PSL(2," + name[3:]
        elif name.startswith("L3("):
            name = "PSL(3," + name[3:]
        elif name.startswith("U3("):
            name = "PSU(3," + name[3:]
        row = remaining.pop(name)
        if ((row["order"], row["outer_order"], row["aut_primes"])
                != (claim["order"], claim["out_order"], claim["aut_primes"])):
            raise AssertionError(f"catalogue metadata disagrees for {name}")
        if ((row["method"] == "Lucchini square-root bound")
                != claim["automatic_exclusion"]):
            raise AssertionError(f"automatic exclusion disagrees for {name}")
    if remaining or author["bound"] != 724052:
        raise AssertionError("catalogue comparison is incomplete")
    return {"input_sha256": hashlib.sha256(data).hexdigest(),
            "matched_rows_and_prime_supports": len(rows),
            "status": "INDEPENDENT_CATALOGUE_METADATA_MATCH"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compare-evidence", type=Path)
    parser.add_argument("--compare-catalogue", type=Path)
    args = parser.parse_args()
    gamma_six = Fraction(8388608, 15015) * 6**4
    limit = -(-gamma_six.numerator // gamma_six.denominator)
    if limit != 724052:
        raise AssertionError("quotient bound mismatch")
    # Initial conservative bounds in the author's full family-cutoff audit.
    # Monotonicity in rank/field is a written argument, not finite sampling.
    cutoffs = {
        "A10": factorial(10)//2,
        "PSL2 q114": 114*(114**2 - 1)//2,
        "PSL3 q7": 7**3*(7**2 - 1)*(7**3 - 1)//3,
        "PSU3 q7": 7**3*(7**2 - 1)*(7**3 + 1)//3,
        "PSL4 q3": 3**6*(3**2 - 1)*(3**3 - 1)*(3**4 - 1)//4,
        "PSU4 q3": 3**6*(3**2 - 1)*(3**3 + 1)*(3**4 - 1)//4,
        "PSL n5 q2": 2**10*3*7*15*31//5,
        "PSU n5 q2": 2**10*3*9*15*33//5,
        "Sp rank3 q2": 2**9*3*15*63//2,
        "Sp rank2 q4": 4**4*(4**2 - 1)*(4**4 - 1),
        "Sp rank2 q5": 5**4*(5**2 - 1)*(5**4 - 1)//2,
        "even orth rank4 q2": 2**12*15*3*15*63//4,
        "G2 q3": 3**6*(3**6 - 1)*(3**2 - 1),
        "3D4 q2": 2**12*(2**8 + 2**4 + 1)*(2**6 - 1)*(2**2 - 1),
        "F4 q2 power": 2**24,
        "E6 and 2E6 q2 power": 2**36//3,
        "E7 q2 power": 2**63//2,
        "E8 q2 power": 2**120,
        "Sz q32": 32**2*(32**2 + 1)*(32 - 1),
        "Ree q27": 27**3*(27**3 + 1)*(27 - 1),
        "Tits": 17971200,
        "large 2F4 q8 power": 8**12,
        "next sporadic M23": 10200960,
    }
    if min(cutoffs.values()) <= limit:
        raise AssertionError("family cutoff fails the finite order bound")
    controls = literal_controls()
    rows = catalogue_rows(limit)
    for row in rows:
        n = row["order"]
        prime_support = primes_of(n * row["outer_order"])
        target = 6 * 2**len(prime_support)
        row.update(aut_primes=prime_support, target=target)
        if "q" in row and n <= target * target:
            row["partition_exact_count"] = psl2_partition_count(row["q"])
            row["partition_order_histogram"] = psl2_partition_histogram(row["q"])
        elif row["name"] == "Sz(8)":
            row["partition_exact_count"] = suzuki8_partition_count()
            row["partition_order_histogram"] = suzuki8_partition_histogram()
            if sum(row["partition_order_histogram"].values()) != n:
                raise AssertionError("Suzuki partition does not cover group order")
        if row["name"] == "A5":
            row.update(method="literal permutation exception",
                       cyclic_lower_bound=32, outcome="allowed simple base")
            continue
        if n > target * target:
            lower = isqrt(n) + (isqrt(n)**2 < n)
            method = "Lucchini square-root bound"
        elif "q" in row:
            lower = row["q"]**2 + 1
            method = "two torus classes plus identity"
        elif row["name"] == "Sz(8)":
            lower = 8**4 + 1
            method = "three torus classes plus identity"
        elif row["name"] in controls:
            lower = controls[row["name"]]["cyclic_count"]
            method = "literal permutation cyclic-subgroup count"
        else:
            raise AssertionError(f"uncovered row {row}")
        if lower <= target:
            raise AssertionError(f"insufficient threshold-6 bound {row}")
        row.update(method=method, cyclic_lower_bound=lower, outcome="excluded")
    if controls["S5"]["cyclic_count"] <= 6 * 2**len(primes_of(120)):
        raise AssertionError("proper A5 overgroup not excluded")
    if psl2_partition_count(4) != 32 or psl2_partition_count(9) != controls["A6"]["cyclic_count"]:
        raise AssertionError("exceptional-isomorphism partition check failed")
    result = {
        "claim_status": "independent finite bounds; catalogue completeness imported separately",
        "gamma_times_six_fourth": str(gamma_six), "quotient_order_limit": limit,
        "family_cutoff_initial_lower_bounds": cutoffs,
        "simple_rows": len(rows), "excluded_simple_rows": len(rows) - 1,
        "methods": dict(sorted(Counter(row["method"] for row in rows).items())),
        "literal_controls": controls, "rows": rows,
        "proper_A5_overgroup": {"name": "S5", "count": controls["S5"]["cyclic_count"],
                                 "target": 48, "outcome": "excluded"},
    }
    if args.compare_evidence:
        result["independent_comparison"] = compare_evidence(args.compare_evidence, rows, controls)
    if args.compare_catalogue:
        result["catalogue_comparison"] = compare_catalogue(args.compare_catalogue, rows)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
