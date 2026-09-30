#!/usr/bin/env python3
"""Exact definition-level matrices and rational invariant-space image checks."""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

import certificates as base
import deletions
import two_centers
from verify import check, psd_ldl, require


def direct_matrix(t):
    members = two_centers.family(t)
    centers = (1 << t) | (1 << (t + 1))
    denominator = 2 * t * (t + 1)
    matrix = []
    for a in members:
        row = []
        for b in members:
            if a == b == 0:
                value = F(-1, 2)
            elif not a or not b:
                value = F(1, 2 * (t + 1))
            elif a & b:
                value = F(0)
            elif a.bit_count() == b.bit_count() == 1:
                count = int(bool(a & centers)) + int(bool(b & centers))
                value = F(0) if count == 2 else F(t - 1, denominator) if count == 1 else F(-1, denominator)
            elif a.bit_count() == b.bit_count() == 2:
                value = F(t + 2, denominator)
            else:
                single, edge = (a, b) if a.bit_count() == 1 else (b, a)
                value = F(t + 2, denominator) if single & centers else F(2 * t + 1, denominator) if edge == centers else F(1, 2 * (t + 1))
            row.append(value)
        matrix.append(row)
    return matrix


def matvec(matrix, vector):
    return [sum(x * y for x, y in zip(row, vector)) for row in matrix]


def linear_combination(basis, coefficients):
    return [sum(v[i] * a for v, a in zip(basis, coefficients)) for i in range(len(basis[0]))]


def basis_check(t, core):
    members = two_centers.family(t)[1:]
    index = {a: i for i, a in enumerate(members)}
    a, b = 1 << t, 1 << (t + 1)
    leaves = [1 << i for i in range(t)]
    xs, ys = [a | c for c in leaves], [b | c for c in leaves]

    def vector(entries):
        result = [F(0) for _ in members]
        for mask, coefficient in entries:
            result[index[mask]] += coefficient
        return result

    kappa = F(t + 3) + F(2, t)
    minus = [vector([(a, 1), (b, -1)]),
             vector([(x, 1) for x in xs] + [(y, -1) for y in ys])]
    minus_operator = [[F(t + 2), F(-t - 2)],
                      [F(-t - 2, t), F(t + 2, t)]]
    for j, v in enumerate(minus):
        require(matvec(core, v) == linear_combination(minus, [row[j] for row in minus_operator]),
                "Wrong antisymmetric constant image")
    singleton_diagonal = F((t + 1) ** 2, t)
    spoke_diagonal = F(t + 1) - F(2, t)
    for i in range(t - 1):
        cm = vector([(leaves[i], 1), (leaves[-1], -1)])
        hp = vector([(xs[i], 1), (ys[i], 1), (xs[-1], -1), (ys[-1], -1)])
        hm = vector([(xs[i], 1), (ys[i], -1), (xs[-1], -1), (ys[-1], 1)])
        require(matvec(core, hm) == [kappa * x for x in hm], "Wrong antisymmetric standard image")
        require(matvec(core, cm) == linear_combination([cm, hp], [singleton_diagonal, -1]),
                "Wrong symmetric singleton image")
        require(matvec(core, hp) == linear_combination([cm, hp], [-2, spoke_diagonal]),
                "Wrong symmetric spoke image")
    plus = [vector([(a, 1), (b, 1)]), vector([(a | b, 1)]),
            vector([(c, 1) for c in leaves]),
            vector([(x, 1) for x in xs] + [(y, 1) for y in ys])]
    gram = [[F(2 * t), F(-2), F(-2), F(4 - 2 * t)],
            [F(-2), F(t + 1), F(t + 1), F(-2 * t)],
            [F(-2), F(t + 1), F(t + 1), F(-2 * t)],
            [F(4 - 2 * t), F(-2 * t), F(-2 * t), F(6 * t - 4)]]
    norms = [2, 1, t, 2 * t]
    for j, v in enumerate(plus):
        require(matvec(core, v) == linear_combination(plus, [gram[i][j] / norms[i] for i in range(4)]),
                "Wrong symmetric constant image")
    small = [[F(2 * t), F(-2)], [F(-2), F(t + 1)]]
    factor = [[1, 0], [0, 1], [0, 1], [-1, -2]]
    rebuilt = [[sum(F(factor[i][p]) * small[p][q] * factor[j][q]
                    for p in range(2) for q in range(2)) for j in range(4)] for i in range(4)]
    require(gram == rebuilt and psd_ldl(small) == (1 if t == 1 else 2), "Wrong constant Gram factorization")
    n = 3 * t + 4
    require(kappa < n and F(2 * t + 5) - F(1, t) < n, "Block cap bound failed")
    if t >= 2:
        require(singleton_diagonal * spoke_diagonal > 2, "Standard block is not positive")
        require(singleton_diagonal + spoke_diagonal < n, "Standard trace cap failed")
    return (t - 1) + 2 + 2 * (t - 1) + 4


