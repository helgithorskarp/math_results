"""Independent exact checker for the EI17--Moser pair-neutrality certificate.

This file imports no producer or model code.  It uses rational midpoint error
bounds, rather than the producer's fixed-denominator interval arithmetic.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from importlib import import_module
from itertools import combinations, product
import argparse
import json
from math import isqrt
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EI = ROOT / "hadwiger_nelson_ei17_common_pair"
DEPENDENCIES = {
    "intervals.py": "0fb646ef2fccf68334e6c0d80d1b2f7210a73a1f0135030a15ccf02c1d5b3ce7",
    "seed.py": "9ec359a35d352b1947d87516df918135eb83658a2125ccfc6515dcbff907e833",
    "seed_edges.json": "b77a3a242467f2c1ed3f047914492e70a0da9cbe6ca8234941c8dd008e25e450",
    "seed_midpoint.json": "fb712ad09168fa51814556641f31280acc8ad1e71a17a9878d1cfd55eeb96565",
}
HORIZONTAL_EI = ((1, 9), (2, 11), (5, 15), (10, 16))
MOSER_TRANSLATES = ((0, 1), (2, 3))
RHOMBI = ((5, 10, 16, 15), (1, 5, 15, 9), (1, 2, 11, 9))
EXTRA_CONTACT_IDENTITY = (
    (1, (0, 3, 12, 7)),
    (-1, (1, 2, 11, 9)),
    (-1, (2, 4, 8, 6)),
    (1, (3, 12, 16, 13)),
    (-1, (4, 7, 14, 13)),
    (1, (8, 9, 11, 10)),
)


def need(test, message):
    if not test:
        raise ValueError(message)


def check_dependencies():
    for name, expected in DEPENDENCIES.items():
        need(sha256((EI / name).read_bytes()).hexdigest() == expected,
             f"EI17 dependency hash: {name}")


def exact_moser():
    def real(a=0, b=0, c=0, d=0):
        return tuple(map(F, (a, b, c, d)))

    def add(a, b):
        return tuple(x + y for x, y in zip(a, b))

    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    def mul(a, b):
        answer = [F(0)] * 4
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                square = (3 if i & j & 1 else 1) * (11 if i & j & 2 else 1)
                answer[i ^ j] += x * y * square
        return tuple(answer)

    points = (
        (real(), real()),
        (real(1), real()),
        (real(F(1, 2)), real(0, F(1, 2))),
        (real(F(3, 2)), real(0, F(1, 2))),
        (real(F(5, 6)), real(0, 0, F(1, 6))),
        (real(F(5, 12), 0, 0, F(-1, 12)), real(0, F(5, 12), F(1, 12))),
        (real(F(5, 4), 0, 0, F(-1, 12)), real(0, F(5, 12), F(1, 4))),
    )
    edges = []
    for a, b in combinations(range(7), 2):
        dx, dy = (sub(points[a][k], points[b][k]) for k in range(2))
        if add(mul(dx, dx), mul(dy, dy)) == real(1):
            edges.append((a, b))
    need(len(edges) == 11, "Moser exact edge count")
    return points, tuple(edges)


def quotient_classes():
    parent = list(range(119))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[max(a, b)] = min(a, b)

    for low, high in HORIZONTAL_EI:
        for left, right in MOSER_TRANSLATES:
            union(7 * low + right, 7 * high + left)
    groups = {}
    for address in range(119):
        groups.setdefault(find(address), []).append(address)
    classes = tuple(tuple(group) for _, group in sorted(groups.items()))
    class_of = {address: k for k, group in enumerate(classes) for address in group}
    return classes, class_of


def rational_geometry():
    check_dependencies()
    sys.path.insert(0, str(EI))
    try:
        seed = import_module("seed")
        _, root = seed.certify()
    finally:
        sys.path.pop(0)

    ei_mid = tuple(tuple(F(x) for x in row)
                   for row in json.loads((EI / "seed_midpoint.json").read_text()))
    ei_edges = tuple(map(tuple, json.loads((EI / "seed_edges.json").read_text())))
    ei_edge_set = set(ei_edges)
    need(ei_mid[10] == (F(-1), F(0)) and ei_mid[16] == (F(0), F(0)),
         "EI17 pinned coordinates")
    for cycle in RHOMBI:
        need(all(tuple(sorted((cycle[k], cycle[(k + 1) % 4]))) in ei_edge_set
                 for k in range(4)), f"EI17 rhombus edges: {cycle}")
        need(len(set(cycle)) == 4, "rhombus labels distinct")
    identity = [0] * 17
    for coefficient, (a, b, c, d) in EXTRA_CONTACT_IDENTITY:
        need(all(tuple(sorted((u, v))) in ei_edge_set
                 for u, v in ((a, b), (b, c), (c, d), (d, a))),
             f"extra-contact rhombus edges: {(a,b,c,d)}")
        for vertex, sign in ((a, 1), (c, 1), (b, -1), (d, -1)):
            identity[vertex] += coefficient * sign
    target = [0] * 17
    for vertex, sign in ((0, 1), (16, 1), (10, -1), (1, -1),
                         (14, -1), (6, 1)):
        target[vertex] += sign
    need(identity == target, "extra-contact rhombus telescoping identity")

    exact_m, moser_edges = exact_moser()
    scale = 10 ** 50
    roots = [F(1)]
    for radicand in (3, 11, 33):
        lower = isqrt(radicand * scale * scale)
        need(lower * lower <= radicand * scale * scale < (lower + 1) ** 2,
             "radical enclosure")
        roots.append(F(lower, scale))
    m_mid = tuple(tuple(sum(c * r for c, r in zip(coord, roots)) for coord in point)
                  for point in exact_m)
    need(all(sum(abs(coord[k]) for k in range(1, 4)) < 2
             for point in exact_m for coord in point), "Moser error coefficient bound")

    classes, class_of = quotient_classes()
    points = []
    for group in classes:
        i, j = divmod(group[0], 7)
        points.append(tuple(ei_mid[i][k] + m_mid[j][k] for k in range(2)))

    edges = set()
    for a, b in ei_edges:
        for j in range(7):
            edges.add(tuple(sorted((class_of[7 * a + j], class_of[7 * b + j]))))
    for a, b in moser_edges:
        for i in range(17):
            edges.add(tuple(sorted((class_of[7 * i + a], class_of[7 * i + b]))))
    for left, right in MOSER_TRANSLATES:
        edges.add(tuple(sorted((class_of[right], class_of[7 + left]))))
    need(all(a < b for a, b in edges), "inherited unit edge contracted")

    radius = F(1, 10 ** 18) + F(2, scale)
    separation = gap = None
    for a, b in combinations(range(len(points)), 2):
        delta = tuple(points[a][k] - points[b][k] for k in range(2))
        d2 = sum(x * x for x in delta)
        error = 4 * radius * sum(abs(x) for x in delta) + 8 * radius * radius
        need(d2 > error, f"unexcluded physical collision: {a},{b}")
        separation = d2 - error if separation is None else min(separation, d2 - error)
        if (a, b) in edges:
            need(abs(d2 - 1) <= error, f"inherited edge midpoint mismatch: {a},{b}")
        else:
            need(abs(d2 - 1) > error, f"unexcluded unit contact: {a},{b}")
            local = abs(d2 - 1) - error
            gap = local if gap is None else min(gap, local)

    edges = tuple(sorted(edges))
    canonical = {"classes": classes, "edges": edges}
    graph_hash = sha256((json.dumps(canonical, separators=(",", ":")) + "\n").encode()).hexdigest()
    return {
        "classes": classes,
        "class_of": class_of,
        "edges": edges,
        "graph_sha256": graph_hash,
        "root": root,
        "squared_separation_lower": separation,
        "nonedge_squared_unit_gap_lower": gap,
        "moser_edges": moser_edges,
    }


def verify_certificate(certificate):
    graph = rational_geometry()
    classes, edges = graph["classes"], graph["edges"]
    order = len(classes)
    expected_keys = {
        "schema", "dependency_sha256", "formal_addresses", "physical_points",
        "unit_edges", "collision_classes", "graph_sha256", "words",
    }
    need(isinstance(certificate, dict) and set(certificate) == expected_keys,
         "certificate schema keys")
    need(certificate["schema"] == "ei17-moser-pair-neutrality-v1", "schema")
    need(certificate["dependency_sha256"] == DEPENDENCIES, "certificate dependency hashes")
    need(certificate["formal_addresses"] == 119, "formal address count")
    need(certificate["physical_points"] == order == 111, "physical point count")
    need(certificate["unit_edges"] == len(edges) == 380, "unit edge count")
    collisions = [list(group) for group in classes if len(group) > 1]
    need(certificate["collision_classes"] == collisions and len(collisions) == 8,
         "collision classes")
    need(certificate["graph_sha256"] == graph["graph_sha256"], "graph hash")

    words = certificate["words"]
    need(isinstance(words, list) and words and len(words) == len(set(words)), "colour words")
    edge_set = set(edges)
    same = set()
    different = set()
    word_checks = 0
    for word in words:
        need(isinstance(word, str) and len(word) == order and set(word) <= set("0123"),
             "colour word format")
        need(all(word[a] != word[b] for a, b in edges), "improper colour word")
        word_checks += len(edges)
        for a, b in combinations(range(order), 2):
            (same if word[a] == word[b] else different).add((a, b))
    pairs = set(combinations(range(order), 2))
    nonedges = pairs - edge_set
    need(different == pairs, "some physical pair is not separated")
    need(nonedges <= same, "some physical nonedge cannot be equal in saved words")

    moser_edges = graph["moser_edges"]
    three_words = 0
    for word in product(range(3), repeat=7):
        three_words += 1
        need(any(word[a] == word[b] for a, b in moser_edges),
             "Moser fibre unexpectedly three-colourable")

    word_stream = ("\n".join(words) + "\n").encode()
    report = {
        "status": "EXACT EI17-MOSER TWO-TERMINAL RELATION IS NEUTRAL",
        "formal_addresses": 119,
        "physical_points": order,
        "collision_classes": len(collisions),
        "complete_unit_edges": len(edges),
        "physical_pairs": len(pairs),
        "physical_nonedges": len(nonedges),
        "colour_words": len(words),
        "colour_edge_checks": word_checks,
        "different_pattern_requests_covered": len(different),
        "equal_pattern_requests_covered": len(nonedges & same),
        "canonical_relation_requests": len(pairs) + len(nonedges),
        "moser_three_colour_words_rejected": three_words,
        "chromatic_number": 4,
        "all_distinct_pairs_separated": True,
        "every_nonedge_pair_can_be_equal": True,
        "complete_two_terminal_relation_neutral": True,
        "graph_sha256": graph["graph_sha256"],
        "colour_word_stream_sha256": sha256(word_stream).hexdigest(),
        "certificate_sha256": sha256((HERE / "certificate.json").read_bytes()).hexdigest()
            if certificate == json.loads((HERE / "certificate.json").read_text()) else None,
        "squared_separation_lower": str(graph["squared_separation_lower"]),
        "nonedge_squared_unit_gap_lower": str(graph["nonedge_squared_unit_gap_lower"]),
        "ei17_root": graph["root"],
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    report = verify_certificate(certificate)
    if args.check_expected:
        need(report == json.loads((HERE / "expected.json").read_text()), "expected report mismatch")
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        need(not args.output.exists(), "output path already exists")
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
