#!/usr/bin/env python3
"""Independent SymPy-field checker for the Parts L/S rotation scan.

This implementation imports neither rotation_scan.py nor parts509.py.  It uses
SymPy's AlgebraicField/ANP representation instead of the search program's
eight-tuples, independently enumerates every K-rational cross-edge event, and
replays all positive colouring and criticality witnesses.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import math
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_POINTS = ROOT / "hadwiger_nelson_parts509_criticality" / "parts509.vtx"
N = 509
L_SIZE = 374
RADICALS = tuple(sympy.sqrt(p) for p in (3, 5, 11))
K = sympy.QQ.algebraic_field(*RADICALS)
Z = K.zero
O = K.one
PRIMES = (3, 5, 11)


def _fraction(value) -> Fraction:
    return Fraction(int(value.numerator), int(value.denominator))


def _anp_power_coefficients(value):
    coefficients = [_fraction(q) for q in reversed(value.to_list())]
    return coefficients + [Fraction(0)] * (8 - len(coefficients))


def _invert_matrix(matrix):
    rows = [
        list(row) + [Fraction(int(i == j)) for j in range(8)]
        for i, row in enumerate(matrix)
    ]
    for col in range(8):
        pivot = next(row for row in range(col, 8) if rows[row][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [entry / scale for entry in rows[col]]
        for row in range(8):
            if row == col:
                continue
            scale = rows[row][col]
            if scale:
                rows[row] = [a - scale * b for a, b in zip(rows[row], rows[col])]
    return [row[8:] for row in rows]


_RADICAL_ANP = tuple(K.from_sympy(radical) for radical in RADICALS)
_BASIS_ANP = []
for _mask in range(8):
    _value = O
    for _bit, _radical in enumerate(_RADICAL_ANP):
        if _mask & (1 << _bit):
            _value *= _radical
    _BASIS_ANP.append(_value)
_BASIS_MATRIX = [
    [_anp_power_coefficients(_BASIS_ANP[column])[row] for column in range(8)]
    for row in range(8)
]
_BASIS_MATRIX_INVERSE = _invert_matrix(_BASIS_MATRIX)


def anp_to_multiquadratic(value):
    powers = _anp_power_coefficients(value)
    return tuple(
        sum(_BASIS_MATRIX_INVERSE[row][column] * powers[column] for column in range(8))
        for row in range(8)
    )


def multiquadratic_to_anp(value):
    result = Z
    for coefficient, basis in zip(value, _BASIS_ANP):
        if coefficient:
            result += K.convert(sympy.Rational(coefficient.numerator, coefficient.denominator)) * basis
    return result


def mq_add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def mq_neg(x):
    return tuple(-a for a in x)


def mq_sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def mq_scale(x, scalar):
    return tuple(scalar * a for a in x)


def mq_mul(x, y, primes=PRIMES):
    if not primes:
        return (x[0] * y[0],)
    half = len(x) // 2
    xa, xb, ya, yb = x[:half], x[half:], y[:half], y[half:]
    lower_primes = primes[:-1]
    real = mq_add(
        mq_mul(xa, ya, lower_primes),
        mq_scale(mq_mul(xb, yb, lower_primes), Fraction(primes[-1])),
    )
    radical = mq_add(mq_mul(xa, yb, lower_primes), mq_mul(xb, ya, lower_primes))
    return real + radical


def mq_inv(x, primes=PRIMES):
    if not primes:
        if not x[0]:
            raise ZeroDivisionError
        return (1 / x[0],)
    half = len(x) // 2
    a, b = x[:half], x[half:]
    lower_primes = primes[:-1]
    denominator = mq_add(
        mq_mul(a, a, lower_primes),
        mq_scale(mq_mul(b, b, lower_primes), Fraction(-primes[-1])),
    )
    inv_denominator = mq_inv(denominator, lower_primes)
    return mq_mul(a, inv_denominator, lower_primes) + mq_neg(
        mq_mul(b, inv_denominator, lower_primes)
    )


def mq_div(x, y, primes=PRIMES):
    return mq_mul(x, mq_inv(y, primes), primes)


def rational_sqrt(value: Fraction):
    if value < 0:
        return None
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        return None
    return Fraction(numerator, denominator)


def mq_sqrt(x, primes=PRIMES):
    """Exact recursive square-root membership in a multiquadratic tower."""
    if not primes:
        root = rational_sqrt(x[0])
        return None if root is None else (root,)
    half = len(x) // 2
    a, b = x[:half], x[half:]
    lower_primes = primes[:-1]
    zero = (Fraction(0),) * half
    if b == zero:
        root_a = mq_sqrt(a, lower_primes)
        if root_a is not None:
            candidate = root_a + zero
            if mq_mul(candidate, candidate, primes) == x:
                return candidate
        root_b = mq_sqrt(mq_scale(a, Fraction(1, primes[-1])), lower_primes)
        if root_b is not None:
            candidate = zero + root_b
            if mq_mul(candidate, candidate, primes) == x:
                return candidate
        return None
    norm = mq_add(
        mq_mul(a, a, lower_primes),
        mq_scale(mq_mul(b, b, lower_primes), Fraction(-primes[-1])),
    )
    norm_root = mq_sqrt(norm, lower_primes)
    if norm_root is None:
        return None
    for signed_root in (norm_root, mq_neg(norm_root)):
        u_squared = mq_scale(mq_add(a, signed_root), Fraction(1, 2))
        u = mq_sqrt(u_squared, lower_primes)
        if u is None or u == zero:
            continue
        v = mq_div(b, mq_scale(u, Fraction(2)), lower_primes)
        candidate = u + v
        if mq_mul(candidate, candidate, primes) == x:
            return candidate
    return None


def split_pair(body: str) -> tuple[str, str]:
    text = body.replace("Sqrt[", "sqrt(").replace("]", ")")
    depth = 0
    for index, character in enumerate(text):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            return text[:index], text[index + 1 :]
    raise ValueError("coordinate pair has no top-level comma")


def expression_to_multiquadratic(expression):
    """Reduce a radical expression to the squarefree 8-element basis."""
    expression = sympy.sqrtdenest(expression).expand(power_base=True, force=True)
    symbols = {prime: sympy.Symbol(f"independent_r{prime}") for prime in PRIMES}

    def positive_integer_sqrt(node):
        return bool(
            node.is_Pow
            and node.exp == sympy.Rational(1, 2)
            and node.base.is_Integer
            and node.base > 0
        )

    def split_sqrt(node):
        value = int(node.base)
        result = sympy.Integer(1)
        for prime, exponent in sympy.factorint(value).items():
            result *= prime ** (exponent // 2)
            if exponent % 2:
                if prime not in symbols:
                    raise ValueError(f"unexpected radical sqrt({prime})")
                result *= symbols[prime]
        return result

    polynomial_expression = sympy.expand(
        expression.replace(positive_integer_sqrt, split_sqrt)
    )
    polynomial = sympy.Poly(
        polynomial_expression, *(symbols[prime] for prime in PRIMES)
    )
    coefficients = [Fraction(0)] * 8
    for monomial, coefficient in polynomial.terms():
        if any(exponent not in (0, 1) for exponent in monomial):
            raise ValueError("unreduced radical power")
        mask = sum(1 << bit for bit, exponent in enumerate(monomial) if exponent)
        rational = sympy.Rational(coefficient)
        coefficients[mask] += Fraction(int(rational.p), int(rational.q))
    return tuple(coefficients)


def parse_points(path: Path):
    points = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        x, y = split_pair(line[1:-1])
        points.append(
            (
                multiquadratic_to_anp(
                    expression_to_multiquadratic(sympy.sympify(x))
                ),
                multiquadratic_to_anp(
                    expression_to_multiquadratic(sympy.sympify(y))
                ),
            )
        )
    if len(points) != N or len(set(points)) != N:
        raise ValueError("expected 509 distinct points")
    return points


def norm2(point):
    return point[0] * point[0] + point[1] * point[1]


def squared_distance(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def sign(value) -> int:
    if value == Z:
        return 0
    approximation = sympy.N(K.to_sympy(value), 80)
    if approximation > 0:
        return 1
    if approximation < 0:
        return -1
    raise ArithmeticError("could not separate algebraic sign")


def nonnegative_sqrt_in_k(value):
    value_sign = sign(value)
    if value_sign < 0:
        return None
    if value_sign == 0:
        return Z
    root_coefficients = mq_sqrt(anp_to_multiquadratic(value))
    if root_coefficients is None:
        return None
    root = multiquadratic_to_anp(root_coefficients)
    if root * root != value:
        raise AssertionError("false field-membership result")
    return -root if sign(root) < 0 else root


def enumerate_events(points):
    radii = [norm2(point) for point in points]
    root_cache = {}
    events = defaultdict(set)
    invariant = []
    counters = defaultdict(int)
    for u in range(L_SIZE):
        px, py = points[u]
        for v in range(L_SIZE, N):
            qx, qy = points[v]
            if px == Z and py == Z:
                if radii[v] == O:
                    invariant.append((u, v))
                continue
            rp2, rq2 = radii[u], radii[v]
            rhs = (rp2 + rq2 - O) / 2
            rr = rp2 * rq2
            discriminant = rr - rhs * rhs
            key = (rp2, rq2)
            if key not in root_cache:
                admissible = sign(discriminant) >= 0
                root_cache[key] = (
                    admissible,
                    nonnegative_sqrt_in_k(discriminant) if admissible else None,
                )
            admissible, root = root_cache[key]
            if not admissible:
                continue
            counters["admissible_cross_pairs"] += 1
            if root is None:
                continue
            counters["k_rational_cross_pairs"] += 1
            if root == Z:
                counters["tangent_cross_pairs"] += 1
            a = px * qx + py * qy
            b = py * qx - px * qy
            for epsilon in (1,) if root == Z else (1, -1):
                signed = epsilon * root
                c = (rhs * a - b * signed) / rr
                s = (rhs * b + a * signed) / rr
                if c * c + s * s != O or a * c + b * s != rhs:
                    raise AssertionError("invalid rotation solution")
                events[(c, s)].add((u, v))
        if u and u % 100 == 0:
            print(f"independent enumeration: L vertex {u}/{L_SIZE - 1}", flush=True)
    counters["radius_pair_classes"] = sum(
        int(admissible) for admissible, _root in root_cache.values()
    )
    counters["invariant_cross_edges"] = len(invariant)
    counters["event_rotations"] = len(events)
    return dict(events), sorted(invariant), dict(counters)


def decoded_field(coefficients):
    if len(coefficients) != 8:
        raise ValueError("field element needs eight coefficients")
    return multiquadratic_to_anp(tuple(Fraction(text) for text in coefficients))


def unpack_four(packed: str):
    raw = base64.b64decode(packed, validate=True)
    if len(raw) != (N + 3) // 4:
        raise ValueError("bad packed four-colouring length")
    colors = [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(N)]
    if raw[-1] >> 2:
        raise ValueError("nonzero packed padding")
    return colors


def unpack_five(packed: str):
    colors = list(base64.b64decode(packed, validate=True))
    if len(colors) != N or any(color > 4 for color in colors):
        raise ValueError("bad five-colouring")
    return colors


def check_coloring(colors, edges, deleted=None):
    for u, v in edges:
        if u != deleted and v != deleted and colors[u] == colors[v]:
            raise ValueError(f"monochromatic edge {(u, v)}; deleted={deleted}")


def internal_edges(points):
    tuple_points = [
        (anp_to_multiquadratic(point[0]), anp_to_multiquadratic(point[1]))
        for point in points
    ]
    one = (Fraction(1),) + (Fraction(0),) * 7
    edges = []
    for u in range(N):
        for v in range(u + 1, N):
            if not (v < L_SIZE or u >= L_SIZE):
                continue
            dx = mq_sub(tuple_points[u][0], tuple_points[v][0])
            dy = mq_sub(tuple_points[u][1], tuple_points[v][1])
            if mq_add(mq_mul(dx, dx), mq_mul(dy, dy)) == one:
                edges.append((u, v))
    return edges


def rotate(point, rotation):
    c, s = rotation
    return (c * point[0] - s * point[1], s * point[0] + c * point[1])


def mq_rotate(point, rotation):
    c, s = rotation
    return (
        mq_sub(mq_mul(c, point[0]), mq_mul(s, point[1])),
        mq_add(mq_mul(s, point[0]), mq_mul(c, point[1])),
    )


def enumerate_overlaps(points):
    """Map each exact rotation to all coincident L/S label pairs."""
    radii = [norm2(point) for point in points]
    overlaps = defaultdict(set)
    for u in range(L_SIZE):
        px, py = points[u]
        if px == Z and py == Z:
            continue
        for v in range(L_SIZE, N):
            if radii[u] != radii[v]:
                continue
            qx, qy = points[v]
            c = (px * qx + py * qy) / radii[u]
            s = (py * qx - px * qy) / radii[u]
            if rotate(points[v], (c, s)) != points[u]:
                raise AssertionError("overlap rotation formula failed")
            overlaps[(c, s)].add((u, v))
    return dict(overlaps)


def relabel(signatures):
    ids = {signature: i for i, signature in enumerate(sorted(set(signatures.values())))}
    return {vertex: ids[signature] for vertex, signature in signatures.items()}


def discrete_refinement(edges):
    adjacency = [set() for _ in range(N)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colors = relabel({v: (len(adjacency[v]),) for v in range(N)})
    counts = [len(set(colors.values()))]
    while counts[-1] < N:
        colors = relabel(
            {
                v: (colors[v], tuple(sorted(colors[w] for w in adjacency[v])))
                for v in range(N)
            }
        )
        new_count = len(set(colors.values()))
        if new_count <= counts[-1]:
            raise ValueError("refinement stabilized non-discretely")
        counts.append(new_count)
    canonical_edges = sorted(
        (min(colors[u], colors[v]), max(colors[u], colors[v])) for u, v in edges
    )
    import hashlib

    digest = hashlib.sha256(
        "".join(f"{u} {v}\n" for u, v in canonical_edges).encode("ascii")
    ).hexdigest()
    return counts, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scan", type=Path)
    parser.add_argument("criticality", type=Path)
    parser.add_argument("--points", type=Path, default=DEFAULT_POINTS)
    args = parser.parse_args()

    scan = json.loads(args.scan.read_text())
    criticality = json.loads(args.criticality.read_text())
    if scan.get("format") != "parts509-k-rational-rotation-scan-v1":
        raise ValueError("rotation certificate format mismatch")
    if criticality.get("format") != "parts509-rotation-criticality-v1":
        raise ValueError("criticality certificate format mismatch")
    if criticality.get("scan_sha256") != hashlib.sha256(args.scan.read_bytes()).hexdigest():
        raise ValueError("criticality certificate is bound to a different scan")
    points = parse_points(args.points)
    events, invariant, stats = enumerate_events(points)
    for key, value in stats.items():
        if scan["counts"].get(key) != value:
            raise ValueError(f"count mismatch for {key}: {value}")
    if [list(edge) for edge in invariant] != scan["invariant_cross_edges"]:
        raise ValueError("invariant cross edges differ")

    certificate_events = {}
    for index, record in enumerate(scan["events"]):
        rotation = (decoded_field(record["cos"]), decoded_field(record["sin"]))
        if rotation in certificate_events:
            raise ValueError("duplicate certificate rotation")
        certificate_events[rotation] = (index, record)
    if set(events) != set(certificate_events):
        raise ValueError("certificate rotation set is incomplete or has extras")

    base_edges = internal_edges(points) + invariant
    overlaps = enumerate_overlaps(points)
    if not set(overlaps).issubset(events):
        raise ValueError("a coincidence rotation is missing from the unit-edge events")
    uncolorable = []
    duplicate_count = 0
    for rotation, event_edges in events.items():
        index, record = certificate_events[rotation]
        if sorted(event_edges) != [tuple(edge) for edge in record["event_cross_edges"]]:
            raise ValueError(f"cross-edge mismatch at event {index}")
        overlap_pairs = overlaps.get(rotation, set())
        distinct = N - len(overlap_pairs)
        if record["distinct_points"] != distinct:
            raise ValueError(f"distinct-point mismatch at event {index}")
        edges = base_edges + sorted(event_edges)
        if record["four_coloring"] is None:
            uncolorable.append(index)
        else:
            colors = unpack_four(record["four_coloring"])
            check_coloring(colors, edges)
            for u, v in overlap_pairs:
                duplicate_count += 1
                if colors[u] != colors[v]:
                    raise ValueError("coincident labels receive different colours")
    uncolorable = sorted(uncolorable)
    if uncolorable != scan["counts"]["uncolorable_event_indices"]:
        raise ValueError("uncolourable-event list mismatch")
    check_coloring(unpack_four(scan["generic_four_coloring"]), base_edges)

    # Independently replay criticality witnesses and refinement identifiers.
    representative_records = {
        int(record["event_index"]): record for record in criticality["representatives"]
    }
    hash_classes = defaultdict(list)
    exceptional_edges = {}
    for index in uncolorable:
        rotation = next(r for r, pair in certificate_events.items() if pair[0] == index)
        edges = base_edges + sorted(events[rotation])
        exceptional_edges[index] = edges
        _, graph_hash = discrete_refinement(edges)
        hash_classes[graph_hash].append(index)
    observed_classes = [
        {"canonical_edge_sha256": key, "event_indices": value}
        for key, value in sorted(hash_classes.items(), key=lambda item: min(item[1]))
    ]
    certified_class_cores = [
        {
            "canonical_edge_sha256": record["canonical_edge_sha256"],
            "event_indices": record["event_indices"],
        }
        for record in criticality["isomorphism_classes"]
    ]
    if observed_classes != certified_class_cores:
        raise ValueError("isomorphism-class certificate mismatch")
    for record in criticality["isomorphism_classes"]:
        representative = int(record["representative_event_index"])
        representative_edges = set(exceptional_edges[representative])
        for text_index, mapping in record["isomorphisms_to_representative"].items():
            index = int(text_index)
            if sorted(mapping) != list(range(N)):
                raise ValueError("isomorphism map is not a permutation")
            mapped_edges = {
                (min(mapping[u], mapping[v]), max(mapping[u], mapping[v]))
                for u, v in exceptional_edges[index]
            }
            if mapped_edges != representative_edges:
                raise ValueError("claimed exceptional-graph isomorphism fails")
    for index in (108, 109):
        rotation = next(r for r, pair in certificate_events.items() if pair[0] == index)
        edges = base_edges + sorted(events[rotation])
        record = representative_records[index]
        check_coloring(unpack_five(record["five_coloring"]), edges)
        witnesses = record["deletion_four_colorings"]
        if len(witnesses) != N:
            raise ValueError("criticality witness count mismatch")
        for deleted, witness in enumerate(witnesses):
            check_coloring(unpack_four(witness), edges, deleted)

    print(f"exact_event_rotations={len(events)}")
    print(f"four_colorable_event_rotations={len(events) - len(uncolorable)}")
    print(f"exceptional_event_rotations={uncolorable}")
    print(f"exceptional_isomorphism_classes={len(hash_classes)}")
    print(f"coincident_labels_checked={duplicate_count}")
    print("alternate_vertex_criticality_witnesses=1018")
    print("independent_all_checks=true")


if __name__ == "__main__":
    main()