def reject_cap(matrix):
    n = len(matrix)
    try:
        psd_ldl([[F(int(i == j)) - matrix[i][j] for j in range(n)] for i in range(n)])
    except ValueError as error:
        require(str(error) in ("Negative exact LDL pivot", "Zero pivot with nonzero residual row"),
                "Unexpected cap rejection")
    else:
        raise ValueError("Known uncapped construction was accepted")


def maximum_intersecting_families(members):
    """Complete maximal-clique branching on the literal intersection graph."""
    nonempty = members[1:]
    adjacency = [sum(1 << j for j, b in enumerate(nonempty) if i != j and a & b)
                 for i, a in enumerate(nonempty)]
    answer = []

    def visit(chosen, available, excluded):
        if not available and not excluded:
            answer.append(tuple(nonempty[i] for i in range(len(nonempty)) if chosen & (1 << i)))
            return
        union = available | excluded
        pivot = max((i for i in range(len(nonempty)) if union & (1 << i)),
                    key=lambda i: (available & adjacency[i]).bit_count())
        candidates = available & ~adjacency[pivot]
        while candidates:
            bit = candidates & -candidates
            i = bit.bit_length() - 1
            visit(chosen | bit, available & adjacency[i], excluded & adjacency[i])
            available ^= bit
            excluded |= bit
            candidates ^= bit

    visit(0, (1 << len(nonempty)) - 1, 0)
    size = max(map(len, answer))
    return {a for a in answer if len(a) == size}


