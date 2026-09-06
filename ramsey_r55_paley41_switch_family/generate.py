#!/usr/bin/env python3
"""Exact K5-free CNF for all switches of Paley(41) plus two free vertices."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time


def core_patterns(vertices, red):
    """Return (monochromatic color, switch assignment) pairs on this core set."""
    anchor = vertices[0]
    for color in (0, 1):
        spin = {v: red[anchor, v] ^ color for v in vertices[1:]}
        spin[anchor] = 0
        if all(red[u, v] ^ spin[u] ^ spin[v] == color
               for u, v in combinations(vertices, 2)):
            for flip in (0, 1):
                yield color, {v: spin[v] ^ flip for v in vertices}


def build():
    residues = {x * x % 41 for x in range(1, 41)}
    red = {(u, v): int((v - u) % 41 in residues)
           for u, v in combinations(range(41), 2)}
    free = {edge: 41 + i for i, edge in enumerate(
        edge for edge in combinations(range(43), 2) if edge[1] >= 41)}
    clauses = []
    counts = Counter()
    sets = Counter()
    for size in (5, 4, 3):
        for core in combinations(range(41), size):
            patterns = list(core_patterns(core, red))
            sets[f"{size}_core_subsets"] += 1
            sets[f"{size}_coherent_core_subsets"] += bool(patterns)
            for added in combinations((41, 42), 5 - size):
                for color, spin in patterns:
                    if spin.get(0, 0):
                        continue  # The forbidden event requires s_0=1: impossible.
                    literals = [(-v if spin[v] else v) for v in core if v != 0]
                    literals += [(-free[u, v] if color else free[u, v])
                                 for u, v in combinations(core + added, 2)
                                 if v >= 41]
                    clauses.append(tuple(literals))
                    counts[f"{size}_core_color_{color}_width_{len(literals)}"] += 1
    if len(clauses) != len(set(clauses)):
        raise RuntimeError("Unexpected duplicate clause")
    return clauses, {
        "family": "Paley(41) Seidel switches, s_0=0, two arbitrary added vertices",
        "vertices": 43, "core_vertices": 41, "variables": 123,
        "switch_variables": 40, "free_edge_variables": 83,
        "labeled_family_size": str(2 ** 123),
        "clauses": len(clauses), "clause_counts": dict(sorted(counts.items())),
        "subset_counts": dict(sorted(sets.items())),
        "residues_mod_41": sorted(residues),
        "free_edges": [[u, v, number] for (u, v), number in free.items()],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    clauses, summary = build()
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output / "family.cnf"
    digest = sha256()
    with path.open("wb") as stream:
        header = f"p cnf 123 {len(clauses)}\n".encode()
        stream.write(header)
        digest.update(header)
        for clause in clauses:
            line = (" ".join(map(str, clause)) + " 0\n").encode()
            stream.write(line)
            digest.update(line)
    summary["cnf_sha256"] = digest.hexdigest()
    summary["cnf_bytes"] = path.stat().st_size
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"clauses": len(clauses), "sha256": digest.hexdigest(),
                      "generation_seconds": time.monotonic() - start}))


if __name__ == "__main__":
    main()
