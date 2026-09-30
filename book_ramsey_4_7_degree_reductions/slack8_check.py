#!/usr/bin/env python3
"""Complete weighted-defect census for the 97-edge histogram (5,16,1).

Standard library only. Integer Bareiss determinants; no solver, timeout,
heuristic pruning, or imports of other research programs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from math import factorial, isqrt
from pathlib import Path

N = 22
DEGREES = [8] * 5 + [9] * 16 + [10]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def determinant(matrix):
    a = [row[:] for row in matrix]
    n, previous, sign = len(a), 1, 1
    require(n > 0 and all(len(row) == n for row in a), "nonsquare matrix")
    for k in range(n - 1):
        row = next((i for i in range(k, n) if a[i][k]), None)
        if row is None:
            return 0
        if row != k:
            a[row], a[k] = a[k], a[row]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                require(numerator % previous == 0, "inexact Bareiss division")
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def core_forms(profile, odd_count=16):
    """Every weighted center graph, quotienting only equal (degree,surplus) types."""
    pairs = list(combinations(range(len(profile)), 2))
    slots = {pair: i for i, pair in enumerate(pairs)}
    relabelings = [p for p in permutations(range(len(profile)))
                  if all(profile[p[i]] == profile[i] for i in range(len(profile)))]
    remaining = [q + d % 2 for d, q in profile]
    weights = [0] * len(pairs)
    odd_available = odd_count - sum(d == 9 for d, q in profile)

    def visit(slot):
        if slot == len(pairs):
            if sum(remaining) > odd_available or (odd_available - sum(remaining)) % 2:
                return
            renamed = {tuple(weights[slots[tuple(sorted((p[i], p[j])))]] for i, j in pairs)
                       for p in relabelings}
            candidate = tuple(weights)
            if candidate == min(renamed):
                yield candidate, tuple(remaining), len(renamed)
            return
        i, j = pairs[slot]
        for w in range(min(remaining[i], remaining[j]) + 1):
            weights[slot] = w
            remaining[i] -= w
            remaining[j] -= w
            yield from visit(slot + 1)
            remaining[i] += w
            remaining[j] += w

    yield from visit(0)


def full_defect(profile, weights, leaf_counts):
    available = {d: [i for i, value in enumerate(DEGREES) if value == d] for d in (8, 9, 10)}
    centers = [available[d].pop(0) for d, q in profile]
    F = [[0] * N for _ in range(N)]
    for (i, j), w in zip(combinations(range(len(centers)), 2), weights):
        a, b = centers[i], centers[j]
        F[a][b] = F[b][a] = w
    for i, count in zip(centers, leaf_counts):
        for _ in range(count):
            j = available[9].pop(0)
            F[i][j] = F[j][i] = 1
    require(len(available[9]) % 2 == 0, "odd matching remainder")
    for slot in range(0, len(available[9]), 2):
        i, j = available[9][slot:slot + 2]
        F[i][j] = F[j][i] = 1
    surplus = [sum(F[i]) - DEGREES[i] % 2 for i in range(N)]
    require(all(x >= 0 and x % 2 == 0 for x in surplus) and sum(surplus) == 8,
            "wrong nonnegative even surplus")
    require([(DEGREES[i], surplus[i]) for i in centers] == list(profile), "wrong center types")
    require({i for i, x in enumerate(surplus) if x} == set(centers), "wrong surplus support")
    require(sum(F[i][j] for i, j in combinations(range(N), 2)) == 12, "wrong total defect")
    return F


def forced_matrix(F):
    y = [10 - d for d in DEGREES]
    return [[25 * (i == j) + 24 - 4 * (y[i] + y[j])
             - 4 * (DEGREES[i] == 9) * (i == j) - 4 * F[i][j]
             for j in range(N)] for i in range(N)]


def survivor_certificate(H):
    def vector(plus, minus=()):
        return [int(i in plus) - int(i in minus) for i in range(N)]
    pairs8 = [(0, 3), (1, 2)]
    pairs9 = [(i, i + 1) for i in range(5, 21, 2)]
    spaces = [(33, [vector((i,), (j,)) for i, j in pairs8]),
              (25, [vector((i,), (j,)) for i, j in pairs9]),
              (17, [vector(pair, pairs9[-1]) for pair in pairs9[:-1]]
               + [vector(pairs8[0], pairs8[1])])]
    for value, basis in spaces:
        for v in basis:
            require([sum(a * b for a, b in zip(row, v)) for row in H] == [value * x for x in v],
                    "wrong invariant eigenvector")
    groups = [list(range(4)), [4], list(range(5, 21)), [21]]
    Q = [[sum(H[group[0]][j] for j in other) for other in groups] for group in groups]
    for group, row in zip(groups, Q):
        require(all([sum(H[i][j] for j in other) for other in groups] == row for i in group),
                "quotient space not invariant")
    basis = [v for value, space in spaces for v in space] + [vector(group) for group in groups]
    basis_det = determinant(basis)
    require(len(basis) == N and basis_det != 0, "incomplete invariant direct sum")
    shifted = [[Q[i][j] - 33 * (i == j) for j in range(4)] for i in range(4)]
    require(determinant(shifted) == -524288 and determinant(Q) == 1577 ** 2,
            "wrong quotient determinants")
    gram = [[sum(x * y for x, y in zip(v, w)) for w in spaces[0][1]] for v in spaces[0][1]]
    require(gram == [[2, 0], [0, 2]], "wrong 33-plane Gram matrix")
    residues = [(a, b, c) for a, b, c in product(range(9), repeat=3)
                if (a * a + b * b - 33 * c * c) % 9 == 0]
    require(len(residues) == 27 and all(a % 3 == b % 3 == c % 3 == 0 for a, b, c in residues),
            "primitive norm obstruction residue control")
    companion = [[0, 33], [1, 0]]
    require([[sum(companion[i][k] * companion[k][j] for k in range(2)) for j in range(2)]
             for i in range(2)] == [[33, 0], [0, 33]], "nonsymmetric-root positive control")
    value = determinant(H)
    require(value == 33 ** 2 * 25 ** 8 * 17 ** 8 * determinant(Q), "wrong spectral determinant")
    return {"degree8_pairs": [list(p) for p in pairs8],
            "degree9_pairs": [list(p) for p in pairs9],
            "eigenspace_dimensions": {"33": 2, "25": 8, "17": 8, "quotient": 4},
            "quotient": Q, "det_quotient": determinant(Q),
            "det_quotient_minus33I": determinant(shifted), "basis_determinant": basis_det,
            "gram_33_plane": gram, "norm_mod9_solutions": len(residues),
            "primitive_norm_mod9_solutions": 0, "det_H": value,
            "necessary_rational_trace": 0, "adjacency_form_traces": [-6, -4, -2]}


def controls():
    require(determinant([[0, 1], [2, 3]]) == -2 and determinant([[1, 2], [2, 4]]) == 0,
            "determinant sign/singular control")
    forms = list(core_forms(((8, 2), (8, 2))))
    require([w for w, leaves, orbit in forms] == [(0,), (1,), (2,)], "two-center weight domain")
    rows = Path(__file__).with_name("baseline21.rows").read_text().split()
    require(len(rows) == 21 and all(len(row) == 21 and set(row) <= {"0", "1"} for row in rows),
            "malformed known construction")
    red = [{j for j, value in enumerate(row) if value == "1"} for row in rows]
    blue = [set(range(21)) - red[i] - {i} for i in range(21)]
    require(all(i not in red[i] and all((j in red[i]) == (i in red[j]) for j in range(21))
                for i in range(21)), "bad known graph")
    hist = Counter(map(len, red))
    maxima = [max(len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i]),
              max(len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j in blue[i])]
    require(hist == {8: 4, 9: 16, 10: 1} and maxima == [3, 6], "known baseline mismatch")
    return {"two_center_weights": [0, 1, 2], "determinant_controls": [-2, 0],
            "baseline21_red_edges": sum(map(len, red)) // 2,
            "baseline21_degree_histogram": [hist[d] for d in (8, 9, 10)],
            "baseline21_max_pages": maxima}


def result(matrix_path=None):
    profiles, records, matrices, square_keys = [], [], [], []
    types = [(d, q) for d in (8, 9, 10) for q in (2, 4, 6, 8)]
    certificate = None
    for k in range(1, 5):
        for profile in combinations_with_replacement(types, k):
            if sum(q for d, q in profile) != 8 or sum(d == 10 for d, q in profile) > 1:
                continue
            index = len(profiles)
            counts, orbit_sum = Counter(), 0
            for weights, leaves, orbit in core_forms(profile):
                F = full_defect(profile, weights, leaves)
                H = forced_matrix(F)
                value = determinant(H)
                require(value > 0, "unexpected nonpositive determinant")
                root = isqrt(value)
                require(root * root <= value < (root + 1) ** 2, "wrong square-root interval")
                square = root * root == value
                if square:
                    require(profile == ((8, 2),) * 4 and weights == (0, 0, 2, 2, 0, 0),
                            "unexpected square survivor")
                    square_keys.append([index, list(weights)])
                    certificate = survivor_certificate(H)
                counts["square" if square else "positive_nonsquare"] += 1
                orbit_sum += orbit
                records.append([index, list(weights), orbit, value, root, sha256(encode([F, H])).hexdigest()])
                if matrix_path:
                    matrices.append({"profile": [list(x) for x in profile], "weights": list(weights),
                                     "F": F, "H": H})
            multiplicity = factorial(k)
            for count in Counter(profile).values():
                multiplicity //= factorial(count)
            profiles.append({"types": [list(x) for x in profile], "forms": sum(counts.values()),
                             "fixed_type_labeled_cores": orbit_sum,
                             "all_ordered_type_cores": orbit_sum * multiplicity})
    require(len(profiles) == 38 and len(records) == 559 and len(square_keys) == 1,
            "unexpected complete census size")
    require(certificate is not None, "missing unique survivor certificate")
    if matrix_path:
        matrix_path.write_text(json.dumps(matrices, separators=(",", ":")) + "\n")
    return {"agent": "six-books-1", "role": "researcher", "degree_histogram": [5, 16, 1],
            "red_edges": 97, "incident_parity_surplus": 8, "total_defect": 12,
            "record_fields": ["profile_index", "center_edge_weights", "fixed_type_orbit_size",
                              "det_H", "floor_sqrt_det", "F_H_sha256"],
            "profiles": profiles, "records": records, "square_keys": square_keys,
            "survivor_certificate": certificate, "controls": controls()}


def write_compact(path, output):
    # Keep the finite certificate readable, with one canonical case per line.
    lines = ["{"]
    for key, value in output.items():
        prefix = "  " + json.dumps(key) + ": "
        if key in ("profiles", "records"):
            lines.append(prefix + "[")
            lines.extend("    " + json.dumps(x, separators=(",", ":")) + ("," if i + 1 < len(value) else "")
                         for i, x in enumerate(value))
            lines.append("  ],")
        else:
            lines.append(prefix + json.dumps(value, separators=(",", ":")) + ",")
    lines[-1] = lines[-1].rstrip(",")
    path.write_text("\n".join(lines) + "\n}\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", type=Path)
    parser.add_argument("--matrices", type=Path, help="optional private, fully entrywise comparison data")
    args = parser.parse_args()
    output = result(args.matrices)
    if args.write_expected:
        write_compact(args.write_expected, output)
    else:
        expected = json.loads(Path(__file__).with_name("slack8_expected.json").read_text())
        require(encode(output) == encode(expected), "expected output differs")
    print(json.dumps({"complete": True, "profiles": len(output["profiles"]),
                      "forms": len(output["records"]), "positive_nonsquare": 558,
                      "square_determinants": 1, "rational_symmetric_root_survivors": 0,
                      "all_ordered_type_cores": sum(p["all_ordered_type_cores"] for p in output["profiles"]),
                      "matrix_records_written": args.matrices is not None}))


if __name__ == "__main__":
    main()
