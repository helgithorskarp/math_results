#!/usr/bin/env python3
"""Exact checker for the 114-carrier two-circle lens closure."""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
UPSTREAM = HERE.parent / "hadwiger_nelson_weighted_rotation_residue_obstruction"
sys.path.insert(0, str(UPSTREAM))
from exact import ONE as E_ONE, norm as e_norm, points as source_points, scale as e_scale, sub as e_sub  # noqa:E402

ZERO = (F(0),) * 8
ONE = (F(1),) + (F(0),) * 7
RAD = (2, 3, 11)
ROOT2_OVER_2 = (F(0), F(1, 2)) + (F(0),) * 6
MOSER_CORE = (236, 240, 326, 327, 328, 397, 399)
MOBIUS_CYCLE = (63, 0, 62, 94)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def scale(a, q):
    return tuple(q * x for x in a)


def mul(a, b):
    out = [F(0)] * 8
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if not y:
                continue
            common = i & j
            factor = 1
            for bit, rad in enumerate(RAD):
                if common & (1 << bit):
                    factor *= rad
            out[i ^ j] += factor * x * y
    return tuple(out)


def sqdist(p, q):
    dx, dy = sub(p[0], q[0]), sub(p[1], q[1])
    return add(mul(dx, dx), mul(dy, dy))


def lift(z):
    # z = a + b*sqrt(33) + i(c*sqrt(3) + d*sqrt(11)).
    a, b, c, d = z
    x, y = [F(0)] * 8, [F(0)] * 8
    x[0], x[6], y[2], y[4] = a, b, c, d
    return tuple(x), tuple(y)


def carrier_points():
    all_points = source_points()
    data = json.loads((UPSTREAM / "auxiliary_certificate.json").read_text())
    ids = data["source_indices"]
    need(len(ids) == 114 and ids == sorted(set(ids)), "carrier source indices")
    need(all(isinstance(i, int) and 0 <= i < len(all_points) for i in ids),
         "carrier source index range")
    return [all_points[i] for i in ids]


def cnf_text(n, edges, k, units=()):
    clauses = [[k * v + c + 1 for c in range(k)] for v in range(n)]
    clauses.extend([-k * a - c - 1, -k * b - c - 1]
                   for a, b in edges for c in range(k))
    clauses.extend([u] for u in units)
    text = f"p cnf {k*n} {len(clauses)}\n"
    return text + "".join(" ".join(map(str, row)) + " 0\n" for row in clauses)


def build_graph():
    carrier_e = carrier_points()
    carrier = [lift(z) for z in carrier_e]
    long_edges, unit_edges = [], []
    target = e_scale(E_ONE, F(4, 3))
    for i, j in combinations(range(114), 2):
        d2 = e_norm(e_sub(carrier_e[i], carrier_e[j]))
        if d2 == E_ONE:
            unit_edges.append((i, j))
        elif d2 == target:
            long_edges.append((i, j))
    need(len(unit_edges) == 379 and len(long_edges) == 156, "carrier distances")

    raw = list(carrier)
    for i, j in long_edges:
        p, q = carrier[i], carrier[j]
        mx, my = scale(add(p[0], q[0]), F(1, 2)), scale(add(p[1], q[1]), F(1, 2))
        dx, dy = sub(q[0], p[0]), sub(q[1], p[1])
        ox, oy = mul(ROOT2_OVER_2, neg(dy)), mul(ROOT2_OVER_2, dx)
        for sign in (-1, 1):
            z = add(mx, scale(ox, sign)), add(my, scale(oy, sign))
            need(sqdist(z, p) == ONE and sqdist(z, q) == ONE, "lens incidence")
            raw.append(z)

    points = sorted(set(raw))
    index = {p: i for i, p in enumerate(points)}
    source_ids = [index[p] for p in carrier]
    edges = [(i, j) for i, j in combinations(range(len(points)), 2)
             if sqdist(points[i], points[j]) == ONE]
    edge_set = set(edges)
    need(len(raw) == len(points) == 426, "unexpected collision")
    need(all(tuple(sorted((source_ids[i], source_ids[j]))) in edge_set
             for i, j in unit_edges), "missing source unit edge")
    need(all(tuple(sorted((index[raw[114 + 2*t + s]], source_ids[v]))) in edge_set
             for t, (a, b) in enumerate(long_edges)
             for s in range(2) for v in (a, b)), "missing lens edge")
    source_set = set(source_ids)
    kinds = {j: sum((a in source_set) + (b in source_set) == j for a, b in edges)
             for j in range(3)}
    stats = {
        "carrier_vertices": 114,
        "carrier_unit_edges": 379,
        "carrier_distance_4_over_3_edges": 156,
        "collision_merged_points": len(points),
        "complete_unit_edges": len(edges),
        "source_source_edges": kinds[2],
        "source_lens_edges": kinds[1],
        "lens_lens_edges": kinds[0],
        "coordinate_field": "Q(sqrt(2),sqrt(3),sqrt(11))",
        "point_sha256": sha256(repr(points).encode()).hexdigest(),
        "edge_sha256": sha256(repr(edges).encode()).hexdigest(),
    }
    return points, edges, source_ids, long_edges, stats


