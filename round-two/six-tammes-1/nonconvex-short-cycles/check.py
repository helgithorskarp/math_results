#!/usr/bin/env python3
"""Exact auxiliary checks; the continuous nonconvex covering proof is written.

CPython >=3.11, standard library only. The pinned parent module supplies
exact quadratic-field arithmetic. It is not an independent implementation
of that arithmetic. EXPECTED.json is output, never a mathematical input.
"""

from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


PARENT_HASH = "52361f7a08e81b5c58433e1f88e18cea9ea7d4c9d391fdf4a45bdb9e910230fc"
parent_path = Path(__file__).resolve().parents[1] / "short-polygon-cover" / "check.py"
require(hashlib.sha256(parent_path.read_bytes()).hexdigest() == PARENT_HASH,
        "parent checker differs from pinned source")
spec = importlib.util.spec_from_file_location("short_polygon_exact_arithmetic", parent_path)
parent = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = parent
spec.loader.exec_module(parent)
Q = parent.Quadratic


def poly_add(*items):
    result = [F(0)] * max(map(len, items))
    for coefficients in items:
        for i, value in enumerate(coefficients):
            result[i] += value
    return result


def poly_scale(coefficients, scalar):
    return [scalar * x for x in coefficients]


def poly_mul(left, right):
    result = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return result


def arithmetic():
    one, a = Q(5, 1), Q(5, F(-1, 4), F(1, 4))
    cosine = [F(0), F(1)]
    cosine2 = [F(-1), F(0), F(2)]
    cosine3 = [F(0), F(-3), F(0), F(4)]
    base = poly_add([F(1)], poly_scale(cosine, 2))
    rows = {
        3: base,
        4: poly_add(base, cosine2),
        5: poly_add(base, poly_scale(cosine2, 2)),
        6: poly_add(base, poly_scale(cosine2, 2), cosine3),
    }
    require(rows[3] == [F(1), F(2)], "triangle row")
    require(rows[4] == poly_mul([F(0), F(2)], [F(1), F(1)]), "quad row factorization")
    require(rows[6] == poly_mul([F(1), F(1)], poly_mul([F(-1), F(2)], [F(1), F(2)])),
            "hexagon row factorization")
    pent_factor = poly_scale(poly_mul([-a, one], [a + F(1, 2), one]), 4)
    require(pent_factor == [Q(5, x) for x in rows[5]], "pentagon row factorization")
    require((a - F(1, 4)).sign() > 0 and (one - a).sign() > 0, "cosine domain")

    upper_a, error, margin = F(3091, 10000), F(1, 60), F(1, 500)
    sqrt_upper = 4 * upper_a + 1
    require(sqrt_upper == F(5591, 2500), "sqrt bound conversion")
    require(sqrt_upper ** 2 - 5 == F(9281, 6250000), "sqrt bound square gap")
    require((Q(5, upper_a) - a).sign() > 0, "positive pentagon cosine gap")
    endpoints = [F(1, 2), F(3, 5)]
    values = [c - error - upper_a - (1 - upper_a) * (c + margin) ** 2
              for c in endpoints]
    require(values == [F(928273, 7500000000), F(178863073, 7500000000)],
            "uniform margin endpoint values")
    require(all(x > 0 for x in values) and -(1 - upper_a) < 0, "positive concave margin")
    require(endpoints[0] - error > upper_a and 0 < endpoints[-1] + margin < 1,
            "uniform domain")
    planarity = [c - error - c * c for c in endpoints]
    require(all(x > 0 for x in planarity), "strict short-edge threshold")

    narrower_endpoints = [F(14, 25), F(3, 5)]
    narrower_error, narrower_margin = F(1, 32), F(1, 400)
    narrower_values = [c - narrower_error - upper_a - (1 - upper_a) * (c + narrower_margin) ** 2
                       for c in narrower_endpoints]
    require(narrower_values == [F(107, 102400), F(14158371, 1600000000)],
            "narrower interval endpoint values")
    require(all(x > 0 for x in narrower_values), "narrower interval positive margin")
    require(narrower_endpoints[0] - narrower_error > upper_a
            and 0 < narrower_endpoints[-1] + narrower_margin < 1,
            "narrower interval domain")

    uniform = (one - 3 * a) / 4
    require(uniform == Q(5, F(7, 16), F(-3, 16)), "sharp uniform tolerance")
    require((uniform - error).sign() > 0, "chosen tolerance below sharp supremum")
    derivative_lower = one - 2 * (one - a) * endpoints[-1]
    require(derivative_lower.sign() > 0, "monotonic tolerance function")
    critical = a / (one - a)
    require(critical == Q(5, 0, F(1, 5)), "regular example packing threshold")

    # Full coefficient comparison for c-K5(c)=(1-c)((1-a)c-a).
    left = [-a, one, -(one - a)]
    right = poly_mul([one, -one], [-a, one - a])
    require(left == right, "pentagon insertion threshold factorization")
    return {
        "hemisphere_row_coefficients": {str(m): [str(x) for x in row] for m, row in rows.items()},
        "c_interval": [str(x) for x in endpoints],
        "edge_tolerance": str(error),
        "strict_cover_margin": str(margin),
        "cos_72_upper_bound": str(upper_a),
        "sqrt5_bound_square_gap": str(sqrt_upper ** 2 - 5),
        "margin_endpoint_lower_bounds": [str(x) for x in values],
        "planarity_endpoint_margins": [str(x) for x in planarity],
        "sharp_uniform_tolerance": uniform.record(),
        "tolerance_derivative_lower_bound": derivative_lower.record(),
        "narrower_band": {
            "c_interval": [str(x) for x in narrower_endpoints],
            "edge_tolerance": str(narrower_error),
            "strict_cover_margin": str(narrower_margin),
            "margin_endpoint_lower_bounds": [str(x) for x in narrower_values],
        },
    }


