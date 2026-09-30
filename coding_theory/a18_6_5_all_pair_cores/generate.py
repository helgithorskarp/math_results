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
    supports = [(p, q) for p, q in itertools.combinations(range(17), 2)
                if sum(not w >> p & 1 and not w >> q & 1 for w in seed) >= 35]
    if len(supports) != 54:
        raise ValueError("wrong remaining cohort")
    cases = []
    for p, q in supports:
        point_mask = (1 << p) | (1 << q)
        removed = [i for i, w in enumerate(seed) if w & point_mask]
        core_size = 69 - len(removed)
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
            minimum = max(0, 50 - core_size - h)
            total = max(2 * minimum, 65 - core_size - h)
            if core_size + h + total != 65:
                raise RuntimeError("uncovered anchor size")
            branches = []
            for p_target in range(minimum, total - minimum + 1):
                q_target = total - p_target
                point = p if p_target >= q_target else q
                left_target, right_target = max(p_target, q_target), min(p_target, q_target)
                left = allowed & sum(1 << v for v, w in enumerate(words)
                                     if w & point_mask == 1 << point)
                other = point_mask ^ (1 << point)
                right = allowed & sum(1 << v for v, w in enumerate(words)
                                      if w & point_mask == other)
                families = cliques(adjacency, left, left_target)
                digest = hashlib.sha256()
                right_count = direct_queries = maximum = 0
                queries, opposite_cache = set(), {}
                for a in families:
                    active = right
                    for v in a:
                        active &= adjacency[v]
                    if active not in opposite_cache:
                        if len(opposite_cache) >= 256:
                            opposite_cache.clear()
                        opposite_cache[active] = cliques(adjacency, active, right_target)
                    opposite = opposite_cache[active]
                    digest.update((json.dumps([a, opposite], separators=(",", ":")) + "\n").encode())
                    right_count += len(opposite)
                    for b in opposite:
                        anchor = chosen + list(a) + list(b)
                        if len(set(anchor)) != h + total:
                            raise RuntimeError("overlapping anchor classes")
                        available = (1 << n) - 1
                        for v in anchor:
                            available &= adjacency[v]
                        available &= ~zero_mask
                        maximum = max(maximum, available.bit_count())
                        if available not in queries:
                            if cover_bound(adjacency, available) > 4:
                                direct_queries += 1
                                if cliques(adjacency, available, 5):
                                    raise RuntimeError("compatible extension to70 exists; no exclusion")
                            queries.add(available)
                branches.append({"p_target": p_target, "q_target": q_target,
                                 "enumerated_first": point, "left_families": len(families),
                                 "right_families": right_count, "extension_queries": len(queries),
                                 "direct_extension_queries": direct_queries,
                                 "maximum_extension_words": maximum,
                                 "families_sha256": digest.hexdigest()})
            states.append({"zero_selection": selection, "zero_count": h,
                           "minimum_pure_count": minimum, "pure_total": total, "branches": branches})
        cases.append({"coordinates": [p, q], "core_size": core_size, "residual_words": n,
                      "zero_words": len(zeros), "states": states})
        print(json.dumps({"completed_pair": [p, q], "core_size": core_size}), flush=True)
    return {"schema": "acl69-all-pair-core-report-v1", "seed_sha256": SEED_HASH,
            "new_pairs": len(cases), "previous_minimum_pairs": 82,
            "previous_coordinate17_pairs": 17, "all_pair_cores": 153, "cases": cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = construct()
    if args.check:
        if result != json.loads(args.check.read_text()):
            raise RuntimeError("exact regeneration differs")
        print("Regenerated all 54 remaining pair-core classifications exactly.")
    elif args.output:
        args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
