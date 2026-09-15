#!/usr/bin/env python3
"""Compare the D31 orbit template with the adjacency in a Wolfram notebook."""

from hashlib import sha256
import json
from pathlib import Path
import re
import sys

from verify import digest_edges, graph31


PATTERN = re.compile(
    r"SparseArray\[\s*Automatic,\s*\{31,\s*31\},\s*0,\s*\{\s*1,"
    r"\s*\{\{(?P<offsets>[0-9,\s]+)\},\s*"
    r"\{(?P<neighbors>(?:\{\s*[0-9]+\s*\},?\s*)+)\}\},\s*Pattern\}\]"
)


def notebook_edges(text):
    marker = 'Cell["\\\"DeGreyGraph31\\\" exact"'
    start = text.find(marker)
    if start < 0:
        raise ValueError("exact DeGreyGraph31 section not found")
    match = PATTERN.search(text, start)
    if match is None:
        raise ValueError("31-by-31 SparseArray not found after exact section")
    offsets = [int(value) for value in re.findall(r"[0-9]+", match["offsets"])]
    neighbors = [int(value) for value in re.findall(r"[0-9]+", match["neighbors"])]
    if len(offsets) != 32 or offsets[0] != 0 or offsets[-1] != len(neighbors):
        raise ValueError("malformed sparse adjacency offsets")
    directed = set()
    for row in range(1, 32):
        for neighbor in neighbors[offsets[row - 1] : offsets[row]]:
            directed.add((row, neighbor))
    if len(directed) != len(neighbors):
        raise ValueError("duplicate directed adjacency entry")
    if any(left == right for left, right in directed):
        raise ValueError("loop in notebook adjacency")
    if any((right, left) not in directed for left, right in directed):
        raise ValueError("notebook adjacency is not symmetric")
    return tuple(sorted((left - 1, right - 1) for left, right in directed if left < right))


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 source_audit.py /path/to/deGreyGraphs.nb")
    path = Path(sys.argv[1])
    raw = path.read_bytes()
    source_edges = notebook_edges(raw.decode("utf-8"))
    template_edges, _orbits = graph31()
    assert source_edges == template_edges
    result = {
        "notebook_bytes": len(raw),
        "notebook_sha256": sha256(raw).hexdigest(),
        "source_section": '"DeGreyGraph31" exact',
        "source_vertices": 31,
        "source_edges": len(source_edges),
        "source_edge_sha256_one_based": digest_edges(source_edges),
        "template_matches_source_adjacency": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
