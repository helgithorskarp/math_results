#!/usr/bin/env python3
"""Independent exact review of the E477 maximum-translation union.

The main geometry uses the two integer equations obtained by expanding the
coordinates directly.  It imports no target code.  Translation overlaps are
recomputed by explicit set intersections, not difference multiplicities.
"""

from collections import Counter, defaultdict
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from json import dumps, loads
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_e477_core_translation_union_stop"
SOURCE = HERE.parent / "hadwiger_nelson_overlapping_forcing_seed"
TARGET_COMMIT = "621db0ad3b4be24ba7c76e1cbd7d57026d5b7669"
TARGET_HASHES = {
    "certificate.json": "3f1d0f52816eead604c1c2370c347dfe7bd56e25ba9c8fab71bf2daba82f9aad",
    "EXPECTED.json": "3f723bfffafd65d532914a813e335af5cbeff71b3dd4624ce3914bc907dd1bea",
    "PROOF.md": "3bf723d9fde69f4608d313e4637e833e87c0afa337300e36f20c7bb1f4b739ab",
    "README.md": "00e9ce2fde74226029e7940363b0f05fe8b56a46ad40b59155cdc1bd82c429af",
    "controls.py": "ec7ad288a71f3ef6b8b7630900da93cbf1861d73527376fdcfcf1945b7cfca8f",
    "verify.py": "4a713d9d46ea718e08dfa4a8bbeee920b0c9e5290e0db8554cd986f54eb67488",
}
SOURCE_HASHES = {
    "certificate.json": "3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237",
    "mandatory_vertices.json": "f0cea2d38b8d43e22bf82cba23ee65fb971cd031918015c9061ee499485cac2d",
}
ZERO = (0, 0, 0, 0)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def sub(left, right):
    return tuple(a - b for a, b in zip(left, right))


def neg(value):
    return tuple(-entry for entry in value)


def squared_distance_coefficients(left, right):
    """Return numerator coefficients (rational, sqrt(33)) at scale 36^2.

    If the row difference is (a,b,c,d), the squared distance is
    (3a^2+11b^2+c^2+33d^2 + 2(ab+cd)sqrt(33))/1296.
    The returned second entry omits the harmless factor two.
    """
    a, b, c, d = sub(left, right)
    return 3 * a * a + 11 * b * b + c * c + 33 * d * d, a * b + c * d


def unit(left, right):
    return squared_distance_coefficients(left, right) == (1296, 0)


def stream_hash(lines):
    return sha256("".join(lines).encode()).hexdigest()


def canonical_colourings(order, edges, colour_count):
    earlier = [[] for _ in range(order)]
    for left, right in edges:
        require(0 <= left < right < order, "canonical edge order")
        earlier[right].append(left)
    word = [-1] * order
    word[0] = 0
    output = []

    def visit(vertex, maximum):
        if vertex == order:
            output.append(tuple(word))
            return
        for colour in range(min(colour_count - 1, maximum + 1) + 1):
            if all(word[neighbour] != colour for neighbour in earlier[vertex]):
                word[vertex] = colour
                visit(vertex + 1, max(maximum, colour))
        word[vertex] = -1

    visit(1, 0)
    return tuple(output)


def graph_components(adjacency):
    unseen = set(range(len(adjacency)))
    components = []
    while unseen:
        root = min(unseen)
        component = {root}
        stack = [root]
        unseen.remove(root)
        while stack:
            vertex = stack.pop()
            new = adjacency[vertex] & unseen
            unseen.difference_update(new)
            component.update(new)
            stack.extend(new)
        components.append(frozenset(component))
    return tuple(sorted(components, key=lambda part: (-len(part), min(part))))


def load_inputs():
    for name, expected in TARGET_HASHES.items():
        require(file_hash(TARGET / name) == expected, "target input hash: " + name)
    for name, expected in SOURCE_HASHES.items():
        require(file_hash(SOURCE / name) == expected, "source input hash: " + name)
    target_certificate = loads((TARGET / "certificate.json").read_text())
    target_expected = loads((TARGET / "EXPECTED.json").read_text())
    source_certificate = loads((SOURCE / "certificate.json").read_text())
    mandatory = loads((SOURCE / "mandatory_vertices.json").read_text())
    return target_certificate, target_expected, source_certificate, mandatory


