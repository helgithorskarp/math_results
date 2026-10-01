#!/usr/bin/env python3
"""Full definition-level exact checks; no research-package or solver imports."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def rational_matrix(a):
    n = len(a)
    require(n > 0 and all(len(row) == n for row in a), "nonsquare matrix")
    return [[F(x) for x in row] for row in a]


def psd_rank(a):
    """Exact symmetric Schur elimination, including singular residuals."""
    a = rational_matrix(a)
    n = len(a)
    require(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
            "nonsymmetric PSD input")
    rank = 0
    for k in range(n):
        pivot = a[k][k]
        require(pivot >= 0, "negative PSD pivot")
        if pivot == 0:
            require(all(a[k][j] == 0 for j in range(k + 1, n)),
                    "zero PSD pivot with nonzero residual")
            continue
        rank += 1
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return rank


def rank(a):
    """General exact Gaussian elimination; used for full spectral nullities."""
    a = rational_matrix(a)
    n = len(a)
    k = 0
    for col in range(n):
        pivot = next((i for i in range(k, n) if a[i][col] != 0), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        for i in range(k + 1, n):
            q = a[i][col] / a[k][col]
            if q:
                for j in range(col, n):
                    a[i][j] -= q * a[k][j]
        k += 1
        if k == n:
            break
    return k


def family_star(family):
    require(family and family[0] == 0 and len(set(family)) == len(family),
            "bad family indexing")
    require(all(isinstance(a, int) and a >= 0 for a in family), "bad set mask")
    present = set(family)
    for a in family:
        sub = a
        while True:
            require(sub in present, "family is not a downset")
            if sub == 0:
                break
            sub = (sub - 1) & a
    require(len(family) >= 2, "trivial family")
    return max(sum(bool(a & (1 << i)) for a in family)
               for i in range(max(family).bit_length()))


def fingerprint(a):
    encoded = json.dumps([[str(x) for x in row] for row in a],
                         separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def check(family, a, s):
    a = rational_matrix(a)
    n = len(family)
    require(len(a) == n and family_star(family) == s, "wrong dimension or star")
    require(0 < s <= n // 2, "invalid largest-star bound")
    for i in range(n):
        require(sum(a[i]) == 1, "wrong row sum")
        for j in range(n):
            require(a[i][j] == a[j][i], "nonsymmetric certificate")
            if family[i] & family[j]:
                require(a[i][j] == 0, "intersecting entry is nonzero")
    lower = [[(n - s) * a[i][j] + s * int(i == j)
              for j in range(n)] for i in range(n)]
    upper = [[F(int(i == j)) - a[i][j] for j in range(n)] for i in range(n)]
    return {"N": n, "s": s, "lower_rank": psd_rank(lower),
            "upper_rank": psd_rank(upper), "matrix_sha256": fingerprint(a)}


def lift(c, s):
    """Core constructor, distinct from the factor-entry union constructor."""
    c = rational_matrix(c)
    m = len(c)
    n = m + 1
    rows = [sum(row) for row in c]
    q = [[sum(rows)] + [-v for v in rows]]
    q += [[-rows[i]] + c[i] for i in range(m)]
    return [[(q[i][j] + 1 - s * int(i == j)) / (n - s)
             for j in range(n)] for i in range(n)]


def core(a, s):
    n = len(a)
    return [[(n - s) * a[i][j] + s * int(i == j) - 1
             for j in range(1, n)] for i in range(1, n)]


def cube(n):
    family = list(range(1 << n))
    full = (1 << n) - 1
    a = [[F(int(b == (full ^ c))) for b in family] for c in family]
    return family, a, 1 << (n - 1), "cube" + str(n)


def proper_cube(n):
    full = (1 << n) - 1
    family = list(range(full))
    s = (1 << (n - 1)) - 1
    a = [[F(0) for _ in family] for _ in family]
    a[0][0] = F(1 - s, s + 1)
    for i in range(1, full):
        a[0][i] = a[i][0] = F(1, s + 1)
        a[i][full ^ i] = F(s, s + 1)
    return family, a, s, "proper_cube" + str(n)


def partition(family, colors, s, label):
    require(len(colors) == len(family) - 1, "bad color dimensions")
    for i, a in enumerate(family[1:]):
        for j, b in enumerate(family[1:]):
            if i != j and colors[i] == colors[j]:
                require((a & b) == 0, "invalid disjoint color class")
    c = [[F(s * int(x == y) - 1) for y in colors] for x in colors]
    return family, lift(c, s), s, label


def path3():
    # Classes {pair12,singleton3}, {pair13,singleton2}, {singleton1}.
    return partition([0, 1, 2, 3, 4, 5], [2, 1, 0, 0, 1], 3, "path3")


def matching2():
    # Two disjoint pairs; each color class has three members.
    return partition([0, 1, 2, 3, 4, 8, 12], [1, 1, 0, 0, 0, 1],
                     2, "matching2")


def uniform_rank2(n):
    require(n >= 3, "rank-two projection needs n>=3")
    family = sorted([0] + [1 << i for i in range(n)]
                    + [(1 << i) | (1 << j) for i, j in combinations(range(n), 2)])
    nonempty = family[1:]
    c = []
    for a in nonempty:
        row = []
        for b in nonempty:
            if a == b:
                v = F(n - 1)
            elif a & b or (a.bit_count() == b.bit_count() == 1):
                v = F(-1)
            else:
                v = F(2, n - 2)
            row.append(v)
        c.append(row)
    return family, lift(c, n), n, "uniform_rank2_" + str(n)


def union_parts(parts, equal=True):
    require(len(parts) >= 2, "union needs at least two parts")
    stars = [p[2] for p in parts]
    require(not equal or len(set(stars)) == 1, "unequal stars")
    s = max(stars)
    # Fresh coordinate blocks. Their positive masks cannot collide.
    family = [0]
    offset = 0
    for f, _, _, _ in parts:
        family += [a << offset for a in f[1:]]
        offset += max(f).bit_length()
    n = len(family)
    c = [[F(0) for _ in range(n - 1)] for _ in range(n - 1)]
    start = 0
    for f, a, sj, _ in parts:
        cj = core(a, sj)
        for i in range(len(cj)):
            for j in range(len(cj)):
                c[start + i][start + j] = cj[i][j] + (s - sj) * int(i == j)
        start += len(cj)
    from_core = lift(c, s)
    if equal:
        # Construct from original full entries without using the lifted core.
        direct = [[F(0) for _ in range(n)] for _ in range(n)]
        component_of = []
        start = 1
        for k, (f, a, _, _) in enumerate(parts):
            factor = F(len(f) - s, n - s)
            for i in range(1, len(f)):
                direct[0][start + i - 1] = direct[start + i - 1][0] = factor * a[0][i]
                for j in range(1, len(f)):
                    direct[start + i - 1][start + j - 1] = factor * a[i][j]
            component_of += [k] * (len(f) - 1)
            start += len(f) - 1
        for i in range(1, n):
            for j in range(1, n):
                if component_of[i - 1] != component_of[j - 1]:
                    direct[i][j] = F(1, n - s)
        direct[0][0] = (sum((len(f) - s) * a[0][0] for f, a, _, _ in parts)
                        + (len(parts) - 1) * (s - 1)) / (n - s)
        require(direct == from_core, "union entry and core constructions disagree")
    return family, from_core, s, "union(" + ",".join(p[3] for p in parts) + ")"


def quantitative_gap(parts, a, s):
    n = len(a)
    ms = [len(p[0]) - 1 for p in parts]
    delta = sum(ms) - max(ms)
    h = max(len(p[0]) for p in parts)
    d0 = sum(F(s, len(p[0]) - s) for p in parts) / sum(ms)
    gamma = F(delta, delta + h) * d0
    test = [[(n - s) * (int(i == j) - a[i][j])
             - gamma * (int(i == j) - F(1, n))
             for j in range(n)] for i in range(n)]
    require(psd_rank(test) == n - 1, "quantitative upper gap failed")
    return str(gamma)


def tensor_parts(parts):
    indexes = list(product(*(range(len(p[0])) for p in parts)))
    shifts = []
    offset = 0
    for f, _, _, _ in parts:
        shifts.append(offset)
        offset += max(f).bit_length()
    family = [sum(parts[j][0][idx[j]] << shifts[j] for j in range(len(parts)))
              for idx in indexes]
    a = []
    for x in indexes:
        row = []
        for y in indexes:
            value = F(1)
            for j, (_, aj, _, _) in enumerate(parts):
                value *= aj[x[j]][y[j]]
            row.append(value)
        a.append(row)
    n = len(family)
    s = max(sj * (n // len(f)) for f, _, sj, _ in parts)
    return family, a, s, "tensor(" + ",".join(p[3] for p in parts) + ")"


def unequal_cubes(large_order, small_order):
    """Aligned full vectors, centered complementary residuals, and rank repair."""
    require(large_order > small_order >= 1, "unequal cube orders required")
    large = cube(large_order)
    small = cube(small_order)
    t, u = large[2], small[2]
    f, shifted, s, _ = union_parts([large, small], equal=False)
    n = len(f)
    big_m, small_m = len(large[0]) - 1, len(small[0]) - 1
    c = [[F(0) for _ in range(n - 1)] for _ in range(n - 1)]
    big_core = core(large[1], t)
    for i in range(big_m):
        for j in range(big_m):
            c[i][j] = big_core[i][j]
    kappa = F(1 + t * (2 * u - 2 - t), t - 1)
    for i in range(small_m):
        for j in range(small_m):
            if i == j:
                v = F(t - 1)
            elif i == small_m - 1 or j == small_m - 1:
                v = F(-1)
            elif (i + 1) ^ (j + 1) == small_m:
                v = kappa
            else:
                v = F(-1)
            c[big_m + i][big_m + j] = v
    for i in range(big_m):
        for j in range(small_m):
            if i == big_m - 1 and j == small_m - 1:
                v = F(t - 1)
            elif i == big_m - 1 or j == small_m - 1:
                v = F(-1)
            else:
                v = F(1, t - 1)
            c[i][big_m + j] = c[big_m + j][i] = v
    capped = lift(c, t)
    beta = F((2 * u - 1) * (t - 2 * u + 1), t - 1)
    q = (n - 1) * (t - 1) + t + u - 2 + (t - u) * (2 * u - 1)
    epsilon = beta / (2 * (beta + q))
    require(beta > 0 and 0 < epsilon < 1, "bad unequal cube repair parameters")
    mixed = [[(1 - epsilon) * capped[i][j] + epsilon * shifted[i][j]
              for j in range(n)] for i in range(n)]
    shifted_core = core(shifted, t)
    actual_q = sum(shifted_core[i][i] for i in range(n - 1)) + sum(sum(row) for row in shifted_core)
    require(actual_q == q, "shifted Q trace formula")
    mixed_core = [[(1 - epsilon) * c[i][j] + epsilon * shifted_core[i][j]
                   for j in range(n - 1)] for i in range(n - 1)]
    require(lift(mixed_core, t) == mixed, "unequal cube mixture/core mismatch")
    metadata = {"large_order": large_order, "small_order": small_order,
                "t": t, "u": u, "beta": str(beta), "shifted_Q_trace": q,
                "epsilon": str(epsilon), "upper_gap_bound": str(beta / (2 * (n - t)))}
    return (f, mixed, t, "unequal_cubes(%d,%d)" % (large_order, small_order)), capped, metadata


def expect_error(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError("malformed control was accepted")


def cube_forced_span(n):
    """Concrete complementary switches; no imported family catalogue."""
    full = (1 << n) - 1
    s = 1 << (n - 1)
    nonempty = list(range(1, full + 1))
    vectors = []
    hashes = []
    for target in range(1, full):
        chosen = {target}
        sub = (target - 1) & target
        while sub:
            chosen.add(full ^ sub)
            sub = (sub - 1) & target
        for a in nonempty:
            if all(a & b for b in chosen):
                chosen.add(a)
        switched = (chosen - {target}) | {full ^ target}
        require(len(chosen) == len(switched) == s, "wrong switched-family size")
        require(full in chosen and full in switched, "full set lost in switch")
        for family in [chosen, switched]:
            require(all(a & b for a, b in combinations(family, 2)), "nonintersecting switch")
            require(all((a in family) != ((full ^ a) in family) for a in range(full + 1)),
                    "switch is not a complementary selector")
        difference = [int(a in chosen) - int(a in switched) for a in nonempty]
        require(difference == [int(a == target) - int(a == (full ^ target)) for a in nonempty],
                "wrong complementary difference")
        if target < (full ^ target):
            vectors.append(difference)
        encoded = json.dumps([sorted(chosen), sorted(switched)], separators=(",", ":"))
        hashes.append(sha256(encoded.encode()).hexdigest())
    star = [int(bool(a & 1)) for a in nonempty]
    vectors.append(star)
    gram = [[sum(v[i] * v[j] for v in vectors) for j in range(full)] for i in range(full)]
    require(psd_rank(gram) == s, "wrong cube forced-span dimension")
    require(len(vectors) == s, "wrong number of independent forced vectors")
    return {"n": n, "switch_count": full - 1, "forced_dimension": s,
            "switch_manifest_sha256": sha256("\n".join(hashes).encode()).hexdigest()}


def cube_family_census(n):
    """All size-s subfamilies, finite scope n<=4 stated by the caller."""
    full = (1 << n) - 1
    s = 1 << (n - 1)
    families = [f for f in combinations(range(1, full + 1), s)
                if all(a & b for a, b in combinations(f, 2))]
    require(all(full in f for f in families), "maximum family omits full set")
    require(all(all((a in f) != ((full ^ a) in f) for a in range(full + 1))
                for f in families), "maximum family is not a selector")
    gram = [[sum(int(i in f) * int(j in f) for f in families)
             for j in range(1, full + 1)] for i in range(1, full + 1)]
    require(psd_rank(gram) == s, "complete census forced span")
    return {"n": n, "maximum_family_count": len(families), "forced_dimension": s}


def run():
    baselines = [cube(n) for n in range(1, 5)]
    baselines += [proper_cube(2), proper_cube(3), path3(), matching2(), uniform_rank2(4)]
    baseline_results = []
    for f, a, s, label in baselines:
        entry = check(f, a, s)
        entry["label"] = label
        baseline_results.append(entry)
    unions = []
    for n, r in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 3), (4, 2), (4, 3)]:
        parts = [cube(n) for _ in range(r)]
        f, a, s, label = union_parts(parts)
        entry = check(f, a, s)
        require(entry["lower_rank"] == len(f) - r * s, "cube lower rank")
        require(entry["upper_rank"] == len(f) - 1, "cube upper rank")
        b = len(f) - s
        spectrum = {F(1): 1, F(-s, b): r * s, F(s, b): r * (s - 2),
                    F(1, b): r - 1, F(r * (s - 1) + 1, b): 1}
        observed = {}
        for value, multiplicity in spectrum.items():
            test = [[a[i][j] - value * int(i == j) for j in range(len(f))]
                    for i in range(len(f))]
            nullity = len(f) - rank(test)
            require(nullity == multiplicity, "cube spectrum multiplicity")
            observed[str(value)] = nullity
        require(sum(observed.values()) == len(f), "incomplete cube spectrum")
        require(all(v >= 0 for row in a for v in row), "cube union negative entry")
        entry.update(label=label, n=n, r=r, spectrum=observed,
                     gamma=quantitative_gap(parts, a, s),
                     exact_upper_gap=str(F((r - 1) * s, b)))
        unions.append(entry)
    for parts in [[cube(3), uniform_rank2(4)], [proper_cube(3), path3()],
                  [cube(2), matching2(), cube(2)]]:
        factor_nullities = []
        for f, a, s, _ in parts:
            factor_nullities.append(len(f) - check(f, a, s)["lower_rank"])
        f, a, s, label = union_parts(parts)
        entry = check(f, a, s)
        require(len(f) - entry["lower_rank"] == sum(factor_nullities), "mixed nullity")
        require(entry["upper_rank"] == len(f) - 1, "mixed upper simplicity")
        entry.update(label=label, factor_nullities=factor_nullities,
                     gamma=quantitative_gap(parts, a, s))
        unions.append(entry)
    products = []
    u2 = union_parts([cube(2), cube(2)])
    u3 = union_parts([cube(2), cube(2), cube(2)])
    for parts in [[u2, u2], [u2, u3]]:
        f, a, s, label = tensor_parts(parts)
        p = max(F(pj[2], len(pj[0])) for pj in parts)
        eligible = [j for j, pj in enumerate(parts) if F(pj[2], len(pj[0])) == p]
        forced = sum(len(parts[j][0]) - check(parts[j][0], parts[j][1], parts[j][2])["lower_rank"]
                     for j in eligible)
        entry = check(f, a, s)
        require(entry["lower_rank"] == len(f) - forced, "tensor lower rank")
        require(entry["upper_rank"] == len(f) - 1, "tensor upper rank")
        entry.update(label=label, eligible_factors=eligible, forced_nullity=forced)
        products.append(entry)
    for c in [1, 2, 3]:
        f, a, s, label = tensor_parts([cube(c), u2])
        entry = check(f, a, s)
        require(2 * s == len(f), "common-core balance")
        require(entry["lower_rank"] == len(f) - (1 << (c - 1)), "common-core lower rank")
        require(entry["upper_rank"] == len(f) - (1 << (c - 1)), "common-core upper rank")
        entry.update(label=label, core_order=c, petal_order=2, petal_count=2)
        products.append(entry)
    unequal = []
    for large_order, small_order in [(2, 1), (3, 1), (3, 2), (4, 1), (4, 2),
                                     (4, 3), (5, 2), (5, 4), (6, 1)]:
        repaired, capped, metadata = unequal_cubes(large_order, small_order)
        f, a, t, label = repaired
        n = len(f)
        entry = check(f, a, t)
        seed = check(f, capped, t)
        require(entry["lower_rank"] == n - t, "unequal universally maximal lower rank")
        require(entry["upper_rank"] == n - 1, "unequal upper simplicity")
        beta = F(metadata["beta"])
        test = [[(n - t) * (int(i == j) - a[i][j])
                 - beta / 2 * (int(i == j) - F(1, n)) for j in range(n)] for i in range(n)]
        require(psd_rank(test) == n - 1, "unequal repaired upper gap")
        cseed = core(capped, t)
        qrows = [sum(row) for row in cseed]
        qseed = [[sum(qrows)] + [-v for v in qrows]]
        qseed += [[-qrows[i]] + cseed[i] for i in range(n - 1)]
        threshold = F(n) - beta
        test = [[threshold * (int(i == j) - F(1, n)) - qseed[i][j]
                 for j in range(n)] for i in range(n)]
        psd_rank(test)
        entry.update(label=label, seed_lower_rank=seed["lower_rank"], **metadata)
        unequal.append(entry)
    for core_order, large_order, small_order in [(1, 3, 1), (2, 3, 2)]:
        repaired, _, _ = unequal_cubes(large_order, small_order)
        f, a, s, label = tensor_parts([cube(core_order), repaired])
        entry = check(f, a, s)
        forced = 1 << (core_order - 1)
        require(2 * s == len(f), "unequal common-core balance")
        require(entry["lower_rank"] == entry["upper_rank"] == len(f) - forced,
                "unequal common-core rank")
        entry.update(label=label, core_order=core_order,
                     large_petal_order=large_order, small_petal_order=small_order)
        products.append(entry)
    # A negative control for general shifted union, with a separate valid cap.
    singleton = cube(1)
    f, a, s, _ = union_parts([cube(3), singleton], equal=False)
    n = len(f)
    lower = [[(n - s) * a[i][j] + s * int(i == j) for j in range(n)] for i in range(n)]
    lower_rank = psd_rank(lower)
    w = [0] + [5] * 6 + [1, 6]
    value = sum(w[i] * ((n - s) * (int(i == j) - a[i][j])) * w[j]
                for i in range(n) for j in range(n))
    require(value == -37, "unequal-star cap witness")
    expect_error(lambda: check(f, a, s))
    # Complementary pairs and the full-cube/singleton pair all have size two.
    colors = [min(x, 7 ^ x) - 1 if x < 7 else 3 for x in range(1, 9)]
    alternate = partition(f, colors, 4, "unequal_star_alternate_cap")
    alternate_result = check(alternate[0], alternate[1], alternate[2])
    controls = [
        lambda: psd_rank([[-1]]),
        lambda: psd_rank([[0, 1], [1, 0]]),
        lambda: psd_rank([[1, 2], [0, 1]]),
        lambda: psd_rank([[1, 2]]),
        lambda: family_star([0, 3]),
        lambda: family_star([0, 1, 1]),
        lambda: union_parts([cube(2), cube(3)]),
        lambda: union_parts([cube(2)]),
        lambda: partition([0, 1, 2, 3], [0, 0, 0], 1, "invalid"),
        lambda: check(cube(2)[0], cube(2)[1], 1),
        lambda: check(cube(2)[0], identity(4), 2),
    ]
    for fn in controls:
        expect_error(fn)
    return {"ok": True, "agent": "six-downset-1", "role": "researcher",
            "arithmetic": "Python integers and fractions.Fraction",
            "baselines": baseline_results, "unions": unions, "products": products,
            "unequal_cube_repairs": unequal,
            "forced_span_checks": [cube_forced_span(n) for n in range(2, 6)],
            "complete_cube_family_censuses": [cube_family_census(n) for n in range(2, 5)],
            "unequal_star_control": {"N": n, "s": s, "lower_rank": lower_rank,
                                     "scaled_upper_quadratic_form": str(value),
                                     "witness": w, "alternate_cap": alternate_result},
            "rejection_controls": len(controls) + 1,
            "coverage": {"baseline_count": len(baseline_results),
                         "union_count": len(unions), "product_count": len(products),
                         "unequal_cube_repair_count": len(unequal),
                         "largest_literal_matrix_order": max(x["N"] for x in products + unions + unequal)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = run()
    content = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        require(args.check.read_text() == content, "expected-results bytes differ")
    if args.output:
        args.output.write_text(content)
    print(json.dumps({"ok": result["ok"], "coverage": result["coverage"],
                      "rejection_controls": result["rejection_controls"],
                      "results_sha256": sha256(content.encode()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
