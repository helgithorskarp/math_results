#!/usr/bin/env python3
"""Generate the compact colouring certificate; the verifier does not trust SAT."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

import verify


def four_colour(points, edges, solver):
    colours = 4
    clauses = []
    for vertex in range(len(points)):
        clauses.append([colours * vertex + colour + 1 for colour in range(colours)])
        clauses.extend([[-(colours * vertex + colour + 1),
                         -(colours * vertex + earlier + 1)]
                        for colour in range(colours) for earlier in range(colour)])
    clauses.extend([[-(colours * a + colour + 1), -(colours * b + colour + 1)]
                    for a, b in edges for colour in range(colours)])
    with tempfile.TemporaryDirectory() as directory:
        cnf = Path(directory) / "host.cnf"
        with cnf.open("w") as stream:
            stream.write(f"p cnf {colours * len(points)} {len(clauses)}\n")
            for clause in clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
        answer = subprocess.run([str(solver), "--seed=0", str(cnf)],
                                capture_output=True, text=True, check=False)
    if answer.returncode != 10:
        raise RuntimeError(f"solver did not return SAT: {answer.returncode}")
    positive = {int(value) for line in answer.stdout.splitlines()
                if line.startswith("v ") for value in line[2:].split()
                if int(value) > 0}
    return "".join(str(next(colour for colour in range(colours)
                            if colours * vertex + colour + 1 in positive))
                   for vertex in range(len(points)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("solver", type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    _, _, base, shell, contacts, points = verify.reconstruct()
    edges = verify.strict_edges(points)
    histogram = dict(sorted(__import__("collections").Counter(contacts.values()).items()))
    certificate = {
        "format": 1,
        "denominator": 96,
        "directions": 60,
        "motif_vertices": 13,
        "base_operation": "C13+C13+C13",
        "minimum_base_contacts": 2,
        "base_vertices": len(base),
        "shell_vertices": len(shell),
        "host_vertices": len(points),
        "host_edges": len(edges),
        "base_contact_histogram": {str(k): v for k, v in histogram.items()},
        "coordinate_sha256": verify.compact_hash(points),
        "edge_sha256": verify.compact_hash(edges),
        "colouring": four_colour(points, edges, args.solver),
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps(verify.check(certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