def exceptional_paths():
    records = {}
    for m in (4, 5, 6):
        count = 0
        lengths = {}
        for word in product("APN", repeat=m):
            active = {i for i, role in enumerate(word) if role == "A"}
            if len(active) < 3:
                continue
            if not any(word[i] == word[(i + 1) % m] == "N" for i in range(m)):
                continue
            require(m in (5, 6), "exceptional quadrilateral")
            runs = []
            for i, role in enumerate(word):
                if role != "N" or word[(i - 1) % m] == "N":
                    continue
                r = 1
                while word[(i + r) % m] == "N":
                    r += 1
                if r >= 2:
                    runs.append((i, r))
            require(len(runs) == 1, "multiple exceptional runs")
            start, r = runs[0]
            require(r in (2, 3) and (m != 5 or r == 2), "exceptional run length")
            path = [(start + r + j) % m for j in range(m - r)]
            require(active <= set(path), "complementary path misses an active vertex")
            require(all(word[i] != "N" or word[j] != "N" for i, j in zip(path, path[1:])),
                    "exceptional edge on complementary path")
            edges = len(path) - 1
            require(edges == m - r - 1, "complementary edge count")
            require((m == 5 and edges == 2) or (m == 6 and edges <= 3),
                    "active-direction path budget")
            count += 1
            key = str(r)
            lengths[key] = lengths.get(key, 0) + 1
        records[str(m)] = {"exceptional_words": count, "run_lengths": lengths}
    require(records == {
        "4": {"exceptional_words": 0, "run_lengths": {}},
        "5": {"exceptional_words": 5, "run_lengths": {"2": 5}},
        "6": {"exceptional_words": 48, "run_lengths": {"2": 42, "3": 6}},
    }, "exceptional path census")
    return records


def winding_control():
    """The parent's genuine contact pentagon has an interior negative increment."""
    D, c = 3835, F(7, 12)
    root = Q(D, 0, 1)
    u, w = F(7, 18) - root / 117, F(7, 18) + root / 45
    metric = (F(13, 24), F(5, 24), F(1))
    points = {
        "V": (0, 0, 1), "A": (u, -w, c), "P": (1, -1, F(1, 2)),
        "Q": (1, 1, F(1, 2)), "B": (u, w, c),
    }

    def dot(p, r):
        return sum((Q(D, h) * x * y for h, x, y in zip(metric, p, r)), Q(D))

    for p in points.values():
        require(dot(p, p) == Q(D, 1), "nonunit winding-example point")
    contacts = []
    for left, right in combinations("VAPQB", 2):
        value = dot(points[left], points[right])
        require((value - c).sign() <= 0 and (1 - value).sign() > 0,
                "winding-example code inequality")
        if value == Q(D, c):
            contacts.append("".join(sorted(left + right)))
    require(sorted(contacts) == ["AP", "AV", "BQ", "BV", "PQ"], "winding-example contacts")

    # Its normalization is strictly inside the minor triangle VAP.
    query = tuple(Q(D).coerce(points["V"][j]) + 8 * points["A"][j] + points["P"][j]
                  for j in range(3))
    require(query[2].sign() > 0, "northern query")
    projected = {name: tuple(Q(D).coerce(x) / p[2] for x in p[:2])
                 for name, p in points.items()}
    q = tuple(x / query[2] for x in query[:2])
    order = "VAPQB"
    vertices = [projected[name] for name in order]
    edges = list(zip(vertices, vertices[1:] + vertices[:1]))

    def orientation(p, r, s):
        return (r[0] - p[0]) * (s[1] - p[1]) - (r[1] - p[1]) * (s[0] - p[0])

    # Direct exact segment test, separate from the ray-crossing winding calculation.
    for i, j in combinations(range(5), 2):
        if (i - j) % 5 in (1, 4):
            continue
        a, b = edges[i]
        d, e = edges[j]
        signs = [orientation(a, b, d).sign(), orientation(a, b, e).sign(),
                 orientation(d, e, a).sign(), orientation(d, e, b).sign()]
        require(all(s != 0 for s in signs), "collinear winding-example edge")
        require(not (signs[0] * signs[1] < 0 and signs[2] * signs[3] < 0),
                "self-crossing winding example")

    winding = 0
    increments = []
    for i, (a, b) in enumerate(edges):
        turn = orientation(a, b, q)
        sign = turn.sign()
        require(sign != 0, "boundary query")
        ay, by = (a[1] - q[1]).sign(), (b[1] - q[1]).sign()
        if ay <= 0 < by and sign > 0:
            winding += 1
        elif by <= 0 < ay and sign < 0:
            winding -= 1
        # Positive diagonal metric and positive northern normalizations
        # make this the sign of det(q,v_i,v_(i+1)), hence of delta_i.
        increments.append({"edge": order[i] + order[(i + 1) % 5],
                           "sign": sign, "projected_determinant": turn.record()})
    require(winding == 1, "interior winding number")
    require([x["sign"] for x in increments] == [1, 1, 1, 1, -1],
            "real contact-cycle negative increment")
    require(orientation(vertices[-1], vertices[0], vertices[1]).sign() < 0,
            "contact control is not concave")
    return {"c": str(c), "contact_set": sorted(contacts), "unit_points": 5,
            "checked_pairs": 10, "query_cone_weights": {"V": 1, "A": 8, "P": 1},
            "winding_number": winding, "increments": increments,
            "negative_increment_count": 1,
            "scope": "genuine concave spherical contact pentagon; tests signed winding"}


