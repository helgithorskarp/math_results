#!/usr/bin/env python3
"""Definition-level rational checks and exact LDL, separate from Gram proofs."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import certificates as build


def require(condition, message):
    if not condition:
        raise ValueError(message)


def psd_ldl(matrix):
    """Exact symmetric elimination, including zero pivots; returns rank."""
    n = len(matrix)
    a = [[F(x) for x in row] for row in matrix]
    require(all(len(row) == n for row in a), "Nonsquare matrix")
    require(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
            "Nonsymmetric PSD input")
    rank = 0
    for k in range(n):
        pivot = a[k][k]
        require(pivot >= 0, "Negative exact LDL pivot")
        if not pivot:
            require(all(not a[k][j] for j in range(k + 1, n)),
                    "Zero pivot with nonzero residual row")
            continue
        rank += 1
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return rank


def check(family, matrix, expected_s, upper=False):
    n = len(family)
    require(len(set(family)) == n and family[0] == 0, "Bad family indexing")
    present = set(family)
    for a in family:
        sub = a
        while True:
            require(sub in present, "Not a downset")
            if not sub:
                break
            sub = (sub - 1) & a
    s = max(sum(bool(a & (1 << i)) for a in family)
            for i in range(max(family).bit_length()))
    require(s == expected_s and 0 < s < n, "Wrong star size")
    require(len(matrix) == n and all(len(row) == n for row in matrix), "Bad dimensions")
    for i in range(n):
        require(sum(matrix[i]) == 1, "Wrong row sum")
        for j in range(n):
            require(matrix[i][j] == matrix[j][i], "Nonsymmetric certificate")
            if family[i] & family[j]:
                require(matrix[i][j] == 0, "Nonzero intersecting entry")
    l = [[(n - s) * matrix[i][j] + (s if i == j else 0)
          for j in range(n)] for i in range(n)]
    rank = psd_ldl(l)
    if upper:
        psd_ldl([[F(int(i == j)) - matrix[i][j]
                  for j in range(n)] for i in range(n)])
    # Equality in Hoffman forces this relation for every maximum star.
    for v in range(max(family).bit_length()):
        star = [j for j, a in enumerate(family) if a & (1 << v)]
        if len(star) == s:
            require(all(sum(l[i][j] for j in star) == s for i in range(n)),
                    "Maximum-star kernel relation failed")
    return rank


def direct_partition_matrix(colors, s):
    """Closed entry formula, independent of the constructor's empty lift."""
    n = len(colors) + 1
    counts = Counter(colors)
    matrix = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, c in enumerate(colors, 1):
        for j, d in enumerate(colors, 1):
            matrix[i][j] = F(s * int(c == d and i != j), n - s)
        matrix[i][0] = matrix[0][i] = F(n - s * counts[c], n - s)
    matrix[0][0] = F(s * sum(counts[c] ** 2 for c in range(s))
                     - n * n + 2 * n - s, n - s)
    return matrix


def independent_isomorphism_partition(n):
    """Full labeled enumeration, used as an independent coverage check for n<=5."""
    edges = list(combinations(range(n), 2))
    indices = {e: i for i, e in enumerate(edges)}
    maps = [tuple(indices[tuple(sorted((p[a], p[b])))] for a, b in edges)
            for p in permutations(range(n))]
    unseen = set(range(1 << len(edges)))
    representatives = []
    while unseen:
        mask = min(unseen)
        representatives.append(mask)
        occupied = [i for i in range(len(edges)) if mask & (1 << i)]
        orbit = {sum(1 << mapping[i] for i in occupied) for mapping in maps}
        unseen.difference_update(orbit)
    return representatives


def tensor_obstruction():
    family = [0, 1, 2, 3, 4, 8, 12]
    colors = [1, 1, 0, 1, 1, 0]
    matrix = direct_partition_matrix(colors, 2)
    check(family, matrix, 2)
    x = [2, -1, -1, 1, -1, -1, 1]
    y = [0, 1, -1, 0, 0, 0, 0]
    require(all(sum(matrix[i][j] * x[j] for j in range(7)) == F(8, 5) * x[i]
                for i in range(7)), "Wrong positive eigenpair")
    require(all(sum(matrix[i][j] * y[j] for j in range(7)) == F(-2, 5) * y[i]
                for i in range(7)), "Wrong negative eigenpair")
    product, tensor, s = build.product_certificate([
        (family, matrix, 2), ([a << 4 for a in family], matrix, 2)])
    require(s == 14 and len(product) == 49, "Wrong product parameters")
    z = [a * b for a in x for b in y]
    value = sum(z[i] * ((49 - 14) * tensor[i][j] + (14 if i == j else 0)) * z[j]
                for i in range(49) for j in range(49))
    require(value == -168, "Wrong exact negative tensor quadratic form")
    return {"factor_N": 7, "factor_s": 2, "positive_eigenvalue": "8/5",
            "negative_eigenvalue": "-2/5", "product_N": 49, "product_s": 14,
            "product_PSD_quadratic_form": str(value)}


