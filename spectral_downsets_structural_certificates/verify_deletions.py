#!/usr/bin/env python3
"""Independent full-matrix exact checks of the DELETIONS.md mechanisms."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
import certificates as build
import deletions as deletion
from verify import check, psd_ldl, require


def direct_matrix(n, removed_pairs):
    """Entry formulas from deleted-edge incidence counts, without the core lift."""
    removed = {(1 << a) | (1 << b) for a, b in removed_pairs}
    family = sorted([0] + [1 << v for v in range(n)] +
                    [(1 << a) | (1 << b) for a, b in combinations(range(n), 2)
                     if ((1 << a) | (1 << b)) not in removed])
    size, k = len(family), len(removed)
    c = F(2, n - 2)
    matrix = [[F(0) for _ in family] for _ in family]
    for i, a in enumerate(family[1:], 1):
        for j, b in enumerate(family[1:], 1):
            if i != j and not a & b and (a.bit_count(), b.bit_count()) != (1, 1):
                matrix[i][j] = (1 + c) / (size - n)
        meets = sum(bool(a & e) for e in removed)
        empty_inner_product = -meets + c * (k - meets)
        matrix[i][0] = matrix[0][i] = (1 + empty_inner_product) / (size - n)
    adjacent = sum(bool(a & b) for a, b in combinations(sorted(removed), 2))
    disjoint = k * (k - 1) // 2 - adjacent
    empty_norm_squared = k * (n - 1) - 2 * adjacent + 2 * c * disjoint
    matrix[0][0] = (empty_norm_squared + 1 - n) / (size - n)
    return family, matrix, n


def check_case(n, removed_pairs):
    family, matrix, s = deletion.deletion_certificate(n, removed_pairs)
    direct = direct_matrix(n, removed_pairs)
    require((family, matrix, s) == direct, "Core lift and incidence-entry formula disagree")
    rank = check(family, matrix, s)
    size = len(family)
    predicted, scalar = deletion.cap_test(n, removed_pairs)
    upper = [[F(int(i == j)) - matrix[i][j] for j in range(size)] for i in range(size)]
    try:
        psd_ldl(upper)
        actual = True
    except ValueError as error:
        require(str(error) in ("Negative exact LDL pivot", "Zero pivot with nonzero residual row"),
                "Unexpected cap checker failure")
        actual = False
    require(predicted == actual, "Scalar cap test and full exact PSD disagree")
    data = deletion.deletion_data(n, removed_pairs)
    q = [[(size - s) * matrix[i][j] + (s if i == j else 0) - 1
          for j in range(size)] for i in range(size)]
    regular = len(set(data["line_degrees"])) <= 1
    if regular:
        top, g = deletion.regular_top_eigenvalue(n, removed_pairs)
        require((top <= size) == actual, "Regular top bound and full exact PSD disagree")
        # Shift positivity and a nonzero exact eigenvector certify it is the top.
        psd_ldl([[top * int(i == j) - q[i][j] for j in range(size)] for i in range(size)])
        if data["k"] and g:
            eigenvalue, vector = deletion.regular_eigenvector(n, removed_pairs)
            require(eigenvalue == top and any(vector), "Missing exact top eigenvector")
            require(sum(vector) == 0, "Top eigenvector is not centered")
            require(sum(x * x for x in vector) == top * data["k"] * g,
                    "Wrong top eigenvector norm")
            require(all(sum(q[i][j] * vector[j] for j in range(size)) == top * vector[i]
                        for i in range(size)), "Wrong regular-case exact eigenpair")
    if data["k"] and data["delta"] > 0:
        gram, k, delta = data["gram"], data["k"], data["delta"]
        system = [[gram[i][j] + delta * int(i == j) for j in range(k)] for i in range(k)]
        solution = deletion.solve_spd(system, [F(1)] * k)
        require(all(sum(system[i][j] * solution[j] for j in range(k)) == 1
                    for i in range(k)), "Exact cap linear-system residual failed")
        require(scalar == k - delta * sum(solution), "Scalar cap forms disagree")
    return {"n": n, "N": size, "s": s, "k": data["k"], "L_rank": rank,
            "capped": actual, "regular_line_graph": regular, "scalar": str(scalar)}


def summary(rows):
    return {"checks": len(rows), "capped": sum(row["capped"] for row in rows),
            "uncapped": sum(not row["capped"] for row in rows),
            "regular_line_graph_checks": sum(row["regular_line_graph"] for row in rows),
            "N_max": max(row["N"] for row in rows),
            "checks_by_n": dict(sorted(Counter(str(row["n"]) for row in rows).items()))}


def restriction_obstruction(n, removed, scale, expected_top, expected_m_top,
                            expected_norm, expected_scaled_quadratic, label):
    family, matrix, s = deletion.deletion_certificate(n, removed)
    check(family, matrix, s)
    top, vector = deletion.regular_eigenvector(n, removed)
    x = [scale * z for z in vector]
    require(all(z.denominator == 1 for z in x), "Obstruction vector is not integral")
    require(top == expected_top, "Wrong obstruction top eigenvalue")
    size = len(family)
    positive_eigenvalue = (top - s) / (size - s)
    require(positive_eigenvalue == expected_m_top, "Wrong obstruction matrix eigenvalue")
    require(all(sum(matrix[i][j] * x[j] for j in range(size)) == positive_eigenvalue * x[i]
                for i in range(size)), "Obstruction matrix eigenpair failed")
    value = sum(x[i] * (F(int(i == j)) - matrix[i][j]) * x[j]
                for i in range(size) for j in range(size))
    require((size - s) * value == expected_scaled_quadratic
            and sum(z * z for z in x) == expected_norm,
            "Wrong exact restriction obstruction")
    # Original factor satisfies both bounds and the restriction keeps actual s.
    check(*build.uniform_rank_two_certificate(n), upper=True)
    return {"n": n, "deleted_graph": label, "k": len(removed), "N": size, "s": s,
            "Q_top_eigenvalue": str(top), "M_top_eigenvalue": str(positive_eigenvalue),
            "integer_vector_norm_squared": expected_norm, "I_minus_M_quadratic_form": str(value),
            "N_I_minus_J_minus_Q_quadratic_form": str((size - s) * value)}


def rejection_controls():
    bad_inputs = [(2, []), (3, [(0, 1), (1, 2)]), (4, [(0, 1), (1, 0)]),
                  (4, [(0, 4)]), (4, [(1, 1)])]
    for n, removed in bad_inputs:
        try:
            deletion.deletion_certificate(n, removed)
        except ValueError:
            pass
        else:
            raise RuntimeError("Invalid deletion accepted")
    try:
        deletion.regular_top_eigenvalue(5, [(0, 1), (1, 2), (2, 3)])
    except ValueError:
        pass
    else:
        raise RuntimeError("Irregular deletion accepted as regular")
    try:
        deletion.solve_spd([[F(0), F(1)], [F(1), F(1)]], [F(1), F(1)])
    except ValueError:
        pass
    else:
        raise RuntimeError("Non-SPD system accepted")
    return len(bad_inputs) + 2


def main():
    labelled = []
    for n in range(3, 6):
        edges = list(combinations(range(n - 1), 2))
        for mask in range(1 << len(edges)):
            removed = [edge for i, edge in enumerate(edges) if mask & (1 << i)]
            row = check_case(n, removed)
            row["edge_mask"] = mask
            labelled.append(row)
    # These are the full labelled exceptional masks on the four first coordinates.
    failed_masks = {(row["n"], row["edge_mask"]) for row in labelled if not row["capped"]}
    require(failed_masks == {(5, mask) for mask in (30, 31, 45, 47, 51, 55, 59, 61, 62)},
            "Small inherited-cap failure cohort differs")
    stars = []
    matchings = []
    for n in range(3, 10):
        for k in range(1, n - 1):
            result = check_case(n, [(0, v) for v in range(1, k + 1)])
            require(result["capped"], "Partial-star theorem failed")
            stars.append(result)
        for k in range(1, (n - 1) // 2 + 1):
            result = check_case(n, [(2 * i, 2 * i + 1) for i in range(k)])
            require(result["capped"], "Matching-deletion theorem failed")
            matchings.append(result)
    cliques = []
    for n in range(3, 11):
        for t in range(2, n):
            result = check_case(n, list(combinations(range(t), 2)))
            cliques.append(result)
            if t == n - 1:
                require(result["capped"], "Star pair-graph endpoint cap failed")
                top, _ = deletion.regular_top_eigenvalue(n, list(combinations(range(t), 2)))
                require(top == result["N"] == 2 * n, "Wrong endpoint equality")
    irregular = []
    for n, removed in ((7, list(combinations(range(5), 2)) + [(0, 5)]),
                       (7, [(0, 1), (1, 2), (2, 3), (3, 4)])):
        result = check_case(n, removed)
        require(not result["regular_line_graph"], "Example is unexpectedly regular")
        irregular.append(result)
    products = []
    cases = [((3, [(0, 1)], 0), (4, [(0, 1), (0, 2)], 3)),
             ((5, [(0, 1), (2, 3)], 0), (3, [(0, 1)], 5))]
    for factors in cases:
        certificates = [deletion.deletion_certificate(n, removed, shift)
                        for n, removed, shift in factors]
        product = build.product_certificate(certificates)
        check(*product, upper=True)
        products.append({"N": len(product[0]), "s": product[2]})
    obstructions = [restriction_obstruction(
        5, [(0, 1), (1, 2), (2, 3), (3, 0)], 9, F(44, 3), F(29, 21),
        12672, -33792, "C4"), restriction_obstruction(
        7, list(combinations(range(5), 2)), 5, F(96, 5), F(61, 60),
        5760, -1152, "K5")]
    result = {"labelled_deletion_cohort": summary(labelled),
              "partial_star_validation": summary(stars),
              "matching_deletion_validation": summary(matchings),
              "clique_deletion_validation": summary(cliques),
              "irregular_examples": irregular,
              "restriction_cap_obstructions": obstructions,
              "bounded_products": products, "rejection_controls": rejection_controls()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
