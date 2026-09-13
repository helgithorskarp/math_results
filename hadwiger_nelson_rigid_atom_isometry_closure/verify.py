#!/usr/bin/env python3
"""Solver-free exact verification of the published positive certificates."""

import argparse
import json
from pathlib import Path

from geometry import closure_geometry, golomb, moser, strict_edges


def check_word(word, vertex_count, edges):
    if len(word) != vertex_count or any(symbol not in "0123" for symbol in word):
        raise ValueError("malformed colour word")
    colours = tuple(map(int, word))
    if not all(colours[a] != colours[b] for a, b in edges):
        raise ValueError("improper colour word")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", default="certificate.json")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(Path(args.certificate).read_text(encoding="utf-8"))
    if certificate["field_basis"] != ["1", "sqrt33", "i_sqrt3", "i_sqrt11"]:
        raise ValueError("field basis mismatch")
    if len(strict_edges(moser())) != 11 or len(strict_edges(golomb())) != 18:
        raise ValueError("atom edge census mismatch")
    verified = []
    by_name = {row["name"]: row for row in certificate["rows"]}
    if set(by_name) != {"moser_self", "golomb_self", "mixed_aligned"}:
        raise ValueError("certificate row inventory mismatch")
    for name in ("moser_self", "golomb_self", "mixed_aligned"):
        expected = by_name[name]
        actual, points, edges = closure_geometry(name)
        for key, value in actual.items():
            if expected.get(key) != value:
                raise ValueError(f"{name}: mismatch in {key}")
        check_word(expected["colour_word"], len(points), edges)
        if args.controls:
            broken = list(expected["colour_word"])
            a, b = edges[0]
            broken[b] = broken[a]
            try:
                check_word("".join(broken), len(points), edges)
            except ValueError:
                pass
            else:
                raise ValueError("mutation control was not rejected")
        verified.append({"name": name, "vertices": len(points), "edges": len(edges),
                         "copies": actual["copy_point_sets"]})
    print(json.dumps({"status": "VERIFIED", "controls": args.controls,
                      "rows": verified}, sort_keys=True))


if __name__ == "__main__":
    main()