def rejection_controls():
    for bad in ([[F(-1)]], [[F(0), F(1)], [F(1), F(1)]]):
        try:
            psd_ldl(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError("Invalid PSD control accepted")
    family, matrix, s = build.matching_certificate(1)
    broken = [row[:] for row in matrix]
    broken[1][1] = F(1)
    try:
        check(family, broken, s)
    except ValueError:
        pass
    else:
        raise RuntimeError("Invalid certificate control accepted")


def main():
    fixture_path = Path(__file__).with_name("rank_two_certificates.json")
    raw = fixture_path.read_bytes()
    fixtures = json.loads(raw)
    expected = [1, 2, 4, 11, 34, 156]
    seen = {n: set() for n in range(1, 7)}
    ranks = Counter()
    bounded_rank_two = 0
    excluded_partition_caps = 0
    for item in fixtures:
        n, mask, s, colors = (item[k] for k in ("n", "edge_mask", "s", "colors"))
        require(1 <= n <= 6 and 0 <= mask < 1 << (n * (n - 1) // 2), "Bad graph encoding")
        require(mask not in seen[n], "Duplicate graph")
        seen[n].add(mask)
        family = build.graph_family(n, mask)
        require(len(colors) == len(family) - 1, "Wrong color count")
        require(all(isinstance(c, int) and 0 <= c < s for c in colors), "Bad color")
        for i, a in enumerate(family[1:]):
            for j, b in enumerate(family[1:]):
                if i != j and a & b:
                    require(colors[i] != colors[j], "Intersecting sets share color")
        matrix = direct_partition_matrix(colors, s)
        require(matrix == build.coloring_certificate(colors, s), "Lift/formula mismatch")
        ranks[str(check(family, matrix, s))] += 1
        counts = [colors.count(c) for c in range(s)]
        require(max(counts) - min(counts) <= 1, "Partition is not equitable")
        if len(family) % s in (0, 1):
            check(family, matrix, s, upper=True)
            bounded_rank_two += 1
        else:
            try:
                psd_ldl([[F(int(i == j)) - matrix[i][j]
                          for j in range(len(family))] for i in range(len(family))])
            except ValueError:
                excluded_partition_caps += 1
            else:
                raise RuntimeError("Partition-cap classification contradicted")
    computed = build.graph_classes(6)
    for n in range(1, 7):
        require(sorted(seen[n]) == computed[n], "Vertex-extension coverage mismatch")
        require(len(seen[n]) == expected[n - 1], "Wrong class count")
        if n <= 5:
            require(sorted(seen[n]) == independent_isomorphism_partition(n),
                    "Independent labeled-orbit coverage mismatch")

    baseline = 0
    for k in range(1, 7):
        check(*build.cube_certificate(k), upper=True)
        baseline += 1

    bounded = 0
    for k in range(5):
        for isolated in range(5):
            if k + isolated:
                check(*build.matching_certificate(k, isolated), upper=True)
                bounded += 1
    union = build.union_certificate([build.cube_certificate(3), build.cube_certificate(2, 3)])
    check(*union)
    original, matrix, s = build.matching_certificate(2, 1)
    retained = [a for a in original if not a & (1 << 4)]
    restriction = build.restrict_certificate(original, matrix, s, retained)
    check(retained, restriction, s)
    products = []
    for k1, l1, k2, l2 in ((2, 0, 2, 0), (2, 0, 1, 1), (0, 2, 1, 1)):
        factors = [build.matching_certificate(k1, l1),
                   build.matching_certificate(k2, l2, 2 * k1 + l1)]
        for factor in factors:
            check(*factor, upper=True)
        product = build.product_certificate(factors)
        check(*product, upper=True)
        products.append({"N": len(product[0]), "s": product[2]})
    triangles = build.product_certificate([build.rank_two_certificate(3, 7),
                                          build.rank_two_certificate(3, 7, 3)])
    check(*triangles, upper=True)
    products.append({"N": len(triangles[0]), "s": triangles[2]})
    projection_checks = []
    for n in range(3, 9):
        family, matrix, s = build.uniform_rank_two_certificate(n)
        core = build.extract_core(matrix, s)
        kappa = F(n * (n - 1), n - 2)
        require(all(sum(row) == 0 for row in core), "Uniform core is not centered")
        require(all(sum(core[i][k] * core[k][j] for k in range(len(core)))
                    == kappa * core[i][j]
                    for i in range(len(core)) for j in range(len(core))),
                "Uniform projection identity failed")
        rank = check(family, matrix, s, upper=True)
        require(rank == n * (n - 1) // 2, "Wrong uniform projection rank")
        projection_checks.append({"n": n, "N": len(family), "s": s,
                                  "core_eigenvalue": str(kappa), "L_rank": rank})
    projected_product = build.product_certificate([build.uniform_rank_two_certificate(4),
                                                   build.matching_certificate(0, 2, 4)])
    check(*projected_product, upper=True)
    products.append({"N": len(projected_product[0]), "s": projected_product[2]})
    obstruction = tensor_obstruction()
    rejection_controls()
    print(json.dumps({"rank_two_classes_by_active_coordinates": expected,
                      "rank_two_total": len(fixtures), "rank_two_N_max": 22,
                      "bounded_rank_two_certificates": bounded_rank_two,
                      "uncapped_equitable_partition_certificates": excluded_partition_caps,
                      "rank_two_fixtures_sha256": sha256(raw).hexdigest(),
                      "independent_full_labeled_orbits_through": 5,
                      "exact_PSD_rank_histogram": dict(sorted(ranks.items())),
                      "cube_baselines": baseline, "bounded_matching_checks": bounded,
                      "union": {"N": len(union[0]), "s": union[2]},
                      "star_preserving_restriction": {"N": len(retained), "s": s},
                      "bounded_products": products, "naive_tensor_obstruction": obstruction,
                      "uniform_rank_two_projection_checks": projection_checks,
                      "rejection_controls": 3}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