def inverse(matrix):
    n = len(matrix)
    work = [row[:] + [Q(5, int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for i in range(n):
        pivot = work[i][i]
        require(pivot.sign() > 0, "nonpositive basis pivot")
        work[i] = [x / pivot for x in work[i]]
        for j in range(n):
            if i == j:
                continue
            coefficient = work[j][i]
            work[j] = [x - coefficient * y for x, y in zip(work[j], work[i])]
    return [row[n:] for row in work]


def validate_gram(gram, c):
    n = len(gram)
    require(n == 6 and all(len(row) == n for row in gram), "Gram shape")
    for i in range(n):
        require(gram[i][i] == Q(5, 1), "nonunit Gram diagonal")
        for j in range(i):
            require(gram[i][j] == gram[j][i], "asymmetric Gram")
            require((gram[i][j] - c).sign() <= 0 and (1 - gram[i][j]).sign() > 0,
                    "Gram code inequality or distinctness")
    basis = [row[:3] for row in gram[:3]]
    inv = inverse(basis)
    for i in range(3, n):
        for j in range(3, n):
            predicted = sum((gram[i][r] * inv[r][s] * gram[s][j]
                             for r in range(3) for s in range(3)), Q(5))
            require(gram[i][j] == predicted, "nonzero Gram Schur complement")
    return {"points": n, "pairs": n * (n - 1) // 2,
            "positive_basis_rank": 3, "zero_schur_entries": 9}


def sharp_example():
    c = F(1, 2)
    a, b = Q(5, F(-1, 4), F(1, 4)), Q(5, F(-1, 4), F(-1, 4))
    adjacent = c * c + (1 - c * c) * a
    diagonal = c * c + (1 - c * c) * b
    gram = [[Q(5, 1) if i == j else Q(5, c) if i == 0 or j == 0
             else adjacent if (i - j) % 5 in (1, 4) else diagonal
             for j in range(6)] for i in range(6)]
    result = validate_gram(gram, c)
    tolerance = Q(5, c) - adjacent
    require(tolerance == Q(5, F(7, 16), F(-3, 16)), "sharp example tolerance")
    require((adjacent - c).sign() < 0 and (diagonal - adjacent).sign() < 0,
            "sharp example noncontact signs")
    result.update({"c": str(c), "boundary_dot": adjacent.record(),
                   "nonadjacent_dot": diagonal.record(), "axis_dot": str(c),
                   "uniform_tolerance": tolerance.record()})

    controls = []
    for name, i, j, new_value in [
        ("overlarge_pair", 0, 3, Q(5, c + F(1, 1000))),
        ("nonrealizable_gram", 3, 4, adjacent + F(1, 1000)),
    ]:
        altered = [row[:] for row in gram]
        altered[i][j] = altered[j][i] = new_value
        try:
            validate_gram(altered, c)
        except ValueError:
            controls.append(name)
        else:
            raise ValueError("invalid Gram control accepted: " + name)
    require(len(controls) == 2, "Gram control count")
    result["rejected_controls"] = controls
    return result


if __name__ == "__main__":
    result = {
        "status": "all exact auxiliary checks passed",
        "parent_checker_sha256": PARENT_HASH,
        "arithmetic": arithmetic(),
        "exceptional_paths": exceptional_paths(),
        "signed_winding_control": winding_control(),
        "sharp_six_point_example": sharp_example(),
        "trust_boundary": "continuous minimum, Jordan winding, and arc geometry remain written",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
