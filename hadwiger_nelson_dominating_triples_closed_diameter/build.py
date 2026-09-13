"""Produce exact boundary-parity and sharpness data; no solver is used."""
import argparse
import hashlib
import json
import math
import time
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def qdist(a, b):
    """Four times squared distance for (s/2,t*sqrt(3)/2)."""
    return (a[0] - b[0]) ** 2 + 3 * (a[1] - b[1]) ** 2


def boundary_patch():
    roots = [(2, 0), (1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1)]
    vertices = roots + [(s + 6, t) for s, t in roots]
    edges = [list(e) for e in combinations(range(12), 2) if qdist(vertices[e[0]], vertices[e[1]]) == 4]
    proper = [list(row) for row in product(range(2), repeat=12) if all(row[a] != row[b] for a, b in edges)]
    need(len(edges) == 13 and len(proper) == 2, "boundary graph")
    return {
        "coordinate_map": "(s,t) -> (s/2,t*sqrt(3)/2)",
        "centres": [[0, 0], [6, 0]],
        "vertices": vertices,
        "edges": edges,
        "cross_edge": [0, 9],
        "colouring": proper[0],
    }


def boundary_cases(patch):
    edges = [tuple(e) for e in patch["edges"]]
    proper = [row for row in product(range(2), repeat=12) if all(row[a] != row[b] for a, b in edges)]
    roots_by_leaf = [list(range(6)), list(range(6, 12))]

    unit_rows = []
    for leaf in range(2):
        cycle = roots_by_leaf[leaf]
        for k in range(6):
            anchor = cycle[k]
            neighbours = [cycle[(k - 1) % 6], cycle[(k + 1) % 6]]
            rows = [r for r in proper if r[anchor] == 0]
            need(rows and all(r[x] == 1 for r in rows for x in neighbours), "unit anchor")
            unit_rows.append([leaf, k, (k - 1) % 6, (k + 1) % 6])

    one_exception = []
    for exceptional_leaf in range(2):
        cycle = roots_by_leaf[exceptional_leaf]
        other = roots_by_leaf[1 - exceptional_leaf]
        for base in range(6):
            exceptional_edge = [cycle[base], cycle[(base + 1) % 6]]
            for anchor_local in [-1] + list(range(6)):
                rows = proper if anchor_local < 0 else [r for r in proper if r[other[anchor_local]] == 0]
                choices = [(ri, x) for ri, r in enumerate(rows) for x in exceptional_edge if r[x] == 1]
                need(choices, "one-exception boundary")
                one_exception.append([exceptional_leaf, base, anchor_local, exceptional_edge.index(choices[0][1])])

    two_exception = []
    for base0 in range(6):
        e0 = [base0, (base0 + 1) % 6]
        for base1 in range(6):
            e1 = [6 + base1, 6 + (base1 + 1) % 6]
            r = proper[0]
            x0 = next(j for j, x in enumerate(e0) if r[x] == 1)
            x1 = next(j for j, x in enumerate(e1) if r[x] == 1)
            two_exception.append([base0, base1, x0, x1])

    return {
        "unit_anchor_columns": ["leaf", "anchor", "left_intersection", "right_intersection"],
        "unit_anchor_rows": unit_rows,
        "one_exception_columns": ["exceptional_leaf", "edge_base", "other_leaf_anchor_or_minus1", "chosen_endpoint"],
        "one_exception_rows": one_exception,
        "two_exception_columns": ["edge0_base", "edge1_base", "chosen0", "chosen1"],
        "two_exception_rows": two_exception,
    }


def times(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (
        a * e + 3 * b * f + 11 * c * g + 33 * d * h,
        a * f + b * e + 11 * c * h + 11 * d * g,
        a * g + 3 * b * h + c * e + 3 * d * f,
        a * h + b * g + c * f + d * e,
    )


def norm(a, b):
    delta = [tuple(x - y for x, y in zip(c, d)) for c, d in zip(a, b)]
    squares = [times(v, v) for v in delta]
    return tuple(sum(v[i] for v in squares) for i in range(4))


def sharpness():
    z = (0, 0, 0, 0)
    vertices = [
        (z, z),
        ((12, 0, 0, 0), z),
        ((6, 0, 0, 0), (0, 6, 0, 0)),
        ((18, 0, 0, 0), (0, 6, 0, 0)),
        ((10, 0, 0, 0), (0, 0, 2, 0)),
        ((5, 0, 0, -1), (0, 5, 1, 0)),
        ((15, 0, 0, -1), (0, 5, 3, 0)),
    ]
    edges = [list(e) for e in combinations(range(7), 2) if norm(vertices[e[0]], vertices[e[1]]) == (144, 0, 0, 0)]
    return {
        "name": "Moser spindle inside an equality-boundary support",
        "basis": ["1", "sqrt3", "sqrt11", "sqrt33"],
        "coordinate_scale": 12,
        "vertices": vertices,
        "edges": edges,
        "dominating_pair": [0, 3],
        "colours": [0, 1, 2, 3, 1, 3, 2],
        "third_centre": [[36, 0, 0, 0], [0, 0, 0, 0]],
        "boundary_pair": [0, "third_centre"],
    }


def generate():
    patch = boundary_patch()
    return {
        "boundary_patch": patch,
        "boundary_cases": boundary_cases(patch),
        "orbit_chords": {
            "columns": ["step", "parity", "chord_squared", "centre_distance_squared"],
            "rows": [[j, j % 2, qdist((2, 0), p) // 4, 4 - qdist((2, 0), p) // 4]
                     for j, p in enumerate([(2, 0), (1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1)])],
        },
        "sharpness": sharpness(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--discover", action="store_true")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    raw = (json.dumps(generate(), sort_keys=True, separators=(",", ":")) + "\n").encode()
    if not args.discover:
        need(raw == (HERE / "certificate.json").read_bytes(), "certificate mismatch")
    (out / "certificate.json").write_bytes(raw)
    result = {
        "status": "PASS",
        "certificate_bytes": len(raw),
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "native_solver_calls": 0,
        "seconds": time.monotonic() - start,
    }
    (out / "build.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
