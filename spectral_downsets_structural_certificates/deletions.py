#!/usr/bin/env python3
"""Exact projection restrictions and cap tests proved in DELETIONS.md."""
from fractions import Fraction as F
from itertools import combinations
import certificates as build


def deleted_masks(n, deleted_pairs):
    if not isinstance(n, int) or n < 3:
        raise ValueError("Projection deletions require n>=3")
    result = []
    touched = set()
    for pair in deleted_pairs:
        if len(pair) != 2:
            raise ValueError("Each deletion must be a pair")
        a, b = pair
        if not (isinstance(a, int) and isinstance(b, int) and 0 <= a < n
                and 0 <= b < n and a != b):
            raise ValueError("Invalid deleted pair")
        mask = (1 << a) | (1 << b)
        if mask in result:
            raise ValueError("Repeated deletion")
        result.append(mask)
        touched.update((a, b))
    if len(touched) == n:
        raise ValueError("Deletion must leave a coordinate untouched, retaining s=n")
    return sorted(result)


def core_entry(n, a, b):
    if a == b:
        return F(n - 1)
    if a & b or a.bit_count() == b.bit_count() == 1:
        return F(-1)
    return F(2, n - 2)


def deletion_certificate(n, deleted_pairs, shift=0):
    removed = set(deleted_masks(n, deleted_pairs))
    family = sorted([0] + [1 << v for v in range(n)] +
                    [(1 << a) | (1 << b) for a, b in combinations(range(n), 2)
                     if ((1 << a) | (1 << b)) not in removed])
    core = [[core_entry(n, a, b) for b in family[1:]] for a in family[1:]]
    return [a << shift for a in family], build.lift(core, n), n


def deletion_data(n, deleted_pairs):
    masks = deleted_masks(n, deleted_pairs)
    k = len(masks)
    n0 = 1 + n + n * (n - 1) // 2
    kappa = F(n * (n - 1), n - 2)
    gram = [[core_entry(n, a, b) for b in masks] for a in masks]
    return {"n": n, "N_0": n0, "N": n0 - k, "s": n, "k": k,
            "kappa": kappa, "delta": F(n0 - k) - kappa,
            "masks": masks, "gram": gram,
            "line_degrees": [sum(a != b and bool(a & b) for b in masks)
                             for a in masks]}


def solve_spd(matrix, rhs):
    """Exact symmetric no-pivot elimination; positivity is checked, not assumed."""
    n = len(rhs)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("Bad linear-system dimensions")
    a = [[F(x) for x in row] for row in matrix]
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        raise ValueError("Nonsymmetric linear system")
    b = [F(x) for x in rhs]
    for k in range(n):
        pivot = a[k][k]
        if pivot <= 0:
            raise ValueError("System is not strictly positive definite")
        for i in range(k + 1, n):
            ratio = a[i][k] / pivot
            b[i] -= ratio * b[k]
            for j in range(i, n):
                a[i][j] -= ratio * a[k][j]
                a[j][i] = a[i][j]
    solution = [F(0)] * n
    for i in range(n - 1, -1, -1):
        solution[i] = (b[i] - sum(a[i][j] * solution[j] for j in range(i + 1, n))) / a[i][i]
    return solution


def cap_test(n, deleted_pairs):
    """Return (passes, scalar value) for this inherited certificate, not feasibility."""
    data = deletion_data(n, deleted_pairs)
    k, delta, gram = data["k"], data["delta"], data["gram"]
    if not k:
        return True, F(0)
    if delta == 0:
        if n != 3 or k != 1:
            raise ValueError("Unproved zero-delta input")
        return True, F(1)
    if delta < 0:
        raise ValueError("Untouched-coordinate delta bound failed")
    system = [[gram[i][j] + (delta if i == j else 0) for j in range(k)]
              for i in range(k)]
    solution = solve_spd(system, [F(1)] * k)
    value = sum(gram[i][j] * solution[j] for i in range(k) for j in range(k))
    return value <= 1, value


def regular_top_eigenvalue(n, deleted_pairs):
    data = deletion_data(n, deleted_pairs)
    k = data["k"]
    if not k:
        return data["kappa"], F(0)
    degree = data["line_degrees"][0]
    if any(d != degree for d in data["line_degrees"]):
        raise ValueError("Deleted line graph is irregular")
    g = F(n - 1 - degree) + F(2 * (k - 1 - degree), n - 2)
    if g < 0:
        raise ValueError("Deleted Gram row sum is negative")
    return data["kappa"] + (k - 1) * g, g


def regular_eigenvector(n, deleted_pairs):
    data = deletion_data(n, deleted_pairs)
    eigenvalue, g = regular_top_eigenvalue(n, deleted_pairs)
    if not data["k"] or not g:
        raise ValueError("This eigenvector requires a nonzero deleted sum")
    family, _, _ = deletion_certificate(n, deleted_pairs)
    vector = [F(data["k"]) * g]
    vector += [sum(core_entry(n, a, e) for e in data["masks"]) for a in family[1:]]
    return eigenvalue, vector
