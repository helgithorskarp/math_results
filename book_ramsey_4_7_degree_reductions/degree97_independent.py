#!/usr/bin/env python3
"""Separate small-graph, labeled-defect, rational and modular audit.

No imports of any author/predecessor program. Expected records never
select the theorem domain. Signed graph masks are validation fixtures only.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

DEGREES = [8] * 4 + [9] * 18
EDGES = list(combinations(range(22), 2))
LOCAL = list(combinations(range(4), 2))


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def determinant(A):
    a = [[Fraction(x) for x in row] for row in A]
    answer = Fraction(1)
    for k in range(len(a)):
        row = next((i for i in range(k, len(a)) if a[i][k]), None)
        if row is None:
            return 0
        if row != k:
            a[row], a[k] = a[k], a[row]
            answer = -answer
        pivot = a[k][k]
        answer *= pivot
        for i in range(k + 1, len(a)):
            multiple = a[i][k] / pivot
            for j in range(k + 1, len(a)):
                a[i][j] -= multiple * a[k][j]
            a[i][k] = 0
    need(answer.denominator == 1, "nonintegral determinant")
    return answer.numerator


def modular_det(A, p):
    need(p in (13, 23), "unexpected prime")
    a, answer = [[x % p for x in row] for row in A], 1
    for col in range(len(a)):
        row = next((i for i in range(col, len(a)) if a[i][col]), None)
        if row is None:
            return 0
        if row != col:
            a[row], a[col] = a[col], a[row]
            answer = -answer
        pivot = a[col][col]
        answer = answer * pivot % p
        inverse = pow(pivot, p - 2, p)
        need(pivot * inverse % p == 1, "bad finite-field inverse")
        for i in range(col + 1, len(a)):
            scale = a[i][col] * inverse % p
            for j in range(col + 1, len(a)):
                a[i][j] = (a[i][j] - scale * a[col][j]) % p
            a[i][col] = 0
    return answer % p


def sqrt_floor(value):
    need(value > 0, "nonpositive determinant")
    lo, hi = 0, 1 << ((value.bit_length() + 1) // 2)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid * mid <= value:
            lo = mid
        else:
            hi = mid
    need(lo * lo < value < hi * hi, "square determinant survived")
    return lo


def complement_matchings():
    yield ()
    for edge in LOCAL:
        yield (edge,)
    for first, second in combinations(LOCAL, 2):
        if len(set(first) | set(second)) == 4:
            yield (first, second)


def bridge_checks():
    graphs = []
    for missing in complement_matchings():
        edges = set(LOCAL) - set(missing)
        mask = sum(1 << slot for slot, pair in enumerate(LOCAL) if pair in edges)
        h = [sum(i in pair for pair in edges) for i in range(4)]
        graphs.append([mask, h, len(edges)])
    graphs.sort()
    need(len(graphs) == 10, "complement matching census")
    c4 = sorted([(i,) for i in range(4)] + [(0, 1), (0, 3), (1, 2), (2, 3)],
                key=lambda s: sum(1 << i for i in s))
    kh = []
    for low, highs in product(((), (0,), (1,)), ((), (2,), (3,), (2, 3))):
        s = tuple(sorted(low + highs))
        if s:
            need(len(low) * len(highs) <= len(s) - 1, "mixed subset inequality")
            kh.append(s)
    kh.sort(key=lambda s: sum(1 << i for i in s))
    # Ordered pair choices (36) plus one triple (4), independently of
    # the author's 21 unordered pair multisets plus four triples.
    families = [(tuple(sorted(set(range(4)) - {i})),) for i in range(4)]
    families += [tuple(sorted((a, b))) for a, b in product(LOCAL, repeat=2)]
    unique = {}
    for columns in families:
        pair_hits = Counter(pair for s in columns for pair in combinations(s, 2))
        local = [[0 if i == j else 3 - (2 + pair_hits[tuple(sorted((i, j)))])
                  for j in range(4)] for i in range(4)]
        disjoint = len(columns) == 2 and not set(columns[0]) & set(columns[1])
        feasible = all(x >= 0 for row in local for x in row) and all(sum(row) <= 2 for row in local)
        need(disjoint == feasible, "written K4 pattern argument differs from literal defect")
        record = {"columns": [list(s) for s in columns], "local_F": local, "allowed": disjoint}
        if columns in unique:
            need(unique[columns] == record, "ordered pattern normalization differs")
        unique[columns] = record
    keys = sorted(unique, key=lambda x: (len(x), x))
    need(len(families) == 40 and len(keys) == 25 and sum(unique[k]["allowed"] for k in keys) == 3,
         "K4 exceptional-column coverage")
    return {"four_vertex_graphs": graphs, "C4_allowed_subsets": [list(s) for s in c4],
            "K4_minus_edge_allowed_subsets": [list(s) for s in kh],
            "K4_exceptional_patterns": [unique[k] for k in keys],
            "C4_required_and_actual_cross_edges": [18 + 4 * 3, 4 * 6],
            "K4_minus_edge_required_and_available_mixed_pairs": [4 * 2, 6 + 6 + 5 + 5 - 18]}


def literal_H(links):
    return [[(2 * DEGREES[i] - 17) ** 2 + 4 * DEGREES[i] if i == j
             else 4 * (DEGREES[i] + DEGREES[j] - 14) - 4 * links.get(tuple(sorted((i, j))), 0)
             for j in range(22)] for i in range(22)]


def normalized(links):
    rows = [{} for _ in DEGREES]
    for (i, j), w in links.items():
        need(0 <= i < j < 22 and isinstance(w, int) and w > 0, "bad positive defect edge")
        rows[i][j] = rows[j][i] = w
    need(all(sum(rows[i].values()) == 2 and all(j < 4 for j in rows[i]) for i in range(4)),
         "wrong D8 cycle/cross row")
    centers = [i for i in range(4, 22) if sum(rows[i].values()) == 3]
    need(len(centers) == 2 and all(sum(rows[i].values()) == 1 for i in range(4, 22) if i not in centers),
         "wrong D9 row types")
    a_order = min(permutations(range(4)),
                  key=lambda p: (tuple(rows[p[i]].get(p[j], 0) for i, j in LOCAL), p))
    remaining = set(range(4, 22)) - set(centers)
    leaves = []
    for i in centers:
        leaf_set = sorted(j for j in rows[i] if j not in centers)
        need(all(j in remaining and rows[i][j] == 1 for j in leaf_set), "bad or shared unit leaf")
        leaves.extend(leaf_set)
        remaining.difference_update(leaf_set)
    paired = []
    while remaining:
        i = min(remaining)
        need(len(rows[i]) == 1, "bad matching endpoint")
        j, w = next(iter(rows[i].items()))
        need(j in remaining - {i} and w == 1, "bad matching remainder")
        paired.extend((i, j))
        remaining.difference_update((i, j))
    order = list(a_order) + centers + leaves + paired
    need(len(order) == len(set(order)) == 22, "normalization is not a permutation")
    F = [[rows[i].get(j, 0) for j in order] for i in order]
    original_H = literal_H(links)
    H = [[original_H[i][j] for j in order] for i in order]
    return rows[centers[0]].get(centers[1], 0), F, H


def matrices():
    forms, placements = {}, 0
    for missing in complement_matchings():
        if len(missing) != 2:
            continue
        local_edges = set(LOCAL) - set(missing)
        for centers in combinations(range(4, 22), 2):
            # Place zero, one, two or three unit edges between the centers;
            # the remaining incident demand three is supplied by unit leaves.
            for count in range(4):
                links = {edge: 1 for edge in local_edges}
                if count:
                    links[centers] = count
                available = sorted(set(range(4, 22)) - set(centers), reverse=True)
                for center in centers:
                    for _ in range(3 - count):
                        leaf = available.pop(0)
                        links[tuple(sorted((center, leaf)))] = 1
                while available:
                    i, j = available[:2]
                    del available[:2]
                    links[tuple(sorted((i, j)))] = 1
                need(sum(links.values()) == 15, "wrong total defect")
                w, F, H = normalized(links)
                need(w == count, "weight changes under normalization")
                if w not in forms:
                    forms[w] = (F, H)
                else:
                    need(forms[w] == (F, H), "full F/H entries differ on a labeled placement")
                placements += 1
    need(placements == 1836 and set(forms) == set(range(4)), "incomplete labeled domain")
    records = []
    for w in sorted(forms):
        F, H = forms[w]
        value = determinant(H)
        root = sqrt_floor(value)
        modulus = 13 if w == 0 else 23
        residue = modular_det(H, modulus)
        need(residue == value % modulus, "rational/modular determinant disagreement")
        need(residue not in {a * a % modulus for a in range(modulus)}, "square finite-field residue")
        records.append({"center_weight": w, "leaves_per_center": 3 - w, "F": F, "H": H,
                        "det_H": value, "floor_sqrt_det": root,
                        "nonsquare_modulus": modulus, "det_residue": residue})
    return records, placements


def check_signed_fixtures(fixtures):
    need(len(fixtures) == 24, "wrong number of signed graph controls")
    results = []
    for fixture in fixtures:
        mask = fixture["red_mask"]
        need(isinstance(mask, int) and 0 <= mask < 1 << 231, "malformed control mask")
        red = [[0] * 22 for _ in range(22)]
        for slot, (i, j) in enumerate(EDGES):
            red[i][j] = red[j][i] = (mask >> slot) & 1
        need(list(map(sum, red)) == DEGREES, "control degree histogram differs")
        F = [[0] * 22 for _ in range(22)]
        for i, j in EDGES:
            if red[i][j]:
                pages = sum(red[i][k] * red[j][k] for k in range(22))
                f = 3 - pages
            else:
                pages = sum(not red[i][k] and not red[j][k] for k in range(22) if k not in (i, j))
                f = 6 - pages
            F[i][j] = F[j][i] = f
        incident = list(map(sum, F))
        for i in range(22):
            mono_triangles = sum(red[i][j] == red[i][k] == red[j][k]
                                 for j, k in combinations([v for v in range(22) if v != i], 2))
            need(incident[i] == 3 * DEGREES[i] + 6 * (21 - DEGREES[i]) - 2 * mono_triangles,
                 "literal triangle incident identity")
            need(incident[i] == 2 * sum(red[i][:4]) - (DEGREES[i] - 10) ** 2,
                 "specialized neighbor identity")
        links = {(i, j): F[i][j] for i, j in EDGES}
        H = literal_H(links)
        K = [[2 * DEGREES[i] - 17 if i == j else 2 * red[i][j] for j in range(22)] for i in range(22)]
        need(all(sum(x * y for x, y in zip(K[i], K[j])) == H[i][j]
                 for i in range(22) for j in range(22)), "literal row-dot square identity")
        need(sum(incident) == 30, "signed total defect control")
        results.append({"red_mask": mask, "incident_defect": incident, "F_H_sha256": sha256(serialize([F, H])).hexdigest()})
    return results


def baseline():
    rows = Path(__file__).with_name("baseline21.rows").read_text().split()
    need(len(rows) == 21 and all(len(row) == 21 and set(row) <= {"0", "1"} for row in rows), "malformed baseline")
    R = [[int(c) for c in row] for row in rows]
    B = [[int(i != j and not R[i][j]) for j in range(21)] for i in range(21)]
    need(all(R[i][i] == 0 and R[i][j] == R[j][i] for i in range(21) for j in range(21)), "baseline symmetry")
    maxima = [max(sum(A[i][k] * A[j][k] for k in range(21))
                  for i, j in combinations(range(21), 2) if A[i][j]) for A in (R, B)]
    need(Counter(map(sum, R)) == {8: 4, 9: 16, 10: 1} and maxima == [3, 6], "known baseline differs")
    return {"red_edges": sum(map(sum, R)) // 2, "degree_histogram": [4, 16, 1], "max_pages": maxima}


def compare(expected, actual):
    need(serialize(expected) == serialize(actual), "full entrywise certificate mismatch")


def corruptions(expected, actual):
    changes = [
        ("missing case", lambda a: a["cases"].pop()),
        ("duplicate case", lambda a: a["cases"].append(deepcopy(a["cases"][0]))),
        ("wrong full defect entry", lambda a: a["cases"][0]["F"][0].__setitem__(0, 1)),
        ("wrong full forced matrix", lambda a: a["cases"][0]["H"][0].__setitem__(1, 99)),
        ("wrong determinant", lambda a: a["cases"][0].__setitem__("det_H", 1)),
        ("wrong floor root", lambda a: a["cases"][0].__setitem__("floor_sqrt_det", 1)),
        ("wrong modular residue", lambda a: a["cases"][0].__setitem__("det_residue", 0)),
        ("wrong modulus", lambda a: a["cases"][0].__setitem__("nonsquare_modulus", 25)),
        ("omitted local graph", lambda a: a["small_bridge_checks"]["four_vertex_graphs"].pop()),
        ("accepted overlapping columns", lambda a: a["small_bridge_checks"]["K4_exceptional_patterns"][0].__setitem__("allowed", True)),
        ("wrong incidence budget", lambda a: a["small_bridge_checks"].__setitem__("C4_required_and_actual_cross_edges", [24, 24])),
        ("altered signed fixture mask", lambda a: a["signed_controls"][0].__setitem__("red_mask", 0)),
    ]
    rejected = []
    for label, mutate in changes:
        candidate = deepcopy(expected)
        mutate(candidate)
        try:
            compare(candidate, actual)
        except RuntimeError:
            rejected.append(label)
        else:
            raise RuntimeError("corrupt certificate accepted: " + label)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("degree97_expected.json"))
    args = parser.parse_args()
    need(determinant([[0, 1], [2, 3]]) == -2 and determinant([[1, 2], [2, 4]]) == 0,
         "rational determinant sign/singular controls")
    need(modular_det([[0, 1], [2, 3]], 13) == 11 and modular_det([[1, 2], [2, 4]], 23) == 0,
         "modular determinant sign/singular controls")
    expected = json.loads(args.expected.read_text())
    cases, placements = matrices()
    actual = {"agent": "six-books-1", "role": "researcher", "degree_histogram": [4, 18, 0],
              "red_edges": 97, "total_defect": 15, "incident_parity_surplus": 12,
              "small_bridge_checks": bridge_checks(), "cases": cases,
              "signed_controls": check_signed_fixtures(expected["signed_controls"]),
              "known_baseline21": baseline()}
    compare(expected, actual)
    rejected = corruptions(expected, actual)
    print(json.dumps({"complete": True, "four_vertex_graphs": 10,
                      "ordered_K4_column_patterns": 40, "unique_K4_column_patterns": 25,
                      "labeled_defect_placements": placements, "full_F_H_entries_agree": True,
                      "positive_nonsquare_determinants": 4,
                      "modular_certificates": [[r["nonsquare_modulus"], r["det_residue"]] for r in cases],
                      "signed_controls": 24, "incident_identity_checks": 528,
                      "square_identity_entries": 11616, "corruptions_rejected": rejected}))


if __name__ == "__main__":
    main()
