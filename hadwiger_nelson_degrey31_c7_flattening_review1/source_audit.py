#!/usr/bin/env python3
"""Independent audit using literal Graph edge lists in the pinned notebook.

The reviewed package parses a SparseArray after one marker.  This audit scans
the notebook's separate explicit Graph renderings instead.
"""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


NOTEBOOK_BYTES = 35685277
NOTEBOOK_SHA256 = "3fc1c341c7a35f26e083929f54c9997fa88773a6de32d6700abbae2389c9d553"
SOURCE_EDGE_SHA256 = "9691aadee6776f4e65e3dc2f3a5ff586b6d86b94c25bfc67e4dfaf819602b671"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge_digest(edges):
    payload = "".join(f"{a} {b}\n" for a, b in edges).encode("ascii")
    return sha256(payload).hexdigest()


def literal_graph31_edge_sets(text):
    vertices = r"\{\s*" + r"\s*,\s*".join(map(str, range(1, 32))) + r"\s*\}"
    pattern = re.compile(
        r"Graph\[\s*" + vertices
        + r"\s*,\s*\{\s*Null\s*,\s*"
        + r"(?P<edges>\{(?:\s*\{\s*\d+\s*,\s*\d+\s*\}\s*,?)+\})"
    )
    answer = []
    for match in pattern.finditer(text):
        pairs = tuple(sorted(
            tuple(map(int, pair))
            for pair in re.findall(r"\{\s*(\d+)\s*,\s*(\d+)\s*\}", match["edges"])
        ))
        if len(pairs) == 98 and all(1 <= a < b <= 31 for a, b in pairs):
            answer.append(pairs)
    return answer


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 source_audit.py /path/to/deGreyGraphs.nb")
    raw = Path(sys.argv[1]).read_bytes()
    require(len(raw) == NOTEBOOK_BYTES, "notebook byte count changed")
    require(sha256(raw).hexdigest() == NOTEBOOK_SHA256, "notebook hash changed")
    text = raw.decode("utf-8")

    graph_sets = literal_graph31_edge_sets(text)
    hashes = Counter(edge_digest(edges) for edges in graph_sets)
    require(len(graph_sets) == 90, "literal 31-vertex Graph census changed")
    require(hashes[SOURCE_EDGE_SHA256] == 89, "D31 literal adjacency not reproduced")

    marker = 'RowBox[{"DeGreyGraph61", "=", "\\[IndentingNewLine]", '
    start = text.find(marker)
    require(start >= 0, "DeGreyGraph61 construction assignment not found")
    construction = text[start:start + 5000]
    fragments = {
        "vertex_delete_62": 'RowBox[{"VertexDelete", "[", "\\[IndentingNewLine]", ',
        "edge_add": 'RowBox[{"EdgeAdd", "[", "\\[IndentingNewLine]", ',
        "range_62": 'RowBox[{"Range", "[", "62", "]"}]',
        "identify_62_with_31": 'RowBox[{"62", "->", "31"}]',
        "bridge_30_61": 'RowBox[{"30", "\\[UndirectedEdge]", "61"}]',
    }
    found = {name: fragment in construction for name, fragment in fragments.items()}
    require(all(found.values()), "D61 construction markers changed")

    output = {
        "notebook_bytes": len(raw),
        "notebook_sha256": sha256(raw).hexdigest(),
        "parser_representation": "literal Graph pair lists, not reviewed SparseArray parser",
        "literal_31_vertex_98_edge_graph_blocks": len(graph_sets),
        "distinct_literal_edge_hashes": dict(sorted(hashes.items())),
        "matching_d31_literal_blocks": hashes[SOURCE_EDGE_SHA256],
        "source_edge_sha256_one_based": SOURCE_EDGE_SHA256,
        "d61_construction_markers": found,
        "d61_construction_matches_two_copies_share_31_bridge_30_61": True,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
