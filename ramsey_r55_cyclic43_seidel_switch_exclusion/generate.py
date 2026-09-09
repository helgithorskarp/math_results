#!/usr/bin/env python3
"""Generate the exact K5-free CNF for one pinned Cyclic43 Seidel class."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INPUT = (ROOT / "ramsey_r55_cyclic43_q13_boundary_certificate" /
         "objective-twelve-component-fast.json")
INPUT_SHA256 = "4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3"
LENGTHS = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def edge_list():
    return list(combinations(range(43), 2))


def sources():
    need(sha256(INPUT.read_bytes()).hexdigest() == INPUT_SHA256,
         "pinned source identity")
    data = json.loads(INPUT.read_text())
    need(data["order"] == 43 and data["edge_count"] == 903,
         "source dimensions")
    values = data["complete_additional_objective_12_rotation_representatives"]
    need(len(values) == 238 and len({tuple(row) for row in values}) == 238,
         "complete 238-source list")
    return values


def graph(toggle_indices):
    pairs = edge_list()
    need(toggle_indices == sorted(set(toggle_indices)), "canonical toggle list")
    need(all(0 <= index < len(pairs) for index in toggle_indices),
         "toggle index range")
    toggles = set(toggle_indices)
    red = [[False] * 43 for _ in range(43)]
    for index, (u, v) in enumerate(pairs):
        length = min((v - u) % 43, (u - v) % 43)
        value = (length in LENGTHS) ^ (index in toggles)
        red[u][v] = red[v][u] = value
    return red


def coherent_pattern(vertices, red):
    """Return (final color, switch values with anchor zero), or None."""
    anchor = vertices[0]
    u, v = vertices[1:3]
    color = red[u][v] ^ red[anchor][u] ^ red[anchor][v]
    spin = {anchor: 0}
    for vertex in vertices[1:]:
        spin[vertex] = int(red[anchor][vertex] ^ color)
    if not all((red[u][v] ^ spin[u] ^ spin[v]) == color
               for u, v in combinations(vertices, 2)):
        return None
    return int(color), spin


def clauses_for_source(toggle_indices):
    red = graph(toggle_indices)
    clauses = []
    colors = Counter()
    widths = Counter()
    coherent_sets = 0
    for vertices in combinations(range(43), 5):
        pattern = coherent_pattern(vertices, red)
        if pattern is None:
            continue
        coherent_sets += 1
        color, base = pattern
        for flip in (0, 1):
            assignment = {v: bit ^ flip for v, bit in base.items()}
            if 0 in assignment and assignment[0]:
                continue
            clause = tuple(-v if assignment[v] else v
                           for v in vertices if v != 0)
            need(len(clause) in (4, 5), "clause width")
            clauses.append(clause)
            colors[str(color)] += 1
            widths[str(len(clause))] += 1
    need(len(clauses) == len(set(clauses)), "duplicate clause")
    return clauses, {
        "clauses": len(clauses),
        "coherent_five_sets": coherent_sets,
        "final_color_clause_counts": dict(sorted(colors.items())),
        "width_counts": dict(sorted(widths.items())),
    }


def write_cnf(path, clauses):
    digest = sha256()
    with path.open("xb") as stream:
        header = f"p cnf 42 {len(clauses)}\n".encode()
        stream.write(header)
        digest.update(header)
        for clause in clauses:
            line = (" ".join(map(str, clause)) + " 0\n").encode()
            stream.write(line)
            digest.update(line)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source_rows = sources()
    need(0 <= args.source < len(source_rows), "source index")
    clauses, report = clauses_for_source(source_rows[args.source])
    report.update({
        "cnf": write_cnf(args.output, clauses),
        "source_index": args.source,
        "switch_normalization": "s_0=0",
        "variables": 42,
    })
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
