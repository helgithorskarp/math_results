#!/usr/bin/env python3
"""Exhaustive small-pattern tests and deliberately damaged-input rejection."""
import argparse
from itertools import combinations
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from generate import core_patterns
from verify import tables, parse, require


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    truth, trials = tables()
    checked = 0
    for k in (3, 4, 5):
        vertices = tuple(range(k))
        pairs = tuple(combinations(vertices, 2))
        for base, expected in truth[k].items():
            red = {edge: base >> bit & 1 for bit, edge in enumerate(pairs)}
            actual = [(color, sum(spin[v] << v for v in vertices))
                      for color, spin in core_patterns(vertices, red)]
            require(sorted(actual) == sorted(expected), f"Pattern mismatch {k} {base}")
            checked += 1
    malformed = [
        "p cnf 122 1\n1 0\n", "p cnf 123 2\n1 0\n", "p cnf 123 1\n124 0\n",
        "p cnf 123 1\n1 1 0\n", "p cnf 123 1\n1 -1 0\n", "p cnf 123 1\n2 1 0\n",
        "p cnf 123 1\n1 0 2 0\n", "p cnf 123 1\n1 2\n", "p cnf 123 2\n1 0\n1 0\n",
    ]
    rejected = 0
    with TemporaryDirectory(prefix="paley-switch-controls-") as tmp:
        path = Path(tmp) / "damaged.cnf"
        for text in malformed:
            path.write_text(text)
            try:
                parse(path)
            except ValueError:
                rejected += 1
            else:
                raise RuntimeError("Malformed DIMACS accepted")
        path.write_text("p cnf 123 2\n1 -3 0\n-4 5 123 0\n")
        require(parse(path) == {(1, -3), (-4, 5, 123)}, "Positive parser control failed")
    report = {"status": "PASS", "base_graphs_checked": checked,
              "physical_switch_truth_cases": trials, "malformed_inputs_rejected": rejected}
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
