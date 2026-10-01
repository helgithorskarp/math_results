#!/usr/bin/env python3
"""Exact remaining surplus-eight census and three square-case certificates.

Standalone standard-library author implementation. No solver, floating
arithmetic, heuristic filtering, or predecessor-program imports.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from math import factorial, gcd, isqrt
from pathlib import Path
from random import Random

N = 22
HISTOGRAMS = ((7, 10, 5), (9, 4, 9))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def determinant(matrix):
    a = [row[:] for row in matrix]
    n, previous, sign = len(a), 1, 1
    require(n and all(len(row) == n for row in a), "nonsquare determinant")
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
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def integer_rank(matrix):
    """Exact rational rank using integer row operations and gcd reduction."""
    a = [row[:] for row in matrix]
    rank = 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        p = a[rank][column]
        for i in range(rank + 1, len(a)):
            v = a[i][column]
            if not v:
                continue
            a[i] = [p * x - v * y for x, y in zip(a[i], a[rank])]
            divisor = 0
            for value in a[i]:
                divisor = gcd(divisor, value)
            if divisor:
                a[i] = [x // divisor for x in a[i]]
        rank += 1
    return rank


def core_forms(profile, odd_count):
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


def full_defect(degrees, profile, weights, leaf_counts):
    available = {d: [i for i, value in enumerate(degrees) if value == d] for d in (8, 9, 10)}
    centers = [available[d].pop(0) for d, q in profile]
    f = [[0] * N for _ in range(N)]
    for (i, j), w in zip(combinations(range(len(centers)), 2), weights):
        a, b = centers[i], centers[j]
        f[a][b] = f[b][a] = w
    for i, count in zip(centers, leaf_counts):
        for _ in range(count):
            j = available[9].pop(0)
            f[i][j] = f[j][i] = 1
    require(len(available[9]) % 2 == 0, "odd matching remainder")
    for slot in range(0, len(available[9]), 2):
        i, j = available[9][slot:slot + 2]
        f[i][j] = f[j][i] = 1
    surplus = [sum(f[i]) - degrees[i] % 2 for i in range(N)]
    require(all(x >= 0 and x % 2 == 0 for x in surplus) and sum(surplus) == 8, "wrong surplus")
    require([(degrees[i], surplus[i]) for i in centers] == list(profile), "wrong center types")
    require({i for i, x in enumerate(surplus) if x} == set(centers), "wrong center support")
    require(sum(map(sum, f)) == 8 + degrees.count(9), "wrong total defect")
    return f


def forced_matrix(degrees, f):
    y = [10 - d for d in degrees]
    return [[25 * (i == j) + 24 - 4 * (y[i] + y[j])
             - 4 * (degrees[i] == 9) * (i == j) - 4 * f[i][j]
             for j in range(N)] for i in range(N)]


def square_certificate(profile, weights, f, h):
    if profile == ((8, 2), (8, 2), (10, 2), (10, 2)) and weights == (2, 0, 0, 0, 0, 2):
        pairs = [(0, 1), (13, 14)]
    elif profile == ((9, 2),) * 4 and weights == (0, 0, 3, 3, 0, 0):
        pairs = [(9, 12), (10, 11)]
    elif profile == ((9, 2),) * 4 and weights == (1,) * 6:
        groups = [list(range(9)), list(range(9, 13)), list(range(13, 22))]
        q = [[sum(h[group[0]][j] for j in other) for other in groups] for group in groups]
        for a, group in enumerate(groups):
            for b, other in enumerate(groups):
                for i in group:
                    for j in other:
                        expected = h[group[0]][other[0]] if a != b else 25 * (i == j) + h[group[0]][group[1]]
                        require(h[i][j] == expected, "contrast/block formula failed")
        shifted = [[q[i][j] - 25 * (i == j) for j in range(3)] for i in range(3)]
        shifted_h = [[h[i][j] - 25 * (i == j) for j in range(N)] for i in range(N)]
        require(determinant(shifted) == 82944 and integer_rank(shifted_h) == 3, "wrong image bridge")
        l = [[5, 4, 6], [9, 1, 9], [6, 4, 13]]
        require([[sum(l[i][k] * l[k][j] for k in range(3)) for j in range(3)] for i in range(3)] == q,
                "explicit rational-root quotient failed")
        classes = [a for a, group in enumerate(groups) for i in group]
        scaled = [[180 * (i == j) + 36 * (l[classes[i]][classes[j]] - 5 * (classes[i] == classes[j]))
                   // len(groups[classes[j]]) for j in range(N)] for i in range(N)]
        require(all(scaled[i][j] == scaled[j][i] for i in range(N) for j in range(N)), "root not symmetric")
        require(all(sum(scaled[i][k] * scaled[k][j] for k in range(N)) == 1296 * h[i][j]
                    for i in range(N) for j in range(N)), "explicit full rational root failed")
        cases = [[k, (9 - k) // 2, 4 * ((9 - k) // 2), (4 * ((9 - k) // 2)) % 9]
                 for k in range(4) if (9 - k) % 2 == 0]
        require(cases == [[1, 4, 16, 7], [3, 3, 12, 3]], "equitable incidence cases differ")
        return {"mechanism": "equitable_degree_partition", "quotient": q,
                "quotient_gram": [9, 4, 9], "det_quotient_minus25I": 82944,
                "rank_H_minus25I": 3, "incidence_cases": cases,
                "rational_root_quotient": l, "rational_root_scale": 36,
                "rational_root_scaled_matrix": scaled, "rational_root_trace": 114}
    else:
        raise RuntimeError("unexpected square case")
    plane = []
    for i, j in pairs:
        v = [0] * N
        v[i], v[j] = 1, -1
        require([sum(a * b for a, b in zip(row, v)) for row in h] == [33 * x for x in v], "wrong33 vector")
        plane.append(v)
    rank = integer_rank([[h[i][j] - 33 * (i == j) for j in range(N)] for i in range(N)])
    gram = [[sum(x * y for x, y in zip(v, w)) for w in plane] for v in plane]
    residues = [(a, b, c) for a, b, c in product(range(9), repeat=3)
                if (a * a + b * b - 33 * c * c) % 9 == 0]
    require(rank == 20 and gram == [[2, 0], [0, 2]], "wrong complete33 plane")
    require(len(residues) == 27 and all(a % 3 == b % 3 == c % 3 == 0 for a, b, c in residues), "primitive norm residue")
    return {"mechanism": "rational33_plane", "basis_pairs": [list(p) for p in pairs],
            "rank_H_minus33I": rank, "gram": gram, "norm_mod9_solutions": len(residues),
            "primitive_norm_mod9_solutions": 0}


def histogram_result(histogram, matrices):
    degrees = [d for d, count in zip((8, 9, 10), histogram) for _ in range(count)]
    profiles, records, squares = [], [], []
    types = [(d, q) for d in (8, 9, 10) for q in (2, 4, 6, 8)]
    for k in range(1, 5):
        for profile in combinations_with_replacement(types, k):
            if sum(q for d, q in profile) != 8 or any(sum(d == t for d, q in profile) > degrees.count(t) for t in (8, 9, 10)):
                continue
            index = len(profiles)
            count, orbit_sum = 0, 0
            for weights, leaves, orbit in core_forms(profile, histogram[1]):
                f = full_defect(degrees, profile, weights, leaves)
                h = forced_matrix(degrees, f)
                value = determinant(h)
                require(value > 0, "unexpected nonpositive determinant")
                root = isqrt(value)
                require(root * root <= value < (root + 1) ** 2, "wrong square-root interval")
                if root * root == value:
                    require(histogram == (9, 4, 9), "unexpected first-histogram square")
                    squares.append({"profile_index": index, "weights": list(weights),
                                    "certificate": square_certificate(profile, weights, f, h)})
                records.append([index, list(weights), orbit, value, root, sha256(encode([f, h])).hexdigest()])
                matrices.append({"histogram": list(histogram), "profile": [list(x) for x in profile],
                                 "weights": list(weights), "F": f, "H": h})
                count += 1
                orbit_sum += orbit
            multiplicity = factorial(k)
            for repeated in Counter(profile).values():
                multiplicity //= factorial(repeated)
            profiles.append({"types": [list(x) for x in profile], "forms": count,
                             "fixed_type_labeled_cores": orbit_sum,
                             "all_ordered_type_cores": orbit_sum * multiplicity})
    require(len(profiles) == 51 and len(records) == (768 if histogram == (7, 10, 5) else 343)
            and len(squares) == (0 if histogram == (7, 10, 5) else 3), "census mismatch")
    return {"degree_histogram": list(histogram), "red_edges": sum(degrees) // 2,
            "incident_parity_surplus": 8, "total_defect": (8 + histogram[1]) // 2,
            "profiles": profiles, "records": records, "square_cases": squares}


def signed_graphs(degrees):
    remaining = list(degrees)
    red = [set() for _ in degrees]
    while any(remaining):
        order = sorted((i for i, value in enumerate(remaining) if value), key=lambda i: (-remaining[i], i))
        i = order[0]
        demand = remaining[i]
        require(demand < len(order), "nongraphical control histogram")
        remaining[i] = 0
        for j in order[1:demand + 1]:
            red[i].add(j)
            red[j].add(i)
            remaining[j] -= 1
    pairs = list(combinations(range(N), 2))
    for seed in range(24):
        r = [row.copy() for row in red]
        rng = Random(9847 + seed)
        for _ in range(80):
            edges = [(i, j) for i, j in pairs if j in r[i]]
            (a, b), (c, d) = rng.sample(edges, 2)
            if len({a, b, c, d}) < 4 or c in r[a] or d in r[b]:
                continue
            for i, j in ((a, b), (c, d)):
                r[i].remove(j)
                r[j].remove(i)
            for i, j in ((a, c), (b, d)):
                r[i].add(j)
                r[j].add(i)
        require(list(map(len, r)) == degrees, "signed control degrees changed")
        yield sum(1 << bit for bit, (i, j) in enumerate(pairs) if j in r[i]), r


def controls():
    require(determinant([[0, 1], [2, 3]]) == -2 and determinant([[1, 2], [2, 4]]) == 0, "determinant controls")
    require(integer_rank([[0, 1], [2, 3]]) == 2 and integer_rank([[1, 2], [2, 4]]) == 1, "rank controls")
    require([w for w, leaf, orbit in core_forms(((8, 2), (8, 2)), 10)] == [(0,), (1,), (2,)], "small core domain")
    fixture = Path(__file__).with_name("baseline21.rows").read_text().split()
    require(len(fixture) == 21 and all(len(row) == 21 and set(row) <= {"0", "1"} for row in fixture), "bad baseline")
    red = [{j for j, value in enumerate(row) if value == "1"} for row in fixture]
    blue = [set(range(21)) - red[i] - {i} for i in range(21)]
    require(all(i not in red[i] and all((j in red[i]) == (i in red[j]) for j in range(21)) for i in range(21)), "baseline symmetry")
    hist = Counter(map(len, red))
    maxima = [max(len(rows[i] & rows[j]) for i, j in combinations(range(21), 2) if j in rows[i]) for rows in (red, blue)]
    require(hist == {8: 4, 9: 16, 10: 1} and maxima == [3, 6], "known baseline mismatch")
    signed = []
    for histogram in HISTOGRAMS:
        degrees = [d for d, count in zip((8, 9, 10), histogram) for _ in range(count)]
        masks = []
        for mask, r in signed_graphs(degrees):
            b = [set(range(N)) - r[i] - {i} for i in range(N)]
            f = [[0] * N for _ in range(N)]
            for i, j in combinations(range(N), 2):
                f[i][j] = f[j][i] = 3 - len(r[i] & r[j]) if j in r[i] else 6 - len(b[i] & b[j])
            h = forced_matrix(degrees, f)
            k = [[2 * (j in r[i]) + (2 * degrees[i] - 17) * (i == j) for j in range(N)] for i in range(N)]
            for i in range(N):
                require(sum(f[i]) == sum(degrees) - 294 + 38 * degrees[i] - degrees[i] ** 2
                        - 2 * sum(degrees[j] for j in r[i]), "literal incident identity")
                require((sum(f[i]) - degrees[i] % 2) % 2 == 0, "signed parity")
                for j in range(N):
                    require(sum(k[i][t] * k[t][j] for t in range(N)) == h[i][j], "literal square identity")
            require(sum(map(sum, f)) == 8 + histogram[1], "signed total surplus")
            masks.append(mask)
        require(len(set(masks)) == 24, "duplicate signed controls")
        signed.append({"histogram": list(histogram), "red_masks": masks, "graphs": 24,
                       "incident_identity_checks": 528, "square_identity_entries": 11616})
    return {"determinant_controls": [-2, 0], "rank_controls": [2, 1], "two_center_weights": [0, 1, 2],
            "baseline21_red_edges": sum(map(len, red)) // 2,
            "baseline21_degree_histogram": [hist[d] for d in (8, 9, 10)],
            "baseline21_max_pages": maxima, "signed": signed}


def write_compact(path, output):
    blocks = []
    for result in output["histograms"]:
        lines = ["  {"]
        for key, value in result.items():
            if key in ("profiles", "records"):
                lines.append("    " + json.dumps(key) + ": [")
                lines.extend("      " + json.dumps(v, separators=(",", ":")) + ("," if i + 1 < len(value) else "")
                             for i, v in enumerate(value))
                lines.append("    ],")
            else:
                lines.append("    " + json.dumps(key) + ": " + json.dumps(value, separators=(",", ":")) + ",")
        lines[-1] = lines[-1].rstrip(",")
        blocks.append("\n".join(lines) + "\n  }")
    prefix = {key: value for key, value in output.items() if key != "histograms"}
    text = json.dumps(prefix, separators=(",", ":"))[:-1] + ',"histograms":[\n'
    path.write_text(text + ",\n".join(blocks) + "\n]}\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", type=Path)
    parser.add_argument("--matrices", type=Path, help="private full-entry comparison corpus")
    args = parser.parse_args()
    matrices = []
    output = {"agent": "six-books-1", "role": "researcher", "record_fields":
              ["profile_index", "center_edge_weights", "fixed_type_orbit_size", "det_H", "floor_sqrt_det", "F_H_sha256"],
              "histograms": [histogram_result(hist, matrices) for hist in HISTOGRAMS], "controls": controls()}
    if args.write_expected:
        write_compact(args.write_expected, output)
    else:
        expected = json.loads(Path(__file__).with_name("slack8_remaining_expected.json").read_text())
        require(encode(output) == encode(expected), "complete certificate differs")
    if args.matrices:
        args.matrices.write_text(json.dumps(matrices, separators=(",", ":")) + "\n")
    print(json.dumps({"complete": True, "profiles": [len(h["profiles"]) for h in output["histograms"]],
                      "nonempty_profiles": [sum(p["forms"] > 0 for p in h["profiles"]) for h in output["histograms"]],
                      "forms": [len(h["records"]) for h in output["histograms"]],
                      "positive_nonsquare": 1108, "square_cases": 3,
                      "adjacency_survivors": 0, "rational_symmetric_root_positive_controls": 1,
                      "matrix_records_written": args.matrices is not None}))


if __name__ == "__main__":
    main()
