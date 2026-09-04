#!/usr/bin/env python3
"""Optionally verify every mapped target through NetworkX VF2++."""

import argparse

import networkx as nx


def parse_edge(text: str) -> tuple[int, int]:
    fields = text.split(",")
    if len(fields) != 2:
        raise ValueError(f"bad edge: {text}")
    low, high = map(int, fields)
    if not 0 <= low < high < 42:
        raise ValueError(f"bad edge: {text}")
    return low, high


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog")
    parser.add_argument("map")
    args = parser.parse_args()

    with open(args.catalog, "rb") as source:
        catalog = [
            nx.from_graph6_bytes(line.rstrip(b"\n"))
            for line in source
            if line.rstrip(b"\n")
        ]
    if len(catalog) != 328 or any(len(graph) != 42 for graph in catalog):
        raise RuntimeError("expected 328 order-42 catalog records")
    complements = [nx.complement(graph) for graph in catalog]

    checked = 0
    summary = None
    with open(args.map, encoding="ascii") as source:
        expected_header = (
            "parent\tedge_1\tedge_2\tedge_3\tedge_4\tedge_5\tedge_6\t"
            "target_kind\ttarget_index"
        )
        if source.readline().rstrip("\n") != expected_header:
            raise RuntimeError("unexpected map header")
        for line in source:
            if line.startswith("# SUMMARY "):
                summary = dict(field.split("=", 1) for field in line.split()[2:])
                break
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 9:
                raise RuntimeError("bad map row")
            parent = int(fields[0])
            target_index = int(fields[8])
            if not 0 <= parent < 328 or not 0 <= target_index < 328:
                raise RuntimeError("bad catalog index")
            if fields[7] == "base":
                target = catalog[target_index]
            elif fields[7] == "complement":
                target = complements[target_index]
            else:
                raise RuntimeError("bad target kind")

            variant = catalog[parent].copy()
            for low, high in map(parse_edge, fields[1:7]):
                if variant.has_edge(low, high):
                    variant.remove_edge(low, high)
                else:
                    variant.add_edge(low, high)
            if not nx.vf2pp_is_isomorphic(variant, target):
                raise RuntimeError(f"wrong target isomorphism at row {checked + 2}")
            checked += 1

    if summary is None:
        raise RuntimeError("missing map summary")
    if int(summary["transitions"]) != checked:
        raise RuntimeError("map summary transition count mismatch")

    print(
        f"networkx={nx.__version__} target_isomorphisms={checked}/{checked}"
    )


if __name__ == "__main__":
    main()
