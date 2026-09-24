#!/usr/bin/env python3
"""Independent definition-level check: vertex adjacency and three-edge paths.

Does not import the construction, its template, or its square enumeration.
With no argument it launches the constructor on the documented validation suite.
With a JSON path it checks that single expanded witness.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


def verify(data: dict) -> dict:
    n = data["dimension"]
    if type(n) is not int or not 2 <= n <= 16:
        raise ValueError("invalid dimension")
    edges = data["edges"]
    if edges != sorted(edges):
        raise ValueError("edge list is not sorted")
    seen = set()
    neighbors = [set() for _ in range(1 << n)]
    for pair in edges:
        if len(pair) != 2 or any(type(v) is not int for v in pair):
            raise ValueError("malformed edge")
        u, v = pair
        delta = u ^ v
        if not (0 <= u < v < 1 << n) or delta & (delta - 1):
            raise ValueError("edge does not belong to the cube")
        if (u, v) in seen:
            raise ValueError("duplicate edge")
        seen.add((u, v))
        neighbors[u].add(v)
        neighbors[v].add(u)
    missing = 0
    for u in range(1 << n):
        for bit in range(n):
            v = u ^ (1 << bit)
            if u > v:
                continue
            # A simple three-edge path between adjacent cube vertices is
            # exactly the other three sides of a square.
            path = any((neighbors[w] & neighbors[v]) - {u}
                       for w in neighbors[u] - {v})
            if v in neighbors[u]:
                if path:
                    raise ValueError("four-cycle in selected graph")
            elif not path:
                raise ValueError(f"missing edge {(u, v)} has no square witness")
            else:
                missing += 1
    digest = hashlib.sha256("".join(f"{u} {v}\n" for u, v in edges).encode()).hexdigest()
    if digest != data["edge_sha256"] or len(edges) != data["edge_count"]:
        raise ValueError("certificate metadata mismatch")
    return {"blocks": data["blocks"], "dimension": n, "edge_count": len(edges),
            "edge_sha256": digest, "missing_edges_checked": missing,
            "initial_edges": data["initial_edges"],
            "completion_edges": data["completion_edges"], "status": "VERIFIED"}


def suite() -> dict:
    program = Path(__file__).with_name("construct.py")
    cases = [(3, 3, 0), (3, 3, 1), (3, 3, 2), (3, 3, 3),
             (3, 7, 0), (7, 3, 0), (7, 3, 1), (3, 7, 2), (7, 7, 0)]
    results = []
    first = None
    for blocks in cases:
        raw = subprocess.check_output([sys.executable, str(program), "--blocks", *map(str, blocks)])
        data = json.loads(raw)
        results.append(verify(data))
        if first is None:
            first = data
    # Negative controls exercise the checker independently of the generator.
    assert first is not None
    rejected = 0
    bad = dict(first, edges=sorted(first["edges"] + [first["edges"][0]]))
    try:
        verify(bad)
    except ValueError:
        rejected += 1
    empty = dict(first, edges=[], edge_count=0,
                 edge_sha256=hashlib.sha256(b"").hexdigest())
    try:
        verify(empty)
    except ValueError:
        rejected += 1
    n = first["dimension"]
    full_edges = sorted([[u, u ^ (1 << i)] for u in range(1 << n)
                         for i in range(n) if not u & (1 << i)])
    full = dict(first, edges=full_edges, edge_count=len(full_edges),
                edge_sha256=hashlib.sha256("".join(f"{u} {v}\n" for u, v in full_edges).encode()).hexdigest())
    try:
        verify(full)
    except ValueError:
        rejected += 1
    if rejected != 3:
        raise AssertionError("negative-control failure")
    return {"instances": results, "negative_controls_rejected": rejected, "status": "VERIFIED"}


if __name__ == "__main__":
    result = verify(json.loads(Path(sys.argv[1]).read_text())) if len(sys.argv) == 2 else suite()
    print(json.dumps(result, sort_keys=True, indent=2))
