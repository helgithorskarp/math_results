#!/usr/bin/env python3
"""Standard-library exact verifier for the fixed Pegg UD12-2 reflection route."""

from __future__ import annotations

import json
from hashlib import sha256
from itertools import combinations
from pathlib import Path

from model import (
    POSITIVE_AXES,
    all_source_four_colorings,
    check_word,
    coordinate_hash,
    edge_hash,
    find_coloring,
    reflected_union,
    source_edges,
    source_points,
    vertex_connectivity,
)


HERE = Path(__file__).resolve().parent


def relation(axis):
    points, edges, labels, maps = reflected_union((axis,))
    base_map = maps[0]
    source_words = all_source_four_colorings()
    surviving = []
    for word in source_words:
        pins = {base_map[i]: int(word[i]) for i in range(12)}
        if find_coloring(len(points), edges, 4, pins) is not None:
            surviving.append(word)
    return points, edges, labels, maps, source_words, tuple(surviving)


def main():
    cert = json.loads((HERE / "certificate.json").read_text())
    assert tuple(map(tuple, cert["full_axes"])) == POSITIVE_AXES
    source = source_points()
    sedges = source_edges()
    assert len(source) == len(set(source)) == 12
    assert len(sedges) == 21
    assert find_coloring(12, sedges, 3) is None
    assert find_coloring(12, sedges, 4) is not None
    source_words = all_source_four_colorings()
    assert len(source_words) == 756
    assert cert["single_blocked_source_word"] in source_words
    assert cert["single_surviving_source_word"] in source_words

    single_axis = tuple(cert["single_axis"])
    points1, edges1, labels1, maps1, words1, surviving1 = relation(single_axis)
    assert words1 == source_words
    assert len(points1) == 22
    assert len(edges1) == 50
    assert len(surviving1) == 620
    assert len(source_words) - len(surviving1) == 136
    blocked = cert["single_blocked_source_word"]
    assert blocked not in surviving1
    assert find_coloring(22, edges1, 4, {i: int(blocked[i]) for i in range(12)}) is None
    extension = check_word(cert["single_extension_word"], 22, edges1)
    assert cert["single_extension_word"][:12] == cert["single_surviving_source_word"]
    assert tuple(extension[:12]) == tuple(map(int, cert["single_surviving_source_word"]))

    # The second copy shares exactly the axis vertices.  Eight complete-graph
    # edges are not inherited from either reflected source copy.
    assert sorted(i for i, labels in enumerate(labels1) if len(labels) == 2) == [0, 6]
    inherited = set()
    for a, b in sedges:
        inherited.add(tuple(sorted((maps1[0][a], maps1[0][b]))))
        inherited.add(tuple(sorted((maps1[1][a], maps1[1][b]))))
    private_edges = tuple(e for e in edges1 if e not in inherited)
    assert len(private_edges) == 8
    no_private_word = cert["single_blocked_word_without_private_edges"]
    assert no_private_word[:12] == blocked
    check_word(no_private_word, 22, tuple(sorted(inherited)))
    critical_private = 0
    pins = {i: int(blocked[i]) for i in range(12)}
    for edge in private_edges:
        if find_coloring(22, tuple(e for e in edges1 if e != edge), 4, pins) is not None:
            critical_private += 1
    assert critical_private == 3
    connectivity, cut = vertex_connectivity(22, edges1)
    assert connectivity == 3
    assert cut == (2, 8, 11)

    # Recheck every member of the frozen completion pool.  Each one has
    # genuine non-inherited contacts and the same strict cardinality loss,
    # although the surviving source relations are not all identical.
    relation_rows = []
    private_histogram = {}
    for axis in POSITIVE_AXES:
        pa, ea, la, ma, wa, sa = relation(axis)
        assert wa == source_words
        assert len(sa) == 620
        inherited_a = set()
        for a, b in sedges:
            inherited_a.add(tuple(sorted((ma[0][a], ma[0][b]))))
            inherited_a.add(tuple(sorted((ma[1][a], ma[1][b]))))
        private = len(set(ea) - inherited_a)
        assert private > 0
        private_histogram[private] = private_histogram.get(private, 0) + 1
        relation_rows.extend(f"{axis[0]} {axis[1]} {word}\n" for word in sa)
    assert private_histogram == {4: 6, 8: 12}
    relation_sha256 = sha256("".join(relation_rows).encode()).hexdigest()

    points, edges, labels, maps = reflected_union(POSITIVE_AXES)
    assert len(points) == 165
    assert len(edges) == 597
    check_word(cert["full_four_word"], 165, edges)
    assert find_coloring(165, edges, 3) is None  # inherited 4-chromatic source

    expected = json.loads((HERE / "expected.json").read_text())
    actual = {
        "source": {
            "points": 12,
            "edges": 21,
            "canonical_four_colorings": 756,
            "coordinate_sha256": coordinate_hash(source),
            "edge_sha256": edge_hash(sedges),
        },
        "single_axis": {
            "axis": list(single_axis),
            "points": 22,
            "edges": 50,
            "private_edges": 8,
            "private_edges_critical_for_blocked_word": critical_private,
            "canonical_inputs_blocked": 136,
            "canonical_inputs_surviving": 620,
            "vertex_connectivity": connectivity,
            "first_cut": list(cut),
            "coordinate_sha256": coordinate_hash(points1),
            "edge_sha256": edge_hash(edges1),
        },
        "full_completion": {
            "axes": len(POSITIVE_AXES),
            "points": 165,
            "edges": 597,
            "collision_classes": sum(len(x) > 1 for x in labels),
            "axis_private_edge_histogram": {str(k): v for k, v in sorted(private_histogram.items())},
            "axis_surviving_relation_sha256": relation_sha256,
            "coordinate_sha256": coordinate_hash(points),
            "edge_sha256": edge_hash(edges),
            "four_colorable": True,
            "three_colorable": False,
        },
    }
    print(json.dumps(actual, sort_keys=True, separators=(",", ":")))
    assert actual == expected
    print("VERIFIED_PEGG12_REFLECTION_COMPLETION_STOP")


if __name__ == "__main__":
    main()
