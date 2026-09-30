#!/usr/bin/env python3
"""Exact proposer using triple owners, bitsets and ordered clique enumeration."""
import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED_HASH = "cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d"


def cliques(adjacency, active, target):
    found = []

    def visit(remaining, selected, budget):
        budget[0] += 1
        if budget[0] > 20_000 or (budget[0] % 128 == 0
                                and time.monotonic() - budget[1] > 3):
            raise RuntimeError("INCOMPLETE: ordered enumeration limit")
        if len(selected) == target:
            found.append(tuple(sorted(selected)))
            return
        order, colors, count = [], [], 0
        current = remaining
        while current:
            count += 1
            group = current
            while group:
                bit = group & -group
                vertex = bit.bit_length() - 1
                order.append(vertex)
                colors.append(count)
                current ^= bit
                group &= ~bit
                group &= ~adjacency[vertex]
        for i in range(len(order) - 1, -1, -1):
            if len(selected) + colors[i] < target:
                break
            vertex = order[i]
            remaining &= ~(1 << vertex)
            child_budget = [0, time.monotonic()] if not selected else budget
            visit(remaining & adjacency[vertex], selected + [vertex], child_budget)

    visit(active, [], [0, time.monotonic()])
    if len(found) != len(set(found)):
        raise RuntimeError("duplicate clique")
    return sorted(found)


def prepare():
    raw = (ROOT / "acl69.txt").read_bytes()
    if hashlib.sha256(raw).hexdigest() != SEED_HASH:
        raise ValueError("wrong seed")
    rows = raw.decode("ascii").splitlines()
    if len(rows) != 69 or any(len(s) != 18 or set(s) - set("01")
                              or s.count("1") != 5 for s in rows):
        raise ValueError("malformed seed")
    seed = [sum(1 << p for p, c in enumerate(s) if c == "1") for s in rows]
    owners = {}
    for i, word in enumerate(seed):
        for triple in itertools.combinations([p for p in range(18) if word >> p & 1], 3):
            if triple in owners:
                raise ValueError("repeated seed triple")
            owners[triple] = i
    candidates = []
    for block in itertools.combinations(range(18), 5):
        word = sum(1 << p for p in block)
        if word not in seed:
            blockers = {owners[t] for t in itertools.combinations(block, 3) if t in owners}
            candidates.append((word, sum(1 << i for i in blockers)))
    return seed, candidates


def cover_bound(adjacency, active):
    count = 0
    while active:
        count += 1
        group = active
        while group:
            bit = group & -group
            vertex = bit.bit_length() - 1
            active ^= bit
            group &= ~bit
            group &= ~adjacency[vertex]
    return count


def construct():
    seed, candidates = prepare()
    saturated = {p for p in range(18) if sum(w >> p & 1 for w in seed) == 20}
    all_minimum = [(p, q) for p, q in itertools.combinations(range(18), 2)
                   if sum(not w >> p & 1 and not w >> q & 1 for w in seed) == 34]
    supports = [(p, q) for p, q in all_minimum if not {p, q} <= saturated]
    cases = []
    for p, q in supports:
        point_mask = (1 << p) | (1 << q)
        removed = [i for i, w in enumerate(seed) if w & point_mask]
        removed_mask = sum(1 << i for i in removed)
        words = sorted([seed[i] for i in removed]
                       + [w for w, blocked in candidates if blocked & removed_mask == blocked])
        n = len(words)
        adjacency = [sum(1 << j for j, b in enumerate(words)
                         if j != i and (a & b).bit_count() <= 2)
                     for i, a in enumerate(words)]
        zeros = [i for i, w in enumerate(words) if not w & point_mask]
        zero_mask = sum(1 << i for i in zeros)
        states = []
        for selection in range(1 << len(zeros)):
            chosen = [v for i, v in enumerate(zeros) if selection >> i & 1]
            if any(not adjacency[a] >> b & 1 for a, b in itertools.combinations(chosen, 2)):
                continue
            allowed = (1 << n) - 1
            for v in chosen:
                allowed &= adjacency[v]
            h = len(chosen)
            small = 16 - h
            large = max(small, (32 - h) // 2)
            if small < 0:
                raise RuntimeError("uncovered zero-word threshold")
            orientations = []
            for point in ([p] if small == large else [p, q]):
                left = allowed & sum(1 << v for v, w in enumerate(words)
                                     if w & point_mask == 1 << point)
                other = point_mask ^ (1 << point)
                right = allowed & sum(1 << v for v, w in enumerate(words)
                                      if w & point_mask == other)
                families = cliques(adjacency, left, large)
                digest = hashlib.sha256()
                right_count = 0
                queries = {}
                maximum = 0
                for a in families:
                    active = right
                    for v in a:
                        active &= adjacency[v]
                    opposite = cliques(adjacency, active, small)
                    digest.update((json.dumps([a, opposite], separators=(",", ":")) + "\n").encode())
                    right_count += len(opposite)
                    for b in opposite:
                        anchor = chosen + list(a) + list(b)
                        if len(set(anchor)) != len(anchor):
                            raise RuntimeError("anchor classes overlap")
                        available = (1 << n) - 1
                        for v in anchor:
                            available &= adjacency[v]
                        available &= ~zero_mask
                        bound = 35 - len(anchor)
                        key = (available, bound)
                        maximum = max(maximum, available.bit_count())
                        if key not in queries:
                            if cover_bound(adjacency, available) > bound:
                                raise RuntimeError("extension upper bound not certified; no exclusion")
                            queries[key] = True
                orientations.append({"larger_coordinate": point, "left_families": len(families),
                                     "right_families": right_count, "extension_queries": len(queries),
                                     "maximum_extension_words": maximum, "families_sha256": digest.hexdigest()})
            states.append({"zero_selection": selection, "zero_count": h,
                           "thresholds": [large, small], "orientations": orientations})
        cases.append({"coordinates": [p, q], "core_size": 34, "residual_words": n,
                      "zero_words": len(zeros), "states": states})
    return {"schema": "acl69-minimum-pair-core-report-v1", "seed_sha256": SEED_HASH,
            "minimum_core_size": 34, "all_minimum_pairs": len(all_minimum),
            "previous_saturated_pairs": 66, "new_pairs": len(cases), "cases": cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = construct()
    if args.check:
        if result != json.loads(args.check.read_text()):
            raise RuntimeError("exact regeneration differs")
        print("Regenerated all 16 new pair-core classifications exactly.")
    elif args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
