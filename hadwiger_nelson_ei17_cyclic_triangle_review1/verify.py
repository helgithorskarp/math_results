#!/usr/bin/env python3
"""Independent exact review of the cyclic EI17 three-copy stopping theorem.

This file deliberately imports neither target code nor the EI17 source code.
It reconstructs the root box with Fraction intervals, builds all frames with
an independent interval type, enumerates fixed-edge labelled colourings, and
solves the contactful upper graphs with a separate backtracker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_ei17_cyclic_triangle_full_input_stop"
SOURCE = ROOT / "hadwiger_nelson_ei17_common_pair"
EXPECTED = HERE / "EXPECTED.json"
PINS = {
    TARGET / "verify.py": "23dada3c84cf5574b5c78965d0f1df333bed1a67f3ea0c61ca407631070d74bc",
    TARGET / "controls.py": "a177fcafd4027a9aa8bcce230af7b490b6cb072f4f283aeafa0a892086dac9c8",
    TARGET / "EXPECTED.json": "7f767c0b83c1d8ff4ba9be13749b1486c60bf8e473e00c85c30c7c3c70442b30",
    SOURCE / "seed_edges.json": "b77a3a242467f2c1ed3f047914492e70a0da9cbe6ca8234941c8dd008e25e450",
    SOURCE / "seed_midpoint.json": "fb712ad09168fa51814556641f31280acc8ad1e71a17a9878d1cfd55eeb96565",
}
FIXED = {10: (Q(-1), Q(0)), 16: (Q(0), Q(0))}
RADIUS = Q(1, 10**18)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __post_init__(self):
        require(isinstance(self.lo, Q) and isinstance(self.hi, Q)
                and self.lo <= self.hi, "invalid interval")

    @classmethod
    def point(cls, value):
        value = Q(value)
        return cls(value, value)

    def __add__(self, other):
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        values = [x*y for x in (self.lo, self.hi)
                  for y in (other.lo, other.hi)]
        return Interval(min(values), max(values))

    def scale(self, value):
        value = Q(value)
        values = (value*self.lo, value*self.hi)
        return Interval(min(values), max(values))

    def square(self):
        upper = max(self.lo*self.lo, self.hi*self.hi)
        lower = Q(0) if self.lo <= 0 <= self.hi else min(
            self.lo*self.lo, self.hi*self.hi)
        return Interval(lower, upper)

    def contains(self, value):
        value = Q(value)
        return self.lo <= value <= self.hi

    def maxabs(self):
        return max(abs(self.lo), abs(self.hi))


def iadd(a, b):
    return a + b


def sqrt_integer_interval(value, decimal_digits=70):
    scale = 10**decimal_digits
    lower_numerator = isqrt(value*scale*scale)
    lower = Q(lower_numerator, scale)
    upper = Q(lower_numerator + 1, scale)
    require(lower*lower <= value <= upper*upper, "square-root bracket")
    return Interval(lower, upper)


def cadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def csub(a, b):
    return a[0] - b[0], a[1] - b[1]


def cmul(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def cconj(a):
    return a[0], -a[1]


def squared_distance(a, b):
    difference = csub(a, b)
    return difference[0].square() + difference[1].square()


def exact_point(x, y):
    return Interval.point(x), Interval.point(y)


def inverse(matrix):
    """Definition-level exact Gauss-Jordan inversion."""
    n = len(matrix)
    work = [list(row) + [Q(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for column in range(n):
        pivot_row = next((row for row in range(column, n)
                          if work[row][column]), None)
        require(pivot_row is not None, "singular midpoint Jacobian")
        work[column], work[pivot_row] = work[pivot_row], work[column]
        pivot = work[column][column]
        work[column] = [entry/pivot for entry in work[column]]
        for row in range(n):
            if row != column and work[row][column]:
                multiplier = work[row][column]
                work[row] = [x - multiplier*y
                             for x, y in zip(work[row], work[column])]
    return [row[n:] for row in work]


def certify_source(midpoint, edges):
    require(len(midpoint) == 17 and all(len(row) == 2 for row in midpoint),
            "source midpoint shape")
    require(midpoint[10] == FIXED[10] and midpoint[16] == FIXED[16],
            "source fixed points")
    require(edges == sorted(set(edges)) and len(edges) == 31
            and (10, 16) in edges, "source edge list")
    free = [(vertex, axis) for vertex in range(17) if vertex not in FIXED
            for axis in (0, 1)]
    at = {coordinate: index for index, coordinate in enumerate(free)}
    equations = [edge for edge in edges if edge != (10, 16)]
    require(len(equations) == len(free) == 30, "source square system")

    residual = []
    jacobian = []
    for a, b in equations:
        difference = [midpoint[a][axis] - midpoint[b][axis]
                      for axis in (0, 1)]
        residual.append(sum(value*value for value in difference) - 1)
        row = [Q(0)]*30
        for axis in (0, 1):
            if (a, axis) in at:
                row[at[a, axis]] = 2*difference[axis]
            if (b, axis) in at:
                row[at[b, axis]] = -2*difference[axis]
        jacobian.append(row)
    approximate_inverse = inverse(jacobian)
    for i in range(30):
        for j in range(30):
            require(sum(approximate_inverse[i][k]*jacobian[k][j]
                        for k in range(30)) == (i == j),
                    "source inverse identity")

    boxes = []
    for vertex, point in enumerate(midpoint):
        radius = Q(0) if vertex in FIXED else RADIUS
        boxes.append(tuple(Interval(value-radius, value+radius)
                           for value in point))
    interval_jacobian = []
    for a, b in equations:
        entries = {}
        for axis in (0, 1):
            difference = boxes[a][axis] - boxes[b][axis]
            if (a, axis) in at:
                entries[at[a, axis]] = difference.scale(2)
            if (b, axis) in at:
                entries[at[b, axis]] = difference.scale(-2)
        interval_jacobian.append(entries)

    contraction = Q(0)
    for i in range(30):
        row = [Interval.point(i == j) for j in range(30)]
        for k, entries in enumerate(interval_jacobian):
            coefficient = approximate_inverse[i][k]
            if coefficient:
                for j, value in entries.items():
                    row[j] = row[j] + (-value.scale(coefficient))
        contraction = max(contraction, sum(value.maxabs() for value in row))
    image = [sum(approximate_inverse[i][k]*residual[k] for k in range(30))
             for i in range(30)]
    displacement = max(map(abs, image))
    self_map = displacement + contraction*RADIUS
    require(contraction < 1 and self_map < RADIUS,
            "source contraction or self-map")

    edge_set = set(edges)
    separation = None
    nonedge_gap = None
    for a, b in combinations(range(17), 2):
        distance2 = squared_distance(boxes[a], boxes[b])
        require(distance2.lo > 0, f"source collision: {(a, b)}")
        separation = distance2.lo if separation is None else min(
            separation, distance2.lo)
        if (a, b) not in edge_set:
            require(not distance2.contains(1), f"source nonedge: {(a, b)}")
            gap = 1-distance2.hi if distance2.hi < 1 else distance2.lo-1
            nonedge_gap = gap if nonedge_gap is None else min(nonedge_gap, gap)
    require(not any((a, b) in edge_set and (a, c) in edge_set
                    and (b, c) in edge_set
                    for a, b, c in combinations(range(17), 3)),
            "source triangle")
    return boxes, {
        "root_unique_in_box": True,
        "radius": str(RADIUS),
        "contraction_upper_units_1e_minus_12": ceil_scaled(contraction, 10**12),
        "displacement_upper_units_1e_minus_24": ceil_scaled(displacement, 10**24),
        "self_map_upper_units_1e_minus_24": ceil_scaled(self_map, 10**24),
        "squared_separation_lower_units_1e_minus_12": floor_scaled(
            separation, 10**12),
        "nonedge_squared_unit_gap_lower_units_1e_minus_12": floor_scaled(
            nonedge_gap, 10**12),
    }


def cyclic_map(point, zeta):
    return cadd(exact_point(1, 0), cmul(zeta, point))


def source_frame(points, edge, reverse, reflected):
    i, j = edge[::-1] if reverse else edge
    delta = csub(points[j], points[i])
    multiplier = delta if reflected else cconj(delta)
    result = []
    for point in points:
        local = csub(point, points[i])
        if reflected:
            local = cconj(local)
        result.append(cmul(multiplier, local))
    result[i], result[j] = exact_point(0, 0), exact_point(1, 0)
    return (i, j), result


def cyclic_copies(points, edge, reverse, reflected, sqrt3):
    anchor, first = source_frame(points, edge, reverse, reflected)
    half = Interval.point(Q(1, 2))
    zeta = (-half, sqrt3*half)
    triangle = (exact_point(0, 0), exact_point(1, 0),
                (half, sqrt3*half))
    second = [cyclic_map(point, zeta) for point in first]
    third = [cyclic_map(point, zeta) for point in second]
    i, j = anchor
    first[i], first[j] = triangle[0], triangle[1]
    second[i], second[j] = triangle[1], triangle[2]
    third[i], third[j] = triangle[2], triangle[0]
    return anchor, (tuple(first), tuple(second), tuple(third))


def interval_gap_from_one(value):
    if value.contains(1):
        return None
    return 1-value.hi if value.hi < 1 else value.lo-1


def build_graph(points, source_edges, edge, reverse, reflected, sqrt3):
    anchor, copies = cyclic_copies(points, edge, reverse, reflected, sqrt3)
    i, j = anchor
    labels = [(copy, vertex) for copy in range(3) for vertex in range(17)]
    boxes = [copies[copy][vertex] for copy, vertex in labels]
    special = {
        (0, i): "A", (2, j): "A",
        (0, j): "B", (1, i): "B",
        (1, j): "C", (2, i): "C",
    }
    keys = [special.get(label, label) for label in labels]
    names = []
    for key in keys:
        if key not in names:
            names.append(key)
    group_of = tuple(names.index(key) for key in keys)
    groups = tuple(tuple(index for index, group in enumerate(group_of)
                         if group == group_number)
                   for group_number in range(len(names)))
    require(len(groups) == 48 and sorted(map(len, groups)) == [1]*45+[2]*3,
            "declared cyclic collision pattern")

    collision_gap = None
    for left, right in combinations(range(51), 2):
        if group_of[left] == group_of[right]:
            continue
        gaps = []
        for x, y in zip(boxes[left], boxes[right]):
            if x.hi < y.lo:
                gaps.append(y.lo-x.hi)
            elif y.hi < x.lo:
                gaps.append(x.lo-y.hi)
        require(gaps, f"undeclared collision not excluded: {(left, right)}")
        local = max(gaps)
        collision_gap = local if collision_gap is None else min(
            collision_gap, local)

    upper_edges = set()
    unit_gap = None
    for ga, gb in combinations(range(48), 2):
        possible = False
        excluded_gaps = []
        for la in groups[ga]:
            for lb in groups[gb]:
                gap = interval_gap_from_one(squared_distance(boxes[la], boxes[lb]))
                if gap is None:
                    possible = True
                else:
                    excluded_gaps.append(gap)
        if possible:
            upper_edges.add((ga, gb))
        else:
            local = min(excluded_gaps)
            unit_gap = local if unit_gap is None else min(unit_gap, local)

    inherited = set()
    addresses = []
    for copy in range(3):
        address = tuple(group_of[17*copy + vertex] for vertex in range(17))
        require(len(set(address)) == 17, "internal source collision")
        addresses.append(address)
        for a, b in source_edges:
            physical = tuple(sorted((address[a], address[b])))
            inherited.add(physical)
            require(physical in upper_edges, "inherited unit edge absent")
    extras = tuple(sorted(upper_edges-inherited))
    return {
        "source_edge": edge,
        "anchor": anchor,
        "reverse": reverse,
        "reflected": reflected,
        "groups": groups,
        "addresses": tuple(addresses),
        "edges": tuple(sorted(upper_edges)),
        "inherited": tuple(sorted(inherited)),
        "extras": extras,
        "collision_gap": collision_gap,
        "unit_gap": unit_gap,
    }


def adjacency(vertex_count, edges):
    result = [set() for _ in range(vertex_count)]
    for a, b in edges:
        result[a].add(b)
        result[b].add(a)
    return result


def component_count(neighbours, omitted_vertices=frozenset(), omitted_edge=None):
    seen = set()
    answer = 0
    for start in range(len(neighbours)):
        if start in omitted_vertices or start in seen:
            continue
        answer += 1
        stack = [start]
        seen.add(start)
        while stack:
            vertex = stack.pop()
            for other in neighbours[vertex]:
                if other in omitted_vertices or other in seen:
                    continue
                if omitted_edge == tuple(sorted((vertex, other))):
                    continue
                seen.add(other)
                stack.append(other)
    return answer


def structure_record(graph):
    neighbours = adjacency(48, graph["inherited"])
    require(component_count(neighbours) == 1, "disconnected inherited union")
    articulations = [v for v in range(48)
                     if component_count(neighbours, frozenset({v})) > 1]
    bridges = [edge for edge in graph["inherited"]
               if component_count(neighbours, omitted_edge=edge) > 1]
    require(not articulations and not bridges, "separable inherited union")
    two_cuts = tuple(pair for pair in combinations(range(48), 2)
                     if component_count(neighbours, frozenset(pair)) > 1)
    i, j = graph["anchor"]
    triangle = tuple(sorted((graph["addresses"][0][i],
                             graph["addresses"][0][j],
                             graph["addresses"][1][j])))
    require(two_cuts == tuple(combinations(triangle, 2)),
            "two-cuts are not exactly the anchor pairs")
    return min(map(len, neighbours)), len(two_cuts)


def three_colour_search(edges):
    neighbours = adjacency(17, edges)
    order = [v for v in range(17) if v not in FIXED]
    colour = [-1]*17
    colour[10], colour[16] = 0, 1
    nodes = 0

    def visit(index):
        nonlocal nodes
        nodes += 1
        if index == len(order):
            return True
        vertex = order[index]
        forbidden = {colour[w] for w in neighbours[vertex] if colour[w] >= 0}
        for value in range(3):
            if value not in forbidden:
                colour[vertex] = value
                if visit(index+1):
                    return True
        colour[vertex] = -1
        return False

    return visit(0), nodes


def fixed_edge_four_colourings(edges):
    """All labelled words with c(10)=0,c(16)=1; no orbit canonicalizer."""
    neighbours = adjacency(17, edges)
    order = [v for v in range(17) if v not in FIXED]
    colour = [-1]*17
    colour[10], colour[16] = 0, 1
    words = []
    nodes = 0

    def visit(index):
        nonlocal nodes
        nodes += 1
        if index == len(order):
            require(len(set(colour)) == 4, "source used fewer than four colours")
            words.append(tuple(colour))
            return
        vertex = order[index]
        forbidden = {colour[w] for w in neighbours[vertex] if colour[w] >= 0}
        for value in range(4):
            if value not in forbidden:
                colour[vertex] = value
                visit(index+1)
        colour[vertex] = -1

    visit(0)
    return tuple(words), nodes


def colour_permutation(source_a, source_b, target_a, target_b):
    require(source_a != source_b and target_a != target_b, "permutation inputs")
    mapping = {source_a: target_a, source_b: target_b}
    unused_source = [c for c in range(4) if c not in mapping]
    unused_target = [c for c in range(4) if c not in mapping.values()]
    mapping.update(zip(unused_source, unused_target))
    answer = tuple(mapping[c] for c in range(4))
    require(sorted(answer) == list(range(4)), "not a colour permutation")
    return answer


def plain_symbolic_check(graph):
    require(graph["edges"] == graph["inherited"], "plain frame has extra edge")
    for a in range(4):
        for b in range(4):
            if a == b:
                continue
            c = next(value for value in range(4) if value not in (a, b))
            first = colour_permutation(a, b, b, c)
            second = colour_permutation(a, b, c, a)
            require((first[a], first[b], second[a], second[b]) == (b, c, c, a),
                    "cyclic anchor permutation")
    return 12


def solve_domains(domains, neighbours):
    assigned = [-1]*len(domains)

    def visit(left):
        if not left:
            return tuple(assigned)
        choices = []
        for vertex in left:
            mask = domains[vertex]
            for other in neighbours[vertex]:
                if assigned[other] >= 0:
                    mask &= ~(1 << assigned[other])
            if not mask:
                return None
            choices.append((mask.bit_count(), -len(neighbours[vertex]), vertex, mask))
        _, _, vertex, mask = min(choices)
        while mask:
            bit = mask & -mask
            mask -= bit
            assigned[vertex] = bit.bit_length()-1
            answer = visit(left-{vertex})
            if answer is not None:
                return answer
        assigned[vertex] = -1
        return None

    return visit(set(range(len(domains))))


def contactful_extensions(graph, words):
    base = graph["addresses"][0]
    base_at = {physical: source for source, physical in enumerate(base)}
    new_vertices = tuple(v for v in range(48) if v not in base_at)
    new_at = {physical: local for local, physical in enumerate(new_vertices)}
    neighbours = [set() for _ in new_vertices]
    base_neighbours = [[] for _ in new_vertices]
    for a, b in graph["edges"]:
        for left, right in ((a, b), (b, a)):
            if left in new_at:
                if right in new_at:
                    neighbours[new_at[left]].add(new_at[right])
                else:
                    base_neighbours[new_at[left]].append(base_at[right])

    states = {}
    state_stream = hashlib.sha256()
    for word in words:
        domains = []
        for vertices in base_neighbours:
            forbidden = 0
            for vertex in vertices:
                forbidden |= 1 << word[vertex]
            domains.append(15 & ~forbidden)
        domains = tuple(domains)
        require(all(domains), "empty domain from source word")
        state_stream.update(bytes(word) + b"|" + bytes(domains) + b"\n")
        if domains not in states:
            answer = solve_domains(domains, neighbours)
            require(answer is not None, "source domain state does not extend")
            require(all(domains[v] & (1 << answer[v]) for v in range(len(answer))),
                    "domain witness")
            require(all(answer[v] != answer[w] for v in range(len(answer))
                        for w in neighbours[v] if v < w), "new-edge witness")
            states[domains] = answer
    witness_stream = hashlib.sha256()
    for domains in sorted(states):
        witness_stream.update(bytes(domains) + b"|" + bytes(states[domains]) + b"\n")
    return len(words), len(states), state_stream.hexdigest(), witness_stream.hexdigest()


def ceil_scaled(value, scale):
    return -((-value.numerator*scale)//value.denominator)


def floor_scaled(value, scale):
    return value.numerator*scale//value.denominator


def verify(check_hashes=True):
    if check_hashes:
        for path, expected in PINS.items():
            require(digest(path) == expected, f"changed reviewed input: {path.name}")
    target_expected = json.loads((TARGET / "EXPECTED.json").read_text())
    midpoint = [tuple(Q(value) for value in row)
                for row in json.loads((SOURCE / "seed_midpoint.json").read_text())]
    source_edges = sorted(tuple(edge) for edge in
                          json.loads((SOURCE / "seed_edges.json").read_text()))
    points, source_root = certify_source(midpoint, source_edges)

    three_colourable, three_nodes = three_colour_search(source_edges)
    require(not three_colourable, "source is three-colourable")
    colourings, four_nodes = fixed_edge_four_colourings(source_edges)
    require(len(colourings) == 170176, "fixed-edge four-colouring count")
    require(len(colourings)//2 ==
            target_expected["source_colour_orbits_modulo_global_permutation"],
            "source orbit count")
    colour_stream = hashlib.sha256(b"".join(bytes(word)+b"\n" for word in colourings))

    sqrt3 = sqrt_integer_interval(3)
    graphs = [build_graph(points, source_edges, edge, reverse, reflected, sqrt3)
              for edge in source_edges
              for reverse in (False, True)
              for reflected in (False, True)]
    require(len(graphs) == 124, "frame count")
    edge_histogram = Counter(len(graph["edges"]) for graph in graphs)
    extra_histogram = Counter(len(graph["extras"]) for graph in graphs)
    require(edge_histogram == {93: 116, 96: 8}, "upper-edge census")
    require(extra_histogram == {0: 116, 3: 8}, "extra-edge census")
    contactful = [graph for graph in graphs if graph["extras"]]
    plain = [graph for graph in graphs if not graph["extras"]]

    geometry_stream = hashlib.sha256()
    collision_gap = None
    unit_gap = None
    structure_histogram = Counter()
    for number, graph in enumerate(graphs):
        geometry_stream.update(f"F {number}\n".encode())
        for group in graph["groups"]:
            geometry_stream.update(("G " + " ".join(map(str, group)) + "\n").encode())
        for a, b in graph["edges"]:
            geometry_stream.update(f"E {a} {b}\n".encode())
        collision_gap = graph["collision_gap"] if collision_gap is None else min(
            collision_gap, graph["collision_gap"])
        unit_gap = graph["unit_gap"] if unit_gap is None else min(
            unit_gap, graph["unit_gap"])
        structure_histogram[structure_record(graph)] += 1
    require(geometry_stream.hexdigest() == target_expected["geometry_stream_sha256"],
            "entry-level geometry stream differs from target")

    symbolic_states = sum(plain_symbolic_check(graph) for graph in plain)
    contact_records = []
    for graph in contactful:
        checked, states, state_hash, witness_hash = contactful_extensions(
            graph, colourings)
        contact_records.append({
            "source_edge": list(graph["source_edge"]),
            "anchor_order": list(graph["anchor"]),
            "reverse": graph["reverse"],
            "reflected": graph["reflected"],
            "extra_edges": [list(edge) for edge in graph["extras"]],
            "fixed_edge_labelled_source_colourings": checked,
            "distinct_domain_states": states,
            "source_domain_stream_sha256": state_hash,
            "state_witness_stream_sha256": witness_hash,
        })

    return {
        "status": "ACCEPT_WITH_STRICT_FIXED_SOURCE_AND_CYCLIC_FRAME_LIMITATION",
        "reviewed_target_commit": "abadf3d5f33005152f588fe0a2e2a52cf0d204eb",
        "reviewed_target_verify_sha256": digest(TARGET / "verify.py"),
        "source_root": source_root,
        "source_three_colour_search_nodes": three_nodes,
        "source_fixed_edge_four_colour_search_nodes": four_nodes,
        "source_fixed_edge_labelled_four_colourings": len(colourings),
        "source_colour_orbits_modulo_global_permutation": len(colourings)//2,
        "source_fixed_edge_colour_stream_sha256": colour_stream.hexdigest(),
        "labelled_frames": len(graphs),
        "physical_points_each": 48,
        "conservative_edge_count_histogram": {str(k): edge_histogram[k]
                                               for k in sorted(edge_histogram)},
        "conservative_extra_edge_histogram": {str(k): extra_histogram[k]
                                                for k in sorted(extra_histogram)},
        "contactful_frames": len(contactful),
        "plain_frames": len(plain),
        "geometry_stream_sha256": geometry_stream.hexdigest(),
        "geometry_stream_matches_target": True,
        "coordinate_separation_lower_units_1e_minus_12": floor_scaled(
            collision_gap, 10**12),
        "squared_unit_exclusion_gap_lower_units_1e_minus_12": floor_scaled(
            unit_gap, 10**12),
        "inherited_minimum_degree_two_cut_histogram": {
            f"{minimum_degree},{two_cuts}": count
            for (minimum_degree, two_cuts), count in sorted(structure_histogram.items())
        },
        "plain_symbolic_ordered_colour_pair_checks": symbolic_states,
        "contactful_fixed_edge_source_frame_checks": len(contactful)*len(colourings),
        "contactful_relation_records": contact_records,
        "all_complete_source_colourings_extend": True,
        "all_actual_complete_physical_graphs_chromatic_number": 4,
        "record_candidate": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.check_expected:
        require(result == json.loads(EXPECTED.read_text()), "EXPECTED mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
