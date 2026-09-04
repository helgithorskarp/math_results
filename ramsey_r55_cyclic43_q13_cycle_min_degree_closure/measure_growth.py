#!/usr/bin/env python3
"""Measure a deterministic 10,000-source prefix of the full cycle-only closure."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter, deque
from pathlib import Path

import generate_closure


def state_sequence_hash(engine, states) -> str:
    digest = hashlib.sha256()
    for state in states:
        for word in engine.state_key(state):
            digest.update(word.to_bytes(8, "little"))
    return digest.hexdigest()


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("boundary", type=Path)
    parser.add_argument("output", type=Path, nargs="?", default=here / "growth_10000.json")
    parser.add_argument("--cap", type=int, default=10_000)
    args = parser.parse_args()
    if args.cap <= 0:
        raise ValueError("cap must be positive")
    if generate_closure.digest(args.boundary) != generate_closure.EXPECTED_BOUNDARY_SHA256:
        raise AssertionError("unexpected parent boundary certificate hash")
    closure, engine = generate_closure.load_fast_engine()
    parent = json.loads(args.boundary.read_text())
    seeds = sorted(
        {
            engine.state_from_edges(item)
            for item in parent["target_states"]
            if engine.support_signature(engine.state_from_edges(item)) == ()
        },
        key=engine.state_key,
    )
    if len(seeds) != 1381:
        raise AssertionError("expected 1381 cycle-only seeds")
    seen = set(seeds)
    queue = deque(seeds)
    processed = []
    degree_histogram = Counter()
    support_histogram = Counter(closure.signature_name(engine, state) for state in seeds)
    directed = 0
    checkpoints = []
    started = time.monotonic()
    while queue and len(processed) < args.cap:
        source = queue.popleft()
        objective, moves = closure.objective_and_moves(engine, source)
        if objective != 13:
            raise AssertionError("processed state is not q=13")
        degree = 0
        for edge, after in moves:
            if after != 13:
                continue
            degree += 1
            directed += 1
            target = engine.canonical_state(source ^ (1 << edge))
            if target not in seen:
                seen.add(target)
                queue.append(target)
                support_histogram[closure.signature_name(engine, target)] += 1
        degree_histogram[degree] += 1
        processed.append(source)
        if len(processed) % 250 == 0:
            checkpoint = {
                "processed": len(processed),
                "reached": len(seen),
                "queue": len(queue),
                "directed_q13_incidences": directed,
            }
            checkpoints.append(checkpoint)
            print(
                f"processed={len(processed)} reached={len(seen)} queue={len(queue)} "
                f"elapsed={time.monotonic() - started:.1f}s",
                flush=True,
            )
    result = {
        "format": "cyclic43-q13-cycle-only-bfs-prefix-v1",
        "parent_boundary_sha256": generate_closure.EXPECTED_BOUNDARY_SHA256,
        "selection": "all 1381 cycle-only q=13 exits, in canonical word order",
        "queue_rule": "FIFO; targets examined in lexicographic K_43 edge order",
        "processing_cap": args.cap,
        "processed_state_count": len(processed),
        "reached_state_count": len(seen),
        "unprocessed_queue_count": len(queue),
        "closed": not queue,
        "directed_q13_incidences_from_processed": directed,
        "processed_q13_degree_histogram": closure.histogram(degree_histogram),
        "reached_support_signature_histogram": closure.histogram(support_histogram),
        "processed_sequence_sha256_words_le": state_sequence_hash(engine, processed),
        "reached_sorted_sha256_words_le": state_sequence_hash(
            engine, sorted(seen, key=engine.state_key)
        ),
        "queue_sequence_sha256_words_le": state_sequence_hash(engine, queue),
        "checkpoints": checkpoints,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        f"PASS processed={len(processed)} reached={len(seen)} queue={len(queue)} "
        f"closed={not queue} directed={directed}"
    )
    print(f"output_sha256={generate_closure.digest(args.output)}")


if __name__ == "__main__":
    main()
