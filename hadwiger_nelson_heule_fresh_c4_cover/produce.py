#!/usr/bin/env python3
"""Optional SAT producer for the H510 plus fresh-centre C4 cover."""
from hashlib import sha256
from pathlib import Path
import argparse
import json

from pysat.solvers import Cadical195

import verify


N_OLD = 510
N = 514


def x(v, c):
    return 4 * v + c + 1


def active(v):
    return 4 * N + v + 1


def build_cnf(edges):
    cnf = [[-active(v)] + [x(v, c) for c in range(4)] for v in range(N_OLD)]
    cnf.extend([[x(v, c) for c in range(4)] for v in range(N_OLD, N)])
    cnf.append([x(N_OLD, 0)])
    for a, b in edges:
        for c in range(4):
            clause = [-x(a, c), -x(b, c)]
            if a < N_OLD:
                clause.insert(0, -active(a))
            if b < N_OLD:
                clause.insert(0, -active(b))
            cnf.append(clause)
    return cnf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--conflicts", type=int, default=200_000)
    args = ap.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    points, edges, _, _ = verify.source_graph()
    if len(points) != N:
        raise ValueError("unexpected point count")
    cnf = build_cnf(edges)
    words = []
    packed = []
    conflicts = 0
    with Cadical195(bootstrap_with=cnf) as solver:
        for omitted in range(N_OLD):
            assumptions = [
                -active(v) if v == omitted else active(v) for v in range(N_OLD)
            ]
            before = solver.accum_stats().get("conflicts", 0)
            solver.conf_budget(args.conflicts)
            answer = solver.solve_limited(assumptions=assumptions, expect_interrupt=True)
            conflicts += solver.accum_stats().get("conflicts", 0) - before
            if answer is not True:
                raise RuntimeError(("non-SAT producer answer", omitted, answer))
            positive = {z for z in solver.get_model() if z > 0}
            colours = []
            for v in range(N):
                if v == omitted:
                    colours.append(0)
                    continue
                choices = [c for c in range(4) if x(v, c) in positive]
                if not choices:
                    raise ValueError(("empty colour", omitted, v))
                colours.append(choices[0])
            if any(
                omitted not in (a, b) and colours[a] == colours[b]
                for a, b in edges
            ):
                raise ValueError(("bad decoded word", omitted))
            words.append(tuple(colours))
            packed.append(verify.pack(colours))
    data = {
        "schema": 1,
        "centre_ids": list(verify.IDS),
        "vertices": N,
        "edges": len(edges),
        "packed_singleton_words": packed,
        "word_stream_sha256": verify.word_hash(words),
    }
    args.out.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(args.out),
        "certificate_sha256": sha256(args.out.read_bytes()).hexdigest(),
        "queries": N_OLD,
        "sat": N_OLD,
        "conflicts": conflicts,
        "word_stream_sha256": data["word_stream_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
