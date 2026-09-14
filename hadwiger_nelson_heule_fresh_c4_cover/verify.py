#!/usr/bin/env python3
"""Solver-free exact verifier for the H510 plus fresh-centre C4 cover."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import base64
import json


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
IDS = (1239, 1370, 1522, 1371)
N_OLD = 510
RAD = (1, 3, 5, 15, 11, 33, 55, 165)
ONE = (F(1),) + (F(0),) * 7


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b):
    out = [F(0)] * 8
    for i, x0 in enumerate(a):
        if not x0:
            continue
        for j, y0 in enumerate(b):
            if y0:
                out[i ^ j] += x0 * y0 * RAD[i & j]
    return tuple(out)


def point(row):
    require(len(row) == 2 and all(len(axis) == 8 for axis in row), "point shape")
    return tuple(tuple(F(x) for x in axis) for axis in row)


def norm2(p, q):
    dx = sub(p[0], q[0])
    dy = sub(p[1], q[1])
    return add(mul(dx, dx), mul(dy, dy))


def exact_edges(points):
    return tuple(
        (a, b)
        for a, b in combinations(range(len(points)), 2)
        if norm2(points[a], points[b]) == ONE
    )


def edge_hash(edges):
    h = sha256()
    for a, b in edges:
        h.update(f"{a} {b}\n".encode("ascii"))
    return h.hexdigest()


def source_graph():
    manifest = json.loads((HERE / "manifest.json").read_text())
    for name, digest in manifest["inputs"].items():
        require(sha256((REPO / name).read_bytes()).hexdigest() == digest, ("input hash", name))
    union = json.loads(
        (REPO / "hadwiger_nelson_parts509_heule_union_minimum/union_510.json").read_text()
    )
    labels = [v for v, provenance in enumerate(union["provenance"]) if "510" in provenance]
    require(len(labels) == N_OLD, "H510 labels")
    old = tuple(point(union["points"][v]) for v in labels)
    require(len(set(old)) == N_OLD, "H510 distinctness")
    rows0 = json.loads(
        (REPO / "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json").read_text()
    )
    rows = {row["centre_index"]: row for row in rows0}
    require(len(rows) == len(rows0) == 122, "fresh table")
    selected = tuple(rows[v] for v in IDS)
    points = old + tuple(point(row["coordinates"]) for row in selected)
    require(len(points) == 514 and len(set(points)) == 514, "parent distinctness")
    edges = exact_edges(points)
    require(len(edges) == 2525, "parent edge count")
    require(sum(b < N_OLD for a, b in edges) == 2504, "H510 edge count")
    old_neighbours = []
    for j, row in enumerate(selected):
        v = N_OLD + j
        got = sorted(a for a, b in edges if b == v and a < N_OLD)
        require(got == row["neighbors"], ("fresh incidence", IDS[j]))
        old_neighbours.append(got)
    fresh_edges = tuple((a - N_OLD, b - N_OLD) for a, b in edges if a >= N_OLD)
    require(fresh_edges == ((0, 1), (0, 3), (1, 2), (2, 3)), ("fresh induced graph", fresh_edges))
    return points, edges, old_neighbours, fresh_edges


def decode_packed(text, length):
    raw = base64.b64decode(text, validate=True)
    require(len(raw) == (length + 3) // 4, "packed word length")
    if length % 4:
        used = 2 * (length % 4)
        require(raw[-1] >> used == 0, "nonzero packed padding")
    return tuple((raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(length))


def pack(colours):
    raw = bytearray((len(colours) + 3) // 4)
    for i, colour in enumerate(colours):
        require(0 <= colour < 4, "colour range")
        raw[i // 4] |= colour << (2 * (i % 4))
    return base64.b64encode(bytes(raw)).decode("ascii")


def word_hash(words):
    h = sha256()
    for omitted, colours in enumerate(words):
        row = "".join("." if i == omitted else str(c) for i, c in enumerate(colours))
        h.update(f"{omitted} {row}\n".encode("ascii"))
    return h.hexdigest()


def validate(data):
    require(data.get("schema") == 1, "schema")
    require(data.get("centre_ids") == list(IDS), "centre IDs")
    points, edges, old_neighbours, fresh_edges = source_graph()
    require(data.get("vertices") == len(points), "certificate vertex count")
    require(data.get("edges") == len(edges), "certificate edge count")
    packed = data.get("packed_singleton_words")
    require(isinstance(packed, list) and len(packed) == N_OLD, "singleton word count")
    words = [decode_packed(row, len(points)) for row in packed]
    require(word_hash(words) == data.get("word_stream_sha256"), "word stream hash")
    checks = 0
    for omitted, colours in enumerate(words):
        require(colours[N_OLD] == 0, ("fresh colour normalization", omitted))
        for a, b in edges:
            if omitted in (a, b):
                continue
            require(colours[a] != colours[b], ("monochromatic edge", omitted, a, b))
            checks += 1
    # A vertex subset of this 514-point parent with at most 509 points omits at
    # least five parent vertices.  There are only four fresh vertices, so at
    # least one omitted vertex is old.  Its singleton word restricts to the
    # subset and supplies a proper four-colouring.
    require(len(points) - 509 > len(IDS), "old omission at closure order")
    return {
        "status": "PASS",
        "centre_ids": list(IDS),
        "vertices": len(points),
        "edges": len(edges),
        "edge_sha256": edge_hash(edges),
        "old_attachment_degrees": [len(v) for v in old_neighbours],
        "old_attachment_union": len(set().union(*map(set, old_neighbours))),
        "fresh_edges_local": [list(v) for v in fresh_edges],
        "singleton_colourings": len(words),
        "edge_inequalities_checked": checks,
        "word_stream_sha256": data["word_stream_sha256"],
        "every_at_most_509_subgraph_four_colourable": True,
        "record_improved": False,
        "non_four_signal": False,
        "scope": "the fixed exact H510 plus centres 1239,1370,1522,1371 parent",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    ap.add_argument("--check-expected", action="store_true")
    args = ap.parse_args()
    result = validate(json.loads(args.certificate.read_text()))
    if args.check_expected:
        require(result == json.loads((HERE / "expected.json").read_text()), "expected result")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
