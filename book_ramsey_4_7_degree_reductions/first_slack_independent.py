#!/usr/bin/env python3
"""Separate labeled-surplus construction and rational determinant verification.

No imports of the generator, its helpers, or predecessor code. Expected
records are comparison targets; they do not choose the domain to be tested.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def serialize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def rational_determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    answer = Fraction(1)
    for col in range(len(a)):
        row = next((i for i in range(col, len(a)) if a[i][col]), None)
        if row is None:
            return 0
        if row != col:
            a[row], a[col] = a[col], a[row]
            answer = -answer
        pivot = a[col][col]
        answer *= pivot
        for i in range(col + 1, len(a)):
            multiplier = a[i][col] / pivot
            for j in range(col + 1, len(a)):
                a[i][j] -= multiplier * a[col][j]
            a[i][col] = 0
    need(answer.denominator == 1, "integer determinant has a denominator")
    return answer.numerator


def sqrt_floor(value):
    need(value > 0, "nonpositive determinant")
    low, high = 0, 1 << ((value.bit_length() + 1) // 2)
    while high - low > 1:
        middle = (low + high) // 2
        if middle * middle <= value:
            low = middle
        else:
            high = middle
    need(low * low < value < high * high, "square determinant survivor")
    return low


def literal_matrix(degree, links):
    return [[(2 * degree[i] - 17) ** 2 + 4 * degree[i] if i == j
             else 4 * (degree[i] + degree[j] - 14) - 4 * links.get(tuple(sorted((i, j))), 0)
             for j in range(22)] for i in range(22)]


def normalize(degree, links):
    incident = [{} for _ in degree]
    for (i, j), weight in links.items():
        need(0 <= i < j < 22 and isinstance(weight, int) and weight > 0, "malformed defect edge")
        incident[i][j] = incident[j][i] = weight
    excess = [sum(row.values()) - d % 2 for row, d in zip(incident, degree)]
    need(sum(excess) == 4 and all(x >= 0 and x % 2 == 0 for x in excess), "wrong parity slack")
    centers = sorted((i for i, x in enumerate(excess) if x), key=lambda i: (degree[i], i))
    need(sorted(excess[i] for i in centers) in ([4], [2, 2]), "wrong surplus support")
    normal_odd = {i for i, d in enumerate(degree) if d == 9 and i not in centers}
    for i in range(22):
        if i not in centers:
            need(sum(incident[i].values()) == degree[i] % 2, "wrong normal vertex")
    # Recover canonical ordering from adjacency, rather than from the generation choices.
    leaves = []
    for i in centers:
        local = sorted(j for j in incident[i] if j not in centers)
        need(all(j in normal_odd and incident[i][j] == 1 for j in local), "nonunit center leaf")
        leaves.extend(local)
    need(len(set(leaves)) == len(leaves), "shared degree-one leaf")
    remaining = normal_odd - set(leaves)
    pairs = []
    while remaining:
        i = min(remaining)
        need(len(incident[i]) == 1, "normal odd vertex is not a leaf")
        j, weight = next(iter(incident[i].items()))
        need(j in remaining - {i} and weight == 1, "bad residual matching")
        pairs.append((i, j))
        remaining.remove(i)
        remaining.remove(j)
    order = []
    for d in (8, 9, 10):
        order.extend(i for i in centers if degree[i] == d)
        if d == 9:
            order.extend(leaves)
            order.extend(i for pair in pairs for i in pair)
        else:
            order.extend(i for i, value in enumerate(degree) if value == d and i not in centers)
    need(len(order) == 22 and set(order) == set(range(22)), "incomplete canonical permutation")
    need([degree[i] for i in order] == degree, "permutation changes degree classes")
    position = {old: new for new, old in enumerate(order)}
    edges = sorted([*sorted((position[i], position[j])), weight] for (i, j), weight in links.items())
    weight = links.get(tuple(sorted(centers)), 0) if len(centers) == 2 else 0
    descriptor = (tuple(degree[i] for i in centers), weight)
    original = literal_matrix(degree, links)
    normalized = [[original[i][j] for j in order] for i in order]
    return descriptor, edges, normalized, [sum(incident[i].values()) for i in centers]


def generate_histogram(histogram):
    degree = [d for d, count in zip((8, 9, 10), histogram) for _ in range(count)]
    total_defect = (132 - 3 * sum((d - 10) ** 2 for d in degree)) // 2
    odd = {i for i, d in enumerate(degree) if d % 2}
    results, matrices, placements = {}, {}, Counter()
    # Enumerate every labeled support of a nonnegative even surplus of total four.
    for count in (1, 2):
        for centers in combinations(range(22), count):
            demand = {i: degree[i] % 2 + (4 if count == 1 else 2) for i in centers}
            for weight in (range(total_defect + 1) if count == 2 else (0,)):
                leaves_needed = {i: demand[i] - weight for i in centers}
                available = sorted(odd - set(centers), reverse=True)
                if any(x < 0 for x in leaves_needed.values()) or sum(leaves_needed.values()) > len(available):
                    continue
                if (len(available) - sum(leaves_needed.values())) % 2:
                    continue
                links = {}
                if weight:
                    links[tuple(sorted(centers))] = weight
                for i in centers:
                    for _ in range(leaves_needed[i]):
                        j = available.pop(0)
                        links[tuple(sorted((i, j)))] = 1
                while available:
                    i, j = available[:2]
                    del available[:2]
                    links[tuple(sorted((i, j)))] = 1
                need(sum(links.values()) == total_defect, "wrong total defect")
                descriptor, edges, matrix, row_degrees = normalize(degree, links)
                if descriptor not in results:
                    value = rational_determinant(matrix)
                    matrices[descriptor] = matrix
                    results[descriptor] = {
                        "center_classes": list(descriptor[0]), "center_row_degrees": row_degrees,
                        "center_edge_weight": descriptor[1], "defect_edges": edges,
                        "det_H": value, "floor_sqrt_det": sqrt_floor(value),
                        "forced_matrix_sha256": sha256(serialize(matrix)).hexdigest()}
                else:
                    prior = results[descriptor]
                    need(prior["defect_edges"] == edges and prior["center_row_degrees"] == row_degrees
                         and matrices[descriptor] == matrix,
                         "normalization failed on a labeled placement")
                placements["one_center" if count == 1 else "two_centers"] += 1
    keys = sorted(results, key=lambda key: (len(key[0]), key))
    return {"degree_histogram": list(histogram), "red_edges": sum(degree) // 2,
            "total_spine_defect": total_defect, "template_count": len(keys),
            "records": [results[key] for key in keys]}, dict(placements)


def bookkeeping():
    # Solve b=32-3a and c=2a-10, rather than scanning the triangular count domain.
    histograms = [[a, 32 - 3 * a, 2 * a - 10] for a in range(23)
                  if 32 - 3 * a >= 0 and 2 * a - 10 >= 0 and a % 2 == 0]
    remaining = []
    for edges in (97, 98, 99):
        # From 2a+b=220-2e and a+b+c=22.
        lists = [[a, 220 - 2 * edges - 2 * a, 2 * edges - 198 + a]
                 for a in range(23)
                 if 220 - 2 * edges - 2 * a >= 0 and 2 * edges - 198 + a >= 0
                 and 3 * a + (220 - 2 * edges - 2 * a) <= 31]
        remaining.append({"red_edges": edges, "necessary_histograms": lists})
    return {"first_slack_histograms": histograms, "remaining_low_edge_histograms": remaining}


def definition_controls():
    counts, digest = Counter(), sha256()
    universe = set(range(22))
    for seed in range(24):
        rng = random.Random(324000 + seed)
        red = [set() for _ in range(22)]
        for i, j in combinations(range(22), 2):
            if rng.randrange(100) < 24 + 2 * seed:
                red[i].add(j)
                red[j].add(i)
        degree = [len(row) for row in red]
        blue = [universe - row - {i} for i, row in enumerate(red)]
        defect = {}
        incident = [0] * 22
        for i, j in combinations(range(22), 2):
            value = (3 - len(red[i] & red[j])) if j in red[i] else (6 - len(blue[i] & blue[j]))
            defect[i, j] = value
            incident[i] += value
            incident[j] += value
        matrix = literal_matrix(degree, defect)
        K = [[2 * degree[i] - 17 if i == j else 2 * int(j in red[i]) for j in range(22)]
             for i in range(22)]
        for i in range(22):
            triangles = sum((j in red[i]) == (k in red[i]) == (k in red[j])
                            for j, k in combinations(sorted(universe - {i}), 2))
            need(incident[i] == 3 * degree[i] + 6 * (21 - degree[i]) - 2 * triangles,
                 "literal incident triangle identity")
            need(incident[i] % 2 == degree[i] % 2, "literal incident parity")
            for j in range(22):
                need(sum(x * y for x, y in zip(K[i], K[j])) == matrix[i][j], "literal row-dot square")
        triangles = sum((j in red[i]) == (k in red[i]) == (k in red[j])
                        for i, j, k in combinations(range(22), 3))
        total = sum(defect.values())
        need(2 * total == 132 - 3 * sum((d - 10) ** 2 for d in degree), "literal total defect")
        need(triangles == 1540 - sum(d * (21 - d) for d in degree) // 2, "literal Goodman identity")
        digest.update(serialize([seed, degree, total, matrix]) + b"\n")
        counts.update(graphs=1, spines=231, matrix_entries=484, incident_parities=22)
    return {"counts": dict(sorted(counts.items())), "sha256": digest.hexdigest()}


def compare(expected, actual):
    need(expected["agent"] == "six-books-1" and expected["role"] == "researcher", "wrong provenance")
    for field in ("template_results", "histogram_audit", "controls"):
        need(serialize(expected[field]) == serialize(actual[field]), "entry-level mismatch: " + field)


def negative_controls(expected, actual):
    changes = []
    def variant(label, mutate):
        candidate = deepcopy(expected)
        mutate(candidate)
        changes.append((label, candidate))
    def first(candidate):
        return candidate["template_results"][0]["records"][0]
    variant("missing template", lambda x: x["template_results"][0]["records"].pop())
    variant("duplicate template", lambda x: x["template_results"][0]["records"].append(deepcopy(first(x))))
    variant("loop defect", lambda x: first(x)["defect_edges"].append([0, 0, 1]))
    variant("negative defect", lambda x: first(x)["defect_edges"][0].__setitem__(2, -1))
    variant("wrong determinant", lambda x: first(x).__setitem__("det_H", first(x)["det_H"] + 1))
    variant("wrong nonsquare interval", lambda x: first(x).__setitem__("floor_sqrt_det", first(x)["floor_sqrt_det"] + 1))
    variant("wrong matrix", lambda x: first(x).__setitem__("forced_matrix_sha256", "0" * 64))
    variant("wrong histogram", lambda x: x["histogram_audit"]["first_slack_histograms"][0].__setitem__(0, 7))
    rejected = []
    for label, candidate in changes:
        try:
            compare(candidate, actual)
        except RuntimeError:
            rejected.append(label)
        else:
            raise RuntimeError("forged certificate accepted: " + label)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("first_slack_expected.json"))
    parser.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args()
    need(rational_determinant([[0, 1], [2, 3]]) == -2 and rational_determinant([[1, 2], [2, 4]]) == 0,
         "determinant sign/singular controls")
    hist = bookkeeping()
    census, placements = [], []
    for histogram in hist["first_slack_histograms"]:
        value, counts = generate_histogram(histogram)
        census.append(value)
        placements.append(counts)
    actual = {"template_results": census, "histogram_audit": hist, "controls": definition_controls()}
    expected = json.loads(args.expected.read_text())
    compare(expected, actual)
    rejected = negative_controls(expected, actual) if args.negative_controls else []
    print(json.dumps({"complete": True, "templates": [r["template_count"] for r in census],
                      "labeled_placements": placements, "square_survivors": 0,
                      "controls": actual["controls"], "corruptions_rejected": rejected}))


if __name__ == "__main__":
    main()
