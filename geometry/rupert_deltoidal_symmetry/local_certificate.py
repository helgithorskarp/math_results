#!/usr/bin/env python3
"""Check positive spanning contact certificates for the three fixed shadows.

The listed small contact bases were selected heuristically. Every weight,
contact, and inequality is rederived here in exact Q(sqrt(5)) arithmetic.
No optimization solver is an input to this checker.
"""

from verify import Q5, F, PHI, ZERO, add, cross, dot, mul, shadow, vec, vertices, verify
import json


# Contacts refer to deterministic exact hull-edge and solid-vertex indices.
# Each line gives a coordinate, its sign, and <= 3 contact-gradient row indices.
BASES = {
    2: [(0, -1, [3, 12]), (0, 1, [4, 11]),
        (1, -1, [3, 11]), (1, 1, [4, 12]),
        (2, -1, [5]), (2, 1, [13])],
    3: [(0, -1, [7, 8]), (0, 1, [0, 4, 11]),
        (1, -1, [3, 4]), (1, 1, [0, 7, 8]),
        (2, -1, [0, 11]), (2, 1, [3, 4, 8])],
    5: [(0, -1, [3, 5, 16]), (0, 1, [0, 2, 15]),
        (1, -1, [6, 12]), (1, 1, [9, 11]),
        (2, -1, [1, 3, 12]), (2, 1, [0, 6, 19])],
}


def solve_independent_columns(columns, rhs):
    """Solve three exact equations in <= 3 independent unknowns; reject gaps."""
    m = len(columns)
    M = [[columns[j][i] for j in range(m)] + [rhs[i]] for i in range(3)]
    pivot_rows = []
    p = 0
    for j in range(m):
        q = next((i for i in range(p, 3) if M[i][j].sign() != 0), None)
        if q is None:
            raise ValueError("dependent certificate columns")
        M[p], M[q] = M[q], M[p]
        d = M[p][j]
        M[p] = [x / d for x in M[p]]
        for i in range(3):
            if i != p:
                d = M[i][j]
                M[i] = [x - d * y for x, y in zip(M[i], M[p])]
        pivot_rows.append(p)
        p += 1
    for i in range(p, 3):
        if any(x.sign() != 0 for x in M[i]):
            raise ValueError("inconsistent certificate equations")
    solution = [M[i][-1] for i in pivot_rows]
    reconstructed = vec((0, 0, 0))
    for w, col in zip(solution, columns):
        reconstructed = add(reconstructed, mul(w, col))
    assert reconstructed == rhs
    return solution


def check_local():
    verify()
    V = vertices()
    summary = {}
    for order, u in [(2, vec((0, 0, 1))), (3, vec((1, 1, 1))), (5, vec((1, 0, PHI)))]:
        H = shadow(V, u)
        assert H["inradius_sq"] > Q5(4)
        rows, contacts = [], []
        for edge_index, (n, b) in enumerate(H["constraints"]):
            for vertex_index, v in enumerate(V):
                if dot(n, v) == b:
                    rows.append(mul(1 / b, cross(v, n)))
                    contacts.append([edge_index, vertex_index])
        weight_sums = []
        used = set()
        for coordinate, sign, indices in BASES[order]:
            rhs = vec([sign if j == coordinate else 0 for j in range(3)])
            weights = solve_independent_columns([rows[i] for i in indices], rhs)
            assert all(w.sign() > 0 for w in weights)
            total = sum(weights, ZERO)
            assert total < Q5(7)
            weight_sums.append(str(total))
            used.update(indices)
        summary[str(order)] = {
            "all_contact_gradients": len(rows),
            "used_contact_gradients": len(used),
            "six_coordinate_certificate_weight_sums": weight_sums,
        }
    assert 7 * 7 * 3 < 13 * 13
    assert F(1, 13) - F(23, 40) * F(1, 10) > 0
    return {
        "agent": "six-rupert-1", "role": "researcher",
        "arithmetic": "exact Q(sqrt(5))",
        "uniform_contact_gradient_support_lower_bound": "1/13",
        "excluded_relative_rotation_angle_radians": "0 < theta <= 1/10",
        "scope": "fixed outer symmetry-axis orientation; no global non-Rupert conclusion",
        "shadows": summary,
    }


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("verification requires assertions; do not use python -O")
    print(json.dumps(check_local(), indent=2, sort_keys=True))
