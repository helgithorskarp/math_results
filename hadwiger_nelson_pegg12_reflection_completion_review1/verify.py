#!/usr/bin/env python3
"""Independent exact review of the Pegg UD12-2 reflection completion.

No target code is imported.  Field arithmetic uses actual square-free
radicands and conjugate norms; reflection uses twice-the-projection rather
than the target matrix formula.  Extension relations are decided by an
explicit bitset census of every labelled source colouring, not DSATUR.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_pegg12_reflection_completion_stop"
INPUT_HASHES = {
    "certificate.json": "0c8a7b2e2015f27adb69855a13768101ec2bf36166d1968c8b44d91b3628edea",
    "expected.json": "660590bc43073e81688164dec3b681eaacb013a928682edff111042db86acbb0",
    "model.py": "ba17b7bad40d2baf6fa0efb6c7064f211a008fa0dfd963d7225b90dcd352135e",
    "verify.py": "8af7692cd13245c94af8498b5b8620537a2005c0dcbfcc93fb98666627de53e5",
}
RADICANDS = (1, 3, 11, 33)
RINDEX = {radicand: index for index, radicand in enumerate(RADICANDS)}
Q = Fraction
F = tuple[Q, Q, Q, Q]
Point = tuple[F, F]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def rat(value=0):
    return (Q(value), Q(0), Q(0), Q(0))


ZERO = rat()
ONE = rat(1)
R3 = (Q(0), Q(1), Q(0), Q(0))
R11 = (Q(0), Q(0), Q(1), Q(0))
R33 = (Q(0), Q(0), Q(0), Q(1))


def fadd(left, right):
    return tuple(a + b for a, b in zip(left, right))


def fneg(value):
    return tuple(-x for x in value)


def fsub(left, right):
    return fadd(left, fneg(right))


def fscale(value, scalar):
    scalar = Q(scalar)
    return tuple(scalar * x for x in value)


def fmul(left, right):
    output = [Q(0), Q(0), Q(0), Q(0)]
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            common = gcd(RADICANDS[i], RADICANDS[j])
            radicand = RADICANDS[i] * RADICANDS[j] // (common * common)
            output[RINDEX[radicand]] += common * a * b
    return tuple(output)


def conjugate(value, sign3, sign11):
    return value[0], sign3 * value[1], sign11 * value[2], sign3 * sign11 * value[3]


def finverse(value):
    require(value != ZERO, "division by zero")
    numerator = fmul(
        fmul(conjugate(value, -1, 1), conjugate(value, 1, -1)),
        conjugate(value, -1, -1),
    )
    norm = fmul(value, numerator)
    require(norm[1:] == (Q(0), Q(0), Q(0)) and norm[0], "non-rational norm")
    return fscale(numerator, Q(1) / norm[0])


def fdiv(left, right):
    return fmul(left, finverse(right))


def padd(left, right):
    return fadd(left[0], right[0]), fadd(left[1], right[1])


def psub(left, right):
    return fsub(left[0], right[0]), fsub(left[1], right[1])


def pscale(point, scalar):
    return fmul(point[0], scalar), fmul(point[1], scalar)


def dot(left, right):
    return fadd(fmul(left[0], right[0]), fmul(left[1], right[1]))


def squared_distance(left, right):
    delta = psub(left, right)
    return dot(delta, delta)


def source_points():
    a = fscale(fsub(R33, rat(3)), Q(1, 12))
    y = fscale(fadd(R3, fscale(R11, 3)), Q(1, 12))
    s = fscale(R3, Q(1, 6))
    half = rat(Q(1, 2))
    return (
        (ZERO, ZERO),
        (ONE, ZERO),
        (fneg(a), y),
        (fadd(ONE, a), y),
        (fsub(half, a), fsub(y, s)),
        (fadd(half, a), fsub(y, s)),
        (half, fneg(s)),
        (fneg(a), fsub(y, fscale(s, 2))),
        (fadd(ONE, a), fsub(y, fscale(s, 2))),
        (fsub(half, a), fadd(y, s)),
        (fadd(half, a), fadd(y, s)),
        (half, s),
    )


def reflect(point, first, second):
    """Reflect by p + 2 proj_d(z-p) - (z-p)."""
    direction = psub(second, first)
    offset = psub(point, first)
    coefficient = fdiv(dot(offset, direction), dot(direction, direction))
    projected_twice = pscale(direction, fscale(coefficient, 2))
    return padd(first, psub(projected_twice, offset))


def complete_edges(points):
    return tuple(
        (left, right)
        for left, right in combinations(range(len(points)), 2)
        if squared_distance(points[left], points[right]) == ONE
    )


def reflected_union(axes):
    base = source_points()
    entries = [(point, (0, vertex)) for vertex, point in enumerate(base)]
    for copy, (left, right) in enumerate(axes, 1):
        entries.extend(
            (reflect(point, base[left], base[right]), (copy, vertex))
            for vertex, point in enumerate(base)
        )
    points = []
    labels = []
    index = {}
    raw_map = []
    for point, label in entries:
        if point not in index:
            index[point] = len(points)
            points.append(point)
            labels.append([])
        vertex = index[point]
        labels[vertex].append(label)
        raw_map.append(vertex)
    maps = tuple(tuple(raw_map[12 * copy : 12 * (copy + 1)]) for copy in range(len(axes) + 1))
    points = tuple(points)
    return points, complete_edges(points), tuple(tuple(row) for row in labels), maps


def edge_hash(edges):
    return sha256("".join(f"{u} {v}\n" for u, v in edges).encode()).hexdigest()


def coordinate_hash(points):
    rows = []
    for x, y in points:
        rows.append(" ".join(f"{value.numerator}/{value.denominator}" for value in x + y) + "\n")
    return sha256("".join(rows).encode()).hexdigest()


def check_word(word, order, edges, colours=4):
    require(type(word) is str and len(word) == order, "colour word length")
    require(all(char.isdigit() and 0 <= int(char) < colours for char in word), "colour symbol")
    values = tuple(map(int, word))
    require(all(values[u] != values[v] for u, v in edges), "monochromatic edge")
    return values


def canonical_words(order, edges, colours):
    """Enumerate restricted-growth words in vertex-label order."""
    earlier = [[] for _ in range(order)]
    for left, right in edges:
        earlier[right].append(left)
    word = [-1] * order
    word[0] = 0
    output = []

    def visit(vertex, maximum):
        if vertex == order:
            output.append("".join(map(str, word)))
            return
        for colour in range(min(colours - 1, maximum + 1) + 1):
            if all(word[neighbour] != colour for neighbour in earlier[vertex]):
                word[vertex] = colour
                visit(vertex + 1, max(maximum, colour))
        word[vertex] = -1

    visit(1, 0)
    return tuple(output)


def labelled_words(canonical):
    output = []
    for word in canonical:
        values = tuple(map(int, word))
        require(set(values) == {0, 1, 2, 3}, "source word does not use four colours")
        for permutation in permutations(range(4)):
            output.append(tuple(permutation[value] for value in values))
    require(len(output) == len(set(output)), "duplicate labelled source colouring")
    return tuple(output)


def colour_bitsets(words):
    bits = [[0] * 4 for _ in range(12)]
    for index, word in enumerate(words):
        flag = 1 << index
        for vertex, colour in enumerate(word):
            bits[vertex][colour] |= flag
    return bits, (1 << len(words)) - 1


def axis_data(axis, source_edge_list):
    points, edges, labels, maps = reflected_union((axis,))
    edge_set = set(edges)
    inherited = set()
    for left, right in source_edge_list:
        inherited.add(tuple(sorted((maps[0][left], maps[0][right]))))
        inherited.add(tuple(sorted((maps[1][left], maps[1][right]))))
    private = tuple(sorted(edge_set - inherited))
    overlaps = tuple(sorted(
        (left, right)
        for left in range(12)
        for right in range(12)
        if maps[0][left] == maps[1][right]
    ))
    cross_by_edge = defaultdict(list)
    for left in range(12):
        for right in range(12):
            physical = tuple(sorted((maps[0][left], maps[1][right])))
            if physical[0] != physical[1] and physical in edge_set:
                cross_by_edge[physical].append((left, right))
    return {
        "axis": axis,
        "points": points,
        "edges": edges,
        "labels": labels,
        "maps": maps,
        "inherited": inherited,
        "private": private,
        "overlaps": overlaps,
        "cross_by_edge": {edge: tuple(pairs) for edge, pairs in cross_by_edge.items()},
    }


def compatible_bits(data, base_word, bitsets, all_bits, removed_edges=()):
    values = tuple(map(int, base_word)) if isinstance(base_word, str) else base_word
    answer = all_bits
    for left, right in data["overlaps"]:
        answer &= bitsets[right][values[left]]
    removed = set(removed_edges)
    for physical, pairs in data["cross_by_edge"].items():
        if physical in removed:
            continue
        for left, right in pairs:
            answer &= all_bits ^ bitsets[right][values[left]]
    return answer


def extension_from_bit(data, base_word, reflected_word, removed_edges=()):
    colours = [-1] * len(data["points"])
    for old, physical in enumerate(data["maps"][0]):
        colours[physical] = int(base_word[old])
    for old, physical in enumerate(data["maps"][1]):
        value = reflected_word[old]
        require(colours[physical] in (-1, value), "overlap colour conflict")
        colours[physical] = value
    removed = set(removed_edges)
    require(all(colours[u] != colours[v] for u, v in data["edges"] if (u, v) not in removed),
            "bad extension")
    return tuple(colours)


def first_extension(data, base_word, labelled, bitsets, all_bits, removed_edges=()):
    candidates = compatible_bits(data, base_word, bitsets, all_bits, removed_edges)
    if not candidates:
        return None
    index = (candidates & -candidates).bit_length() - 1
    return extension_from_bit(data, base_word, labelled[index], removed_edges)


def connected_after(order, edges, removed):
    removed = set(removed)
    vertices = [vertex for vertex in range(order) if vertex not in removed]
    if len(vertices) <= 1:
        return True
    adjacency = [[] for _ in range(order)]
    for left, right in edges:
        if left not in removed and right not in removed:
            adjacency[left].append(right)
            adjacency[right].append(left)
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen) == len(vertices)


def three_cuts(order, edges):
    require(all(connected_after(order, edges, cut) for size in (1, 2) for cut in combinations(range(order), size)),
            "connectivity below three")
    cuts = tuple(cut for cut in combinations(range(order), 3) if not connected_after(order, edges, cut))
    require(cuts, "no three-cut")
    return cuts


def digest_lines(rows):
    return sha256("".join(rows).encode()).hexdigest()


def verify(certificate=None):
    for name, expected_hash in INPUT_HASHES.items():
        require(file_hash(TARGET / name) == expected_hash, "unexpected target input: " + name)
    if certificate is None:
        certificate = json.loads((TARGET / "certificate.json").read_text())
    target_expected = json.loads((TARGET / "expected.json").read_text())
    require(certificate.get("schema") == "pegg-ud12-reflection-v1", "certificate schema")
    selected_axes = tuple(map(tuple, certificate["full_axes"]))
    require(len(selected_axes) == len(set(selected_axes)) == 18, "selected axes")

    source = source_points()
    require(len(source) == len(set(source)) == 12, "source points")
    source_edge_list = complete_edges(source)
    require(len(source_edge_list) == 21, "source edge census")
    three_words = canonical_words(12, source_edge_list, 3)
    source_words = canonical_words(12, source_edge_list, 4)
    require(not three_words and len(source_words) == 756, "source chromatic census")
    labelled = labelled_words(source_words)
    require(len(labelled) == 18144, "labelled source colouring count")
    bitsets, all_bits = colour_bitsets(labelled)

    single_axis = tuple(certificate["single_axis"])
    require(single_axis == (0, 6), "single axis")
    single = axis_data(single_axis, source_edge_list)
    surviving = tuple(
        word for word in source_words if compatible_bits(single, word, bitsets, all_bits)
    )
    require(len(single["points"]) == 22 and len(single["edges"]) == 50, "single census")
    require(single["overlaps"] == ((0, 0), (6, 6)), "single overlaps")
    require(len(single["private"]) == 8, "single private contacts")
    require(len(surviving) == 620, "single surviving relation")
    blocked_word = certificate["single_blocked_source_word"]
    surviving_word = certificate["single_surviving_source_word"]
    require(blocked_word in source_words and blocked_word not in surviving, "blocked fixture")
    require(surviving_word in surviving, "surviving fixture")
    require(first_extension(single, blocked_word, labelled, bitsets, all_bits) is None, "blocked input extends")
    generated_extension = first_extension(single, surviving_word, labelled, bitsets, all_bits)
    require(generated_extension is not None, "surviving input blocked")
    check_word(certificate["single_extension_word"], 22, single["edges"])
    require(certificate["single_extension_word"][:12] == surviving_word, "extension prefix")
    check_word(certificate["single_blocked_word_without_private_edges"], 22, tuple(sorted(single["inherited"])))
    require(certificate["single_blocked_word_without_private_edges"][:12] == blocked_word,
            "private-deletion prefix")

    critical = tuple(
        edge
        for edge in single["private"]
        if first_extension(single, blocked_word, labelled, bitsets, all_bits, (edge,)) is not None
    )
    require(len(critical) == 3, "critical private contacts")
    cuts = three_cuts(22, single["edges"])
    require(cuts[0] == (2, 8, 11), "first three-cut")

    # Full selector audit: all 66 source-pair reflection axes, not just the
    # 18 axes committed to the completion.
    axis_rows = []
    positive_axes = []
    axis_histogram = Counter()
    selected_relation_rows = []
    selected_private_histogram = Counter()
    for axis in combinations(range(12), 2):
        data = axis_data(axis, source_edge_list)
        axis_surviving = tuple(
            word for word in source_words if compatible_bits(data, word, bitsets, all_bits)
        )
        blocked = len(source_words) - len(axis_surviving)
        collisions = sum(len(labels) > 1 for labels in data["labels"])
        key = (len(data["points"]), len(data["private"]), blocked, collisions)
        axis_histogram[key] += 1
        axis_rows.append(f"{axis[0]} {axis[1]} {key[0]} {len(data['edges'])} {key[1]} {key[2]} {key[3]}\n")
        if data["private"] and blocked:
            positive_axes.append(axis)
        if axis in selected_axes:
            require(blocked == 136 and data["private"], "selected axis relation")
            selected_private_histogram[len(data["private"])] += 1
            selected_relation_rows.extend(f"{axis[0]} {axis[1]} {word}\n" for word in axis_surviving)
    require(tuple(positive_axes) == selected_axes, "selected axes are not the exact private-loss set")
    require(selected_private_histogram == {4: 6, 8: 12}, "selected private histogram")
    selected_relation_hash = digest_lines(selected_relation_rows)
    require(selected_relation_hash == target_expected["full_completion"]["axis_surviving_relation_sha256"],
            "selected relation hash")

    full_points, full_edges, full_labels, full_maps = reflected_union(selected_axes)
    require(len(full_points) == 165 and len(full_edges) == 597, "full completion census")
    full_word = certificate["full_four_word"]
    check_word(full_word, 165, full_edges)
    require(not three_words, "source unexpectedly three-colourable")
    collision_histogram = Counter(len(labels) for labels in full_labels if len(labels) > 1)
    require(sum(collision_histogram.values()) == 27, "full collision classes")

    # Reproduce all target stream hashes from the independent field model.
    require(coordinate_hash(source) == target_expected["source"]["coordinate_sha256"], "source coordinate hash")
    require(edge_hash(source_edge_list) == target_expected["source"]["edge_sha256"], "source edge hash")
    require(coordinate_hash(single["points"]) == target_expected["single_axis"]["coordinate_sha256"],
            "single coordinate hash")
    require(edge_hash(single["edges"]) == target_expected["single_axis"]["edge_sha256"], "single edge hash")
    require(coordinate_hash(full_points) == target_expected["full_completion"]["coordinate_sha256"],
            "full coordinate hash")
    require(edge_hash(full_edges) == target_expected["full_completion"]["edge_sha256"], "full edge hash")

    histogram_rows = [
        {"points": key[0], "private_edges": key[1], "blocked_inputs": key[2],
         "collision_classes": key[3], "axes": count}
        for key, count in sorted(axis_histogram.items())
    ]
    result = {
        "checker": "independent radicand/conjugate-norm and labelled-colouring census",
        "target_code_imported": False,
        "source": {
            "points": len(source),
            "complete_unit_edges": len(source_edge_list),
            "canonical_three_colourings": len(three_words),
            "canonical_four_colourings": len(source_words),
            "labelled_four_colourings": len(labelled),
            "coordinate_sha256": coordinate_hash(source),
            "edge_sha256": edge_hash(source_edge_list),
        },
        "single_axis": {
            "axis": list(single_axis),
            "points": len(single["points"]),
            "complete_unit_edges": len(single["edges"]),
            "overlap_pairs": [list(pair) for pair in single["overlaps"]],
            "private_edges": [list(edge) for edge in single["private"]],
            "critical_private_edges": [list(edge) for edge in critical],
            "blocked_inputs": len(source_words) - len(surviving),
            "surviving_inputs": len(surviving),
            "surviving_words_sha256": digest_lines(word + "\n" for word in surviving),
            "generated_extension_sha256": sha256("".join(map(str, generated_extension)).encode()).hexdigest(),
            "vertex_connectivity": 3,
            "three_cuts": len(cuts),
            "three_cuts_sha256": digest_lines(" ".join(map(str, cut)) + "\n" for cut in cuts),
            "coordinate_sha256": coordinate_hash(single["points"]),
            "edge_sha256": edge_hash(single["edges"]),
        },
        "all_axes": {
            "checked_axes": len(tuple(combinations(range(12), 2))),
            "private_contact_and_loss_axes": len(positive_axes),
            "selected_axes_exact": True,
            "census": histogram_rows,
            "census_sha256": digest_lines(axis_rows),
        },
        "full_completion": {
            "axes": len(selected_axes),
            "points": len(full_points),
            "complete_unit_edges": len(full_edges),
            "collision_classes": sum(collision_histogram.values()),
            "collision_size_histogram": {str(size): count for size, count in sorted(collision_histogram.items())},
            "selected_relation_sha256": selected_relation_hash,
            "coordinate_sha256": coordinate_hash(full_points),
            "edge_sha256": edge_hash(full_edges),
            "four_colour_word_sha256": sha256(full_word.encode()).hexdigest(),
            "chromatic_number": 4,
        },
        "verdict": "ACCEPT_WITH_FIXED_COMPLETION_SCOPE",
        "record_candidate": False,
        "scope": "one exact Pegg12 realization, its 66 source-pair reflection axes, and the fixed union of the 18 private-contact loss axes",
    }
    return result


def main():
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
