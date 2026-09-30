#!/usr/bin/env python3
"""Separate complete domain and rational determinant audit of slack eight.

Enumerates ordered surplus compositions and multisets of unit center edges,
then quotients all center permutations. No imports of author/predecessor code.
The expected file is only a comparison target, never an enumeration input.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path

DEGREE = [8] * 5 + [9] * 16 + [10]


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def elimination(matrix, want_determinant=False):
    a = [[Fraction(x) for x in row] for row in matrix]
    rank, answer = 0, Fraction(1)
    for col in range(len(a[0])):
        pivot_row = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot_row is None:
            continue
        if pivot_row != rank:
            a[pivot_row], a[rank] = a[rank], a[pivot_row]
            answer = -answer
        pivot = a[rank][col]
        answer *= pivot
        for i in range(rank + 1, len(a)):
            multiplier = a[i][col] / pivot
            for j in range(col + 1, len(a[0])):
                a[i][j] -= multiplier * a[rank][j]
            a[i][col] = 0
        rank += 1
        if rank == len(a):
            break
    if not want_determinant:
        return rank
    need(len(a) == len(a[0]), "nonsquare determinant")
    if rank != len(a):
        return 0
    need(answer.denominator == 1, "nonintegral determinant")
    return answer.numerator


def sqrt_floor(value):
    need(value > 0, "nonpositive determinant")
    low, high = 0, 1 << ((value.bit_length() + 1) // 2)
    while high - low > 1:
        mid = (low + high) // 2
        if mid * mid <= value:
            low = mid
        else:
            high = mid
    need(low * low <= value < high * high, "wrong square-root interval")
    return low


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for head in range(1, total - length + 2):
            for tail in compositions(total - head, length - 1):
                yield (head,) + tail


def domain():
    """Unit-edge multisets; includes every ordered colored surplus support."""
    canonical, raw_counts = {}, Counter()
    for k in range(1, 5):
        pairs = list(combinations(range(k), 2))
        relabelings = list(permutations(range(k)))
        for units in compositions(4, k):
            for colors in product((8, 9, 10), repeat=k):
                if any(colors.count(d) > DEGREE.count(d) for d in (8, 9, 10)):
                    continue
                typed = tuple((d, 2 * u) for d, u in zip(colors, units))
                demand = [d % 2 + 2 * u for d, u in zip(colors, units)]
                available_odd = 16 - colors.count(9)
                for m in range(sum(demand) // 2 + 1):
                    for multiset in combinations_with_replacement(range(len(pairs)), m):
                        weights = Counter(multiset)
                        adjacent = [[0] * k for _ in range(k)]
                        incident = [0] * k
                        for slot, w in weights.items():
                            i, j = pairs[slot]
                            adjacent[i][j] = adjacent[j][i] = w
                            incident[i] += w
                            incident[j] += w
                        leaves = [a - b for a, b in zip(demand, incident)]
                        if min(leaves) < 0 or sum(leaves) > available_odd:
                            continue
                        if (available_odd - sum(leaves)) % 2:
                            continue
                        keys = [(tuple(typed[p[i]] for i in range(k)),
                                 tuple(adjacent[p[i]][p[j]] for i, j in pairs)) for p in relabelings]
                        key = min(keys)
                        raw_counts[key[0]] += 1
                        if key not in canonical:
                            canonical[key] = (typed, adjacent)
    return canonical, raw_counts


def labeled_defect(typed, adjacent):
    # Choose labels in reverse order; no canonical labels from the generator.
    available = {d: [i for i, value in enumerate(DEGREE) if value == d] for d in (8, 9, 10)}
    centers = [available[d].pop() for d, q in typed]
    links = {}
    for i, j in combinations(range(len(typed)), 2):
        if adjacent[i][j]:
            links[tuple(sorted((centers[i], centers[j])))] = adjacent[i][j]
    for i, (d, q) in enumerate(typed):
        remaining = d % 2 + q - sum(adjacent[i])
        for _ in range(remaining):
            leaf = available[9].pop()
            links[tuple(sorted((centers[i], leaf)))] = 1
    while available[9]:
        i, j = available[9].pop(), available[9].pop()
        links[tuple(sorted((i, j)))] = 1
    return links


def normalize(links):
    rows = [{} for _ in DEGREE]
    for (i, j), w in links.items():
        need(0 <= i < j < 22 and isinstance(w, int) and w > 0, "malformed defect")
        rows[i][j] = rows[j][i] = w
    surplus = [sum(row.values()) - d % 2 for d, row in zip(DEGREE, rows)]
    need(sum(surplus) == 8 and all(x >= 0 and x % 2 == 0 for x in surplus), "wrong surplus")
    centers = [i for i, value in enumerate(surplus) if value]
    pairs = list(combinations(range(len(centers)), 2))
    candidates = []
    for ordered in permutations(centers):
        types = tuple((DEGREE[i], surplus[i]) for i in ordered)
        weights = tuple(rows[ordered[i]].get(ordered[j], 0) for i, j in pairs)
        candidates.append(((types, weights), ordered))
    key, centers = min(candidates)
    leaves, remaining = [], {i for i, d in enumerate(DEGREE) if d == 9 and i not in centers}
    for i in centers:
        local = sorted(j for j in rows[i] if j not in centers)
        need(all(j in remaining and rows[i][j] == 1 for j in local), "nonunit/shared odd leaf")
        leaves.extend(local)
        remaining.difference_update(local)
    matching = []
    while remaining:
        i = min(remaining)
        need(len(rows[i]) == 1, "wrong normal odd vertex")
        j, w = next(iter(rows[i].items()))
        need(j in remaining - {i} and w == 1, "wrong residual matching")
        matching.extend((i, j))
        remaining.difference_update((i, j))
    order = []
    for d in (8, 9, 10):
        order.extend(i for i in centers if DEGREE[i] == d)
        order.extend(leaves + matching if d == 9 else
                     [i for i, value in enumerate(DEGREE) if value == d and i not in centers])
    need(len(order) == 22 and set(order) == set(range(22)) and [DEGREE[i] for i in order] == DEGREE,
         "wrong degree-preserving normalization")
    F = [[rows[i].get(j, 0) for j in order] for i in order]
    literal_H = [[(2 * DEGREE[i] - 17) ** 2 + 4 * DEGREE[i] if i == j
                  else 4 * (DEGREE[i] + DEGREE[j] - 14) - 4 * rows[i].get(j, 0)
                  for j in range(22)] for i in range(22)]
    H = [[literal_H[i][j] for j in order] for i in order]
    need(sum(links.values()) == 12, "wrong total defect")
    return key, F, H


def orbit_size(key):
    types, weights = key
    pairs = list(combinations(range(len(types)), 2))
    adjacent = [[0] * len(types) for _ in types]
    for (i, j), w in zip(pairs, weights):
        adjacent[i][j] = adjacent[j][i] = w
    values = {tuple(adjacent[p[i]][p[j]] for i, j in pairs) for p in permutations(range(len(types)))
              if tuple(types[p[i]] for i in range(len(types))) == types}
    return len(values)


def certificate(H):
    dimensions = {}
    for lam in (33, 25, 17):
        shifted = [[H[i][j] - lam * (i == j) for j in range(22)] for i in range(22)]
        dimensions[str(lam)] = 22 - elimination(shifted)
    need(dimensions == {"33": 2, "25": 8, "17": 8}, "wrong eigenspace dimensions")
    p8, p9 = [(0, 3), (1, 2)], [(i, i + 1) for i in range(5, 21, 2)]
    def v(plus, minus=()):
        return [int(i in plus) - int(i in minus) for i in range(22)]
    plane = [v((i,), (j,)) for i, j in p8]
    need(all([sum(a * b for a, b in zip(row, x)) for row in H] == [33 * a for a in x]
             for x in plane), "wrong full 33-plane basis")
    gram = [[sum(a * b for a, b in zip(x, y)) for y in plane] for x in plane]
    need(gram == [[2, 0], [0, 2]], "wrong plane inner product")
    groups = [list(range(4)), [4], list(range(5, 21)), [21]]
    quotient_rows = [[[sum(H[i][j] for j in other) for other in groups] for i in group]
                     for group in groups]
    need(all(all(row == rows[0] for row in rows) for rows in quotient_rows), "noninvariant quotient")
    Q = [rows[0] for rows in quotient_rows]
    def det4(A):
        total = 0
        for p in permutations(range(4)):
            value = (-1) ** sum(p[i] > p[j] for i, j in combinations(range(4), 2))
            for i in range(4):
                value *= A[i][p[i]]
            total += value
        return total
    shifted_Q = [[Q[i][j] - 33 * (i == j) for j in range(4)] for i in range(4)]
    basis = plane + [v((i,), (j,)) for i, j in p9]
    basis += [v(pair, p9[-1]) for pair in p9[:-1]] + [v(p8[0], p8[1])]
    basis += [v(group) for group in groups]
    basis_det = elimination(basis, True)
    need(basis_det != 0 and det4(shifted_Q) == -524288 and det4(Q) == 2486929,
         "wrong complete direct sum")
    solutions = [(a, b, c) for a, b, c in product(range(9), repeat=3)
                 if (a * a + b * b - 33 * c * c) % 9 == 0]
    need(all(a % 3 == b % 3 == c % 3 == 0 for a, b, c in solutions), "primitive mod9 norm solution")
    # The infinite rational impossibility is proved by coprime clearing of
    # denominators in slack8.md; this is its finite residue consistency check.
    return {"degree8_pairs": [list(p) for p in p8], "degree9_pairs": [list(p) for p in p9],
            "eigenspace_dimensions": dict(dimensions, quotient=4), "quotient": Q,
            "det_quotient": det4(Q), "det_quotient_minus33I": det4(shifted_Q),
            "basis_determinant": basis_det, "gram_33_plane": gram,
            "norm_mod9_solutions": len(solutions), "primitive_norm_mod9_solutions": 0,
            "det_H": elimination(H, True), "necessary_rational_trace": 0,
            "adjacency_form_traces": sorted({-2 - 2 * (a + b) for a, b in product((0, 1), repeat=2)})}


def controls():
    need(elimination([[0, 1], [2, 3]], True) == -2 and elimination([[1, 2], [2, 4]], True) == 0,
         "determinant controls")
    rows = Path(__file__).with_name("baseline21.rows").read_text().split()
    need(len(rows) == 21 and all(len(row) == 21 and set(row) <= {"0", "1"} for row in rows),
         "malformed known construction")
    R = [[int(c) for c in row] for row in rows]
    B = [[1 - R[i][j] - (i == j) for j in range(21)] for i in range(21)]
    need(all(R[i][i] == 0 and R[i][j] == R[j][i] for i in range(21) for j in range(21)),
         "bad baseline symmetry")
    maxima = [max(sum(A[i][k] * A[j][k] for k in range(21))
                  for i, j in combinations(range(21), 2) if A[i][j]) for A in (R, B)]
    hist = Counter(map(sum, R))
    need(hist == {8: 4, 9: 16, 10: 1} and maxima == [3, 6], "known baseline differs")
    # Independently list unit-edge multisets with row budget two at both ends.
    allowed = [len(s) for size in range(4) for s in combinations_with_replacement((0,), size)
               if len(s) <= 2]
    need(allowed == [0, 1, 2], "small unit-multiset domain")
    return {"two_center_weights": allowed, "determinant_controls": [-2, 0],
            "baseline21_red_edges": sum(map(sum, R)) // 2,
            "baseline21_degree_histogram": [hist[d] for d in (8, 9, 10)],
            "baseline21_max_pages": maxima}


def compute():
    candidates, raw_counts = domain()
    profiles = sorted(raw_counts, key=lambda p: (len(p), p))
    indices = {p: i for i, p in enumerate(profiles)}
    metadata = [{"types": [list(x) for x in p], "forms": 0, "fixed_type_labeled_cores": 0,
                 "all_ordered_type_cores": raw_counts[p]} for p in profiles]
    records, full, squares, survivor = [], [], [], None
    for key in sorted(candidates, key=lambda x: (len(x[0]), x)):
        normalized, F, H = normalize(labeled_defect(*candidates[key]))
        need(normalized == key, "domain and adjacency normalization disagree")
        value, orbit = elimination(H, True), orbit_size(key)
        root = sqrt_floor(value)
        index = indices[key[0]]
        records.append([index, list(key[1]), orbit, value, root, sha256(serialize([F, H])).hexdigest()])
        full.append({"profile": [list(x) for x in key[0]], "weights": list(key[1]), "F": F, "H": H})
        metadata[index]["forms"] += 1
        metadata[index]["fixed_type_labeled_cores"] += orbit
        if root * root == value:
            squares.append([index, list(key[1])])
            survivor = certificate(H)
    need(len(metadata) == 38 and len(records) == 559 and len(squares) == 1, "wrong census totals")
    output = {"agent": "six-books-1", "role": "researcher", "degree_histogram": [5, 16, 1],
              "red_edges": 97, "incident_parity_surplus": 8, "total_defect": 12,
              "record_fields": ["profile_index", "center_edge_weights", "fixed_type_orbit_size",
                                "det_H", "floor_sqrt_det", "F_H_sha256"],
              "profiles": metadata, "records": records, "square_keys": squares,
              "survivor_certificate": survivor, "controls": controls()}
    return output, full


def compare(expected, actual):
    need(serialize(expected) == serialize(actual), "complete entry-level certificate differs")


def compare_matrices(author, separate):
    need(len(author) == len(separate) == 559, "wrong matrix record count")
    for a, b in zip(author, separate):
        need(set(a) == set(b) and a["profile"] == b["profile"] and a["weights"] == b["weights"],
             "wrong full matrix key")
        need(a["F"] == b["F"] and a["H"] == b["H"], "full defect/forced matrix entries differ")


def corruptions(expected, actual, full):
    mutations = [
        ("missing form", lambda x: x["records"].pop()),
        ("duplicate form", lambda x: x["records"].append(deepcopy(x["records"][0]))),
        ("wrong center weight", lambda x: x["records"][-1][1].__setitem__(0, 99)),
        ("wrong orbit size", lambda x: x["records"][0].__setitem__(2, 2)),
        ("wrong determinant", lambda x: x["records"][0].__setitem__(3, x["records"][0][3] + 1)),
        ("wrong square-root interval", lambda x: x["records"][0].__setitem__(4, x["records"][0][4] + 1)),
        ("wrong matrix digest", lambda x: x["records"][0].__setitem__(5, "0" * 64)),
        ("wrong histogram", lambda x: x.__setitem__("degree_histogram", [4, 18, 0])),
        ("missing square survivor", lambda x: x["square_keys"].clear()),
        ("wrong plane dimension", lambda x: x["survivor_certificate"]["eigenspace_dimensions"].__setitem__("33", 4)),
        ("wrong primitive norm residue", lambda x: x["survivor_certificate"].__setitem__("primitive_norm_mod9_solutions", 1)),
        ("wrong adjacency trace", lambda x: x["survivor_certificate"]["adjacency_form_traces"].append(0)),
    ]
    rejected = []
    for label, mutate in mutations:
        candidate = deepcopy(expected)
        mutate(candidate)
        try:
            compare(candidate, actual)
        except RuntimeError:
            rejected.append(label)
        else:
            raise RuntimeError("corrupt certificate was accepted: " + label)
    changed = full[:]
    changed[0] = deepcopy(full[0])
    changed[0]["F"][0][0] = 1
    try:
        compare_matrices(changed, full)
    except RuntimeError:
        rejected.append("full matrix loop")
    else:
        raise RuntimeError("corrupt full matrix was accepted")
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("slack8_expected.json"))
    parser.add_argument("--matrices", type=Path, help="author temporary full matrices, checked entry by entry")
    args = parser.parse_args()
    actual, full = compute()
    expected = json.loads(args.expected.read_text())
    compare(expected, actual)
    if args.matrices:
        compare_matrices(json.loads(args.matrices.read_text()), full)
    rejected = corruptions(expected, actual, full)
    print(json.dumps({"complete": True, "separate_domain": "ordered compositions and unit-edge multisets",
                      "profiles": len(actual["profiles"]), "forms": len(actual["records"]),
                      "all_ordered_type_cores": sum(p["all_ordered_type_cores"] for p in actual["profiles"]),
                      "positive_nonsquare": 558, "square_determinants": 1,
                      "rational_symmetric_root_survivors": 0, "rank_H_minus33I": 20,
                      "full_F_H_entry_comparison": args.matrices is not None,
                      "corruptions_rejected": rejected}))


if __name__ == "__main__":
    main()
