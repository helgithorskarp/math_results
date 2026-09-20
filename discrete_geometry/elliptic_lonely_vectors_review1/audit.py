#!/usr/bin/env python3
"""Independent exact audit for the rational central-ellipse LVP theorem.

This checker deliberately does not import the submitted verifier.  It uses two
independent models:

* exhaustive labelled direction multisets in Z x C_w (w = 2, 4, 6), and
* exact Fraction arithmetic on rational conics and their Gale duals.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
import json


def abstract_entries(points, w):
    """Return labelled directions for points of Z x C_w, additively."""
    out = []
    half = w // 2  # the element -1
    for i, (q, e) in enumerate(points):
        out.append((("original", i), (2 * q, 2 * e % w)))
    for i, j in combinations(range(len(points)), 2):
        q = points[i][0] + points[j][0]
        e = (points[i][1] + points[j][1]) % w
        out.append((("pair", i, j, +1), (q, e)))
        out.append((("pair", i, j, -1), (q, (e + half) % w)))
    assert len(out) == len(points) ** 2
    return out


def lonely_labels(entries):
    counts = Counter(value for _, value in entries)
    return [label for label, value in entries if counts[value] == 1]


def audit_abstract_groups():
    result = {}
    for w in (2, 4, 6):
        # One representative from every antipodal pair in five quotient fibers.
        universe = [(q, e) for q in range(-2, 3) for e in range(w // 2)]
        checked = 0
        minimum = None
        minimum_original = None
        no_original = 0
        saturated_extrema = 0
        for mask in range(1, 1 << len(universe)):
            if mask.bit_count() < 2:
                continue
            points = [universe[k] for k in range(len(universe)) if mask >> k & 1]
            entries = abstract_entries(points, w)
            lonely = lonely_labels(entries)
            originals = [x for x in lonely if x[0] == "original"]
            assert len(lonely) >= 2
            if w != 6:
                assert len(originals) >= 2

            # Audit the completeness bridge in the extremal-fiber proof: every
            # locally lonely label at the maximum/minimum quotient value remains
            # globally lonely.  This tests labels, not merely direction sets.
            qs = [q for q, _ in points]
            for extreme in {min(qs), max(qs)}:
                idx = [i for i, (q, _) in enumerate(points) if q == extreme]
                local_points = [points[i] for i in idx]
                local = abstract_entries(local_points, w)
                local_counts = Counter(value for _, value in local)
                global_counts = Counter(value for _, value in entries)
                locally_single = [value for _, value in local if local_counts[value] == 1]
                assert locally_single
                assert all(global_counts[value] == 1 for value in locally_single)
                if len(local_points) == w // 2:
                    saturated_extrema += 1

            checked += 1
            minimum = len(lonely) if minimum is None else min(minimum, len(lonely))
            minimum_original = (len(originals) if minimum_original is None
                                else min(minimum_original, len(originals)))
            no_original += not originals

        result[str(w)] = {
            "configurations": checked,
            "minimum_lonely": minimum,
            "minimum_lonely_originals": minimum_original,
            "no_lonely_original_configurations": no_original,
            "saturated_extreme_fibers_seen": saturated_extrema,
        }

    # Smallest exceptional obstruction: the full C_6/{+/-1} fiber.
    tri = [(0, 0), (0, 1), (0, 2)]
    tri_lonely = lonely_labels(abstract_entries(tri, 6))
    assert len(tri_lonely) == 3
    assert all(label[0] == "pair" for label in tri_lonely)

    # Two saturated exceptional fibers: extrema really are distinct, yet neither
    # supplies a lonely original.
    two_tri = tri + [(1, 0), (1, 1), (1, 2)]
    two_lonely = lonely_labels(abstract_entries(two_tri, 6))
    assert len(two_lonely) == 6
    assert all(label[0] == "pair" for label in two_lonely)
    result["exceptional_smallest"] = {
        "one_fiber_lonely_pairs": len(tri_lonely),
        "two_fibers_lonely_pairs": len(two_lonely),
    }
    return result


def det2(p, q):
    return p[0] * q[1] - p[1] * q[0]


def add2(p, q, sign=1):
    return (p[0] + sign * q[0], p[1] + sign * q[1])


def direction(p):
    assert p != (0, 0)
    return (F(0), F(1)) if p[0] == 0 else (F(1), p[1] / p[0])


def geometric_entries(points):
    out = []
    for i, p in enumerate(points):
        out.append((("original", i), direction(p)))
    for i, j in combinations(range(len(points)), 2):
        out.append((("pair", i, j, +1), direction(add2(points[i], points[j], +1))))
        out.append((("pair", i, j, -1), direction(add2(points[i], points[j], -1))))
    assert len(out) == len(points) ** 2
    return out


def solve_square_system(matrix, rhs):
    a = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    n = len(a)
    for col in range(n):
        pivot = next(i for i in range(col, n) if a[i][col])
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for row in range(n):
            if row != col and a[row][col]:
                scale = a[row][col]
                a[row] = [a[row][j] - scale * a[col][j] for j in range(n + 1)]
    return [a[i][-1] for i in range(n)]


def fit_form(points):
    matrix = [(x * x, 2 * x * y, y * y) for x, y in points[:3]]
    return tuple(solve_square_system(matrix, [F(1)] * 3))


def is_rational_square(x):
    if x < 0:
        return False
    return isqrt(x.numerator) ** 2 == x.numerator and isqrt(x.denominator) ** 2 == x.denominator


def qadd(x, y, sign=1):
    return (x[0] + sign * y[0], x[1] + sign * y[1])


def qmul(x, y, delta):
    # Formal quadratic algebra with s^2 = -delta.
    return (x[0] * y[0] - delta * x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def qconj(x):
    return (x[0], -x[1])


def qdiv(x, y, delta):
    norm = y[0] * y[0] + delta * y[1] * y[1]
    z = qmul(x, qconj(y), delta)
    return (z[0] / norm, z[1] / norm)


def audit_direction_bridge(points, form):
    A, B, C = form
    delta = A * C - B * B
    zs = [(A * x + B * y, y) for x, y in points]
    assert all(qmul(z, qconj(z), delta) == (A, F(0)) for z in zs)
    z0 = zs[0]
    units = [qdiv(z, z0, delta) for z in zs]
    common = qdiv(z0, qconj(z0), delta)
    for z, u in zip(zs, units):
        assert qdiv(qdiv(z, qconj(z), delta), common, delta) == qmul(u, u, delta)
    identities = 0
    for i, j in combinations(range(len(zs)), 2):
        product = qmul(units[i], units[j], delta)
        for eps in (+1, -1):
            z = qadd(zs[i], zs[j], eps)
            lhs = qdiv(qdiv(z, qconj(z), delta), common, delta)
            rhs = product if eps == 1 else (-product[0], -product[1])
            assert lhs == rhs
            identities += 1
    return identities + len(points)


def matrix_rank(rows):
    a = [list(row) for row in rows]
    if not a:
        return 0
    nr, nc = len(a), len(a[0])
    rank = 0
    for col in range(nc):
        pivot = next((i for i in range(rank, nr) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [x / scale for x in a[rank]]
        for row in range(nr):
            if row != rank and a[row][col]:
                scale = a[row][col]
                a[row] = [a[row][j] - scale * a[rank][j] for j in range(nc)]
        rank += 1
        if rank == nr:
            break
    return rank


def gale_matrix(points):
    """Rows are an explicit basis of ker(P^T), using the first two pivots."""
    n = len(points)
    d = n - 2
    p0, p1 = points[:2]
    determinant = det2(p0, p1)
    assert determinant
    rows = []
    for k in range(2, n):
        x, y = points[k]
        alpha = (-x * p1[1] + p1[0] * y) / determinant
        beta = (-p0[0] * y + p0[1] * x) / determinant
        row = [alpha, beta] + [F(int(j == k)) for j in range(2, n)]
        assert sum(row[i] * points[i][0] for i in range(n)) == 0
        assert sum(row[i] * points[i][1] for i in range(n)) == 0
        rows.append(row)
    assert matrix_rank(rows) == d
    return rows


def columns(rows):
    return [tuple(row[j] for row in rows) for j in range(len(rows[0]))]


def vector_sum(coefficients, vectors):
    if not vectors:
        return ()
    return tuple(sum(coefficients[j] * vectors[j][i] for j in range(len(vectors)))
                 for i in range(len(vectors[0])))


def good_coefficients(values):
    return all(values) and len({abs(x) for x in values}) == len(values)


def audit_gale(points):
    entries = geometric_entries(points)
    lonely = lonely_labels(entries)
    Urows = gale_matrix(points)
    Ucols = columns(Urows)
    d = len(points) - 2
    verified = 0
    sign_mutations_rejected = 0
    for label in lonely:
        if label[0] == "original":
            i = label[1]
            w = points[i]
            t = (-w[1], w[0])
            lambdas = [det2(p, w) for p in points]  # p dot (w_y,-w_x)
            assert lambdas[i] == 0
            reduced_cols = [Ucols[k] for k in range(len(points)) if k != i]
            reduced_lam = [lambdas[k] for k in range(len(points)) if k != i]
        else:
            _, i, j, eps = label
            w = add2(points[i], points[j], eps)
            lambdas = [det2(p, w) for p in points]
            assert lambdas[j] == -eps * lambdas[i]
            merged = tuple(Ucols[i][k] - eps * Ucols[j][k] for k in range(d))
            wrong = tuple(Ucols[i][k] + eps * Ucols[j][k] for k in range(d))
            keep = [k for k in range(len(points)) if k not in (i, j)]
            reduced_cols = [merged] + [Ucols[k] for k in keep]
            reduced_lam = [lambdas[i]] + [lambdas[k] for k in keep]
            wrong_residual = vector_sum(reduced_lam, [wrong] + [Ucols[k] for k in keep])
            assert any(wrong_residual)
            sign_mutations_rejected += 1

        assert len(reduced_cols) == d + 1
        assert good_coefficients(reduced_lam)
        assert not any(vector_sum(reduced_lam, reduced_cols))
        assert matrix_rank([[col[j] for col in reduced_cols] for j in range(d)]) == d
        verified += 1

    # Every non-lonely original must fail the corresponding deletion criterion.
    lonely_originals = {label[1] for label in lonely if label[0] == "original"}
    deletion_failures = 0
    for i, w in enumerate(points):
        lambdas = [det2(p, w) for p in points]
        reduced = [lambdas[k] for k in range(len(points)) if k != i]
        good = good_coefficients(reduced)
        assert good == (i in lonely_originals)
        deletion_failures += not good
    return {
        "lonely_reductions_verified": verified,
        "merge_sign_mutations_rejected": sign_mutations_rejected,
        "noncosimple_deletions_verified": deletion_failures,
    }


def conic_point(D, t):
    denominator = 1 + D * t * t
    return ((1 - D * t * t) / denominator, 2 * t / denominator)


def transform_point(M, p):
    return (M[0][0] * p[0] + M[0][1] * p[1],
            M[1][0] * p[0] + M[1][1] * p[1])


def audit_rational_case(D, parameters, M):
    points = [transform_point(M, conic_point(F(D), F(t))) for t in parameters]
    assert all(det2(points[i], points[j]) for i, j in combinations(range(len(points)), 2))
    A, B, C = fit_form(points)
    delta = A * C - B * B
    assert A > 0 and delta > 0
    assert all(A * x * x + 2 * B * x * y + C * y * y == 1 for x, y in points)
    detM = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    assert delta == F(D) / (detM * detM)
    assert is_rational_square(delta / D)
    identities = audit_direction_bridge(points, (A, B, C))
    lonely = lonely_labels(geometric_entries(points))
    assert len(lonely) >= 2
    if D != 3:
        assert sum(label[0] == "original" for label in lonely) >= 2
    gale = audit_gale(points)
    return {
        "D": D,
        "n": len(points),
        "form": [str(A), str(B), str(C)],
        "delta": str(delta),
        "direction_identities": identities,
        "lonely": len(lonely),
        "lonely_originals": sum(label[0] == "original" for label in lonely),
        **gale,
    }


def qpow(x, exponent, D):
    out = (F(1), F(0))
    for _ in range(exponent):
        out = qmul(out, x, F(D))
    return out


def exceptional_family(m):
    D = 3
    u = (F(23, 26), F(7, 26))
    zeta = (F(1, 2), F(1, 2))
    points = []
    for k in range(m):
        uk = qpow(u, k, D)
        for j in range(3):
            points.append(qmul(uk, qpow(zeta, j, D), F(D)))
    assert all(x * x + 3 * y * y == 1 for x, y in points)
    assert all(det2(points[i], points[j]) for i, j in combinations(range(len(points)), 2))
    entries = geometric_entries(points)
    lonely = lonely_labels(entries)
    assert len(lonely) >= 2
    assert not any(label[0] == "original" for label in lonely)
    gale = audit_gale(points)
    assert gale["noncosimple_deletions_verified"] == len(points)
    return {
        "m": m,
        "n": len(points),
        "lonely_pairs": len(lonely),
        **gale,
    }


def main():
    if not __debug__:
        raise RuntimeError("audit.py requires assertions; do not run with python -O")
    abstract = audit_abstract_groups()
    rational = [
        audit_rational_case(1, [0, 1, F(1, 2), F(-1, 3)],
                            ((F(1), F(0)), (F(0), F(1)))),
        audit_rational_case(2, [0, F(1, 2), F(-1, 3), F(2, 3), F(-2, 5)],
                            ((F(2), F(1)), (F(-1), F(1)))),
        audit_rational_case(5, [0, F(1, 3), F(-1, 2), F(1, 4), F(-3, 7), F(4, 9)],
                            ((F(3, 2), F(-2, 3)), (F(1, 4), F(5, 3)))),
        audit_rational_case(3, [0, F(1, 2), F(-1, 4), F(2, 5), F(-3, 8)],
                            ((F(1), F(2)), (F(-1), F(3)))),
    ]
    exceptional = [exceptional_family(m) for m in (1, 2, 3)]
    summary = {
        "status": "VERIFIED",
        "abstract_groups": abstract,
        "rational_cases": rational,
        "exceptional_family": exceptional,
        "totals": {
            "abstract_configurations": sum(abstract[str(w)]["configurations"] for w in (2, 4, 6)),
            "direction_identities": sum(case["direction_identities"] for case in rational),
            "gale_reductions": (sum(case["lonely_reductions_verified"] for case in rational)
                                + sum(case["lonely_reductions_verified"] for case in exceptional)),
            "rejected_wrong_merge_signs": (
                sum(case["merge_sign_mutations_rejected"] for case in rational)
                + sum(case["merge_sign_mutations_rejected"] for case in exceptional)),
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