def reconstruct():
    target_certificate, target_expected, source_certificate, mandatory = load_inputs()
    equal = source_certificate["equal"]
    require(equal["denominator"] == 1, "source denominator")
    source_rows = tuple(tuple(row) for row in equal["points"])
    require(len(source_rows) == len(set(source_rows)) == 477, "distinct E477 rows")
    require(all(len(row) == 4 and all(type(value) is int for value in row)
                for row in source_rows), "source row format")
    source_edges = tuple((left, right)
                         for left, right in combinations(range(477), 2)
                         if unit(source_rows[left], source_rows[right]))
    require(len(source_edges) == 2458, "complete E477 edge census")
    source_edge_hash = stream_hash(f"{left} {right}\n" for left, right in source_edges)
    require(source_edge_hash ==
            "7a71d2181f5cbb43220059551f434101f509e9e3ad5ca914b3cfdc15bc03e391",
            "source edge stream hash")
    equal_word = equal["colouring"]
    require(type(equal_word) is list and len(equal_word) == 477
            and all(type(colour) is int and 0 <= colour < 4 for colour in equal_word)
            and equal_word[0] == equal_word[1],
            "source equal-terminal word format")
    require(all(equal_word[left] != equal_word[right] for left, right in source_edges),
            "source equal-terminal word")
    deleted = tuple(entry["deleted"] for entry in mandatory)
    require(len(deleted) == len(set(deleted)) == 253 and deleted == tuple(sorted(deleted)),
            "mandatory label census")
    require(not ({0, 1} & set(deleted)) and all(0 <= label < 477 for label in deleted),
            "mandatory labels")
    for entry in mandatory:
        omitted = entry["deleted"]
        word = entry["colouring"]
        require(type(word) is str and len(word) == 477 and set(word) <= set("0123")
                and word[0] != word[1], "deletion word format")
        require(all(word[left] != word[right]
                    for left, right in source_edges if omitted not in (left, right)),
                "deletion word")
    core_labels = tuple(sorted({0, 1, *deleted}))
    core_by_label = {label: source_rows[label] for label in core_labels}
    core_rows = tuple(sorted(core_by_label.values()))
    core_set = frozenset(core_rows)
    require(len(core_set) == 255, "core order")

    # Any positive overlap has t=q-p for two core rows.  Conversely every such
    # candidate is evaluated by the literal intersection C intersect (C+t).
    candidates = {
        sub(right, left)
        for left in core_rows for right in core_rows if left != right
    }
    overlaps = {
        translation: sum(add(row, translation) in core_set for row in core_rows)
        for translation in candidates
    }
    maximum = max(overlaps.values())
    maximizers = tuple(sorted(translation for translation, count in overlaps.items()
                              if count == maximum))
    selected = maximizers[0]
    require(maximum == 75 and maximizers == (selected, neg(selected)),
            "maximum overlap census")

    representations = defaultdict(list)
    for label in core_labels:
        row = core_by_label[label]
        representations[row].append((0, label))
        representations[add(row, selected)].append((1, label))
    physical_rows = tuple(sorted(representations))
    row_index = {row: index for index, row in enumerate(physical_rows)}
    require(len(physical_rows) == 435, "physical union order")
    overlap_rows = tuple(row for row in physical_rows
                         if {copy for copy, _ in representations[row]} == {0, 1})
    require(len(overlap_rows) == maximum, "physical overlap bridge")

    edges = tuple((left, right) for left, right in combinations(range(435), 2)
                  if unit(physical_rows[left], physical_rows[right]))
    edge_set = frozenset(edges)
    core_edges = tuple((left, right)
                       for left, right in combinations(range(len(core_rows)), 2)
                       if unit(core_rows[left], core_rows[right]))
    require(len(core_edges) == 659 and len(edges) == 1589, "edge censuses")

    inherited_images = []
    for shift in (ZERO, selected):
        image = tuple(row_index[add(row, shift)] for row in core_rows)
        inherited_images.extend(tuple(sorted((image[left], image[right])))
                                for left, right in core_edges)
    inherited = frozenset(inherited_images)
    require(inherited <= edge_set and len(inherited) == 1231, "inherited edges")
    private = edge_set - inherited
    require(len(private) == 358, "private contacts")
    for left, right in private:
        left_copies = {copy for copy, _ in representations[physical_rows[left]]}
        right_copies = {copy for copy, _ in representations[physical_rows[right]]}
        require(left_copies in ({0}, {1}) and right_copies in ({0}, {1})
                and left_copies != right_copies, "private contact is not cross-copy")

    adjacency = [set() for _ in physical_rows]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    components = graph_components(tuple(map(frozenset, adjacency)))
    require(tuple(map(len, components)) == (434, 1), "component orders")
    isolated_index = next(index for index, neighbours in enumerate(adjacency) if not neighbours)
    isolated_row = physical_rows[isolated_index]
    require(representations[isolated_row] == [(0, 91)], "isolated source identity")
    triangle_count = sum(len(adjacency[left] & adjacency[right])
                         for left, right in edges) // 3

    direction_multiplicities = Counter()
    for left, right in edges:
        difference = sub(physical_rows[right], physical_rows[left])
        direction_multiplicities[min(difference, neg(difference))] += 1

    point_hash = stream_hash(f"{','.join(map(str, row))}\n" for row in physical_rows)
    edge_hash = stream_hash(f"{left},{right}\n" for left, right in edges)
    return {
        "target_certificate": target_certificate,
        "target_expected": target_expected,
        "source_rows": source_rows,
        "source_edges": source_edges,
        "source_edge_hash": source_edge_hash,
        "core_labels": core_labels,
        "core_rows": core_rows,
        "candidate_translations": candidates,
        "overlap_counts": overlaps,
        "maximum": maximum,
        "maximizers": maximizers,
        "selected": selected,
        "representations": representations,
        "physical_rows": physical_rows,
        "row_index": row_index,
        "edges": edges,
        "edge_set": edge_set,
        "core_edges": core_edges,
        "inherited_images": tuple(inherited_images),
        "inherited": inherited,
        "private": private,
        "adjacency": tuple(map(frozenset, adjacency)),
        "components": components,
        "isolated_index": isolated_index,
        "isolated_row": isolated_row,
        "triangle_count": triangle_count,
        "direction_multiplicities": direction_multiplicities,
        "point_hash": point_hash,
        "edge_hash": edge_hash,
    }


