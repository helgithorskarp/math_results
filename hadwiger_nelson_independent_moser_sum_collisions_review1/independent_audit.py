#!/usr/bin/env python3
"""Clean-room exact inventory and positive-certificate audit.

The checker imports no code from the reviewed package.  Its representation
is E=Q(sqrt(33))[alpha]/(alpha^2+3), rather than the target's four-coordinate
basis.  The target certificate and expected summary are inputs, not code.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from math import isqrt, lcm
from pathlib import Path

Q = tuple[F, F]                 # a+b*sqrt(33)
E = tuple[Q, Q]                 # x+alpha*y, alpha^2=-3
X = tuple[E, E]                 # z0+z1*sqrt(s)

Q0: Q = (F(0), F(0))
Q1: Q = (F(1), F(0))
E0: E = (Q0, Q0)
E1: E = (Q1, Q0)


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def qa(a: Q, b: Q) -> Q:
    return (a[0] + b[0], a[1] + b[1])


def qs(a: Q, b: Q) -> Q:
    return (a[0] - b[0], a[1] - b[1])


def qc(a: Q, c: F | int) -> Q:
    return (a[0] * c, a[1] * c)


def qm(a: Q, b: Q) -> Q:
    return (a[0] * b[0] + 33 * a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def qi(a: Q) -> Q:
    denominator = a[0] * a[0] - 33 * a[1] * a[1]
    need(denominator != 0, "division by zero in Q(sqrt(33))")
    return (a[0] / denominator, -a[1] / denominator)


def qsign(a: Q) -> int:
    x, y = a
    if y == 0:
        return (x > 0) - (x < 0)
    if x == 0:
        return (y > 0) - (y < 0)
    if (x > 0) == (y > 0):
        return (x > 0) - (x < 0)
    comparison = x * x - 33 * y * y
    return ((x > 0) - (x < 0)) * ((comparison > 0) - (comparison < 0))


def rational_sqrt(a: F) -> F | None:
    if a < 0:
        return None
    numerator, denominator = isqrt(a.numerator), isqrt(a.denominator)
    if numerator * numerator == a.numerator and denominator * denominator == a.denominator:
        return F(numerator, denominator)
    return None


def qsqrt(a: Q) -> Q | None:
    x, y = a
    if y == 0:
        root = rational_sqrt(x)
        if root is not None:
            return (root, F(0))
        root = rational_sqrt(x / 33)
        return None if root is None else (F(0), root)
    discriminant_root = rational_sqrt(x * x - 33 * y * y)
    if discriminant_root is None:
        return None
    for sign in (-1, 1):
        root = rational_sqrt((x + sign * discriminant_root) / 2)
        if root:
            answer = (root, y / (2 * root))
            need(qm(answer, answer) == a, "quadratic square-root identity")
            return answer
    return None


def ea(a: E, b: E) -> E:
    return (qa(a[0], b[0]), qa(a[1], b[1]))


def es(a: E, b: E) -> E:
    return (qs(a[0], b[0]), qs(a[1], b[1]))


def ec(a: E, c: F | int) -> E:
    return (qc(a[0], c), qc(a[1], c))


def em(a: E, b: E) -> E:
    return (qs(qm(a[0], b[0]), qc(qm(a[1], b[1]), 3)),
            qa(qm(a[0], b[1]), qm(a[1], b[0])))


def econj(a: E) -> E:
    return (a[0], qc(a[1], -1))


def enorm(a: E) -> Q:
    return qa(qm(a[0], a[0]), qc(qm(a[1], a[1]), 3))


def ei(a: E) -> E:
    inverse_norm = qi(enorm(a))
    conjugate = econj(a)
    return (qm(conjugate[0], inverse_norm), qm(conjugate[1], inverse_norm))


def ediv(a: E, b: E) -> E:
    return em(a, ei(b))


def xm_e(a: X, b: E) -> X:
    return (em(a[0], b), em(a[1], b))


def xa(*values: X) -> X:
    answer = (E0, E0)
    for value in values:
        answer = (ea(answer[0], value[0]), ea(answer[1], value[1]))
    return answer


def xmul(a: X, b: X, s: Q) -> X:
    return (ea(em(a[0], b[0]), em((s, Q0), em(a[1], b[1]))),
            ea(em(a[0], b[1]), em(a[1], b[0])))


def xconj(a: X) -> X:
    return (econj(a[0]), econj(a[1]))


def flat(a: E) -> tuple[F, F, F, F]:
    # alpha*(c+d*sqrt(33)) = c*alpha + 3*d*beta.
    return (a[0][0], a[0][1], a[1][0], 3 * a[1][1])


def ser_e(a: E) -> list[str]:
    return [str(value) for value in flat(a)]


def digest(value: object) -> str:
    packed = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(packed).hexdigest()


@lru_cache(maxsize=None)
def root33(bits: int) -> int:
    need(bits >= 3, "root precision")
    # Write root=1+8*t.  Then 4*t^2+t-2=0 has odd derivative,
    # so ordinary one-bit Hensel lifting applies to t.
    t = 0
    for exponent in range(bits - 3):
        if (4 * t * t + t - 2) % (1 << (exponent + 1)):
            t += 1 << exponent
    root = (1 + 8 * t) % (1 << bits)
    root %= 1 << bits
    need((root * root - 33) % (1 << bits) == 0 and root % 8 == 1,
         "independent Hensel lift")
    return root


@lru_cache(maxsize=None)
def q2_data(a: Q, residue_bits: int = 3) -> tuple[int, int]:
    denominator = lcm(a[0].denominator, a[1].denominator)
    left, right = int(a[0] * denominator), int(a[1] * denominator)
    denominator_valuation = (denominator & -denominator).bit_length() - 1
    odd_denominator = denominator >> denominator_valuation
    bits = 16
    while bits < 4096:
        modulus = 1 << bits
        numerator = (left + right * root33(bits)) * pow(odd_denominator, -1, modulus) % modulus
        if numerator:
            valuation = (numerator & -numerator).bit_length() - 1
            if valuation + residue_bits <= bits:
                return (valuation - denominator_valuation,
                        (numerator >> valuation) % (1 << residue_bits))
        bits *= 2
    raise ValueError("2-adic valuation did not stabilize")


def spindle() -> list[E]:
    rho: E = ((F(1, 2), F(0)), (F(1, 2), F(0)))
    eta: E = ((F(5, 6), F(0)), (F(0), F(1, 18)))
    return [E0, E1, rho, ea(E1, rho), eta, em(eta, rho), em(eta, ea(E1, rho))]


def difference_map(points: list[E]) -> dict[E, list[tuple[int, int]]]:
    answer: dict[E, list[tuple[int, int]]] = {}
    for i, left in enumerate(points):
        for j, right in enumerate(points):
            answer.setdefault(es(left, right), []).append((i, j))
    return answer


def generic_edges(source_edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    answer: set[tuple[int, int]] = set()
    for axis in range(3):
        for fixed in product(range(7), repeat=2):
            for left, right in source_edges:
                a = [0, 0, 0]
                b = [0, 0, 0]
                a[axis], b[axis] = left, right
                other = [i for i in range(3) if i != axis]
                for position, value in zip(other, fixed):
                    a[position] = b[position] = value
                ia, ib = 49 * a[0] + 7 * a[1] + a[2], 49 * b[0] + 7 * b[1] + b[2]
                answer.add(tuple(sorted((ia, ib))))
    return sorted(answer)


def three_factor_inventory(M: list[E]) -> tuple[dict, list[tuple[int, X, X, tuple[int, int, int]]], list[Q]]:
    D = sorted({es(a, b) for a in M for b in M if a != b})
    index = {value: i for i, value in enumerate(D)}
    norms = sorted({enorm(value) for value in D})
    shapes: dict[tuple[Q, Q, Q], tuple[Q, Q, Q | None] | None] = {}
    counts: Counter[str] = Counter()
    radicands: set[Q] = set()
    for A, B, C in product(norms, repeat=3):
        H = qs(qa(A, B), C)
        delta = qs(qc(qm(A, B), 4), qm(H, H))
        sign = qsign(delta)
        counts[f"shape_{sign}"] += 1
        if sign < 0:
            shapes[A, B, C] = None
            continue
        s = qc(delta, F(1, 3))
        root = qsqrt(s)
        shapes[A, B, C] = (H, s, root)
        if sign > 0 and root is None:
            radicands.add(s)

    representatives: list[Q] = []
    classes: dict[Q, tuple[int, Q]] = {}
    for s in sorted(radicands):
        for field, representative in enumerate(representatives):
            factor = qsqrt(qm(s, qi(representative)))
            if factor is not None:
                classes[s] = (field, factor)
                break
        else:
            classes[s] = (len(representatives), Q1)
            representatives.append(s)

    outside: dict[tuple[int, X, X], tuple[int, int, int]] = {}
    infield: set[tuple[E, E]] = set()
    norm_cache = {value: enorm(value) for value in D}
    inverse_cache = {value: ei(value) for value in D}
    for a, b, c in product(D, repeat=3):
        shape = shapes[norm_cache[a], norm_cache[b], norm_cache[c]]
        if shape is None:
            counts["nonphysical_triples"] += 1
            continue
        H, s, root = shape
        denominator = qc(qi(norm_cache[a]), F(1, 2))
        base_e: E = (qm(H, denominator), Q0)
        if root is not None:
            tail: E = (Q0, qm(root, denominator))
            for sign in ((1,) if root == Q0 else (-1, 1)):
                x = ea(base_e, ec(tail, sign))
                u = ec(em(em(a, x), inverse_cache[b]), -1)
                v = ec(em(em(a, es(E1, x)), inverse_cache[c]), -1)
                need(enorm(u) == enorm(v) == Q1, "in-field phase norm")
                need(ea(ea(a, em(u, b)), em(v, c)) == E0, "in-field collision")
                infield.add((u, v))
                counts["E_labelled_roots"] += 1
        else:
            field, factor = classes[s]
            tail = (Q0, qm(factor, denominator))
            for sign in (-1, 1):
                x: X = (base_e, ec(tail, sign))
                u = xm_e(x, ec(em(a, inverse_cache[b]), -1))
                v = xm_e((es(E1, x[0]), ec(x[1], -1)),
                         ec(em(a, inverse_cache[c]), -1))
                need(xmul(u, xconj(u), representatives[field]) == (E1, E0),
                     "outside phase u norm")
                need(xmul(v, xconj(v), representatives[field]) == (E1, E0),
                     "outside phase v norm")
                collision = xa((a, E0), xm_e(u, b), xm_e(v, c))
                need(collision == (E0, E0), "outside collision")
                outside.setdefault((field, u, v), (index[a], index[b], index[c]))
                counts["outside_labelled_roots"] += 1

    roots = [(field, u, v, witness) for (field, u, v), witness in sorted(outside.items())]
    data = {
        "D": [ser_e(value) for value in D],
        "fields": [ser_e((value, Q0)) for value in representatives],
        "roots": [
            {
                "field": field,
                "u": [ser_e(u[0]), ser_e(u[1])],
                "v": [ser_e(v[0]), ser_e(v[1])],
                "witness": witness,
            }
            for field, u, v, witness in roots
        ],
        "infield": [[ser_e(u), ser_e(v)] for u, v in sorted(infield)],
        "summary": dict(counts,
                        source_differences=len(D), norms=len(norms),
                        radicands=len(radicands), quadratic_extensions=len(representatives),
                        outside_pairs=len(roots), infield_pairs=len(infield)),
    }
    return data, roots, representatives


def rotations(M: list[E], D: list[E]) -> tuple[list[E], int]:
    phases = {
        ec(ediv(a, b), -1)
        for a, b in product(D, repeat=2)
        if enorm(a) == enorm(b)
    }
    lam = em(M[2], M[4])
    need({em(lam, econj(m)) for m in M} == set(M), "spindle conjugation symmetry")
    need({econj(u) for u in phases} == phases, "phase conjugation closure")
    return sorted({min(u, econj(u)) for u in phases}), len(phases)


def two_factor_inventory(M: list[E], D: list[E], certificate: dict) -> tuple[list, list[dict], str]:
    representatives, phase_count = rotations(M, D)
    need(phase_count == 30 and len(representatives) == 16, "rotation census")
    Dm = difference_map(M)
    nonzero_m = [value for value in Dm if value != E0]
    norm_m = {value: enorm(value) for value in nonzero_m}
    two_keys: list = []
    summaries: list[dict] = []
    edge_hash = sha256()
    total_groups = 0

    for case_number, u in enumerate(representatives):
        B = sorted({ea(a, em(u, b)) for a, b in product(M, repeat=2)})
        b_index = {value: i for i, value in enumerate(B)}
        Db = difference_map(B)
        nonzero_b = [value for value in Db if value != E0]
        norm_b = {value: enorm(value) for value in nonzero_b}
        groups: dict[tuple[E, E], list[tuple[E, E]]] = {}
        stats: Counter[str] = Counter()
        for a, b in product(nonzero_b, nonzero_m):
            S = qs(qa(norm_b[a], norm_m[b]), Q1)
            if S == Q0:
                stats["trace_zero"] += 1
                continue
            va, vb = q2_data(norm_b[a])[0], q2_data(norm_m[b])[0]
            need(va % 2 == vb % 2 == 0, "norm valuation parity")
            trace_valuation = q2_data(S)[0] - (va + vb) // 2
            if trace_valuation >= -1:
                stats["trace_ge_minus1"] += 1
                continue
            delta = qs(qc(qm(norm_b[a], norm_m[b]), 4), qm(S, S))
            if qsign(delta) <= 0:
                stats["nonpositive_delta"] += 1
                continue
            radicand = qc(delta, F(1, 3))
            if qsqrt(radicand) is not None:
                stats["E_root"] += 1
                continue
            c = em(econj(a), b)
            T = ec(ediv((S, Q0), c), -1)
            J = ediv(econj(c), c)
            groups.setdefault((T, J), []).append((a, b))
            stats["event"] += 1

        ordered_groups = sorted(groups.items())
        rows = certificate["two"][case_number]
        need(len(rows) == len(ordered_groups), "two-factor certificate coverage")

        base: set[tuple[int, int]] = set()
        source_edges = [(i, j) for i, j in combinations(range(7), 2)
                        if enorm(es(M[i], M[j])) == Q1]
        b_edges = [(i, j) for i, j in combinations(range(len(B)), 2)
                   if enorm(es(B[i], B[j])) == Q1]
        for i, ii in b_edges:
            for j in range(7):
                base.add((7 * i + j, 7 * ii + j))
        for i in range(len(B)):
            for j, jj in source_edges:
                base.add((7 * i + j, 7 * i + jj))

        formal_to_physical = [
            7 * b_index[ea(M[i], em(u, M[j]))] + k
            for i, j, k in product(range(7), repeat=3)
        ]
        edge_counts: Counter[int] = Counter()
        for group_number, (((T, J), directions), row) in enumerate(zip(ordered_groups, rows)):
            need(isinstance(row, int) and 0 <= row < len(certificate["words"]),
                 "two-factor word index")
            word = certificate["words"][row]
            colours: list[str | None] = [None] * (7 * len(B))
            for formal, physical in enumerate(formal_to_physical):
                colour = word[formal]
                need(colours[physical] is None or colours[physical] == colour,
                     "two-factor word does not descend")
                colours[physical] = colour
            need(all(colour is not None for colour in colours), "uncoloured physical point")

            edges = set(base)
            for a, b in directions:
                for i, ii in Db[a]:
                    for j, jj in Dm[b]:
                        edges.add(tuple(sorted((7 * i + j, 7 * ii + jj))))
            edge_list = sorted(edges)
            need(all(colours[left] != colours[right] for left, right in edge_list),
                 "two-factor event edge is monochromatic")
            edge_counts[len(edge_list)] += 1
            edge_hash.update(f"{case_number},{group_number}:{digest(edge_list)}\n".encode())
            two_keys.append([ser_e(u), [ser_e(T), ser_e(J)]])
        total_groups += len(ordered_groups)
        clean_stats = {key: value for key, value in stats.items() if value}
        summaries.append({
            "B_vertices": len(B),
            "groups": len(ordered_groups),
            "filters": clean_stats,
            "edge_counts": {str(key): value for key, value in edge_counts.items()},
        })
    need(total_groups == 5064, "two-factor group total")
    return two_keys, summaries, edge_hash.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", required=True)
    parser.add_argument("--expected", required=True)
    args = parser.parse_args()
    certificate_path, expected_path = Path(args.certificate), Path(args.expected)
    certificate = json.loads(certificate_path.read_text())
    expected = json.loads(expected_path.read_text())
    certificate_hash = sha256(certificate_path.read_bytes()).hexdigest()
    need(certificate_hash == expected["certificate_sha256"], "certificate digest")
    need(certificate.get("format") == "formal343-v1", "certificate format")
    words = certificate.get("words")
    need(isinstance(words, list) and len(words) == 483, "word census")
    need(all(isinstance(word, str) and len(word) == 343 and set(word) <= set("0123")
             for word in words), "word syntax")

    M = spindle()
    need(len(set(M)) == 7, "source vertex count")
    source_edges = [(i, j) for i, j in combinations(range(7), 2)
                    if enorm(es(M[i], M[j])) == Q1]
    need(len(source_edges) == 11, "source edge count")
    need(not any(all(colours[i] != colours[j] for i, j in source_edges)
                 for colours in product(range(3), repeat=7)), "source 3-colouring")
    need(any(all(colours[i] != colours[j] for i, j in source_edges)
             for colours in product(range(4), repeat=7)), "source 4-colouring")

    product_edges = generic_edges(source_edges)
    used_rows = {row for row in certificate["three"] if row != -1}
    used_rows.update(row for case in certificate["two"] for row in case)
    need(all(all(word[left] != word[right] for left, right in product_edges)
             for index, word in enumerate(words) if index in used_rows),
         "certificate word fails a Cartesian edge")

    three_data, roots, fields = three_factor_inventory(M)
    need(digest(three_data) == expected["three_factor"]["complete_root_inventory_sha256"],
         "three-factor inventory digest")
    need(len(certificate["three"]) == len(roots) == 6528, "three-factor row coverage")
    field_local = []
    for field in fields:
        valuation, unit = q2_data(field)
        field_local.append(valuation % 2 == 0 and unit == 1)
    local_count = explicit_count = 0
    vertex_counts: Counter[int] = Counter()
    for (field, u, v, _), row in zip(roots, certificate["three"]):
        if field_local[field]:
            need(row == -1, "local-field tag")
            local_count += 1
            continue
        need(isinstance(row, int) and 0 <= row < len(words), "three-factor word index")
        colour_for_point: dict[X, str] = {}
        rotated_u = [xm_e(u, point) for point in M]
        rotated_v = [xm_e(v, point) for point in M]
        pair_sums = [xa(left, right) for left, right in product(rotated_u, rotated_v)]
        for formal, (a, pair_sum) in enumerate(product(M, pair_sums)):
            point = xa((a, E0), pair_sum)
            colour = words[row][formal]
            need(point not in colour_for_point or colour_for_point[point] == colour,
                 "three-factor word does not descend")
            colour_for_point[point] = colour
        need(len(colour_for_point) < 343, "missing three-factor collision")
        vertex_counts[len(colour_for_point)] += 1
        explicit_count += 1
    need((local_count, explicit_count) == (3024, 3504), "three-factor local split")
    need(dict(vertex_counts) == {340: 48, 341: 816, 342: 2640},
         "three-factor physical vertex census")

    D = sorted({es(a, b) for a in M for b in M if a != b})
    two_keys, two_summaries, two_edge_hash = two_factor_inventory(M, D, certificate)
    need(digest(two_keys) == expected["two_factor"]["complete_quadratic_inventory_sha256"],
         "two-factor inventory digest")
    need(two_edge_hash == expected["two_factor"]["edge_stream_sha256"],
         "two-factor edge stream digest")
    for actual, wanted in zip(two_summaries, expected["two_factor"]["cases"]):
        for field in ("B_vertices", "groups", "filters", "edge_counts"):
            need(actual[field] == wanted[field], f"two-factor {field}")

    result = {
        "certificate_bytes": certificate_path.stat().st_size,
        "certificate_sha256": certificate_hash,
        "certificate_words": len(words),
        "generic_cartesian_edges_per_word": len(product_edges),
        "source_edges": len(source_edges),
        "source_vertices": len(M),
        "three_factor": {
            "explicit_descents": explicit_count,
            "infield_pairs": three_data["summary"]["infield_pairs"],
            "inventory_sha256": digest(three_data),
            "local_field_pairs": local_count,
            "outside_pairs": len(roots),
            "vertex_counts": dict(vertex_counts),
        },
        "two_factor": {
            "edge_stream_sha256": two_edge_hash,
            "groups": len(two_keys),
            "inventory_sha256": digest(two_keys),
            "representatives": len(two_summaries),
        },
        "used_words_checked_on_cartesian_edges": len(used_rows),
        "status": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