def run():
    cases = []
    for t in list(range(1, 13)) + [19, 20, 21]:
        members, matrix, s = two_centers.certificate(t)
        require(matrix == direct_matrix(t), "Direct entry formula and lift differ")
        n = len(members)
        rank = check(members, matrix, s, upper=True)
        core = base.extract_core(matrix, s)
        require(all(sum(row) == 0 for row in core), "Core is not centered")
        nullity = 4 if t == 1 else 3
        require(rank == n - nullity and psd_ldl(core) == n - 1 - nullity, "Wrong lower rank")
        require(psd_ldl([[F(int(i == j)) - matrix[i][j] for j in range(n)] for i in range(n)]) == n - 1,
                "Upper endpoint is not simple")
        require(basis_check(t, core) == n - 1, "Invariant spaces do not exhaust the core")
        leaves = [1 << i for i in range(t)]
        positions = {a: i for i, a in enumerate(members)}
        if t >= 2:
            average = sum(core[positions[a] - 1][positions[b] - 1] for a in leaves for b in leaves if a != b) / (t * (t - 1))
            require(average == F(-t - 1, t), "Forced average identity failed")
        require(all(matrix[i][j] >= 0 or (a.bit_count() == b.bit_count() == 1 and
                    a in leaves and b in leaves) for i, a in enumerate(members)
                    for j, b in enumerate(members) if i != j), "Negative weight outside leaf singletons")
        expected_families = {tuple(a for a in members if a & (1 << i)) for i in range(t, t + 2)}
        if t == 1:
            expected_families.add(tuple(a for a in members if a & 1))
            expected_families.add(tuple(a for a in members if a.bit_count() == 2))
        require(maximum_intersecting_families(members) == expected_families,
                "Complete intersection-clique check disagrees with equality classification")
        q, remainder = divmod(n - 1, s)
        convex_partition_bound = remainder * (s - remainder)
        require(sum(map(sum, core)) == 0 and (t == 1 or (q == 2 and convex_partition_bound == 3 * (t - 1) > 0)),
                "Centered convex-partition separation failed")
        raw = json.dumps([[str(x) for x in row] for row in matrix], separators=(",", ":")).encode()
        cases.append({"t": t, "N": n, "s": s, "L_rank": rank,
                      "C_rank": n - 1 - nullity, "upper_rank": n - 1,
                      "maximum_intersecting_families": len(expected_families),
                      "convex_partition_core_sum_lower_bound": convex_partition_bound,
                      "matrix_sha256": sha256(raw).hexdigest()})
    # Boundary is the old independently established uniform incidence baseline.
    require(two_centers.certificate(1) == base.uniform_rank_two_certificate(3), "Triangle baseline differs")
    # Two templates can fail on the same families even though the new cap passes.
    inherited = deletions.deletion_certificate(7, list(combinations(range(5), 2)))
    require(inherited[0] == two_centers.family(5), "Wrong failed inherited comparison")
    check(*inherited)
    reject_cap(inherited[1])
    edges = list(combinations(range(4), 2))
    members = set(two_centers.family(2))
    mask = sum(1 << i for i, (a, b) in enumerate(edges) if ((1 << a) | (1 << b)) in members)
    partition = base.rank_two_certificate(4, mask)
    check(*partition)
    reject_cap(partition[1])
    products = []
    for first, second in [(1, 2), (2, 2), (2, 3)]:
        product = base.product_certificate([two_centers.certificate(first),
                                           two_centers.certificate(second, first + 2)])
        rank = check(*product, upper=True)
        nullity = sum(4 if t == 1 else 3 for t in (first, second) if t == min(first, second))
        require(rank == len(product[0]) - nullity, "Mixed product rank failed")
        products.append({"t": [first, second], "N": len(product[0]), "s": product[2], "L_rank": rank})
    friendship_comparisons = []
    for k in range(2, 9):
        removed = [(a, b) for a, b in combinations(range(2 * k), 2) if a // 2 != b // 2]
        require(len(removed) == 2 * k * (k - 1), "Wrong friendship deleted edge count")
        top = F(4 * (k - 1) * (k * k + 3 * k + 1), 2 * k - 1)
        actual_top, g = deletions.regular_top_eigenvalue(2 * k + 1, removed)
        require(actual_top == top > 5 * k + 2 and g == F(2 * (k + 2), 2 * k - 1),
                "Friendship inherited top formula failed")
        excess = F((k - 2) * (4 * k * k + 6 * k + 5) + 8, 2 * k - 1)
        require(top - (5 * k + 2) == excess > 0, "Friendship separation failed")
        friendship_comparisons.append({"k": k, "inherited_Gram_top": str(top)})
    for function, args in [(two_centers.family, (0,)), (two_centers.core, (True,)),
                           (two_centers.certificate, (3, -1)), (two_centers.family, (F(3, 2),))]:
        try:
            function(*args)
        except ValueError:
            pass
        else:
            raise ValueError("Invalid construction input accepted")
    return {"agent": "six-downset-1", "role": "researcher", "cases": cases,
            "N_max": 67, "full_matrix_products": products,
            "inherited_t5_cap_rejected": True, "partition_t2_cap_rejected": True,
            "friendship_inherited_separations": friendship_comparisons,
            "invalid_input_rejections": 4,
            "scope": "Finite exact validation; all-parameter proof and product ranks are written in TWO_CENTERS.md."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare with the published deterministic expected output")
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name("two_centers_expected.json").read_text())
        require(result == expected, "Expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