def validate(certificate, data):
    require(certificate.get("format") ==
            "E477 mandatory-core maximum-translation union certificate v1", "format")
    require(certificate["input_sha256"] == SOURCE_HASHES, "certificate source hashes")
    selected = tuple(certificate["selected_translation"])
    require(selected == data["selected"] == (-3, 3, 3, 3), "selected translation")
    require(certificate["translation_overlap_maximum"] == data["maximum"] == 75,
            "overlap maximum")
    require(certificate["maximum_translation_count"] == len(data["maximizers"]) == 2,
            "maximizer count")
    require(certificate["source_core_points"] == len(data["core_rows"]) == 255,
            "certificate core order")
    require(certificate["source_core_edges"] == len(data["core_edges"]) == 659,
            "certificate core edges")
    require(certificate["union_points"] == len(data["physical_rows"]) == 435,
            "certificate union order")
    require(certificate["union_complete_unit_edges"] == len(data["edges"]) == 1589,
            "certificate union edges")
    require(certificate["union_inherited_edge_union"] == len(data["inherited"]) == 1231,
            "certificate inherited edges")
    require(certificate["union_private_contacts"] == len(data["private"]) == 358,
            "certificate private contacts")
    require(certificate["point_sha256"] == data["point_hash"], "point stream hash")
    require(certificate["edge_sha256"] == data["edge_hash"], "edge stream hash")

    word = certificate["four_colouring"]
    require(type(word) is str and len(word) == 435 and set(word) <= set("0123"),
            "four-colour word format")
    require(all(word[left] != word[right] for left, right in data["edges"]),
            "four-colour word")

    moser_labels = certificate["moser_source_labels"]
    require(len(moser_labels) == len(set(moser_labels)) == 7
            and set(moser_labels) <= set(data["core_labels"]), "witness labels")
    witness_vertices = tuple(data["row_index"][data["source_rows"][label]]
                             for label in moser_labels)
    witness_edges = tuple((left, right) for left, right in combinations(range(7), 2)
                          if tuple(sorted((witness_vertices[left], witness_vertices[right])))
                          in data["edge_set"])
    witness_adjacency = [set() for _ in range(7)]
    for left, right in witness_edges:
        witness_adjacency[left].add(right)
        witness_adjacency[right].add(left)
    three_words = canonical_colourings(7, witness_edges, 3)
    four_words = canonical_colourings(7, witness_edges, 4)
    require(len(witness_edges) == 11 and not three_words and len(four_words) == 16,
            "seven-point four-chromatic witness")
    require(sorted(map(len, witness_adjacency)) == [3, 3, 3, 3, 3, 3, 4],
            "Moser degree sequence")
    require(all(vertex in data["components"][0] for vertex in witness_vertices),
            "witness in main component")

    target_summary = {
        "status": "VERIFIED_FOUR_CHROMATIC_STOP",
        "source_points": len(data["source_rows"]),
        "source_core_points": len(data["core_rows"]),
        "source_core_complete_unit_edges": len(data["core_edges"]),
        "maximal_nonzero_translation_overlap": data["maximum"],
        "maximizing_translations": len(data["maximizers"]),
        "selected_translation": list(data["selected"]),
        "union_points": len(data["physical_rows"]),
        "union_complete_unit_edges": len(data["edges"]),
        "physical_overlaps": sum(len(part) > 1 for part in data["representations"].values()),
        "inherited_edge_union": len(data["inherited"]),
        "private_contacts": len(data["private"]),
        "four_colouring_verified": True,
        "embedded_moser_vertices": 7,
        "embedded_moser_edges": len(witness_edges),
        "embedded_moser_proper_three_colourings": len(three_words),
        "chromatic_number": 4,
        "point_sha256": data["point_hash"],
        "edge_sha256": data["edge_hash"],
        "record_candidate": False,
    }
    require(target_summary == data["target_expected"], "target expected summary")

    rational, radical = squared_distance_coefficients(ZERO, selected)
    require(radical == 0 and Fraction(rational, 1296) == Fraction(1, 3),
            "translation squared norm")
    degree_histogram = Counter(map(len, data["adjacency"]))
    colour_histogram = Counter(word)
    return {
        "checker": "direct two-equation geometry plus set-intersection autocorrelation",
        "target_code_imported": False,
        "target_mathematical_commit": TARGET_COMMIT,
        "source": {
            "points": len(data["source_rows"]),
            "complete_unit_edges": len(data["source_edges"]),
            "edge_stream_sha256": data["source_edge_hash"],
            "equal_terminal_four_word_verified": True,
            "unequal_terminal_deletion_words_verified": len(data["core_labels"]) - 2,
            "mandatory_labels": len(data["core_labels"]) - 2,
            "core_points": len(data["core_rows"]),
            "core_complete_unit_edges": len(data["core_edges"]),
            "mandatory_core_implication_verified": True,
        },
        "translation_selection": {
            "nonzero_candidates": len(data["candidate_translations"]),
            "maximum_overlap": data["maximum"],
            "maximizers": [list(value) for value in data["maximizers"]],
            "selected": list(selected),
            "selected_squared_length": "1/3",
        },
        "union": {
            "points": len(data["physical_rows"]),
            "complete_unit_edges": len(data["edges"]),
            "overlaps": data["maximum"],
            "inherited_edge_images_before_merging": len(data["inherited_images"]),
            "inherited_edge_union": len(data["inherited"]),
            "merged_inherited_edge_duplicates": len(data["inherited_images"]) - len(data["inherited"]),
            "private_cross_copy_contacts": len(data["private"]),
            "unit_direction_classes_up_to_sign": len(data["direction_multiplicities"]),
            "triangles": data["triangle_count"],
            "degree_histogram": {str(key): value for key, value in sorted(degree_histogram.items())},
            "component_orders": list(map(len, data["components"])),
            "point_sha256": data["point_hash"],
            "edge_sha256": data["edge_hash"],
        },
        "chromatic_certificate": {
            "literal_four_word_verified": True,
            "colour_class_sizes": {key: colour_histogram[key] for key in sorted(colour_histogram)},
            "witness_vertices": 7,
            "witness_edges": len(witness_edges),
            "witness_canonical_three_colourings": len(three_words),
            "witness_canonical_four_colourings": len(four_words),
            "chromatic_number": 4,
        },
        "refinement": {
            "isolated_physical_index": data["isolated_index"],
            "isolated_row": list(data["isolated_row"]),
            "isolated_source_representations": [list(value) for value in data["representations"][data["isolated_row"]]],
            "connected_component_points": len(data["components"][0]),
            "connected_component_complete_unit_edges": len(data["edges"]),
            "connected_component_chromatic_number": 4,
        },
        "verdict": "ACCEPT_AND_REFINE_DISCONNECTED_UNION",
        "record_candidate": False,
        "scope": "one exact maximum-overlap translation of the reviewed 255-point E477 mandatory core",
    }


def verify(certificate=None, data=None):
    if data is None:
        data = reconstruct()
    if certificate is None:
        certificate = deepcopy(data["target_certificate"])
    return validate(certificate, data)


def main():
    print(dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
