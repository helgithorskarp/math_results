#!/usr/bin/env python3
"""Exact verifier for every Moser--Golomb double-neighbour docking.

Only the Python standard library is used.  Coordinates lie in the real
biquadratic field Q(sqrt(3),sqrt(11)), represented on the ordered basis
(1,sqrt(3),sqrt(11),sqrt(33)); a plane point is a pair of field elements.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_moser_all_terminal_contacts" / "certificate.json"
SOURCE_SHA256 = "bddb9275204535cccce1d66bd2ad1415040a6807fdffb7902dec31fd57126a98"
EXPECTED = HERE / "expected.json"
ZERO = (Q(0),) * 4
ONE = (Q(1), Q(0), Q(0), Q(0))


def fadd(x, y):
    return tuple(a + b for a, b in zip(x, y))


def fsub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def fneg(x):
    return tuple(-a for a in x)


def fmul(x, y):
    out = [Q(0)] * 4
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            out[i ^ j] += a * b * (3 if i & j & 1 else 1) * (11 if i & j & 2 else 1)
    return tuple(out)


def finv(x):
    columns = [fmul(x, tuple(Q(i == j) for i in range(4))) for j in range(4)]
    rows = [[columns[j][i] for j in range(4)] + [Q(i == 0)] for i in range(4)]
    for column in range(4):
        pivot = next(row for row in range(column, 4) if rows[row][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        leading = rows[column][column]
        rows[column] = [value / leading for value in rows[column]]
        for row in range(4):
            if row != column and rows[row][column]:
                leading = rows[row][column]
                rows[row] = [a - leading * b for a, b in zip(rows[row], rows[column])]
    answer = tuple(row[-1] for row in rows)
    if fmul(x, answer) != ONE:
        raise ValueError("field inverse failed")
    return answer


def cadd(p, q):
    return fadd(p[0], q[0]), fadd(p[1], q[1])


def csub(p, q):
    return fsub(p[0], q[0]), fsub(p[1], q[1])


def cconj(p):
    return p[0], fneg(p[1])


def cmul(p, q):
    return (fsub(fmul(p[0], q[0]), fmul(p[1], q[1])),
            fadd(fmul(p[0], q[1]), fmul(p[1], q[0])))


def cnorm(p):
    return fadd(fmul(p[0], p[0]), fmul(p[1], p[1]))


def cinv(p):
    return cmul(cconj(p), (finv(cnorm(p)), ZERO))


def decode(row, denominator=12):
    return tuple(tuple(Q(value, denominator) for value in coordinate) for coordinate in row)


def sources():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("imported Moser contact certificate hash mismatch")
    certificate = json.loads(raw)
    moser = tuple(decode(row) for row in certificate["M"])
    circles = tuple(decode(row) for row in certificate["C"])
    docking = tuple(circles[i] for i in certificate["D_indices"])
    rows = (
        (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
        (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
        (18, 0, -18, 0), (6, 0, 0, 2), (-3, -3, 3, -1),
        (-3, 3, -3, -1),
    )
    golomb = tuple(
        ((Q(a, 36), Q(0), Q(0), Q(b, 36)),
         (Q(0), Q(c, 36), Q(d, 12), Q(0)))
        for a, b, c, d in rows
    )
    return moser, docking, golomb, certificate


def distance_classes(points):
    classes = defaultdict(list)
    for i, j in combinations(range(len(points)), 2):
        classes[cnorm(csub(points[j], points[i]))].append((i, j))
    return classes


def apply(transform, point):
    translation, multiplier, reflected = transform
    return cadd(translation, cmul(multiplier, cconj(point) if reflected else point))


def enumerate_placements(docking, golomb):
    docking_classes = distance_classes(docking)
    golomb_classes = distance_classes(golomb)
    by_transform = {}
    recipes = 0
    for distance, golomb_pairs in golomb_classes.items():
        for gi, gj in golomb_pairs:
            x0, x1 = golomb[gi], golomb[gj]
            for di, dj in docking_classes.get(distance, ()):
                for reflected in (False, True):
                    z0 = cconj(x0) if reflected else x0
                    z1 = cconj(x1) if reflected else x1
                    inverse_difference = cinv(csub(z1, z0))
                    for swapped in (False, True):
                        y0, y1 = docking[di], docking[dj]
                        if swapped:
                            y0, y1 = y1, y0
                        multiplier = cmul(csub(y1, y0), inverse_difference)
                        translation = csub(y0, cmul(multiplier, z0))
                        transform = translation, multiplier, reflected
                        recipe = gi, gj, di, dj, int(reflected), int(swapped)
                        if cnorm(multiplier) != ONE:
                            raise ValueError("non-isometric placement")
                        if apply(transform, x0) != y0 or apply(transform, x1) != y1:
                            raise ValueError("docking equations failed")
                        recipes += 1
                        if transform not in by_transform or recipe < by_transform[transform]:
                            by_transform[transform] = recipe
    cohort = tuple(sorted(
        ((recipe, transform) for transform, recipe in by_transform.items()),
        key=lambda item: item[0],
    ))
    return recipes, cohort


def physical_graph(moser, golomb, transform):
    addresses = moser + tuple(apply(transform, point) for point in golomb)
    groups = defaultdict(list)
    for address, point in enumerate(addresses):
        groups[point].append(address)
    classes = tuple(sorted(map(tuple, groups.values()), key=lambda group: group[0]))
    points = tuple(addresses[group[0]] for group in classes)
    class_of = {address: index for index, group in enumerate(classes) for address in group}
    edges = tuple((i, j) for i, j in combinations(range(len(points)), 2)
                  if cnorm(csub(points[i], points[j])) == ONE)
    moser_terminals = tuple(class_of[i] for i in range(7))
    golomb_terminals = tuple(class_of[7 + i] for i in range(10))
    if len(set(moser_terminals)) != 7 or len(set(golomb_terminals)) != 10:
        raise ValueError("an isometric component collapsed internally")
    return classes, points, edges, moser_terminals, golomb_terminals


def canonical_patterns(points, triangle):
    edges = tuple((i, j) for i, j in combinations(range(len(points)), 2)
                  if cnorm(csub(points[i], points[j])) == ONE)
    rest = tuple(i for i in range(len(points)) if i not in triangle)
    patterns = []
    for tail in product(range(4), repeat=len(rest)):
        word = [-1] * len(points)
        for vertex, colour in zip(triangle, (0, 1, 2)):
            word[vertex] = colour
        for vertex, colour in zip(rest, tail):
            word[vertex] = colour
        if all(word[i] != word[j] for i, j in edges):
            patterns.append(tuple(word))
    return edges, tuple(patterns)


class ColourGraph:
    def __init__(self, order, edges):
        self.order = order
        self.edges = frozenset(edges)
        self.adjacency = [set() for _ in range(order)]
        for i, j in edges:
            self.adjacency[i].add(j)
            self.adjacency[j].add(i)

    def extension(self, terminals=(), pattern=()):
        colours = [-1] * self.order
        for vertex, colour in zip(terminals, pattern):
            if colours[vertex] not in (-1, colour):
                return None
            colours[vertex] = colour
        if any(colours[i] == colours[j] != -1 for i, j in self.edges):
            return None

        def search():
            choice = None
            for vertex, colour in enumerate(colours):
                if colour != -1:
                    continue
                allowed = tuple(c for c in range(4)
                                if all(colours[w] != c for w in self.adjacency[vertex]))
                if not allowed:
                    return False
                key = len(allowed), -len(self.adjacency[vertex]), vertex
                if choice is None or key < choice[0]:
                    choice = key, vertex, allowed
            if choice is None:
                return True
            _, vertex, allowed = choice
            for colour in allowed:
                colours[vertex] = colour
                if search():
                    return True
            colours[vertex] = -1
            return False

        if not search():
            return None
        word = tuple(colours)
        if any(word[i] == word[j] for i, j in self.edges):
            raise ValueError("internal colouring error")
        return word


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def point_text(point):
    return ";".join(
        ",".join(fraction_text(value) for value in coordinate)
        for coordinate in point
    )


def digest_lines(lines):
    digest = hashlib.sha256()
    for line in lines:
        digest.update(line.encode("ascii") + b"\n")
    return digest.hexdigest()


def verify():
    moser, docking, golomb, source = sources()
    moser_edges, moser_patterns = canonical_patterns(moser, (0, 1, 2))
    golomb_edges, golomb_patterns = canonical_patterns(golomb, (0, 1, 2))
    if (len(moser_edges), len(moser_patterns)) != (11, 16):
        raise ValueError("unexpected Moser source")
    if (len(golomb_edges), len(golomb_patterns)) != (18, 95):
        raise ValueError("unexpected Golomb source")
    if any(sum(cnorm(csub(point, m)) == ONE for m in moser) != 2 for point in docking):
        raise ValueError("a docking point does not have exactly two Moser neighbours")
    if len(set(docking)) != 18 or len(source["D_indices"]) != 18:
        raise ValueError("unexpected docking set")

    recipe_count, cohort = enumerate_placements(docking, golomb)
    order_histogram = Counter()
    edge_histogram = Counter()
    collision_histogram = Counter()
    pair_status = Counter()
    graph_lines = []
    projection_lines = []
    pair_lines = []

    for index, (recipe, transform) in enumerate(cohort):
        classes, points, edges, mt, gt = physical_graph(moser, golomb, transform)
        graph = ColourGraph(len(points), edges)
        order_histogram[len(points)] += 1
        edge_histogram[len(edges)] += 1
        collision_histogram[17 - len(points)] += 1
        graph_lines.append(
            f"{index}|{','.join(map(str, recipe))}|"
            f"{'/'.join(','.join(map(str, group)) for group in classes)}|"
            f"{'/'.join(f'{i},{j}' for i, j in edges)}|"
            f"{'/'.join(point_text(point) for point in points)}"
        )

        for source_name, terminals, patterns in (
                ("M", mt, moser_patterns), ("G", gt, golomb_patterns)):
            for pattern_index, pattern in enumerate(patterns):
                word = graph.extension(terminals, pattern)
                if word is None:
                    raise ValueError(f"{source_name} projection restricted at placement {index}")
                projection_lines.append(
                    f"{index}|{source_name}|{pattern_index}|{''.join(map(str, word))}"
                )

        for i, j in combinations(range(len(points)), 2):
            if (i, j) in graph.edges:
                pair_status["unit_forced_different"] += 1
                continue
            equal_word = graph.extension((i, j), (0, 0))
            different_word = graph.extension((i, j), (0, 1))
            if equal_word is None or different_word is None:
                state = "forced_different" if equal_word is None else "forced_equal"
                raise ValueError(f"nonedge pair {i,j} is {state} at placement {index}")
            pair_status["nonunit_both_states"] += 1
            pair_lines.append(
                f"{index}|{i},{j}|{''.join(map(str, equal_word))}|"
                f"{''.join(map(str, different_word))}"
            )

    # The Moser spindle is not three-colourable by literal finite exhaustion.
    moser_three_colourings = 0
    for word in product(range(3), repeat=7):
        if all(word[i] != word[j] for i, j in moser_edges):
            moser_three_colourings += 1
    if moser_three_colourings:
        raise ValueError("Moser lower-bound control failed")

    return {
        "source_certificate_sha256": SOURCE_SHA256,
        "docking_points": len(docking),
        "docking_moser_neighbours_each": 2,
        "matched_distance_classes": len(set(distance_classes(docking)) & set(distance_classes(golomb))),
        "recipes": recipe_count,
        "placements": len(cohort),
        "moser_edges": len(moser_edges),
        "moser_canonical_patterns": len(moser_patterns),
        "golomb_edges": len(golomb_edges),
        "golomb_canonical_patterns": len(golomb_patterns),
        "order_histogram": {str(key): value for key, value in sorted(order_histogram.items())},
        "edge_histogram": {str(key): value for key, value in sorted(edge_histogram.items())},
        "collision_histogram": {str(key): value for key, value in sorted(collision_histogram.items())},
        "pair_status": dict(sorted(pair_status.items())),
        "component_projection_witnesses": len(projection_lines),
        "pair_witnesses": 2 * len(pair_lines),
        "moser_three_colourings": moser_three_colourings,
        "graph_stream_sha256": digest_lines(graph_lines),
        "component_projection_stream_sha256": digest_lines(projection_lines),
        "pair_witness_stream_sha256": digest_lines(pair_lines),
        "all_component_patterns_extend": True,
        "all_nonunit_pairs_admit_both_states": True,
        "all_graphs_exactly_four_chromatic": True,
        "record_improvement": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.check_expected:
        expected = json.loads(EXPECTED.read_text())
        if result != expected:
            print(json.dumps({"expected": expected, "observed": result}, indent=2, sort_keys=True))
            raise SystemExit("expected-result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