def word(text, n, k):
    need(isinstance(text, str) and len(text) == n, "colour word length")
    need(all(c in "0123456789" and int(c) < k for c in text), "colour word alphabet")
    return tuple(map(int, text))


def proper(colours, edges):
    return all(colours[a] != colours[b] for a, b in edges)


def verify(emit_dir=None):
    points, edges, source_ids, long_edges, stats = build_graph()
    cert = json.loads((HERE / "certificate.json").read_text())
    four = word(cert["four_colouring"], len(points), 4)
    need(proper(four, edges), "four-colouring")

    entries = cert["long_pair_equal_four_colourings"]
    need(len(entries) == len(long_edges), "long-pair witness count")
    for entry, pair in zip(entries, long_edges):
        need(entry["pair"] == list(pair), "long-pair witness order")
        colours = word(entry["word"], len(points), 4)
        need(proper(colours, edges), "long-pair four-colouring")
        a, b = pair
        need(colours[source_ids[a]] == colours[source_ids[b]], "long-pair equality")

    induced = [(MOSER_CORE.index(a), MOSER_CORE.index(b)) for a, b in edges
               if a in MOSER_CORE and b in MOSER_CORE]
    need(len(induced) == 11, "seven-point core edge count")
    need(not any(proper(c, induced) for c in product(range(3), repeat=7)),
         "seven-point core unexpectedly three-colourable")

    labels = []
    carrier_e = carrier_points()
    for a, b in zip(MOBIUS_CYCLE, MOBIUS_CYCLE[1:] + MOBIUS_CYCLE[:1]):
        d2 = e_norm(e_sub(carrier_e[a], carrier_e[b]))
        need(d2 in (E_ONE, e_scale(E_ONE, F(4, 3))), "Möbius cycle distance")
        labels.append(0 if d2 == E_ONE else 1)
    need(labels == [0, 0, 1, 0], "Möbius contradiction cycle")

    stats.update({
        "chromatic_number": 4,
        "nonthree_core_vertices": list(MOSER_CORE),
        "nonthree_core_edges": 11,
        "long_pairs_with_checked_equal_extension": len(entries),
        "mobius_product_cycle": list(MOBIUS_CYCLE),
        "mobius_cycle_length_labels": labels,
        "record_improvement": False,
    })
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(stats == expected, "summary differs from EXPECTED.json")
    if emit_dir is not None:
        emit_dir.mkdir(parents=True, exist_ok=False)
        (emit_dir / "points.tsv").write_text("\n".join(
            "\t".join(str(x) for q in p for x in q) for p in points) + "\n")
        (emit_dir / "edges.tsv").write_text("\n".join(f"{a}\t{b}" for a, b in edges) + "\n")
        (emit_dir / "three_colour.cnf").write_text(cnf_text(len(points), edges, 3))
    return stats


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--emit-dir", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.emit_dir), indent=2, sort_keys=True))
