#!/usr/bin/env python3
"""Independent coefficient-reduction and certificate-corruption controls."""

from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path
import tempfile

import model
import verify


HERE = Path(__file__).resolve().parent


def poly_mul(x, y):
    """Multiply in Q[s,r,t]/(s^2-3,r^2-11,t^2-2+s/2)."""
    raw = {}
    for (a, b, c), u in x.items():
        for (d, e, f), v in y.items():
            raw[(a + d, b + e, c + f)] = raw.get((a + d, b + e, c + f), Q(0)) + u * v
    changed = True
    while changed:
        changed = False
        out = {}
        for (a, b, c), u in raw.items():
            if a >= 2:
                out[(a - 2, b, c)] = out.get((a - 2, b, c), Q(0)) + 3 * u
                changed = True
            elif b >= 2:
                out[(a, b - 2, c)] = out.get((a, b - 2, c), Q(0)) + 11 * u
                changed = True
            elif c >= 2:
                out[(a, b, c - 2)] = out.get((a, b, c - 2), Q(0)) + 2 * u
                out[(a + 1, b, c - 2)] = out.get((a + 1, b, c - 2), Q(0)) - u / 2
                changed = True
            else:
                out[(a, b, c)] = out.get((a, b, c), Q(0)) + u
        raw = {k: v for k, v in out.items() if v}
    return raw


def as_poly(x):
    out = {}
    for mask, q in enumerate(x.a.c):
        if q:
            out[(mask & 1, (mask >> 1) & 1, 0)] = q
    for mask, q in enumerate(x.b.c):
        if q:
            out[(mask & 1, (mask >> 1) & 1, 1)] = q
    return out


def main():
    _, _, points, edges, _, _ = model.build_geometry()
    unit = {(0, 0, 0): Q(1)}
    checked = 0
    edge_set = set(edges)
    for a in range(len(points)):
        for b in range(a):
            dx = points[a][0] - points[b][0]
            dy = points[a][1] - points[b][1]
            squared = poly_mul(as_poly(dx), as_poly(dx))
            other = poly_mul(as_poly(dy), as_poly(dy))
            for monomial, value in other.items():
                squared[monomial] = squared.get(monomial, Q(0)) + value
            squared = {k: v for k, v in squared.items() if v}
            if ((b, a) in edge_set) != (squared == unit):
                raise ValueError("independent distance disagreement")
            checked += 1

    original = json.loads((HERE / "certificate.json").read_text())
    rejected = 0
    for mutation in ("word", "point_hash", "edge_hash", "address_hash"):
        damaged = json.loads(json.dumps(original))
        if mutation == "word":
            a, b = edges[0]
            word = list(damaged["proper_four_word"])
            word[a] = word[b]
            damaged["proper_four_word"] = "".join(word)
        else:
            key = {"point_hash": "point_rows_sha256", "edge_hash": "edge_rows_sha256",
                   "address_hash": "address_map_sha256"}[mutation]
            damaged[key] = "0" * 64
        with tempfile.NamedTemporaryFile("w", suffix=".json") as handle:
            json.dump(damaged, handle)
            handle.flush()
            try:
                verify.run(Path(handle.name))
            except ValueError:
                rejected += 1
            else:
                raise ValueError(f"accepted damaged {mutation}")

    if checked != 26796 or rejected != 4:
        raise ValueError("control census")
    print(json.dumps({
        "status": "INDEPENDENT_POLYNOMIAL_CONTROLS_PASSED",
        "independent_pair_checks": checked,
        "rejected_corruptions": rejected,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
