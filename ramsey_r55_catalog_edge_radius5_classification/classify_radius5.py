#!/usr/bin/env python3
"""Map exactly-five-edge variants to canonical catalog records."""

import argparse
from collections import Counter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("variants_tsv")
    parser.add_argument("variant_canonical")
    parser.add_argument("catalog_canonical")
    parser.add_argument("complements_canonical")
    args = parser.parse_args()

    with open(args.catalog_canonical, encoding="ascii") as source:
        base = source.read().splitlines()
    with open(args.complements_canonical, encoding="ascii") as source:
        complements = source.read().splitlines()
    if len(base) != 328 or len(complements) != 328:
        raise RuntimeError("expected 328 catalog and 328 complement records")

    lookup = {graph: ("base", index) for index, graph in enumerate(base)}
    for index, graph in enumerate(complements):
        if graph in lookup:
            raise RuntimeError("base/complement canonical sets overlap")
        lookup[graph] = ("complement", index)

    with open(args.variants_tsv, encoding="ascii") as source:
        rows = [line.rstrip("\n").split("\t") for line in source]
    with open(args.variant_canonical, encoding="ascii") as source:
        canonical = source.read().splitlines()
    if len(rows) != len(canonical):
        raise RuntimeError("variant/canonical length mismatch")

    transition_kinds = Counter()
    targets = set()
    print(
        "parent\tedge_1\tedge_2\tedge_3\tedge_4\tedge_5\t"
        "target_kind\ttarget_index"
    )
    for row, canon in zip(rows, canonical):
        if len(row) != 7:
            raise RuntimeError("bad variant row")
        parent, edge1, edge2, edge3, edge4, edge5, _ = row
        if canon not in lookup:
            raise RuntimeError(f"variant outside catalog at parent {parent}")
        kind, index = lookup[canon]
        print(
            f"{parent}\t{edge1}\t{edge2}\t{edge3}\t{edge4}\t{edge5}\t"
            f"{kind}\t{index}"
        )
        transition_kinds[kind] += 1
        targets.add((kind, index))

    target_kinds = Counter(kind for kind, _ in targets)
    print(
        "# SUMMARY "
        f"transitions={len(rows)} "
        f"base_transitions={transition_kinds['base']} "
        f"complement_transitions={transition_kinds['complement']} "
        f"distinct_targets={len(targets)} "
        f"base_targets={target_kinds['base']} "
        f"complement_targets={target_kinds['complement']}"
    )


if __name__ == "__main__":
    main()
