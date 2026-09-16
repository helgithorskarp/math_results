#!/usr/bin/env python3
"""Independent exact review of the opposed241 forced-equal-pair gate.

The checker reconstructs the physical graph in the full eight-term
multiquadratic basis.  It checks the submitted eight positive witnesses, then
builds a different pair-separating family by deterministic direct DSATUR
search without consulting those submitted words.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_opposed241_equal_pair_gate"
PARENT = ROOT / "hadwiger_nelson_opposed241_conditional_core"
B214 = ROOT / "hadwiger_nelson_nonmono159_214_lowden2/points214.tsv"
SCALE = 36
PRIMES = (3, 5, 11)
UNIT = (SCALE * SCALE,) + (0,) * 7

PINNED = {
    TARGET / "README.md": "49b3033974d4fba0538911fbf0442153fb61a1435da7d8c58eb90f0e4f4a80b0",
    TARGET / "PROOF.md": "23a7e4355514a7010746a53698b0c4126e908b2e0443be7a4025f682ffb17b6a",
    TARGET / "PROVENANCE.md": "fe0d78ca9c6205fb6f5ab75993e23668effbbf816c9f577689552b74bdc2d407",
    TARGET / "certificate.json": "1872c210dbc0ce3a981c86c35cd4cef787118ef1c4e73a03dbca2132b4c86ad0",
    TARGET / "EXPECTED.json": "7240be173e633e854de24ce20870ca03c8f0b5793bf3450828cfa7a033ee0b79",
    TARGET / "verify.py": "025aabeeaf0deeb282d8bdfe96b4ea96c71944bd0827d1c6dbcfaf44df65f89c",
    TARGET / "controls.py": "96fb321147ba1fbd3c7723c633e6255408aadf83ac3f590f20b33467f53c3848",
    PARENT / "certificate.json": "37e1397276f931ee1b9b63f4ca5c343a2ac129fa3b1c6d526e4c151031a750e4",
    B214: "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
}

POINT_HASH = "70c14dfaec7875038c0f3cc1b9f84f5469143f5227fbd49377340bb46e27d908"
EDGE_HASH = "02e1fbb4c9f94cc5aca57945657706088e25560d3ca0c00217d0d17d647f55ab"
TARGET_WORD_HASH = "0e88e2bf0d0c306238db2bdaee31224f89cf04c299f897f3d8b3694981fa3dd0"


class ReviewFailure(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ReviewFailure(message)


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def stream_hash(rows):
    return sha256("".join(rows).encode("ascii"))


def field_product(left, right):
    common = left & right
    factor = 1
    for bit, prime in enumerate(PRIMES):
        if common & (1 << bit):
            factor *= prime
    return factor, left ^ right


PRODUCTS = tuple(tuple(field_product(i, j) for j in range(8)) for i in range(8))


def multiply(left, right):
    result = [0] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if b:
                factor, mask = PRODUCTS[i][j]
                result[mask] += factor * a * b
    return tuple(result)


def squared_distance(left, right):
    dx = tuple(a - b for a, b in zip(left[0], right[0]))
    dy = tuple(a - b for a, b in zip(left[1], right[1]))
    xx = multiply(dx, dx)
    yy = multiply(dy, dy)
    return tuple(a + b for a, b in zip(xx, yy))


def flat_point(a, b, c, d):
    x = [0] * 8
    y = [0] * 8
    x[0], x[5] = a, b
    y[1], y[4] = c, d
    return tuple(x), tuple(y)


def golomb_points():
    rows = (
        (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
        (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
        (18, 0, -18, 0), (6, 0, 0, 6), (-3, -3, 3, -3),
        (-3, 3, -3, -3),
    )
    return [flat_point(*row) for row in rows]


def read_b214():
    points = []
    for line in B214.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        need(len(row) == 16, "B214 row width")
        need(all(row[index] == 0 for index in range(16)
                 if index not in (0, 5, 9, 12)), "B214 field support")
        points.append((tuple(3 * value for value in row[:8]),
                       tuple(3 * value for value in row[8:])))
    need(len(points) == len(set(points)) == 214, "B214 point census")
    return points


def transform(points, reflected):
    output = []
    for x, y in points:
        xx = tuple(-value for value in x) if reflected else x
        shift = 18 if reflected else -18
        output.append(((xx[0] + shift,) + xx[1:], y))
    return output


def merge(*blocks):
    result = []
    seen = set()
    for block in blocks:
        for point in block:
            if point not in seen:
                seen.add(point)
                result.append(point)
    return result


def reconstruct(source_ids):
    base = read_b214()
    source = merge(golomb_points(), transform(base, False), transform(base, True))
    need(len(source) == 343, "opposed source order")
    need(source_ids == sorted(set(source_ids)) and len(source_ids) == 241,
         "canonical core labels")
    points = [source[index] for index in source_ids]
    need(len(set(points)) == 241, "core physical collisions")
    edges = [
        (left, right)
        for left, right in itertools.combinations(range(241), 2)
        if squared_distance(points[left], points[right]) == UNIT
    ]
    need(len(edges) == 991, "complete unit-edge census")
    return points, edges


def point_hash(points):
    order = (0, 1, 4, 5)
    need(all(axis[index] == 0 for point in points for axis in point
             for index in range(8) if index not in order), "unexpected field term")
    rows = []
    for x, y in points:
        values = tuple(x[index] for index in order) + tuple(y[index] for index in order)
        rows.append(" ".join(map(str, values)) + "\n")
    return stream_hash(rows)


def edge_hash(edges):
    return stream_hash(f"{left} {right}\n" for left, right in edges)


def validate_word(word, edges):
    need(isinstance(word, str) and len(word) == 241, "word length")
    need(set(word) <= set("0123"), "word alphabet")
    need(all(word[left] != word[right] for left, right in edges), "improper word")


def signatures(words):
    return [tuple(word[vertex] for word in words) for vertex in range(241)]


def separation_histogram(words):
    histogram = {}
    for left, right in itertools.combinations(range(241), 2):
        count = sum(word[left] != word[right] for word in words)
        histogram[count] = histogram.get(count, 0) + 1
    return histogram


def smallest_separating_subset(words):
    for size in range(1, len(words) + 1):
        good = []
        for subset in itertools.combinations(range(len(words)), size):
            chosen = [words[index] for index in subset]
            if len(set(signatures(chosen))) == 241:
                good.append(subset)
        if good:
            return size, good
    raise ReviewFailure("no separating word subset")


def target_certificate_checks(words, edges):
    need(len(words) == len(set(words)) == 8, "target word count")
    for word in words:
        validate_word(word, edges)
    need(len(set(signatures(words))) == 241, "target signatures")
    size, subsets = smallest_separating_subset(words)
    need(size == 8 and subsets == [tuple(range(8))], "target row irredundance")
    unique_pairs = []
    for index, word in enumerate(words):
        count = 0
        for left, right in itertools.combinations(range(241), 2):
            if word[left] != word[right] and all(
                    words[other][left] == words[other][right]
                    for other in range(8) if other != index):
                count += 1
        unique_pairs.append(count)
    return unique_pairs, separation_histogram(words)


def adjacency(edges, extra):
    graph = [set() for _ in range(241)]
    for left, right in list(edges) + [extra]:
        graph[left].add(right)
        graph[right].add(left)
    return graph


def colour_with_separation(edges, extra):
    """Direct deterministic four-colour search with one extra inequality."""
    graph = adjacency(edges, extra)
    need(all(other in graph[vertex] for vertex, other in ((0, 1), (0, 2), (1, 2))),
         "normalizing triangle")
    colours = [-1] * 241
    masks = [0] * 241
    degrees = list(map(len, graph))
    for vertex, colour in enumerate((0, 1, 2)):
        colours[vertex] = colour
    for vertex, colour in enumerate(colours):
        if colour >= 0:
            for other in graph[vertex]:
                if colours[other] < 0:
                    masks[other] |= 1 << colour
    nodes = 0
    backtracks = 0

    def search(done, maximum):
        nonlocal nodes, backtracks
        nodes += 1
        if done == 241:
            return True
        vertex = max(
            (item for item in range(241) if colours[item] < 0),
            key=lambda item: (masks[item].bit_count(), degrees[item], -item),
        )
        available = [
            colour for colour in range(min(3, maximum + 1) + 1)
            if not masks[vertex] & (1 << colour)
        ]
        available.sort(key=lambda colour: (
            sum(colours[other] < 0 and not masks[other] & (1 << colour)
                for other in graph[vertex]),
            (colour + extra[0] + extra[1]) % 4,
        ))
        for colour in available:
            bit = 1 << colour
            colours[vertex] = colour
            changed = []
            conflict = False
            for other in graph[vertex]:
                if colours[other] < 0 and not masks[other] & bit:
                    masks[other] |= bit
                    changed.append(other)
                    if masks[other] == 15:
                        conflict = True
            if not conflict and search(done + 1, max(maximum, colour)):
                return True
            for other in changed:
                masks[other] ^= bit
            colours[vertex] = -1
            backtracks += 1
        return False

    need(search(3, 2), "four-colour separation search")
    word = "".join(map(str, colours))
    validate_word(word, edges)
    need(word[extra[0]] != word[extra[1]], "requested pair not separated")
    return word, nodes, backtracks


def fresh_family(edges):
    unresolved = set(itertools.combinations(range(241), 2))
    words = []
    pairs = []
    nodes = []
    backtracks = []
    while unresolved:
        pair = min(unresolved)
        word, visited, failed = colour_with_separation(edges, pair)
        words.append(word)
        pairs.append(pair)
        nodes.append(visited)
        backtracks.append(failed)
        unresolved = {
            edge for edge in unresolved if word[edge[0]] == word[edge[1]]
        }
        need(len(words) <= 30, "fresh family failed to converge")
    need(len(set(signatures(words))) == 241, "fresh signatures")
    return words, pairs, nodes, backtracks


def sign_a_plus_b_sqrt33(a, b):
    if not b:
        return (a > 0) - (a < 0)
    if not a:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    comparison = a * a - 33 * b * b
    need(comparison != 0, "rational square root of 33")
    return ((comparison > 0) - (comparison < 0)) * (1 if a > 0 else -1)


def quarter_class(distance):
    need(all(distance[index] == 0 for index in range(8) if index not in (0, 5)),
         "distance outside Q(sqrt(33))")
    return sign_a_plus_b_sqrt33(distance[0] - SCALE * SCALE // 4, distance[5])


def golomb_has_three_colouring(edges):
    small = [(left, right) for left, right in edges if left < 10 and right < 10]
    need(len(small) == 18, "Golomb induced edge count")
    for tail in itertools.product(range(3), repeat=7):
        word = (0, 1, 2) + tail
        if all(word[left] != word[right] for left, right in small):
            return True
    return False


def construct_report():
    for path, expected in PINNED.items():
        need(sha256(path.read_bytes()) == expected, "pinned bytes: " + str(path))
    certificate = json.loads((TARGET / "certificate.json").read_text())
    parent = json.loads((PARENT / "certificate.json").read_text())
    need(certificate["source_ids"] == parent["source_ids"], "parent core labels")
    points, edges = reconstruct(certificate["source_ids"])
    need(point_hash(points) == parent["point_sha256"] == POINT_HASH, "point stream")
    need(edge_hash(edges) == parent["edge_sha256"] == EDGE_HASH, "edge stream")

    target_words = certificate["words"]
    need(stream_hash(word + "\n" for word in target_words) == TARGET_WORD_HASH,
         "target word stream")
    target_unique, target_histogram = target_certificate_checks(target_words, edges)

    fresh_words, requested_pairs, nodes, backtracks = fresh_family(edges)
    need(all(word not in set(target_words) for word in fresh_words),
         "fresh family overlaps submitted family")
    fresh_minimum, fresh_subsets = smallest_separating_subset(fresh_words)
    fresh_histogram = separation_histogram(fresh_words)

    quarter = {-1: 0, 0: 0, 1: 0}
    for left, right in itertools.combinations(range(241), 2):
        quarter[quarter_class(squared_distance(points[left], points[right]))] += 1
    need(quarter == {-1: 1910, 0: 0, 1: 27010}, "distance-half census")
    need(not golomb_has_three_colouring(edges), "Golomb three-colouring")

    return {
        "status": "ACCEPT_AND_STRENGTHEN_NO_FORCED_EQUAL_PAIR",
        "reviewed_target_commit": "b1b1bf00c80b0524956a889ceb3a82920b3571dc",
        "points": 241,
        "all_pairs_checked": 28920,
        "complete_unit_edges": len(edges),
        "chromatic_number": 4,
        "point_sha256": point_hash(points),
        "edge_sha256": edge_hash(edges),
        "submitted_words": len(target_words),
        "submitted_word_stream_sha256": TARGET_WORD_HASH,
        "submitted_signature_count": len(set(signatures(target_words))),
        "submitted_family_smallest_separating_subset": 8,
        "submitted_family_separating_subsets_of_size_8": len([x for x in [tuple(range(8))]]),
        "submitted_unique_pair_counts_by_word": target_unique,
        "submitted_pair_separation_histogram": {
            str(key): target_histogram[key] for key in sorted(target_histogram)
        },
        "fresh_words": len(fresh_words),
        "fresh_word_stream_sha256": stream_hash(word + "\n" for word in fresh_words),
        "fresh_word_sha256": [sha256(word.encode()) for word in fresh_words],
        "fresh_requested_pairs": [list(pair) for pair in requested_pairs],
        "fresh_search_nodes": nodes,
        "fresh_search_backtracks": backtracks,
        "fresh_search_total_nodes": sum(nodes),
        "fresh_search_total_backtracks": sum(backtracks),
        "fresh_signature_count": len(set(signatures(fresh_words))),
        "fresh_family_smallest_separating_subset": fresh_minimum,
        "fresh_family_separating_subsets_at_minimum": len(fresh_subsets),
        "fresh_family_first_minimum_subset": list(fresh_subsets[0]),
        "fresh_pair_separation_histogram": {
            str(key): fresh_histogram[key] for key in sorted(fresh_histogram)
        },
        "fresh_family_disjoint_from_submitted_words": True,
        "forced_equal_pairs": 0,
        "pairs_distance_squared_lt_quarter": quarter[-1],
        "pairs_distance_squared_eq_quarter": quarter[0],
        "pairs_distance_squared_gt_quarter": quarter[1],
        "eligible_pairs_for_two_copy_spindle": quarter[0] + quarter[1],
        "maximum_two_copy_shared_anchor_order": 481,
        "all_subgraphs_corollary": True,
        "record_candidate": False,
        "scope": "fixed 241-point core and all its vertex/edge subgraphs; pair-equality route only",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    report = construct_report()
    if arguments.check_expected:
        need(report == json.loads((HERE / "EXPECTED.json").read_text()),
             "EXPECTED.json mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
