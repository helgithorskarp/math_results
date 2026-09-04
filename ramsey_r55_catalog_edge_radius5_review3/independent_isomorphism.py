#!/usr/bin/env python3
"""Check every claimed radius-five target with exact NetworkX isomorphism."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import networkx as nx


def parse_edge(text: str) -> tuple[int, int]:
    low, high = map(int, text.split(","))
    if not 0 <= low < high < 42:
        raise ValueError(text)
    return low, high


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: independent_isomorphism.py CATALOG MAP")
    records = Path(sys.argv[1]).read_bytes().splitlines()
    if len(records) != 328:
        raise AssertionError(len(records))
    catalog = [nx.from_graph6_bytes(record) for record in records]
    if any(graph.number_of_nodes() != 42 for graph in catalog):
        raise AssertionError("wrong graph order")

    mapping_digest = hashlib.sha256()
    checked = 0
    with Path(sys.argv[2]).open(encoding="ascii") as source:
        header = source.readline().rstrip("\n")
        if header != (
            "parent\tedge_1\tedge_2\tedge_3\tedge_4\tedge_5\t"
            "target_kind\ttarget_index"
        ):
            raise AssertionError(header)
        for line in source:
            if line.startswith("# SUMMARY"):
                break
            fields = line.rstrip("\n").split("\t")
            parent = int(fields[0])
            target_index = int(fields[7])
            variant = catalog[parent].copy()
            for edge_text in fields[1:6]:
                low, high = parse_edge(edge_text)
                if variant.has_edge(low, high):
                    variant.remove_edge(low, high)
                else:
                    variant.add_edge(low, high)
            target = catalog[target_index]
            if fields[6] == "complement":
                target = nx.complement(target)
            elif fields[6] != "base":
                raise AssertionError(fields[6])

            matcher = nx.algorithms.isomorphism.GraphMatcher(variant, target)
            if not matcher.is_isomorphic():
                raise AssertionError(f"row {checked + 2} is not in its claimed class")
            mapping = matcher.mapping
            if len(mapping) != 42:
                raise AssertionError("incomplete isomorphism")
            for first in range(42):
                for second in range(first + 1, 42):
                    if variant.has_edge(first, second) != target.has_edge(
                        mapping[first], mapping[second]
                    ):
                        raise AssertionError("invalid isomorphism witness")
            mapping_digest.update(
                (
                    f"{checked}:"
                    + ",".join(f"{vertex}>{mapping[vertex]}" for vertex in range(42))
                    + "\n"
                ).encode("ascii")
            )
            checked += 1

    if checked != 6224:
        raise AssertionError(checked)
    print(f"networkx_version={nx.__version__}")
    print(f"exact_isomorphisms={checked}")
    print(f"mapping_witnesses_sha256={mapping_digest.hexdigest()}")
    print("independent_isomorphism_check=true")


if __name__ == "__main__":
    main()
