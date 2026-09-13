"""Produce the finite parity and sharpness certificate; no solver is used."""
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


def central_rows():
    """All same-orbit two-anchor cases not excluded by |a0-a1|>3."""
    rows = []
    kinds = ("unit", "sqrt3")
    for t0 in kinds:
        for t1 in kinds:
            if t0 == t1 == "unit":
                continue
            c0 = [0] if t0 == "unit" else [0, 1]
            desired0 = 0 if t0 == "unit" else 1
            for base in range(6):
                c1 = [base] if t1 == "unit" else [base, (base + 1) % 6]
                desired1 = 1 if t1 == "unit" else 0
                if set(c0) & set(c1):
                    continue
                choices = [
                    (x, y)
                    for x, y in product(c0, c1)
                    if ((x - y) & 1) == (desired0 ^ desired1)
                ]
                need(choices, "uncovered central parity case")
                rows.append([t0, t1, base, choices[0][0], choices[0][1]])
    return rows


def generate():
    roots = [(2, 0), (1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1)]
    chords = []
    for j, (a, b) in enumerate(roots):
        squared = ((a - 2) ** 2 + 3 * b * b) // 4
        chords.append([j, j % 2, squared, 4 - squared])

    z = (0, 0, 0, 0)
    moser = [
        (z, z),
        ((12, 0, 0, 0), z),
        ((6, 0, 0, 0), (0, 6, 0, 0)),
        ((18, 0, 0, 0), (0, 6, 0, 0)),
        ((10, 0, 0, 0), (0, 0, 2, 0)),
        ((5, 0, 0, -1), (0, 5, 1, 0)),
        ((15, 0, 0, -1), (0, 5, 3, 0)),
    ]
    edges = [
        list(e)
        for e in combinations(range(7), 2)
        if norm(moser[e[0]], moser[e[1]]) == (144, 0, 0, 0)
    ]
    return {
        "orbit_chords": {
            "columns": ["step", "parity", "chord_squared", "centre_distance_squared"],
            "rows": chords,
        },
        "central_same_orbit_choices": {
            "columns": ["type0", "type1", "second_base", "chosen0", "chosen1"],
            "rows": central_rows(),
        },
        "sharpness": {
            "name": "classical Moser spindle inside a separated-triple support",
            "basis": ["1", "sqrt3", "sqrt11", "sqrt33"],
            "coordinate_scale": 12,
            "vertices": moser,
            "edges": edges,
            "dominating_pair": [0, 3],
            "colours": [0, 1, 2, 3, 1, 3, 2],
            "third_centre": [[48, 0, 0, 0], [0, 0, 0, 0]],
            "separated_pair": [0, "third_centre"],
        },
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
