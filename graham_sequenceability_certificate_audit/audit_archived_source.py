#!/usr/bin/env python3
"""Hash and inspect the exact Zenodo source cited by arXiv:2603.20961v1."""

from __future__ import annotations

import argparse
import hashlib
import urllib.request
from pathlib import Path


URL = "https://zenodo.org/api/records/18997905/files/treeSearch.py/content"
EXPECTED_SHA256 = "d3dbceb4728f5cc0614813d4b352ab1000b6b160e068f8cce397629dda19ab91"


def source_bytes(path: str | None) -> bytes:
    if path is not None:
        return Path(path).read_bytes()
    with urllib.request.urlopen(URL, timeout=30) as response:
        return response.read()


def line_number(lines: list[str], needle: str) -> int:
    matches = [index for index, line in enumerate(lines, 1) if needle in line]
    assert len(matches) == 1, (needle, matches)
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="audit a local treeSearch.py instead of downloading")
    args = parser.parse_args()
    raw = source_bytes(args.source)
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == EXPECTED_SHA256, digest
    lines = raw.decode("utf-8").splitlines()

    facts = {
        "floating_matrix_conversion": "C = np.array(self.constraints, dtype=float)",
        "floating_rank": "rank_C = np.linalg.matrix_rank(C)",
        "unconditional_half_interval_cutoff": "if j - i > n // 2:",
        "configured_n": "n = 22",
        "configured_nonzero_mode": "sum_zero = 0",
        "configured_nonzero_constraints": "initial_cons = generate_initial_cons_non_zero(len(initial_ordering))",
        "bfs_node_cap": "results = searcher.build_tree_bfs(max_depth=100, max_nodes=1000000000)",
    }
    print(f"sha256={digest}")
    for name, needle in facts.items():
        print(f"{name}_line={line_number(lines, needle)}")

    assert any(
        line.strip() == "while queue and self.total_nodes < max_nodes:"
        for line in lines
    )
    assert not any("queue_exhausted" in line for line in lines)
    assert not any("assert not queue" in line for line in lines)
    print("explicit_queue_exhaustion_check=ABSENT")
    print("source_audit=PASS")


if __name__ == "__main__":
    main()
